;--------------------------------------------------------
; File Created by SDCC : free open source ISO C Compiler
; Version 4.6.0 #16555 (MINGW64)
;--------------------------------------------------------
	.module sys
	
	.optsdcc -mmcs51 --model-small
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _mDelaymS
	.globl _mDelayuS
	.globl _CfgFsys
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
	.area	OSEG    (OVR,DATA)
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
;------------------------------------------------------------
;Allocation info for local variables in function 'CfgFsys'
;------------------------------------------------------------
;	sys.c:11: void CfgFsys(void)
;	-----------------------------------------
;	 function CfgFsys
;	-----------------------------------------
_CfgFsys:
	ar7 = 0x07
	ar6 = 0x06
	ar5 = 0x05
	ar4 = 0x04
	ar3 = 0x03
	ar2 = 0x02
	ar1 = 0x01
	ar0 = 0x00
;	sys.c:13: SAFE_MOD = 0x55;
	mov	_SAFE_MOD,#0x55
;	sys.c:14: SAFE_MOD = 0xAA;
	mov	_SAFE_MOD,#0xaa
;	sys.c:16: CLOCK_CFG = (CLOCK_CFG & ~MASK_SYS_CK_SEL) | 0x06;
	mov	a,#0xf8
	anl	a,_CLOCK_CFG
	orl	a,#0x06
	mov	_CLOCK_CFG,a
;	sys.c:17: SAFE_MOD = 0x00;
	mov	_SAFE_MOD,#0x00
;	sys.c:18: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'mDelayuS'
;------------------------------------------------------------
;n             Allocated to registers 
;------------------------------------------------------------
;	sys.c:20: void mDelayuS(UINT16 n)
;	-----------------------------------------
;	 function mDelayuS
;	-----------------------------------------
_mDelayuS:
	mov	r6, dpl
	mov	r7, dph
;	sys.c:22: while (n) {
00101$:
	mov	a,r6
	orl	a,r7
	jz	00104$
;	sys.c:28: NOP(); NOP(); NOP(); NOP(); NOP(); NOP(); NOP();
	nop
	nop
	nop
	nop
	nop
	nop
	nop
;	sys.c:30: --n;
	dec	r6
	cjne	r6,#0xff,00122$
	dec	r7
00122$:
	sjmp	00101$
00104$:
;	sys.c:32: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'mDelaymS'
;------------------------------------------------------------
;n             Allocated to registers 
;------------------------------------------------------------
;	sys.c:34: void mDelaymS(UINT16 n)
;	-----------------------------------------
;	 function mDelaymS
;	-----------------------------------------
_mDelaymS:
	mov	r6, dpl
	mov	r7, dph
;	sys.c:36: while (n) { mDelayuS(1000); --n; }
00101$:
	mov	a,r6
	orl	a,r7
	jz	00104$
	mov	dptr,#0x03e8
	push	ar7
	push	ar6
	lcall	_mDelayuS
	pop	ar6
	pop	ar7
	dec	r6
	cjne	r6,#0xff,00122$
	dec	r7
00122$:
	sjmp	00101$
00104$:
;	sys.c:37: }
	ret
	.area CSEG    (CODE)
	.area CONST   (CODE)
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
