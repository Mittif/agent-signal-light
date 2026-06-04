#!/usr/bin/env python3
"""Agent Signal Light installer — cross-platform (macOS / Windows / Linux).

Run once to:
  • install hidapi (pip --user)
  • copy default config to ~/.agent-signal-light/config.json
  • register an auto-start service so the daemon runs at login + respawns on crash
  • auto-wire Claude Code and Codex hooks (with backups), or print snippets
  • verify the daemon is up

Re-runnable. Pass --uninstall to undo. Pass --uninstall --purge to also wipe data.
Pass --no-hooks to skip auto-wiring the agent hooks.

    python3 install.py
    python3 install.py --no-hooks
    python3 install.py --uninstall [--purge]
"""
from __future__ import annotations

import argparse
import json
import platform
import shlex
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
APP_NAME = "Agent Signal Light"
APP_SLUG = "agent-signal-light"
DATA_DIR = Path.home() / f".{APP_SLUG}"
LABEL = "dev.agent-signal-light"
# Removed in a future release. Cleaned up on install/uninstall so machines that ran
# the original "com.mitty.*" build don't end up with two services fighting for the port.
LEGACY_LABEL = "com.mitty.agent-signal-light"
DAEMON_URL = "http://127.0.0.1:7878/api/status"


# ──────────────────────────────────────────────────────────── helpers ──
def info(m): print(f"▶ {m}")
def ok(m):   print(f"✓ {m}")
def warn(m): print(f"! {m}")
def err(m):  print(f"✗ {m}", file=sys.stderr)


def install_hidapi() -> None:
    try:
        import hid  # noqa: F401
        ok("hidapi already installed")
        return
    except ImportError:
        pass
    info("installing hidapi …")
    base = [sys.executable, "-m", "pip", "install", "--quiet", "--user", "hidapi"]
    # macOS / recent Debian default to PEP 668 "externally managed" — retry once
    # with --break-system-packages if the plain --user install fails.
    for extra in ([], ["--break-system-packages"]):
        try:
            subprocess.check_call(base + extra)
            ok("hidapi installed"); return
        except subprocess.CalledProcessError:
            continue
    err("hidapi install failed (try manually: python3 -m pip install hidapi)")
    sys.exit(1)


def setup_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    user_cfg = DATA_DIR / "config.json"
    if user_cfg.exists():
        ok(f"existing config kept ({user_cfg})")
    else:
        shutil.copy(PROJECT_DIR / "config.default.json", user_cfg)
        ok(f"wrote default config -> {user_cfg}")


def stop_running_daemons() -> None:
    server = str(PROJECT_DIR / "server.py")
    for pattern in (server, "agent-signal-light/server.py"):
        subprocess.run(["pkill", "-f", pattern], check=False)


# ───────────────────────────────────────────────────────────── macOS ──
def macos_plist_text() -> str:
    log = DATA_DIR / "daemon.log"
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTD/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>          <string>{LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{PROJECT_DIR / "server.py"}</string>
    </array>
    <key>WorkingDirectory</key>   <string>{PROJECT_DIR}</string>
    <key>RunAtLoad</key>          <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key> <false/>
        <key>Crashed</key>        <true/>
    </dict>
    <key>ThrottleInterval</key>   <integer>5</integer>
    <key>StandardOutPath</key>    <string>{log}</string>
    <key>StandardErrorPath</key>  <string>{log}</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>           <string>/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin</string>
    </dict>
</dict>
</plist>
"""


def _remove_macos_plist(label: str, *, quiet: bool = False) -> None:
    plist = Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"
    if plist.exists():
        subprocess.run(["launchctl", "unload", str(plist)], check=False, stderr=subprocess.DEVNULL)
        plist.unlink()
        if not quiet:
            ok(f"removed {plist}")


def install_macos() -> None:
    plist = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    plist.parent.mkdir(parents=True, exist_ok=True)
    _remove_macos_plist(LEGACY_LABEL, quiet=True)
    plist.write_text(macos_plist_text())
    ok(f"wrote LaunchAgent -> {plist}")
    stop_running_daemons()
    subprocess.run(["launchctl", "unload", str(plist)], check=False, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "load", str(plist)], check=True)
    ok("LaunchAgent loaded")


def uninstall_macos() -> None:
    for label in (LABEL, LEGACY_LABEL):
        _remove_macos_plist(label)
    stop_running_daemons()


# ─────────────────────────────────────────────────────────── Windows ──
def install_windows() -> None:
    startup = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    startup.mkdir(parents=True, exist_ok=True)

    # pythonw.exe avoids a console window flashing at login.
    pythonw = Path(sys.executable).with_name("pythonw.exe")
    if not pythonw.exists():
        pythonw = Path(sys.executable)

    server = PROJECT_DIR / "server.py"
    log = DATA_DIR / "daemon.log"

    # VBS shim: starts python hidden, redirects output to the log.
    vbs = startup / f"{APP_SLUG}.vbs"
    vbs.write_text(
        'Set sh = CreateObject("WScript.Shell")\r\n'
        f'sh.Run """{pythonw}"" ""{server}"" > ""{log}"" 2>&1", 0, False\r\n',
        encoding="utf-8",
    )
    ok(f"wrote startup launcher → {vbs}")

    # Launch now so the user doesn't need to log out first.
    CREATE_NO_WINDOW = 0x08000000
    log_fh = open(log, "a", buffering=1)
    subprocess.Popen(
        [str(pythonw), str(server)],
        cwd=str(PROJECT_DIR),
        creationflags=CREATE_NO_WINDOW,
        stdout=log_fh,
        stderr=subprocess.STDOUT,
    )
    ok("daemon launched")

    # Ship a Windows hook script alongside the POSIX hook.sh.
    hook = PROJECT_DIR / "hook.cmd"
    if not hook.exists():
        hook.write_text(
            "@echo off\r\n"
            "REM Forward an agent hook's stdin JSON to the local light daemon.\r\n"
            "curl -fsS --max-time 1 -X POST http://127.0.0.1:7878/hook "
            '-H "Content-Type: application/json" --data-binary @- >nul 2>&1\r\n'
            "exit /b 0\r\n",
            encoding="utf-8",
        )
        ok(f"wrote {hook}")


def uninstall_windows() -> None:
    startup = Path.home() / "AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"
    vbs = startup / f"{APP_SLUG}.vbs"
    if vbs.exists():
        vbs.unlink()
        ok(f"removed {vbs}")
    # Best-effort kill any running daemon. WMIC is deprecated on Win11 but still
    # available; fall back to taskkill image-name otherwise.
    subprocess.run(
        ['taskkill', '/F', '/FI', 'IMAGENAME eq pythonw.exe', '/FI', 'WINDOWTITLE eq server.py*'],
        capture_output=True, check=False,
    )


# ───────────────────────────────────────────────────────────── Linux ──
def install_linux() -> None:
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    unit = unit_dir / f"{LABEL}.service"
    legacy_unit = unit_dir / f"{LEGACY_LABEL}.service"
    log = DATA_DIR / "daemon.log"
    if legacy_unit.exists():
        subprocess.run(["systemctl", "--user", "disable", "--now", f"{LEGACY_LABEL}.service"],
                       check=False, stderr=subprocess.DEVNULL)
        legacy_unit.unlink()
    unit.write_text(
        f"""[Unit]
Description={APP_NAME} daemon
After=default.target

[Service]
ExecStart={sys.executable} {PROJECT_DIR / "server.py"}
WorkingDirectory={PROJECT_DIR}
Restart=on-failure
RestartSec=5
StandardOutput=append:{log}
StandardError=append:{log}

[Install]
WantedBy=default.target
""")
    ok(f"wrote systemd unit -> {unit}")
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)
    subprocess.run(["systemctl", "--user", "enable", "--now", f"{LABEL}.service"], check=False)
    ok("systemd unit enabled")


def uninstall_linux() -> None:
    unit_dir = Path.home() / ".config" / "systemd" / "user"
    for label in (LABEL, LEGACY_LABEL):
        subprocess.run(["systemctl", "--user", "disable", "--now", f"{label}.service"], check=False)
        unit = unit_dir / f"{label}.service"
        if unit.exists():
            unit.unlink()
            ok(f"removed {unit}")
    subprocess.run(["systemctl", "--user", "daemon-reload"], check=False)


# ────────────────────────────────────────────────────── verify / wrap ──
def verify() -> bool:
    info("waiting for daemon …")
    for _ in range(15):
        try:
            with urllib.request.urlopen(DAEMON_URL, timeout=1) as r:
                r.read()
            ok("daemon up at http://127.0.0.1:7878")
            return True
        except Exception:
            time.sleep(0.4)
    err("daemon did not come up — check the log")
    return False


def _hook_command(osname: str, agent: str) -> str:
    hook_path = PROJECT_DIR / ("hook.cmd" if osname == "Windows" else "hook.sh")
    if osname == "Windows":
        cmd = f'"{hook_path}" {agent}'
        return cmd.replace("\\", "\\\\")
    return f"{shlex.quote(str(hook_path))} {agent}"


def _command_hook(cmd: str, *, codex: bool = False) -> dict:
    hook = {"type": "command", "command": cmd}
    if codex:
        hook["timeout"] = 5
        hook["statusMessage"] = "Updating signal light"
    return hook


def _hook_group(cmd: str, matcher: str | None = None, *, codex: bool = False) -> dict:
    group = {"hooks": [_command_hook(cmd, codex=codex)]}
    if matcher is not None:
        group["matcher"] = matcher
    return group


def _hook_path(osname: str) -> Path:
    return PROJECT_DIR / ("hook.cmd" if osname == "Windows" else "hook.sh")


def _is_ours(cmd: str) -> bool:
    """A hook command is ours iff it points at this checkout's hook script."""
    return str(_hook_path("Windows")) in (cmd or "") or str(_hook_path("Linux")) in (cmd or "")


def _build_claude_hooks(osname: str) -> dict:
    cmd = _hook_command(osname, "claude")
    return {
        "SessionStart":     [_hook_group(cmd)],
        "SessionEnd":       [_hook_group(cmd)],
        "UserPromptSubmit": [_hook_group(cmd)],
        "Stop":             [_hook_group(cmd)],
        "StopFailure":      [_hook_group(cmd)],
        "Elicitation":      [_hook_group(cmd)],
        "Notification":     [_hook_group(cmd, "permission_prompt|elicitation_dialog")],
        "PreToolUse":       [_hook_group(cmd, "AskUserQuestion")],
        "PostToolUse":      [_hook_group(cmd, "AskUserQuestion")],
    }


def _codex_hooks_toml(osname: str) -> str:
    cmd = _hook_command(osname, "codex")
    qcmd = json.dumps(cmd)
    handler = f'{{ type = "command", command = {qcmd}, timeout = 5, statusMessage = "Updating signal light" }}'
    return f"""# agent-signal-light hooks (auto-installed)
[features]
hooks = true
codex_hooks = true  # older Codex CLI builds

[hooks]
SessionStart    = [{{ matcher = "startup|resume|clear|compact", hooks = [{handler}] }}]
UserPromptSubmit = [{{ hooks = [{handler}] }}]
PreToolUse        = [{{ hooks = [{handler}] }}]
PermissionRequest = [{{ hooks = [{handler}] }}]
PostToolUse       = [{{ hooks = [{handler}] }}]
PreCompact        = [{{ matcher = "manual|auto", hooks = [{handler}] }}]
PostCompact       = [{{ matcher = "manual|auto", hooks = [{handler}] }}]
SubagentStart     = [{{ hooks = [{handler}] }}]
SubagentStop      = [{{ hooks = [{handler}] }}]
Stop              = [{{ hooks = [{handler}] }}]
StopFailure       = [{{ hooks = [{handler}] }}]
"""


def install_claude_hooks(osname: str) -> None:
    """Merge our hook entries into ~/.claude/settings.json, preserving other config.

    For each event we own, drop any pre-existing group whose first hook command
    fingerprints as ours, then append our group. Idempotent.
    """
    settings = Path.home() / ".claude" / "settings.json"
    settings.parent.mkdir(parents=True, exist_ok=True)
    if settings.exists():
        try:
            data = json.loads(settings.read_text() or "{}")
            if not isinstance(data, dict):
                raise ValueError("not a JSON object")
        except (ValueError, json.JSONDecodeError) as e:
            warn(f"Claude settings.json is not valid JSON ({e}); printing snippet instead")
            print_claude_hooks_snippet(osname)
            return
        settings.with_suffix(".json.bak").write_text(json.dumps(data, indent=2))
    else:
        data = {}

    hooks_root = data.setdefault("hooks", {})
    if not isinstance(hooks_root, dict):
        warn('"hooks" in settings.json is not an object; printing snippet instead')
        print_claude_hooks_snippet(osname)
        return

    our_hooks = _build_claude_hooks(osname)
    for event, our_groups in our_hooks.items():
        existing = hooks_root.get(event)
        if not isinstance(existing, list):
            existing = []
        kept = []
        for group in existing:
            try:
                first_cmd = (group.get("hooks") or [{}])[0].get("command", "")
            except (AttributeError, TypeError, IndexError):
                first_cmd = ""
            if not _is_ours(first_cmd):
                kept.append(group)
        hooks_root[event] = kept + our_groups

    settings.write_text(json.dumps(data, indent=2) + "\n")
    ok(f"merged Claude hooks -> {settings}")


def install_codex_hooks(osname: str) -> None:
    """Append our [features]/[hooks] block to ~/.codex/config.toml when it's safe.

    TOML is tricky to rewrite in place without a writer library, so we only touch
    the file when there's no existing [features] or [hooks] table to clobber.
    Anything else falls back to the printable snippet.
    """
    config_path = Path.home() / ".codex" / "config.toml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    snippet = _codex_hooks_toml(osname)

    if not config_path.exists():
        config_path.write_text(snippet)
        ok(f"wrote Codex hooks -> {config_path}")
        return

    existing = config_path.read_text()
    if str(_hook_path(osname)) in existing:
        ok(f"Codex hooks already present in {config_path}")
        return
    if "[hooks]" in existing or "[features]" in existing:
        warn("Codex config already defines [hooks]/[features]; printing snippet for manual merge")
        print_codex_hooks_snippet(osname)
        return

    config_path.with_suffix(".toml.bak").write_text(existing)
    suffix = "" if existing.endswith("\n") else "\n"
    config_path.write_text(existing + suffix + "\n" + snippet)
    ok(f"appended Codex hooks -> {config_path}")


def print_claude_hooks_snippet(osname: str) -> None:
    settings = Path.home() / ".claude" / "settings.json"
    print()
    info(f"Merge the following into {settings}:")
    print()
    print(json.dumps({"hooks": _build_claude_hooks(osname)}, indent=2))


def print_codex_hooks_snippet(osname: str) -> None:
    config_path = Path.home() / ".codex" / "config.toml"
    print()
    info(f"Merge the following into {config_path}:")
    print()
    print(_codex_hooks_toml(osname))


def install_hooks(osname: str) -> None:
    install_claude_hooks(osname)
    install_codex_hooks(osname)


def main() -> None:
    ap = argparse.ArgumentParser(description=f"{APP_NAME} installer (cross-platform)")
    ap.add_argument("--uninstall", action="store_true", help="remove auto-start")
    ap.add_argument("--purge", action="store_true",
                    help=f"with --uninstall, also delete ~/.{APP_SLUG}/")
    ap.add_argument("--no-hooks", action="store_true",
                    help="don't touch ~/.claude/settings.json or ~/.codex/config.toml")
    args = ap.parse_args()

    osname = platform.system()
    info(f"OS:      {osname}")
    info(f"project: {PROJECT_DIR}")
    info(f"data:    {DATA_DIR}")

    if osname not in ("Darwin", "Windows", "Linux"):
        err(f"unsupported OS: {osname}")
        sys.exit(1)

    if args.uninstall:
        if osname == "Darwin":   uninstall_macos()
        elif osname == "Windows": uninstall_windows()
        else:                     uninstall_linux()
        if args.purge and DATA_DIR.exists():
            shutil.rmtree(DATA_DIR)
            ok(f"purged {DATA_DIR}")
        else:
            info(f"data preserved at {DATA_DIR} (use --purge to delete)")
        return

    install_hidapi()
    setup_data_dir()
    if osname == "Darwin":   install_macos()
    elif osname == "Windows": install_windows()
    else:                     install_linux()

    if verify():
        if args.no_hooks:
            info("skipping agent hook auto-install (--no-hooks)")
            print_claude_hooks_snippet(osname)
            print_codex_hooks_snippet(osname)
        else:
            install_hooks(osname)


if __name__ == "__main__":
    main()
