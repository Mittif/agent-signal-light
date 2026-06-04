;--------------------------------------------------------
; File Created by SDCC : free open source ISO C Compiler
; Version 4.6.0 #16555 (MINGW64)
;--------------------------------------------------------
	.module usb_desc
	
	.optsdcc -mmcs51 --model-small
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _MyReportDescrLen
	.globl _MyProdInfoLen
	.globl _MyManuInfoLen
	.globl _MyLangDescrLen
	.globl _MyCfgDescrLen
	.globl _MyDevDescrLen
	.globl _MyProdInfo
	.globl _MyManuInfo
	.globl _MyLangDescr
	.globl _MyCfgDescr
	.globl _MyDevDescr
	.globl _MyReportDescr
	.globl _U_IS_NAK
	.globl _U_TOG_OK
	.globl _U_SIE_FREE
	.globl _UIF_FIFO_OV
	.globl _UIF_SUSPEND
	.globl _UIF_TRANSFER
	.globl _UIF_BUS_RST
	.globl _TF0
	.globl _TR0
	.globl _IE_USB
	.globl _EA
	.globl _ET0
	.globl _UEP1_DMA_H
	.globl _UEP1_DMA_L
	.globl _UEP0_DMA_H
	.globl _UEP0_DMA_L
	.globl _UEP2_3_MOD
	.globl _UEP4_1_MOD
	.globl _UEP2_DMA_H
	.globl _UEP2_DMA_L
	.globl _USB_DEV_AD
	.globl _USB_CTRL
	.globl _USB_INT_EN
	.globl _UEP0_T_LEN
	.globl _UEP0_CTRL
	.globl _USB_RX_LEN
	.globl _USB_MIS_ST
	.globl _USB_INT_ST
	.globl _USB_INT_FG
	.globl _UEP3_T_LEN
	.globl _UEP3_CTRL
	.globl _UEP2_T_LEN
	.globl _UEP2_CTRL
	.globl _UEP1_T_LEN
	.globl _UEP1_CTRL
	.globl _UDEV_CTRL
	.globl _P3_DIR_PU
	.globl _P3_MOD_OC
	.globl _P3
	.globl _P1_DIR_PU
	.globl _P1_MOD_OC
	.globl _P1
	.globl _TH0
	.globl _TL0
	.globl _TMOD
	.globl _TCON
	.globl _IE_EX
	.globl _IE
	.globl _CLOCK_CFG
	.globl _WAKE_CTRL
	.globl _SAFE_MOD
	.globl _PCON
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
_PCON	=	0x0087
_SAFE_MOD	=	0x00a1
_WAKE_CTRL	=	0x00a9
_CLOCK_CFG	=	0x00b9
_IE	=	0x00a8
_IE_EX	=	0x00e8
_TCON	=	0x0088
_TMOD	=	0x0089
_TL0	=	0x008a
_TH0	=	0x008c
_P1	=	0x0090
_P1_MOD_OC	=	0x0092
_P1_DIR_PU	=	0x0093
_P3	=	0x00b0
_P3_MOD_OC	=	0x0096
_P3_DIR_PU	=	0x0097
_UDEV_CTRL	=	0x00d1
_UEP1_CTRL	=	0x00d2
_UEP1_T_LEN	=	0x00d3
_UEP2_CTRL	=	0x00d4
_UEP2_T_LEN	=	0x00d5
_UEP3_CTRL	=	0x00d6
_UEP3_T_LEN	=	0x00d7
_USB_INT_FG	=	0x00d8
_USB_INT_ST	=	0x00d9
_USB_MIS_ST	=	0x00da
_USB_RX_LEN	=	0x00db
_UEP0_CTRL	=	0x00dc
_UEP0_T_LEN	=	0x00dd
_USB_INT_EN	=	0x00e1
_USB_CTRL	=	0x00e2
_USB_DEV_AD	=	0x00e3
_UEP2_DMA_L	=	0x00e4
_UEP2_DMA_H	=	0x00e5
_UEP4_1_MOD	=	0x00ea
_UEP2_3_MOD	=	0x00eb
_UEP0_DMA_L	=	0x00ec
_UEP0_DMA_H	=	0x00ed
_UEP1_DMA_L	=	0x00ee
_UEP1_DMA_H	=	0x00ef
;--------------------------------------------------------
; special function bits
;--------------------------------------------------------
	.area RSEG    (ABS,DATA)
	.org 0x0000
_ET0	=	0x00a9
_EA	=	0x00af
_IE_USB	=	0x00ea
_TR0	=	0x008c
_TF0	=	0x008d
_UIF_BUS_RST	=	0x00d8
_UIF_TRANSFER	=	0x00d9
_UIF_SUSPEND	=	0x00da
_UIF_FIFO_OV	=	0x00dc
_U_SIE_FREE	=	0x00dd
_U_TOG_OK	=	0x00de
_U_IS_NAK	=	0x00df
;--------------------------------------------------------
; overlayable register banks
;--------------------------------------------------------
	.area REG_BANK_0	(REL,OVR,DATA)
	.ds 8
;--------------------------------------------------------
; internal ram data
;--------------------------------------------------------
	.area DSEG    (DATA)
;--------------------------------------------------------
; overlayable items in internal ram
;--------------------------------------------------------
;--------------------------------------------------------
; indirectly addressable internal ram data
;--------------------------------------------------------
	.area ISEG    (DATA)
;--------------------------------------------------------
; absolute internal ram data
;--------------------------------------------------------
	.area IABS    (ABS,DATA)
	.area IABS    (ABS,DATA)
;--------------------------------------------------------
; bit data
;--------------------------------------------------------
	.area BSEG    (BIT)
;--------------------------------------------------------
; paged external ram data
;--------------------------------------------------------
	.area PSEG    (PAG,XDATA)
;--------------------------------------------------------
; uninitialized external ram data
;--------------------------------------------------------
	.area XSEG    (XDATA)
;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area XABS    (ABS,XDATA)
;--------------------------------------------------------
; initialized external ram data
;--------------------------------------------------------
	.area XISEG   (XDATA)
	.area HOME    (CODE)
	.area GSINIT0 (CODE)
	.area GSINIT1 (CODE)
	.area GSINIT2 (CODE)
	.area GSINIT3 (CODE)
	.area GSINIT4 (CODE)
	.area GSINIT5 (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area CSEG    (CODE)
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area HOME    (CODE)
	.area GSINIT  (CODE)
	.area GSFINAL (CODE)
	.area GSINIT  (CODE)
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area HOME    (CODE)
	.area HOME    (CODE)
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area CSEG    (CODE)
	.area CSEG    (CODE)
	.area CONST   (CODE)
	.area CONST   (CODE)
_MyReportDescr:
	.db #0x06	; 6
	.db #0x00	; 0
	.db #0xff	; 255
	.db #0x09	; 9
	.db #0x01	; 1
	.db #0xa1	; 161
	.db #0x01	; 1
	.db #0x09	; 9
	.db #0x02	; 2
	.db #0x15	; 21
	.db #0x00	; 0
	.db #0x26	; 38
	.db #0xff	; 255
	.db #0x00	; 0
	.db #0x75	; 117	'u'
	.db #0x08	; 8
	.db #0x95	; 149
	.db #0x01	; 1
	.db #0x91	; 145
	.db #0x02	; 2
	.db #0xc0	; 192
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyDevDescr:
	.db #0x12	; 18
	.db #0x01	; 1
	.db #0x10	; 16
	.db #0x01	; 1
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x08	; 8
	.db #0x09	; 9
	.db #0x12	; 18
	.db #0x52	; 82	'R'
	.db #0xc5	; 197
	.db #0x00	; 0
	.db #0x10	; 16
	.db #0x01	; 1
	.db #0x02	; 2
	.db #0x00	; 0
	.db #0x01	; 1
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyCfgDescr:
	.db #0x09	; 9
	.db #0x02	; 2
	.db #0x22	; 34
	.db #0x00	; 0
	.db #0x01	; 1
	.db #0x01	; 1
	.db #0x00	; 0
	.db #0x80	; 128
	.db #0x32	; 50	'2'
	.db #0x09	; 9
	.db #0x04	; 4
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x01	; 1
	.db #0x03	; 3
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x00	; 0
	.db #0x09	; 9
	.db #0x21	; 33
	.db #0x11	; 17
	.db #0x01	; 1
	.db #0x00	; 0
	.db #0x01	; 1
	.db #0x22	; 34
	.db #0x15	; 21
	.db #0x00	; 0
	.db #0x07	; 7
	.db #0x05	; 5
	.db #0x81	; 129
	.db #0x03	; 3
	.db #0x08	; 8
	.db #0x00	; 0
	.db #0x0a	; 10
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyLangDescr:
	.db #0x04	; 4
	.db #0x03	; 3
	.db #0x09	; 9
	.db #0x04	; 4
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyManuInfo:
	.db #0x0e	; 14
	.db #0x03	; 3
	.db #0x6d	; 109	'm'
	.db #0x00	; 0
	.db #0x69	; 105	'i'
	.db #0x00	; 0
	.db #0x74	; 116	't'
	.db #0x00	; 0
	.db #0x74	; 116	't'
	.db #0x00	; 0
	.db #0x69	; 105	'i'
	.db #0x00	; 0
	.db #0x66	; 102	'f'
	.db #0x00	; 0
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyProdInfo:
	.db #0x10	; 16
	.db #0x03	; 3
	.db #0x52	; 82	'R'
	.db #0x00	; 0
	.db #0x47	; 71	'G'
	.db #0x00	; 0
	.db #0x42	; 66	'B'
	.db #0x00	; 0
	.db #0x2d	; 45
	.db #0x00	; 0
	.db #0x4c	; 76	'L'
	.db #0x00	; 0
	.db #0x45	; 69	'E'
	.db #0x00	; 0
	.db #0x44	; 68	'D'
	.db #0x00	; 0
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyDevDescrLen:
	.db #0x12	; 18
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyCfgDescrLen:
	.db #0x22	; 34
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyLangDescrLen:
	.db #0x04	; 4
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyManuInfoLen:
	.db #0x0e	; 14
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyProdInfoLen:
	.db #0x10	; 16
	.area CSEG    (CODE)
	.area CONST   (CODE)
_MyReportDescrLen:
	.db #0x15	; 21
	.area CSEG    (CODE)
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
