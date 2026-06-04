# rgb-cli — host controller for the CH552 USB HID 3-LED board

设备是标准 HID 类，跨平台免驱：Windows / macOS / Linux 直接能用，
不需要 Zadig、不需要 INF、不需要管理员权限。

## 准备

板子烧了 `../src/build/RGB.hex` 并正常插上即可。设备管理器里应在
*Human Interface Devices* 下能看到 `RGB-LED`。

## 安装

```cmd
cd cli
uv sync
```

`uv` 会建虚拟环境到 `cli\.venv`，安装 `hidapi`（自带 native lib，
不需要额外装系统库）。

## 使用

每路 LED 有三种状态：`off` / `on` / `breathe`（呼吸周期约 2.4 秒）。

```cmd
uv run rgb on                       :: 三盏全亮
uv run rgb on 0 2                   :: LED0 + LED2 亮，其余灭
uv run rgb off                      :: 全灭
uv run rgb off 1                    :: 只灭 LED1，其余灭（其它路也置 off）
uv run rgb breathe                  :: 三盏一起呼吸
uv run rgb breathe 1                :: 只 LED1 呼吸，其余灭
uv run rgb set off on breathe       :: 分别指定三路
uv run rgb info                     :: 看 HID 描述符 (VID/PID/usage 等)
```

注意 `on/off/breathe <indices...>` 是「只对列出的下标设为该状态、
其余设为 off」。若想保留多路独立状态，请用 `rgb set <s0> <s1> <s2>`。

入口脚本 `rgb` 在 `pyproject.toml [project.scripts]` 里注册，激活
venv 后也可直接 `rgb on 0`。

## 协议（与固件 `../src/usb_isr.c` 对齐）

| 项 | 值 |
| --- | --- |
| VID / PID | `0x1209` / `0xC552` |
| HID Usage Page / Usage | `0xFF00` / `0x0001` |
| Output Report | 1 字节，每路 2 bits（见下） |

| bits | LED  | 取值 |
| ---- | ---- | --- |
| `[1:0]` | LED0 | `0=off, 1=on, 2=breathe` |
| `[3:2]` | LED1 | 同上 |
| `[5:4]` | LED2 | 同上 |
| `[7:6]` | 保留 | 写 0 |

`hid.device.write([0x00, state])` —— 第一个字节是 Report ID（本设备
没有声明 ID，固定 0），第二个字节才是上面编码后的状态字节。

设备没有 Interrupt OUT 端点，`hidapi` 自动改走 **SET_REPORT 控制传输**
(`bmRequestType=0x21, bRequest=0x09`)，固件在 EP0 OUT 数据阶段读出
编码字节并立即应用。呼吸由固件内部 Timer0 软件 PWM 驱动（~211 Hz），
完整呼吸周期 ≈ **2.4 秒**。

## 当前命令面

```
rgb [-h] {on,off,breathe,set,info} ...
    on      [I...]            把列出的 LED 设为 on，其余 off；无参数 = 全亮
    off     [I...]            把列出的 LED 设为 off，其余 off（兼容写法）
    breathe [I...]            把列出的 LED 设为呼吸，其余 off
    set     S0 S1 S2          单独指定三路状态：off|on|breathe (或 0|1|2)
    info                      dump HID descriptor info
```

## 跨平台说明

- **Windows**：直接 `uv sync` + `uv run rgb on`。无需 Zadig。
- **Linux**：可能要给非 root 用户 `udev` 权限：
  ```
  echo 'SUBSYSTEM=="hidraw", ATTRS{idVendor}=="1209", ATTRS{idProduct}=="c552", MODE="0666"' \
    | sudo tee /etc/udev/rules.d/99-rgb-led.rules
  sudo udevadm control --reload-rules && sudo udevadm trigger
  ```
- **macOS**：开箱即用。
