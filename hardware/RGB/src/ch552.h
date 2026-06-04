/********************************************************************
 * ch552.h — SDCC-compatible CH552 register definitions
 * 仅包含本工程使用到的 SFR / 位 / 常量；如需扩展可参考
 * CH552EVT/EVT/CH552.H（Keil 版）补齐。
 ********************************************************************/
#ifndef __CH552_SDCC_H__
#define __CH552_SDCC_H__

/*--------- 基本类型 ---------*/
typedef unsigned char           UINT8;
typedef unsigned short          UINT16;
typedef unsigned long           UINT32;
typedef __bit                   BOOL;
typedef const unsigned char __code  UINT8C;
typedef unsigned char          *PUINT8;
typedef unsigned char __xdata  *PUINT8X;

#ifndef MIN
#define MIN(a,b)  (((a)<=(b))?(a):(b))
#endif

/*--------- 系统/电源 ---------*/
__sfr __at(0x87) PCON;
__sfr __at(0xA1) SAFE_MOD;
__sfr __at(0xA9) WAKE_CTRL;
__sfr __at(0xB9) CLOCK_CFG;
#define MASK_SYS_CK_SEL     0x07

/*--------- 中断 ---------*/
__sfr  __at(0xA8) IE;
__sbit __at(0xA9) ET0;
__sbit __at(0xAF) EA;

__sfr  __at(0xE8) IE_EX;
__sbit __at(0xEA) IE_USB;

/*--------- Timer0 / Timer1 ---------*/
__sfr  __at(0x88) TCON;
__sbit __at(0x8C) TR0;
__sbit __at(0x8D) TF0;
__sfr  __at(0x89) TMOD;
__sfr  __at(0x8A) TL0;
__sfr  __at(0x8C) TH0;

#define INT_NO_TMR0         1

/*--------- GPIO ---------*/
__sfr __at(0x90) P1;
__sfr __at(0x92) P1_MOD_OC;
__sfr __at(0x93) P1_DIR_PU;

__sfr __at(0xB0) P3;
__sfr __at(0x96) P3_MOD_OC;
__sfr __at(0x97) P3_DIR_PU;

/*--------- USB ---------*/
__sfr __at(0xD1) UDEV_CTRL;
#define bUD_PD_DIS          0x80
#define bUD_PORT_EN         0x01

__sfr __at(0xD2) UEP1_CTRL;
__sfr __at(0xD3) UEP1_T_LEN;
__sfr __at(0xD4) UEP2_CTRL;
__sfr __at(0xD5) UEP2_T_LEN;
__sfr __at(0xD6) UEP3_CTRL;
__sfr __at(0xD7) UEP3_T_LEN;

#define bUEP_R_TOG          0x80
#define bUEP_T_TOG          0x40
#define bUEP_AUTO_TOG       0x10
#define MASK_UEP_R_RES      0x0C
#define UEP_R_RES_ACK       0x00
#define UEP_R_RES_NAK       0x08
#define UEP_R_RES_STALL     0x0C
#define MASK_UEP_T_RES      0x03
#define UEP_T_RES_ACK       0x00
#define UEP_T_RES_NAK       0x02
#define UEP_T_RES_STALL     0x03

/* USB_INT_FG @0xD8 是可位寻址 SFR */
__sfr  __at(0xD8) USB_INT_FG;
__sbit __at(0xD8) UIF_BUS_RST;
__sbit __at(0xD9) UIF_TRANSFER;
__sbit __at(0xDA) UIF_SUSPEND;
__sbit __at(0xDC) UIF_FIFO_OV;
__sbit __at(0xDD) U_SIE_FREE;
__sbit __at(0xDE) U_TOG_OK;
__sbit __at(0xDF) U_IS_NAK;

__sfr __at(0xD9) USB_INT_ST;
#define MASK_UIS_TOKEN      0x30
#define UIS_TOKEN_OUT       0x00
#define UIS_TOKEN_SOF       0x10
#define UIS_TOKEN_IN        0x20
#define UIS_TOKEN_SETUP     0x30
#define MASK_UIS_ENDP       0x0F

__sfr __at(0xDA) USB_MIS_ST;
#define bUMS_SUSPEND        0x04

__sfr __at(0xDB) USB_RX_LEN;
__sfr __at(0xDC) UEP0_CTRL;
__sfr __at(0xDD) UEP0_T_LEN;

__sfr __at(0xE1) USB_INT_EN;
#define bUIE_SUSPEND        0x04
#define bUIE_TRANSFER       0x02
#define bUIE_BUS_RST        0x01

__sfr __at(0xE2) USB_CTRL;
#define bUC_DEV_PU_EN       0x20
#define bUC_INT_BUSY        0x08
#define bUC_DMA_EN          0x01

__sfr __at(0xE3) USB_DEV_AD;
#define bUDA_GP_BIT         0x80

/* DMA 地址寄存器：用 8 位高/低对组合 */
__sfr __at(0xE4) UEP2_DMA_L;
__sfr __at(0xE5) UEP2_DMA_H;
__sfr __at(0xEA) UEP4_1_MOD;
#define bUEP1_RX_EN         0x80
#define bUEP1_TX_EN         0x40

__sfr __at(0xEB) UEP2_3_MOD;
#define bUEP2_RX_EN         0x08
#define bUEP2_TX_EN         0x04

__sfr __at(0xEC) UEP0_DMA_L;
__sfr __at(0xED) UEP0_DMA_H;
__sfr __at(0xEE) UEP1_DMA_L;
__sfr __at(0xEF) UEP1_DMA_H;

#define INT_NO_USB          8

/*--------- USB 协议常量 ---------*/
#ifndef DEFAULT_ENDP0_SIZE
#define DEFAULT_ENDP0_SIZE  8
#endif
#ifndef MAX_PACKET_SIZE
#define MAX_PACKET_SIZE     64
#endif

#define USB_REQ_TYP_MASK        0x60
#define USB_REQ_TYP_STANDARD    0x00
#define USB_REQ_TYP_CLASS       0x20
#define USB_REQ_TYP_VENDOR      0x40
#define USB_REQ_RECIP_MASK      0x1F
#define USB_REQ_RECIP_DEVICE    0x00
#define USB_REQ_RECIP_INTERF    0x01
#define USB_REQ_RECIP_ENDP      0x02

#define USB_GET_STATUS          0x00
#define USB_CLEAR_FEATURE       0x01
#define USB_SET_FEATURE         0x03
#define USB_SET_ADDRESS         0x05
#define USB_GET_DESCRIPTOR      0x06
#define USB_SET_DESCRIPTOR      0x07
#define USB_GET_CONFIGURATION   0x08
#define USB_SET_CONFIGURATION   0x09
#define USB_GET_INTERFACE       0x0A
#define USB_SET_INTERFACE       0x0B

/* HID class */
#define USB_DESCR_TYP_HID       0x21
#define USB_DESCR_TYP_REPORT    0x22
#define HID_GET_REPORT          0x01
#define HID_GET_IDLE            0x02
#define HID_SET_REPORT          0x09
#define HID_SET_IDLE            0x0A
#define HID_SET_PROTOCOL        0x0B

typedef struct _USB_SETUP_REQ {
    UINT8 bRequestType;
    UINT8 bRequest;
    UINT8 wValueL;
    UINT8 wValueH;
    UINT8 wIndexL;
    UINT8 wIndexH;
    UINT8 wLengthL;
    UINT8 wLengthH;
} USB_SETUP_REQ;

typedef USB_SETUP_REQ __xdata *PXUSB_SETUP_REQ;

#endif /* __CH552_SDCC_H__ */
