/********************************************************************
 * main.c — RGB 3 路 LED USB 控制器 (SDCC)
 ********************************************************************/
#include "ch552.h"
#include "usb_config.h"

extern void CfgFsys(void);
extern void mDelaymS(UINT16 n);
extern void LEDs_Init(void);
extern void USB_DeviceInit(void);

/* 关键：让 SDCC 在本文件（含 main）感知到 ISR 的 __interrupt(N)，
 * 否则不会在向量地址 0x0043 生成跳转，USB 中断永远不进 ISR。 */
extern void USB_DeviceInterrupt(void) __interrupt(INT_NO_USB);
extern void Timer0Interrupt(void)     __interrupt(INT_NO_TMR0);

void main(void)
{
    CfgFsys();
    mDelaymS(5);

    LEDs_Init();
    USB_DeviceInit();

    EA = 1;

    while (1) {
        /* 一切由 USB 中断处理 */
    }
}
