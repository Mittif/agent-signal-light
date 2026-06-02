#!/usr/bin/env python3
"""Agent Signal Light installer — cross-platform (macOS / Windows / Linux).

Run once to:
  • install hidapi (pip --user)
  • copy default config to ~/.agent-signal-light/config.json
  • register an auto-start service so the daemon runs at login + respawns on crash
  • verify the daemon is up

Re-runnable. Pass --uninstall to undo. Pass --uninstall --purge to also wipe data.

    python3 install.py
    python3 install.py --uninstall [--purge]
"""
from __future__ import annotations

import argparse
import json
import platform
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
LEGACY_DATA_DIR = Path.home() / ".claude-light"
LABEL = "com.mitty.agent-signal-light"
LEGACY_LABEL = "com.mitty.claude-light"
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
    elif (LEGACY_DATA_DIR / "config.json").exists():
        shutil.copy(LEGACY_DATA_DIR / "config.json", user_cfg)
        ok(f"migrated existing config -> {user_cfg}")
    else:
        shutil.copy(PROJECT_DIR / "config.default.json", user_cfg)
        ok(f"wrote default config -> {user_cfg}")


def stop_running_daemons() -> None:
    server = str(PROJECT_DIR / "server.py")
    for pattern in (server, "agent-signal-light/server.py", "claude-light/server.py"):
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


def install_macos() -> None:
    plist = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
    legacy_plist = Path.home() / "Library" / "LaunchAgents" / f"{LEGACY_LABEL}.plist"
    plist.parent.mkdir(parents=True, exist_ok=True)
    if legacy_plist.exists():
        subprocess.run(["launchctl", "unload", str(legacy_plist)], check=False, stderr=subprocess.DEVNULL)
        legacy_plist.unlink()
        ok(f"removed legacy LaunchAgent -> {legacy_plist}")
    plist.write_text(macos_plist_text())
    ok(f"wrote LaunchAgent -> {plist}")
    stop_running_daemons()
    subprocess.run(["launchctl", "unload", str(plist)], check=False, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "load", str(plist)], check=True)
    ok("LaunchAgent loaded")


def uninstall_macos() -> None:
    for label in (LABEL, LEGACY_LABEL):
        plist = Path.home() / "Library" / "LaunchAgents" / f"{label}.plist"
        if plist.exists():
            subprocess.run(["launchctl", "unload", str(plist)], check=False, stderr=subprocess.DEVNULL)
            plist.unlink()
            ok(f"removed {plist}")
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
    legacy_vbs = startup / "claude-light.vbs"
    if legacy_vbs.exists():
        legacy_vbs.unlink()
        ok(f"removed legacy startup launcher -> {legacy_vbs}")

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
    for name in (f"{APP_SLUG}.vbs", "claude-light.vbs"):
        vbs = startup / name
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
        subprocess.run(["systemctl", "--user", "disable", "--now", f"{LEGACY_LABEL}.service"], check=False)
        legacy_unit.unlink()
        ok(f"removed legacy systemd unit -> {legacy_unit}")
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


def _hook_command(osname: str) -> str:
    hook_path = PROJECT_DIR / ("hook.cmd" if osname == "Windows" else "hook.sh")
    return str(hook_path).replace("\\", "\\\\")


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


def print_claude_hooks_snippet(osname: str) -> None:
    hook_path = PROJECT_DIR / ("hook.cmd" if osname == "Windows" else "hook.sh")
    settings = Path.home() / ".claude" / "settings.json"
    print()
    info("Wire Claude Code hooks (one-time):")
    print(f"   Edit {settings}")
    print(f"   Add (or merge) the following \"hooks\" block — command points to:")
    print(f"     {hook_path}")
    print()
    cmd = _hook_command(osname)
    hooks = {
        "SessionStart": [_hook_group(cmd)],
        "SessionEnd": [_hook_group(cmd)],
        "UserPromptSubmit": [_hook_group(cmd)],
        "Stop": [_hook_group(cmd)],
        "StopFailure": [_hook_group(cmd)],
        "Elicitation": [_hook_group(cmd)],
        "Notification": [_hook_group(cmd, "permission_prompt|elicitation_dialog")],
        "PreToolUse": [_hook_group(cmd, "AskUserQuestion")],
        "PostToolUse": [_hook_group(cmd, "AskUserQuestion")],
    }
    print(json.dumps({"hooks": hooks}, indent=2))


def print_codex_hooks_snippet(osname: str) -> None:
    hooks_path = Path.home() / ".codex" / "hooks.json"
    config_path = Path.home() / ".codex" / "config.toml"
    hook_path = PROJECT_DIR / ("hook.cmd" if osname == "Windows" else "hook.sh")
    print()
    info("Wire Codex hooks (one-time):")
    print(f"   Edit {hooks_path}")
    print(f"   Add (or merge) the following JSON — command points to:")
    print(f"     {hook_path}")
    print()
    cmd = _hook_command(osname)
    hooks = {
        "SessionStart": [_hook_group(cmd, "startup|resume|clear|compact", codex=True)],
        "UserPromptSubmit": [_hook_group(cmd, codex=True)],
        "PreToolUse": [_hook_group(cmd, codex=True)],
        "PermissionRequest": [_hook_group(cmd, codex=True)],
        "PostToolUse": [_hook_group(cmd, codex=True)],
        "PreCompact": [_hook_group(cmd, "manual|auto", codex=True)],
        "PostCompact": [_hook_group(cmd, "manual|auto", codex=True)],
        "SubagentStart": [_hook_group(cmd, codex=True)],
        "SubagentStop": [_hook_group(cmd, codex=True)],
        "Stop": [_hook_group(cmd, codex=True)],
    }
    print(json.dumps({"hooks": hooks}, indent=2))
    print()
    print(f"   Then ensure hooks are enabled in {config_path}:")
    print("""[features]
hooks = true
codex_hooks = true  # older Codex CLI builds""")


def print_hooks_snippets(osname: str) -> None:
    print_claude_hooks_snippet(osname)
    print_codex_hooks_snippet(osname)


def main() -> None:
    ap = argparse.ArgumentParser(description=f"{APP_NAME} installer (cross-platform)")
    ap.add_argument("--uninstall", action="store_true", help="remove auto-start")
    ap.add_argument("--purge", action="store_true",
                    help=f"with --uninstall, also delete ~/.{APP_SLUG}/")
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
        print_hooks_snippets(osname)


if __name__ == "__main__":
    main()
