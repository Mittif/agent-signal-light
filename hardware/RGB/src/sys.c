/********************************************************************
 * sys.c — 时钟 + 延时 (SDCC)
 * 24 MHz 内部 RC，满足 USB 模块 ≥ 12 MHz 要求。
 ********************************************************************/
#include "ch552.h"

#define FREQ_SYS    24000000UL

#define NOP() __asm__("nop")

void CfgFsys(void)
{
    SAFE_MOD = 0x55;
    SAFE_MOD = 0xAA;
    /* Fsys = Fpll/4 = 24 MHz */
    CLOCK_CFG = (CLOCK_CFG & ~MASK_SYS_CK_SEL) | 0x06;
    SAFE_MOD = 0x00;
}

void mDelayuS(UINT16 n)
{
    while (n) {
#if   FREQ_SYS <= 6000000
        /* 6 MHz：循环本身约 1 µs */
#elif FREQ_SYS <= 12000000
        NOP(); NOP();
#elif FREQ_SYS <= 24000000
        NOP(); NOP(); NOP(); NOP(); NOP(); NOP(); NOP();
#endif
        --n;
    }
}

void mDelaymS(UINT16 n)
{
    while (n) { mDelayuS(1000); --n; }
}
