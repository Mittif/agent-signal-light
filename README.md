# Agent Signal Light

A tiny local daemon that turns Claude Code and Codex hook events into a
signal-light effect — in your browser, and on an optional CH552 USB HID light.

- Tracks every concurrent agent session and shows the highest-priority event.
- Drives a CH552 USB HID light (VID `0x1209` / PID `0xc552`).
- Browser mirror **and** config editor at <http://127.0.0.1:7878>.
- Per-agent (Claude / Codex) bindings, priorities, and live-response filter.
- Custom effects, event bindings, priority order, all editable from the UI.
- Installs as a login daemon on macOS, Windows, and Linux.
- Hook scripts are non-blocking (1-second cap), so a stopped daemon never blocks
  your agent.

## 中文说明

Agent Signal Light 是一个本地小守护进程，用来把 Claude Code 和 Codex
的 hook 事件转换成信号灯效果。它可以在浏览器中显示当前状态，也可以驱动
可选的 CH552 USB HID 灯。

主要功能：

- 同时跟踪多个 agent 会话，并显示优先级最高的事件状态。
- 支持 Claude / Codex 分别配置事件绑定、优先级和实时响应过滤。
- 浏览器镜像和配置编辑器地址为 <http://127.0.0.1:7878>。
- 支持自定义灯效、事件绑定和事件优先级。
- 可安装为 macOS、Windows、Linux 的登录自启动服务。
- hook 脚本有 1 秒超时并始终返回成功，守护进程停止时不会阻塞 agent。

快速安装：

Windows:

```bat
.\install.cmd
```

macOS / Linux:

```sh
python3 install.py
```

安装脚本会创建默认配置、注册自启动服务、启动守护进程，并尽量自动写入
Claude Code 和 Codex 的 hook 配置。若不希望安装脚本修改 agent 配置文件，
请使用：

Windows:

```bat
.\install.cmd --no-hooks
```

macOS / Linux:

```sh
python3 install.py --no-hooks
```

卸载但保留配置：

Windows:

```bat
.\install.cmd --uninstall
```

macOS / Linux:

```sh
python3 install.py --uninstall
```

卸载并删除本工具的数据目录：

Windows:

```bat
.\install.cmd --uninstall --purge
```

macOS / Linux:

```sh
python3 install.py --uninstall --purge
```

默认灯效含义：

| 状态 | 灯效 |
| ---- | ---- |
| 会话开始或停止 | 绿灯常亮 |
| 正在工作、调用工具、压缩上下文、子 agent 运行 | 黄灯呼吸 |
| 权限请求、通知、提问、等待用户输入 | 黄灯闪烁 |
| 停止失败 | 红灯闪烁 |
| 没有活动会话 | 熄灭 |

配置文件位于 `~/.agent-signal-light/config.json`。建议优先通过浏览器页面编辑，
也可以直接修改 JSON 或通过 `/api/config` 接口保存。

隐私与安全注意事项：

- 守护进程只监听 `127.0.0.1:7878`，不主动上传数据。
- 本地浏览器页面会显示活动会话的 `cwd` 路径，路径可能包含项目名或用户名。
- 安装脚本会备份并修改 Claude Code / Codex 的 hook 配置；使用 `--no-hooks`
  可以改为手动合并。

## Requirements

- Python 3.10 or newer.
- On Windows, install Python from <https://www.python.org/downloads/windows/>
  and enable **Add python.exe to PATH**, or run with the Python launcher (`py -3`).
- `curl` (already present on every supported OS).
- Optional: a CH552 USB HID light. Without one, the browser mirror still works.

## One-command install

From a fresh clone:

Windows PowerShell / Command Prompt:

```bat
.\install.cmd
```

macOS / Linux:

```sh
python3 install.py
```

The installer will:

1. install `hidapi` into your user Python environment (best-effort);
2. write the default config to `~/.agent-signal-light/config.json`;
3. register a login-time auto-start service
   (LaunchAgent on macOS, Startup VBS on Windows, systemd `--user` unit on Linux);
4. start the daemon and wait for it to come up;
5. **auto-merge Claude Code hooks** into `~/.claude/settings.json`
   (preserves your other hooks, makes a `.json.bak` first);
6. **auto-append Codex hooks** to `~/.codex/config.toml`
   (only if you don't already have a `[hooks]` table, with a `.toml.bak` backup).

After that, open <http://127.0.0.1:7878> and start using Claude Code or Codex —
events will flow in immediately.

Pass `--no-hooks` if you'd rather merge the snippets yourself; the installer
will print them to stdout instead.

## Uninstall

Keep your config:

Windows:

```bat
.\install.cmd --uninstall
```

macOS / Linux:

```sh
python3 install.py --uninstall
```

Wipe `~/.agent-signal-light/` too:

Windows:

```bat
.\install.cmd --uninstall --purge
```

macOS / Linux:

```sh
python3 install.py --uninstall --purge
```

The uninstaller does **not** touch your `~/.claude/settings.json` or
`~/.codex/config.toml` — delete the hook entries from those files manually if
you want them gone.

## Default light states

The defaults map common agent states like this:

| State                                                    | Effect          |
| -------------------------------------------------------- | --------------- |
| Session started or stopped                               | green on        |
| Prompt submitted, tool use, compaction, subagent running | yellow breathe  |
| Permission request, notification, elicitation, question  | yellow blink    |
| Stop failure                                             | red blink       |
| No active session                                        | off             |

When multiple sessions are active, the daemon picks the highest-priority event
according to the configured `event_priority`. The defaults order: error → waiting
for user → idle/completed → working.

## Configuration

User config lives at:

```
~/.agent-signal-light/config.json
```

Edit it in the browser editor, or POST a new version to `/api/config`. The
config holds:

- `effects` — named LED animations (frames of 3 LED states + duration).
- `event_bindings` — hook event names → effect IDs.
- `event_priority` — global, highest first.
- `agent_priority` — per-agent (`claude` / `codex`) priority order.

LED states per frame are `off`, `on`, or `breathe`. Frame `ms` is the duration;
use `null` to hold a frame until the active event changes.

### Per-agent overrides

Event keys may be prefixed with `claude/` or `codex/` to bind that agent
specifically — the daemon checks the agent-prefixed key first, then falls back
to the unprefixed global binding. The browser editor's **All / Claude / Codex**
switch chooses which scope you're editing, and the same switch sets the live
response filter (`All`, `Claude`-only, or `Codex`-only).

### Tool-specific bindings

```
PreToolUse:AskUserQuestion
PostToolUse:AskUserQuestion
```

Combine the two:

```
claude/UserPromptSubmit
codex/PreToolUse:AskUserQuestion
```

## HTTP API

The daemon binds to `127.0.0.1` only and rejects requests with a non-loopback
`Host` header (DNS-rebinding mitigation).

| Method | Path                  | Description                                |
| ------ | --------------------- | ------------------------------------------ |
| GET    | `/`                   | Browser mirror + config editor             |
| GET    | `/stream`             | SSE: effect, LEDs, HID status, sessions    |
| GET    | `/api/status`         | One-shot status JSON                       |
| GET    | `/api/config`         | Current configuration                      |
| POST   | `/api/config`         | Save a validated configuration             |
| POST   | `/api/config/reset`   | Restore the bundled defaults               |
| POST   | `/api/agent-filter`   | Set live-response scope: `all/claude/codex`|
| POST   | `/hook`               | Agent hook payload (used by `hook.sh`/`.cmd`) |
| POST   | `/event`              | Legacy manual test: `G` / `Y` / `W` / `R` / `O` |

Manual test:

```sh
curl -X POST http://127.0.0.1:7878/event --data-binary G   # green
curl -X POST http://127.0.0.1:7878/event --data-binary Y   # yellow breathe
curl -X POST http://127.0.0.1:7878/event --data-binary W   # waiting-for-user blink
curl -X POST http://127.0.0.1:7878/event --data-binary R   # red blink
curl -X POST http://127.0.0.1:7878/event --data-binary O   # off
```

## Running manually

For development or troubleshooting, run the daemon directly:

Windows:

```bat
py -3 server.py
```

macOS / Linux:

```sh
python3 server.py
```

It listens on `127.0.0.1:7878` and writes logs to stdout. The installed
auto-start daemon writes logs to:

```
~/.agent-signal-light/daemon.log
```

## Repository layout

```
server.py             Local HTTP/SSE daemon, browser UI, config, HID output
install.py            Cross-platform installer / uninstaller / hook auto-wirer
config.default.json   Bundled default effects, bindings, and priorities
hook.sh               macOS/Linux hook forwarder
hook.cmd              Windows hook forwarder
install.cmd           Windows installer launcher
```

## Privacy and security notes

- The daemon binds **only** to loopback (`127.0.0.1`), validates the `Host`
  header, and emits no cross-origin headers. This mitigates DNS rebinding and
  prevents normal cross-origin reads of the SSE/API responses; keep the port
  local-only and avoid exposing it through proxies or tunnels.
- Active session `cwd` paths are visible in the local browser UI; nothing is
  uploaded anywhere.
- Hook scripts cap latency at 1 second and always exit `0`, so a stopped or
  missing daemon never blocks your agent.
