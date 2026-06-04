/********************************************************************
 * usb_isr.c — USB HID 设备中断 + LED 控制 (SDCC)
 *
 * 主机协议：HID Output Report，1 字节
 *           bit0=LED0, bit1=LED1, bit2=LED2
 * 数据通道：SET_REPORT (类请求 0x09)，data stage 在 EP0 OUT。
 * EP1 IN  : HID 规范要求至少一个 Interrupt IN，本工程暂不主动上传，
 *           主机如果发 IN token 会得到 NAK。
 ********************************************************************/
#include "ch552.h"
#include "usb_config.h"
#include "usb_desc.h"
#include <string.h>

#define THIS_ENDP0_SIZE     DEFAULT_ENDP0_SIZE
#define ENDP1_IN_SIZE       8

__xdata __at(0x0000) UINT8 Ep0Buffer[MIN(64, THIS_ENDP0_SIZE + 2)];
__xdata __at(0x0040) UINT8 Ep1Buffer[MIN(64, ENDP1_IN_SIZE + 2)];

#define UsbSetupBuf  ((PXUSB_SETUP_REQ)Ep0Buffer)

/*--------------------------------------------------------------------
 * 协议：HID Output Report，1 字节
 *   bits[1:0] = LED0 状态, bits[3:2] = LED1, bits[5:4] = LED2
 *   0 = 灭, 1 = 亮, 2 = 呼吸
 * 兼容旧版“点位掩码”需通过 CLI 重新组帧。
 *
 * 呼吸由 Timer0 定时器以 ~18.5µs 间隔做软件 PWM：
 *   - 每 256 个 tick 为 1 个 PWM 周期 (~4.74ms, ~211 Hz)
 *   - 每个 PWM 周期末更新一次三角波亮度 (0..255..0)，512 步 ≈ 2.4 s
 *   - 亮/灭 状态直接驱动 IO，不参与 PWM，避免抖动
 *------------------------------------------------------------------*/
#define LED_OFF      0
#define LED_ON       1
#define LED_BREATHE  2

#if LED_ACTIVE_LOW
#  define LED_DRIVE_ON(P,B)  do { (P) &= ~(1u << (B)); } while (0)
#  define LED_DRIVE_OFF(P,B) do { (P) |=  (1u << (B)); } while (0)
#else
#  define LED_DRIVE_ON(P,B)  do { (P) |=  (1u << (B)); } while (0)
#  define LED_DRIVE_OFF(P,B) do { (P) &= ~(1u << (B)); } while (0)
#endif

volatile __bit Ready    = 0;
volatile UINT8 LedState = 0;             /* 主机最近一次写入的原字节，用于 GET_REPORT */
static   volatile UINT8 LedMode[3] = {0,0,0};

/* PWM / 呼吸状态 (仅 Timer0 ISR 读写) */
static volatile UINT8 PwmTick      = 0;
static volatile UINT8 BreathLevel  = 0;
static volatile __bit BreathRising = 1;

static void DriveStatic(UINT8 i, UINT8 mode)
{
    /* 亮/灭：直接驱动 IO；呼吸：交给 Timer0 ISR */
    if (mode == LED_ON) {
        if (i == 0) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
        else if (i == 1) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
        else LED_DRIVE_ON(LED2_PORT, LED2_BIT);
    } else if (mode == LED_OFF) {
        if (i == 0) LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
        else if (i == 1) LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
        else LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
    }
}

static void ApplyLEDs(UINT8 raw)
{
    UINT8 m0 = (raw >> 0) & 0x03;
    UINT8 m1 = (raw >> 2) & 0x03;
    UINT8 m2 = (raw >> 4) & 0x03;

    if (m0 > LED_BREATHE) m0 = LED_OFF;
    if (m1 > LED_BREATHE) m1 = LED_OFF;
    if (m2 > LED_BREATHE) m2 = LED_OFF;

    LedState = (m2 << 4) | (m1 << 2) | m0;

    LedMode[0] = m0; DriveStatic(0, m0);
    LedMode[1] = m1; DriveStatic(1, m1);
    LedMode[2] = m2; DriveStatic(2, m2);
}

void LEDs_Init(void)
{
    LED0_MOD_OC &= ~(1 << LED0_BIT); LED0_DIR_PU |= (1 << LED0_BIT);
    LED1_MOD_OC &= ~(1 << LED1_BIT); LED1_DIR_PU |= (1 << LED1_BIT);
    LED2_MOD_OC &= ~(1 << LED2_BIT); LED2_DIR_PU |= (1 << LED2_BIT);
    ApplyLEDs(0);

    /* Timer0 模式 2：8 位自动重载，时钟 Fsys/12 = 2 MHz
     * 37 计满 = 18.5µs 中断一次 → 重载 = 256-37 = 0xDB
     * PWM 周期 = 256×18.5µs = 4.74ms；呼吸 512 步 ≈ 2.425s (~2.4s) */
    TMOD = (TMOD & 0xF0) | 0x02;
    TH0  = 0xDB;
    TL0  = 0xDB;
    TR0  = 1;
    ET0  = 1;
}

void Timer0Interrupt(void) __interrupt(INT_NO_TMR0) __using(2)
{
    UINT8 tick = ++PwmTick;

    if (tick == 0) {
        /* 三角波，约 256+256 = 512 步 × 5.12ms ≈ 2.6s 一个完整呼吸 */
        if (BreathRising) {
            if (BreathLevel == 0xFF) { BreathRising = 0; --BreathLevel; }
            else                       ++BreathLevel;
        } else {
            if (BreathLevel == 0x00) { BreathRising = 1; ++BreathLevel; }
            else                       --BreathLevel;
        }
    }

    if (LedMode[0] == LED_BREATHE) {
        if (tick < BreathLevel) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
        else                    LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
    }
    if (LedMode[1] == LED_BREATHE) {
        if (tick < BreathLevel) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
        else                    LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
    }
    if (LedMode[2] == LED_BREATHE) {
        if (tick < BreathLevel) LED_DRIVE_ON(LED2_PORT, LED2_BIT);
        else                    LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
    }
}

void USB_DeviceInterrupt(void) __interrupt(INT_NO_USB) __using(1)
{
    UINT8  errflag;
    UINT16 len;
    static UINT8  SetupReqCode;
    static UINT8  SetupReqType;
    static UINT16 SetupLen;
    static PUINT8 pDescr;

    if (UIF_TRANSFER) {
        switch (USB_INT_ST & (MASK_UIS_TOKEN | MASK_UIS_ENDP)) {

        /* ------ EP1 IN : 我们不主动上传，主机轮询时回 NAK ------ */
        case UIS_TOKEN_IN | 1:
            UEP1_CTRL ^= bUEP_T_TOG;
            UEP1_CTRL  = (UEP1_CTRL & ~MASK_UEP_T_RES) | UEP_T_RES_NAK;
            break;

        /* ------ EP0 SETUP ------ */
        case UIS_TOKEN_SETUP | 0:
            UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
            len = USB_RX_LEN;
            if (len == sizeof(USB_SETUP_REQ)) {
                SetupLen     = ((UINT16)UsbSetupBuf->wLengthH << 8) | UsbSetupBuf->wLengthL;
                len          = 0;
                errflag      = 0;
                SetupReqCode = UsbSetupBuf->bRequest;
                SetupReqType = UsbSetupBuf->bRequestType;

                switch (SetupReqType & USB_REQ_TYP_MASK) {

                case USB_REQ_TYP_STANDARD:
                    switch (SetupReqCode) {
                    case USB_GET_DESCRIPTOR:
                        switch (UsbSetupBuf->wValueH) {
                        case 1:  /* device */
                            pDescr = (PUINT8)MyDevDescr; len = MyDevDescrLen; break;
                        case 2:  /* configuration */
                            pDescr = (PUINT8)MyCfgDescr; len = MyCfgDescrLen; break;
                        case 3:  /* string */
                            switch (UsbSetupBuf->wValueL) {
                            case 0: pDescr = (PUINT8)MyLangDescr; len = MyLangDescrLen; break;
                            case 1: pDescr = (PUINT8)MyManuInfo;  len = MyManuInfoLen;  break;
                            case 2: pDescr = (PUINT8)MyProdInfo;  len = MyProdInfoLen;  break;
                            default: errflag = 0xFF; break;
                            }
                            break;
                        case USB_DESCR_TYP_HID:       /* 0x21 */
                            pDescr = (PUINT8)&MyCfgDescr[HID_DESCR_OFFSET_IN_CFG];
                            len    = HID_DESCR_LEN;
                            break;
                        case USB_DESCR_TYP_REPORT:    /* 0x22 */
                            pDescr = (PUINT8)MyReportDescr;
                            len    = MyReportDescrLen;
                            break;
                        default: errflag = 0xFF; break;
                        }
                        if (SetupLen > len) SetupLen = len;
                        len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
                        memcpy(Ep0Buffer, pDescr, len);
                        SetupLen -= len;
                        pDescr   += len;
                        break;

                    case USB_SET_ADDRESS:
                        SetupLen = UsbSetupBuf->wValueL;
                        break;
                    case USB_GET_CONFIGURATION:
                        Ep0Buffer[0] = Ready;
                        if (SetupLen >= 1) len = 1;
                        break;
                    case USB_SET_CONFIGURATION:
                        Ready = UsbSetupBuf->wValueL ? 1 : 0;
                        break;
                    case USB_CLEAR_FEATURE:
                        if ((SetupReqType & USB_REQ_RECIP_MASK) == USB_REQ_RECIP_ENDP) {
                            switch (UsbSetupBuf->wIndexL) {
                            case 0x81:
                                UEP1_CTRL = (UEP1_CTRL & ~(bUEP_T_TOG | MASK_UEP_T_RES)) | UEP_T_RES_NAK;
                                break;
                            default:
                                errflag = 0xFF; break;
                            }
                        } else {
                            errflag = 0xFF;
                        }
                        break;
                    case USB_GET_INTERFACE:
                        Ep0Buffer[0] = 0x00;
                        if (SetupLen >= 1) len = 1;
                        break;
                    case USB_GET_STATUS:
                        Ep0Buffer[0] = 0x00;
                        Ep0Buffer[1] = 0x00;
                        len = SetupLen >= 2 ? 2 : SetupLen;
                        break;
                    default:
                        errflag = 0xFF; break;
                    }
                    break;

                case USB_REQ_TYP_CLASS:
                    /* HID 类请求 */
                    switch (SetupReqCode) {
                    case HID_SET_REPORT:
                        /* OUT 数据会在 UIS_TOKEN_OUT | 0 阶段到达，
                         * 仅 1 字节，长度直接看 SetupLen */
                        len = 0;
                        break;
                    case HID_SET_IDLE:
                    case HID_SET_PROTOCOL:
                        len = 0;
                        break;
                    case HID_GET_REPORT:
                        Ep0Buffer[0] = LedState;
                        len = SetupLen >= 1 ? 1 : SetupLen;
                        break;
                    case HID_GET_IDLE:
                        Ep0Buffer[0] = 0x00;
                        len = SetupLen >= 1 ? 1 : SetupLen;
                        break;
                    default:
                        errflag = 0xFF; break;
                    }
                    break;

                default:
                    errflag = 0xFF; break;
                }
            } else {
                errflag = 0xFF;
            }

            if (errflag == 0xFF) {
                UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
            } else {
                UEP0_T_LEN = (len <= THIS_ENDP0_SIZE) ? len : 0;
                UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
            }
            break;

        /* ------ EP0 IN : 多包描述符续传 ------ */
        case UIS_TOKEN_IN | 0:
            switch (SetupReqCode) {
            case USB_GET_DESCRIPTOR:
                len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
                memcpy(Ep0Buffer, pDescr, len);
                SetupLen -= len;
                pDescr   += len;
                UEP0_T_LEN = len;
                UEP0_CTRL ^= bUEP_T_TOG;
                break;
            case USB_SET_ADDRESS:
                USB_DEV_AD  = (USB_DEV_AD & bUDA_GP_BIT) | (UINT8)SetupLen;
                UEP0_CTRL   = UEP_R_RES_ACK | UEP_T_RES_NAK;
                break;
            default:
                UEP0_T_LEN = 0;
                UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
                break;
            }
            break;

        /* ------ EP0 OUT : HID SET_REPORT 的数据阶段 ------ */
        case UIS_TOKEN_OUT | 0:
            if (U_TOG_OK) {
                if ((SetupReqType & USB_REQ_TYP_MASK) == USB_REQ_TYP_CLASS
                    && SetupReqCode == HID_SET_REPORT
                    && USB_RX_LEN >= 1) {
                    ApplyLEDs(Ep0Buffer[0]);
                }
            }
            /* 状态阶段：主机马上发 IN，我们用 DATA1 ZLP 回应 */
            UEP0_T_LEN = 0;
            UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
            break;

        default:
            break;
        }
        UIF_TRANSFER = 0;
    } else if (UIF_BUS_RST) {
        UEP0_CTRL    = UEP_R_RES_ACK | UEP_T_RES_NAK;
        UEP1_CTRL    = UEP_T_RES_NAK;
        Ready        = 0;
        USB_DEV_AD   = 0x00;
        UIF_SUSPEND  = 0;
        UIF_TRANSFER = 0;
        UIF_BUS_RST  = 0;
    } else if (UIF_SUSPEND) {
        UIF_SUSPEND = 0;
    } else {
        USB_INT_FG = 0xFF;
    }
}

void USB_DeviceInit(void)
{
    UINT16 ep0_addr = (UINT16)(UINT8 __xdata *)Ep0Buffer;
    UINT16 ep1_addr = (UINT16)(UINT8 __xdata *)Ep1Buffer;

    IE_USB     = 0;
    USB_CTRL   = 0x00;
    UEP4_1_MOD = bUEP1_TX_EN;       /* EP1 仅上传 (IN) */
    UEP2_3_MOD = 0x00;

    UEP0_DMA_L = (UINT8)(ep0_addr & 0xFF);
    UEP0_DMA_H = (UINT8)(ep0_addr >> 8);
    UEP1_DMA_L = (UINT8)(ep1_addr & 0xFF);
    UEP1_DMA_H = (UINT8)(ep1_addr >> 8);

    UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
    UEP1_CTRL  = UEP_T_RES_NAK;

    USB_DEV_AD = 0x00;
    UDEV_CTRL  = bUD_PD_DIS;
    USB_CTRL   = bUC_DEV_PU_EN | bUC_INT_BUSY | bUC_DMA_EN;
    UDEV_CTRL |= bUD_PORT_EN;
    USB_INT_FG = 0xFF;
    USB_INT_EN = bUIE_SUSPEND | bUIE_TRANSFER | bUIE_BUS_RST;
    IE_USB     = 1;
}
