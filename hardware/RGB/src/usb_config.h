/********************************************************************
 * usb_config.h
 * 用户可配置项：VID / PID / 字符串描述符 / 3 路 LED 引脚
 * 修改本文件后重新 make 即可。
 ********************************************************************/
#ifndef __USB_CONFIG_H__
#define __USB_CONFIG_H__

/*--------------------------------------------------------------------
 * USB 标识 (小端两字节)
 *   默认沿用 WCH 自定义接口示例的 VID/PID，可被 CH37x 驱动识别。
 *   要走 WinUSB/libusb 自定义路线时改成自己的 VID/PID。
 *------------------------------------------------------------------*/
/* 注意：不要用 0x4348:0x5537 —— 那对 ID 被 WCH 的 ch375wdm.inf 占了，
 * Windows 会直接匹配那个驱动，绕过 WCID 流程导致免驱失效。
 * 1209h 是 pid.codes 测试段；C552 暗示芯片。 */
#define USB_VID_L           0x09
#define USB_VID_H           0x12        /* VID = 0x1209 */
#define USB_PID_L           0x52
#define USB_PID_H           0xC5        /* PID = 0xC552 */

#define USB_VENDOR_STR      'm',0,'i',0,'t',0,'t',0,'i',0,'f',0
#define USB_VENDOR_STR_LEN  (2 + 6*2)

#define USB_PRODUCT_STR     'R',0,'G',0,'B',0,'-',0,'L',0,'E',0,'D',0
#define USB_PRODUCT_STR_LEN (2 + 7*2)

/*--------------------------------------------------------------------
 * LED GPIO 配置
 *   PORT      : P1 / P3 SFR 名
 *   BIT       : 0..7
 *   MOD_OC    : Px_MOD_OC 寄存器名
 *   DIR_PU    : Px_DIR_PU 寄存器名
 *   修改这里就能换引脚，无需触碰其它文件。
 *
 *   默认：LED0=P1.4  LED1=P1.5  LED2=P1.6
 *------------------------------------------------------------------*/
#define LED0_PORT           P1
#define LED0_BIT            4
#define LED0_MOD_OC         P1_MOD_OC
#define LED0_DIR_PU         P1_DIR_PU

#define LED1_PORT           P1
#define LED1_BIT            5
#define LED1_MOD_OC         P1_MOD_OC
#define LED1_DIR_PU         P1_DIR_PU

#define LED2_PORT           P1
#define LED2_BIT            6
#define LED2_MOD_OC         P1_MOD_OC
#define LED2_DIR_PU         P1_DIR_PU

/* 1 = 低电平点亮（共阳/上拉到 VCC）, 0 = 高电平点亮（共阴） */
#define LED_ACTIVE_LOW      1

#endif
