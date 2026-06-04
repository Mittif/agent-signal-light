# RGB — CH552 USB HID 三路 LED 控制器 (SDCC)

枚举为标准 **HID 设备**（厂商定义 Usage Page 0xFF00），Windows /
macOS / Linux 全部使用系统内置 HID 驱动，**无任何驱动安装步骤**。

## 文件结构

| 文件 | 说明 |
| --- | --- |
| `usb_config.h` | **唯一需要改的配置文件**：VID/PID、LED 引脚号、共阴/共阳 |
| `ch552.h`      | SDCC 用 CH552 SFR 头（本工程子集） |
| `usb_desc.c`   | 设备/配置/HID Report 描述符 |
| `usb_desc.h`   | 描述符 extern 声明、长度常量、HID 描述符偏移 |
| `usb_isr.c`    | USB 中断、SET_REPORT 处理、LED 输出、Timer0 呼吸 PWM |
| `sys.c`        | 时钟与延时 |
| `main.c`       | 入口（含 ISR 的 extern 声明，关键！） |
| `Makefile`     | SDCC 编译 / 烧录脚本 |

## USB 接口

| 项 | 值 |
| --- | --- |
| VID / PID | `0x1209` / `0xC552` |
| Class | HID, no subclass, no protocol |
| Usage Page / Usage | `0xFF00` / `0x0001` (Vendor Defined) |
| 端点 | EP0 控制；EP1 IN Interrupt（HID 规范保留，本工程不主动上传） |
| Output Report | 1 字节，每路 2 bits（见下） |

## 主机协议

发一个 HID Output Report，Report ID = 0（无 ID），数据 1 字节。
该字节里 **每路 LED 占 2 位**：

| bits | LED  | 取值 |
| ---- | ---- | --- |
| `[1:0]` | LED0 | `0=灭`, `1=亮`, `2=呼吸` |
| `[3:2]` | LED1 | 同上 |
| `[5:4]` | LED2 | 同上 |
| `[7:6]` | 保留 | 写 0 |

伪代码：
```
state = (mode_led2 << 4) | (mode_led1 << 2) | mode_led0
hid_device.write(bytes([0x00, state]))   # [报告ID, 编码字节]
```

呼吸由固件内部 Timer0 软件 PWM 实现，亮度按三角波 0→255→0，
一个完整呼吸周期 ≈ **2.4 秒**（PWM ~211 Hz，无可见闪烁）。
亮/灭直接驱动 IO，不参与 PWM。

Windows 上 `hidapi` 会自动走 SET_REPORT 控制传输（无 Interrupt OUT 端点）。
完整 host 端实现见 `../cli/`。

---

## 工具链

| 工具 | 用途 | 安装 |
| --- | --- | --- |
| **SDCC** ≥ 4.0 | 编译 | <https://sdcc.sourceforge.net/> 或 `choco install sdcc` |
| **make** | 构建 | MSYS2 / `choco install make` / 用 Git 自带 `mingw32-make` |
| **wchisp** | 烧录 | <https://github.com/ch32-rs/wchisp>（GUI 替代：[WCHISPTool](https://www.wch.cn/downloads/WCHISPTool_Setup_exe.html)） |

## 编译 / 烧录

```
cd src
make            # → build/RGB.hex （≈ 1.8 KB / 14 KB Flash）
```

进入 BootLoader（按住板上 *Download* 键插 USB）：

```
make flash      # 调用 wchisp 烧录 build/RGB.hex
```

烧完拔插一次，Windows 设备管理器里应在 *Human Interface Devices*
下看到产品名 `RGB-LED`，不会出现"未知设备"。

---

## 关键设计点

1. **xdata 布局**：`Ep0Buffer @0x0000` (10 B) + `Ep1Buffer @0x0040`
   (10 B)，普通 xdata 从 `0x00C0` 开始（见 `Makefile --xram-loc`）。
2. **ISR `extern` 放在 main.c**：让 SDCC 在含 main 的翻译单元里看到
   `__interrupt(INT_NO_USB)`，才会在 0x0043 生成跳转向量，否则
   USB 中断到了不被调度，主机超时报"设备描述符请求失败"。
3. **手动 DATA toggle**：未开 `bUEP_AUTO_TOG`，所有 EP0 数据/状态阶段
   的 `bUEP_T_TOG` 都手动维护，特别是 SET_REPORT 数据阶段后状态阶段
   IN 必须置 1。
4. **HID 描述符位置**：在配置描述符里的偏移由 `HID_DESCR_OFFSET_IN_CFG`
   (= 18) 给出，`GET_DESCRIPTOR(HID)` 直接从配置描述符里切片回，
   无需重复一份。
5. **呼吸 = 软件 PWM**：Timer0 模式 2，重载 `0xDB`，每 ~18.5µs 中断
   一次；累计 256 tick 完成一个 PWM 周期（~211 Hz），每个 PWM 周期
   末让 `BreathLevel` 沿三角波走一步，512 步合计 ~2.4 秒。亮/灭路径
   不进入 PWM 比较，避免微抖。Timer0 ISR 用 `__using(2)`，与 USB
   ISR (`__using(1)`) 寄存器组隔离；二者同优先级不嵌套。
