;--------------------------------------------------------
; File Created by SDCC : free open source ISO C Compiler
; Version 4.6.0 #16555 (MINGW64)
;--------------------------------------------------------
	.module usb_isr
	
	.optsdcc -mmcs51 --model-small
;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl _USB_DeviceInit
	.globl _USB_DeviceInterrupt
	.globl _Timer0Interrupt
	.globl _LEDs_Init
	.globl ___memcpy
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
	.globl _Ep1Buffer
	.globl _Ep0Buffer
	.globl _Ready
	.globl _LedState
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
	.area REG_BANK_1	(REL,OVR,DATA)
	.ds 8
	.area REG_BANK_2	(REL,OVR,DATA)
	.ds 8
;--------------------------------------------------------
; overlayable bit register bank
;--------------------------------------------------------
	.area BIT_BANK	(REL,OVR,DATA)
bits:
	.ds 1
	b0 = bits[0]
	b1 = bits[1]
	b2 = bits[2]
	b3 = bits[3]
	b4 = bits[4]
	b5 = bits[5]
	b6 = bits[6]
	b7 = bits[7]
;--------------------------------------------------------
; internal ram data
;--------------------------------------------------------
	.area DSEG    (DATA)
_LedState::
	.ds 1
_LedMode:
	.ds 3
_PwmTick:
	.ds 1
_BreathLevel:
	.ds 1
_USB_DeviceInterrupt_SetupReqCode_10000_78:
	.ds 1
_USB_DeviceInterrupt_SetupReqType_10000_78:
	.ds 1
_USB_DeviceInterrupt_SetupLen_10000_78:
	.ds 2
_USB_DeviceInterrupt_pDescr_10000_78:
	.ds 3
;--------------------------------------------------------
; overlayable items in internal ram
;--------------------------------------------------------
	.area	OSEG    (OVR,DATA)
_DriveStatic_PARM_2:
	.ds 1
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
_Ready::
	.ds 1
_BreathRising:
	.ds 1
;--------------------------------------------------------
; paged external ram data
;--------------------------------------------------------
	.area PSEG    (PAG,XDATA)
;--------------------------------------------------------
; uninitialized external ram data
;--------------------------------------------------------
	.area XSEG    (XDATA)
_Ep0Buffer	=	0x0000
_Ep1Buffer	=	0x0040
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
;	usb_isr.c:47: volatile UINT8 LedState = 0;             /* 主机最近一次写入的原字节，用于 GET_REPORT */
	mov	_LedState,#0x00
;	usb_isr.c:48: static   volatile UINT8 LedMode[3] = {0,0,0};
	mov	_LedMode,#0x00
	mov	(_LedMode + 0x0001),#0x00
	mov	(_LedMode + 0x0002),#0x00
;	usb_isr.c:51: static volatile UINT8 PwmTick      = 0;
	mov	_PwmTick,#0x00
;	usb_isr.c:52: static volatile UINT8 BreathLevel  = 0;
	mov	_BreathLevel,#0x00
;	usb_isr.c:46: volatile __bit Ready    = 0;
;	assignBit
	clr	_Ready
;	usb_isr.c:53: static volatile __bit BreathRising = 1;
;	assignBit
	setb	_BreathRising
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
;Allocation info for local variables in function 'DriveStatic'
;------------------------------------------------------------
;mode          Allocated with name '_DriveStatic_PARM_2'
;i             Allocated to registers r7 
;------------------------------------------------------------
;	usb_isr.c:55: static void DriveStatic(UINT8 i, UINT8 mode)
;	-----------------------------------------
;	 function DriveStatic
;	-----------------------------------------
_DriveStatic:
	ar7 = 0x07
	ar6 = 0x06
	ar5 = 0x05
	ar4 = 0x04
	ar3 = 0x03
	ar2 = 0x02
	ar1 = 0x01
	ar0 = 0x00
	mov	r7, dpl
;	usb_isr.c:58: if (mode == LED_ON) {
	mov	a,#0x01
	cjne	a,_DriveStatic_PARM_2,00134$
;	usb_isr.c:59: if (i == 0) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
	mov	a,r7
	jnz	00114$
	anl	_P1,#0xef
	ret
00114$:
;	usb_isr.c:60: else if (i == 1) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
	cjne	r7,#0x01,00107$
	anl	_P1,#0xdf
;	usb_isr.c:61: else LED_DRIVE_ON(LED2_PORT, LED2_BIT);
	ret
00107$:
	anl	_P1,#0xbf
	ret
00134$:
;	usb_isr.c:62: } else if (mode == LED_OFF) {
	mov	a,_DriveStatic_PARM_2
	jnz	00136$
;	usb_isr.c:63: if (i == 0) LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
	mov	a,r7
	jnz	00129$
	orl	_P1,#0x10
	ret
00129$:
;	usb_isr.c:64: else if (i == 1) LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
	cjne	r7,#0x01,00122$
	orl	_P1,#0x20
;	usb_isr.c:65: else LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
	ret
00122$:
	orl	_P1,#0x40
00136$:
;	usb_isr.c:67: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'ApplyLEDs'
;------------------------------------------------------------
;raw           Allocated to registers r7 
;m0            Allocated to registers r6 
;m1            Allocated to registers r5 
;m2            Allocated to registers r7 
;------------------------------------------------------------
;	usb_isr.c:69: static void ApplyLEDs(UINT8 raw)
;	-----------------------------------------
;	 function ApplyLEDs
;	-----------------------------------------
_ApplyLEDs:
	mov	r7, dpl
;	usb_isr.c:71: UINT8 m0 = (raw >> 0) & 0x03;
	mov	ar6,r7
	anl	ar6,#0x03
;	usb_isr.c:72: UINT8 m1 = (raw >> 2) & 0x03;
	mov	a,r7
	rr	a
	rr	a
	anl	a,#0x3f
	mov	r5,a
	anl	ar5,#0x03
;	usb_isr.c:73: UINT8 m2 = (raw >> 4) & 0x03;
	mov	a,r7
	swap	a
	anl	a,#0x0f
	mov	r7,a
	anl	ar7,#0x03
;	usb_isr.c:75: if (m0 > LED_BREATHE) m0 = LED_OFF;
	mov	a,r6
	add	a,#0xff - 0x02
	jnc	00102$
;	free result
	mov	r6,#0x00
00102$:
;	usb_isr.c:76: if (m1 > LED_BREATHE) m1 = LED_OFF;
	mov	a,r5
	add	a,#0xff - 0x02
	jnc	00104$
;	free result
	mov	r5,#0x00
00104$:
;	usb_isr.c:77: if (m2 > LED_BREATHE) m2 = LED_OFF;
	mov	a,r7
	add	a,#0xff - 0x02
	jnc	00106$
;	free result
	mov	r7,#0x00
00106$:
;	usb_isr.c:79: LedState = (m2 << 4) | (m1 << 2) | m0;
	mov	a,r7
	swap	a
	anl	a,#0xf0
	mov	r4,a
	mov	a,r5
	add	a,r5
	add	a,acc
	orl	a,r4
	orl	a,r6
	mov	_LedState,a
;	usb_isr.c:81: LedMode[0] = m0; DriveStatic(0, m0);
	mov	_LedMode,r6
	mov	_DriveStatic_PARM_2,r6
	mov	dpl, #0x00
	push	ar7
	push	ar5
	lcall	_DriveStatic
	pop	ar5
;	usb_isr.c:82: LedMode[1] = m1; DriveStatic(1, m1);
	mov	(_LedMode + 0x0001),r5
	mov	_DriveStatic_PARM_2,r5
	mov	dpl, #0x01
	lcall	_DriveStatic
	pop	ar7
;	usb_isr.c:83: LedMode[2] = m2; DriveStatic(2, m2);
	mov	(_LedMode + 0x0002),r7
	mov	_DriveStatic_PARM_2,r7
	mov	dpl, #0x02
;	usb_isr.c:84: }
	ljmp	_DriveStatic
;------------------------------------------------------------
;Allocation info for local variables in function 'LEDs_Init'
;------------------------------------------------------------
;	usb_isr.c:86: void LEDs_Init(void)
;	-----------------------------------------
;	 function LEDs_Init
;	-----------------------------------------
_LEDs_Init:
;	usb_isr.c:88: LED0_MOD_OC &= ~(1 << LED0_BIT); LED0_DIR_PU |= (1 << LED0_BIT);
	anl	_P1_MOD_OC,#0xef
	orl	_P1_DIR_PU,#0x10
;	usb_isr.c:89: LED1_MOD_OC &= ~(1 << LED1_BIT); LED1_DIR_PU |= (1 << LED1_BIT);
	anl	_P1_MOD_OC,#0xdf
	orl	_P1_DIR_PU,#0x20
;	usb_isr.c:90: LED2_MOD_OC &= ~(1 << LED2_BIT); LED2_DIR_PU |= (1 << LED2_BIT);
	anl	_P1_MOD_OC,#0xbf
	orl	_P1_DIR_PU,#0x40
;	usb_isr.c:91: ApplyLEDs(0);
	mov	dpl, #0x00
	lcall	_ApplyLEDs
;	usb_isr.c:96: TMOD = (TMOD & 0xF0) | 0x02;
	mov	a,_TMOD
	anl	a,#0xf0
	orl	a,#0x02
	mov	_TMOD,a
;	usb_isr.c:97: TH0  = 0xDB;
	mov	_TH0,#0xdb
;	usb_isr.c:98: TL0  = 0xDB;
	mov	_TL0,#0xdb
;	usb_isr.c:99: TR0  = 1;
;	assignBit
	setb	_TR0
;	usb_isr.c:100: ET0  = 1;
;	assignBit
	setb	_ET0
;	usb_isr.c:101: }
	ret
;------------------------------------------------------------
;Allocation info for local variables in function 'Timer0Interrupt'
;------------------------------------------------------------
;tick          Allocated to registers r7 
;------------------------------------------------------------
;	usb_isr.c:103: void Timer0Interrupt(void) __interrupt(INT_NO_TMR0) __using(2)
;	-----------------------------------------
;	 function Timer0Interrupt
;	-----------------------------------------
_Timer0Interrupt:
	ar7 = 0x17
	ar6 = 0x16
	ar5 = 0x15
	ar4 = 0x14
	ar3 = 0x13
	ar2 = 0x12
	ar1 = 0x11
	ar0 = 0x10
	push	acc
	push	psw
	mov	psw,#0x10
;	usb_isr.c:105: UINT8 tick = ++PwmTick;
	mov	a,_PwmTick
	inc	a
;	usb_isr.c:107: if (tick == 0) {
	mov	r7,a
	mov	_PwmTick,r7
	jnz	00111$
;	usb_isr.c:109: if (BreathRising) {
	jnb	_BreathRising,00108$
;	usb_isr.c:110: if (BreathLevel == 0xFF) { BreathRising = 0; --BreathLevel; }
	mov	a,#0xff
	cjne	a,_BreathLevel,00102$
;	assignBit
	clr	_BreathRising
	dec	_BreathLevel
	sjmp	00111$
00102$:
;	usb_isr.c:111: else                       ++BreathLevel;
	inc	_BreathLevel
	sjmp	00111$
00108$:
;	usb_isr.c:113: if (BreathLevel == 0x00) { BreathRising = 1; ++BreathLevel; }
	mov	a,_BreathLevel
	jnz	00105$
;	assignBit
	setb	_BreathRising
	inc	_BreathLevel
	sjmp	00111$
00105$:
;	usb_isr.c:114: else                       --BreathLevel;
	dec	_BreathLevel
00111$:
;	usb_isr.c:118: if (LedMode[0] == LED_BREATHE) {
	mov	a,#0x02
	cjne	a,_LedMode,00122$
;	usb_isr.c:119: if (tick < BreathLevel) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
	clr	c
	mov	a,r7
	subb	a,_BreathLevel
	jnc	00115$
	anl	_P1,#0xef
;	usb_isr.c:120: else                    LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
	sjmp	00122$
00115$:
	orl	_P1,#0x10
00122$:
;	usb_isr.c:122: if (LedMode[1] == LED_BREATHE) {
	mov	a,#0x02
	cjne	a,(_LedMode + 0x0001),00133$
;	usb_isr.c:123: if (tick < BreathLevel) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
	clr	c
	mov	a,r7
	subb	a,_BreathLevel
	jnc	00126$
	anl	_P1,#0xdf
;	usb_isr.c:124: else                    LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
	sjmp	00133$
00126$:
	orl	_P1,#0x20
00133$:
;	usb_isr.c:126: if (LedMode[2] == LED_BREATHE) {
	mov	a,#0x02
	cjne	a,(_LedMode + 0x0002),00145$
;	usb_isr.c:127: if (tick < BreathLevel) LED_DRIVE_ON(LED2_PORT, LED2_BIT);
	clr	c
	mov	a,r7
	subb	a,_BreathLevel
	jnc	00137$
	anl	_P1,#0xbf
;	usb_isr.c:128: else                    LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
	sjmp	00145$
00137$:
	orl	_P1,#0x40
00145$:
;	usb_isr.c:130: }
	pop	psw
	pop	acc
	reti
;	eliminated unneeded push/pop dpl
;	eliminated unneeded push/pop dph
;	eliminated unneeded push/pop b
;------------------------------------------------------------
;Allocation info for local variables in function 'USB_DeviceInterrupt'
;------------------------------------------------------------
;SetupReqCode  Allocated with name '_USB_DeviceInterrupt_SetupReqCode_10000_78'
;SetupReqType  Allocated with name '_USB_DeviceInterrupt_SetupReqType_10000_78'
;SetupLen      Allocated with name '_USB_DeviceInterrupt_SetupLen_10000_78'
;pDescr        Allocated with name '_USB_DeviceInterrupt_pDescr_10000_78'
;errflag       Allocated to registers r5 
;len           Allocated to registers r6 r7 
;------------------------------------------------------------
;	usb_isr.c:132: void USB_DeviceInterrupt(void) __interrupt(INT_NO_USB) __using(1)
;	-----------------------------------------
;	 function USB_DeviceInterrupt
;	-----------------------------------------
_USB_DeviceInterrupt:
	ar7 = 0x0f
	ar6 = 0x0e
	ar5 = 0x0d
	ar4 = 0x0c
	ar3 = 0x0b
	ar2 = 0x0a
	ar1 = 0x09
	ar0 = 0x08
	push	bits
	push	acc
	push	b
	push	dpl
	push	dph
	push	(0+7)
	push	(0+6)
	push	(0+5)
	push	(0+4)
	push	(0+3)
	push	(0+2)
	push	(0+1)
	push	(0+0)
	push	psw
	mov	psw,#0x08
;	usb_isr.c:141: if (UIF_TRANSFER) {
	jb	_UIF_TRANSFER,00526$
	ljmp	00174$
00526$:
;	usb_isr.c:142: switch (USB_INT_ST & (MASK_UIS_TOKEN | MASK_UIS_ENDP)) {
	mov	a,#0x3f
	anl	a,_USB_INT_ST
	mov	r7,a
	mov	r6,a
	jnz	00527$
	ljmp	00158$
00527$:
	cjne	r7,#0x20,00528$
	ljmp	00153$
00528$:
	cjne	r7,#0x21,00529$
	sjmp	00101$
00529$:
	cjne	r7,#0x30,00530$
	sjmp	00102$
00530$:
	ljmp	00166$
;	usb_isr.c:145: case UIS_TOKEN_IN | 1:
00101$:
;	usb_isr.c:146: UEP1_CTRL ^= bUEP_T_TOG;
	xrl	_UEP1_CTRL,#0x40
;	usb_isr.c:147: UEP1_CTRL  = (UEP1_CTRL & ~MASK_UEP_T_RES) | UEP_T_RES_NAK;
	mov	a,#0xfc
	anl	a,_UEP1_CTRL
	orl	a,#0x02
	mov	_UEP1_CTRL,a
;	usb_isr.c:148: break;
	ljmp	00166$
;	usb_isr.c:151: case UIS_TOKEN_SETUP | 0:
00102$:
;	usb_isr.c:152: UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
	mov	_UEP0_CTRL,#0xc0
;	usb_isr.c:153: len = USB_RX_LEN;
	mov	r6,_USB_RX_LEN
	mov	r7,#0x00
;	usb_isr.c:154: if (len == sizeof(USB_SETUP_REQ)) {
	cjne	r6,#0x08,00531$
	cjne	r7,#0x00,00531$
	sjmp	00532$
00531$:
	ljmp	00148$
00532$:
;	usb_isr.c:155: SetupLen     = ((UINT16)UsbSetupBuf->wLengthH << 8) | UsbSetupBuf->wLengthL;
	mov	dptr,#(_Ep0Buffer + 0x0007)
	movx	a,@dptr
	mov	r4,a
	mov	r5,#0x00
	mov	dptr,#(_Ep0Buffer + 0x0006)
	movx	a,@dptr
	mov	r2,#0x00
	orl	a,r5
	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
	mov	a,r2
	orl	a,r4
	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
;	usb_isr.c:156: len          = 0;
	mov	r6,#0x00
	mov	r7,#0x00
;	usb_isr.c:157: errflag      = 0;
;	usb_isr.c:158: SetupReqCode = UsbSetupBuf->bRequest;
	mov	dptr,#(_Ep0Buffer + 0x0001)
	movx	a,@dptr
	mov	_USB_DeviceInterrupt_SetupReqCode_10000_78,a
;	usb_isr.c:159: SetupReqType = UsbSetupBuf->bRequestType;
	mov	dptr,#_Ep0Buffer
	movx	a,@dptr
	mov	_USB_DeviceInterrupt_SetupReqType_10000_78,a
;	usb_isr.c:161: switch (SetupReqType & USB_REQ_TYP_MASK) {
	mov	r4,_USB_DeviceInterrupt_SetupReqType_10000_78
	mov	a,#0x60
	anl	a,r4
	mov	r3,a
	jz	00103$
	cjne	r3,#0x20,00534$
	ljmp	00137$
00534$:
	ljmp	00145$
;	usb_isr.c:163: case USB_REQ_TYP_STANDARD:
00103$:
;	usb_isr.c:164: switch (SetupReqCode) {
	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
	add	a,#0xff - 0x0a
	jnc	00535$
	ljmp	00135$
00535$:
;	free result
	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
	add	a,#(00536$-3-.)
	movc	a,@a+pc
	mov	dpl,a
	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
	add	a,#(00537$-3-.)
	movc	a,@a+pc
	mov	dph,a
	clr	a
	jmp	@a+dptr
00536$:
	.db	00134$
	.db	00124$
	.db	00135$
	.db	00135$
	.db	00135$
	.db	00119$
	.db	00104$
	.db	00135$
	.db	00120$
	.db	00123$
	.db	00131$
00537$:
	.db	00134$>>8
	.db	00124$>>8
	.db	00135$>>8
	.db	00135$>>8
	.db	00135$>>8
	.db	00119$>>8
	.db	00104$>>8
	.db	00135$>>8
	.db	00120$>>8
	.db	00123$>>8
	.db	00131$>>8
;	usb_isr.c:165: case USB_GET_DESCRIPTOR:
00104$:
;	usb_isr.c:166: switch (UsbSetupBuf->wValueH) {
	mov	dptr,#(_Ep0Buffer + 0x0003)
	movx	a,@dptr
	mov	r3,a
	cjne	r3,#0x01,00538$
	sjmp	00105$
00538$:
	cjne	r3,#0x02,00539$
	sjmp	00106$
00539$:
	cjne	r3,#0x03,00540$
	sjmp	00107$
00540$:
	cjne	r3,#0x21,00541$
	ljmp	00113$
00541$:
	cjne	r3,#0x22,00542$
	ljmp	00114$
00542$:
	ljmp	00115$
;	usb_isr.c:167: case 1:  /* device */
00105$:
;	usb_isr.c:168: pDescr = (PUINT8)MyDevDescr; len = MyDevDescrLen; break;
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyDevDescr
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyDevDescr >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
	mov	dptr,#_MyDevDescrLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
	ljmp	00116$
;	usb_isr.c:169: case 2:  /* configuration */
00106$:
;	usb_isr.c:170: pDescr = (PUINT8)MyCfgDescr; len = MyCfgDescrLen; break;
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyCfgDescr
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyCfgDescr >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
	mov	dptr,#_MyCfgDescrLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
;	usb_isr.c:171: case 3:  /* string */
	sjmp	00116$
00107$:
;	usb_isr.c:172: switch (UsbSetupBuf->wValueL) {
	mov	dptr,#(_Ep0Buffer + 0x0002)
	movx	a,@dptr
	mov	r3,a
	jz	00108$
	cjne	r3,#0x01,00544$
	sjmp	00109$
00544$:
;	usb_isr.c:173: case 0: pDescr = (PUINT8)MyLangDescr; len = MyLangDescrLen; break;
	cjne	r3,#0x02,00111$
	sjmp	00110$
00108$:
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyLangDescr
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyLangDescr >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
	mov	dptr,#_MyLangDescrLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
;	usb_isr.c:174: case 1: pDescr = (PUINT8)MyManuInfo;  len = MyManuInfoLen;  break;
	sjmp	00116$
00109$:
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyManuInfo
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyManuInfo >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
	mov	dptr,#_MyManuInfoLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
;	usb_isr.c:175: case 2: pDescr = (PUINT8)MyProdInfo;  len = MyProdInfoLen;  break;
	sjmp	00116$
00110$:
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyProdInfo
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyProdInfo >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
	mov	dptr,#_MyProdInfoLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
;	usb_isr.c:176: default: errflag = 0xFF; break;
	sjmp	00116$
00111$:
	mov	r5,#0xff
;	usb_isr.c:178: break;
;	usb_isr.c:179: case USB_DESCR_TYP_HID:       /* 0x21 */
	sjmp	00116$
00113$:
;	usb_isr.c:180: pDescr = (PUINT8)&MyCfgDescr[HID_DESCR_OFFSET_IN_CFG];
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#(_MyCfgDescr + 0x0012)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#((_MyCfgDescr + 0x0012) >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
;	usb_isr.c:181: len    = HID_DESCR_LEN;
	mov	r6,#0x09
	mov	r7,#0x00
;	usb_isr.c:182: break;
;	usb_isr.c:183: case USB_DESCR_TYP_REPORT:    /* 0x22 */
	sjmp	00116$
00114$:
;	usb_isr.c:184: pDescr = (PUINT8)MyReportDescr;
	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyReportDescr
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyReportDescr >> 8)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
;	usb_isr.c:185: len    = MyReportDescrLen;
	mov	dptr,#_MyReportDescrLen
	clr	a
	movc	a,@a+dptr
	mov	r6,a
	mov	r7,#0x00
;	usb_isr.c:186: break;
;	usb_isr.c:187: default: errflag = 0xFF; break;
	sjmp	00116$
00115$:
	mov	r5,#0xff
;	usb_isr.c:188: }
00116$:
;	usb_isr.c:189: if (SetupLen > len) SetupLen = len;
	clr	c
	mov	a,r6
	subb	a,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	a,r7
	subb	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	jnc	00118$
;	free result
	mov	_USB_DeviceInterrupt_SetupLen_10000_78,r6
	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),r7
00118$:
;	usb_isr.c:190: len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r2
	subb	a,#0x08
	mov	a,r3
	subb	a,#0x00
	jc	00178$
	mov	r2,#0x08
	mov	r3,#0x00
	sjmp	00179$
00178$:
	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
00179$:
	mov	ar6,r2
	mov	ar7,r3
;	usb_isr.c:191: memcpy(Ep0Buffer, pDescr, len);
	mov	___memcpy_PARM_2,_USB_DeviceInterrupt_pDescr_10000_78
	mov	(___memcpy_PARM_2 + 1),(_USB_DeviceInterrupt_pDescr_10000_78 + 1)
	mov	(___memcpy_PARM_2 + 2),(_USB_DeviceInterrupt_pDescr_10000_78 + 2)
	mov	___memcpy_PARM_3,r6
	mov	(___memcpy_PARM_3 + 1),r7
	mov	dptr,#_Ep0Buffer
	mov	b, #0x00
	push	ar7
	push	ar6
	push	ar5
	mov	psw,#0x00
	lcall	___memcpy
	mov	psw,#0x08
	pop	ar5
	pop	ar6
	pop	ar7
;	usb_isr.c:192: SetupLen -= len;
	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
	clr	c
	subb	a,r6
	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
	mov	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	subb	a,r7
	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
;	usb_isr.c:193: pDescr   += len;
	mov	a,r6
	add	a, _USB_DeviceInterrupt_pDescr_10000_78
	mov	_USB_DeviceInterrupt_pDescr_10000_78,a
	mov	a,r7
	addc	a, (_USB_DeviceInterrupt_pDescr_10000_78 + 1)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),a
;	usb_isr.c:194: break;
	ljmp	00149$
;	usb_isr.c:196: case USB_SET_ADDRESS:
00119$:
;	usb_isr.c:197: SetupLen = UsbSetupBuf->wValueL;
	mov	dptr,#(_Ep0Buffer + 0x0002)
	movx	a,@dptr
	mov	r3,a
	mov	_USB_DeviceInterrupt_SetupLen_10000_78,r3
	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),#0x00
;	usb_isr.c:198: break;
	ljmp	00149$
;	usb_isr.c:199: case USB_GET_CONFIGURATION:
00120$:
;	usb_isr.c:200: Ep0Buffer[0] = Ready;
	mov	c,_Ready
	clr	a
	rlc	a
	mov	dptr,#_Ep0Buffer
	movx	@dptr,a
;	usb_isr.c:201: if (SetupLen >= 1) len = 1;
	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r2
	subb	a,#0x01
	mov	a,r3
	subb	a,#0x00
	jnc	00548$
	ljmp	00149$
00548$:
	mov	r6,#0x01
	mov	r7,#0x00
;	usb_isr.c:202: break;
	ljmp	00149$
;	usb_isr.c:203: case USB_SET_CONFIGURATION:
00123$:
;	usb_isr.c:204: Ready = UsbSetupBuf->wValueL ? 1 : 0;
	mov	dptr,#(_Ep0Buffer + 0x0002)
	movx	a,@dptr
;	assignBit
	mov	r3,a
	add	a,#0xff
	mov	_Ready,c
;	usb_isr.c:205: break;
	ljmp	00149$
;	usb_isr.c:206: case USB_CLEAR_FEATURE:
00124$:
;	usb_isr.c:207: if ((SetupReqType & USB_REQ_RECIP_MASK) == USB_REQ_RECIP_ENDP) {
	anl	ar4,#0x1f
	cjne	r4,#0x02,00129$
;	usb_isr.c:208: switch (UsbSetupBuf->wIndexL) {
	mov	dptr,#(_Ep0Buffer + 0x0004)
	movx	a,@dptr
	mov	r4,a
	cjne	r4,#0x81,00126$
;	usb_isr.c:210: UEP1_CTRL = (UEP1_CTRL & ~(bUEP_T_TOG | MASK_UEP_T_RES)) | UEP_T_RES_NAK;
	mov	a,#0xbc
	anl	a,_UEP1_CTRL
	orl	a,#0x02
	mov	_UEP1_CTRL,a
;	usb_isr.c:211: break;
	ljmp	00149$
;	usb_isr.c:212: default:
00126$:
;	usb_isr.c:213: errflag = 0xFF; break;
	mov	r5,#0xff
;	usb_isr.c:214: }
	ljmp	00149$
00129$:
;	usb_isr.c:216: errflag = 0xFF;
	mov	r5,#0xff
;	usb_isr.c:218: break;
	ljmp	00149$
;	usb_isr.c:219: case USB_GET_INTERFACE:
00131$:
;	usb_isr.c:220: Ep0Buffer[0] = 0x00;
	mov	dptr,#_Ep0Buffer
	clr	a
	movx	@dptr,a
;	usb_isr.c:221: if (SetupLen >= 1) len = 1;
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r3
	subb	a,#0x01
	mov	a,r4
	subb	a,#0x00
	jnc	00553$
	ljmp	00149$
00553$:
	mov	r6,#0x01
	mov	r7,#0x00
;	usb_isr.c:222: break;
	ljmp	00149$
;	usb_isr.c:223: case USB_GET_STATUS:
00134$:
;	usb_isr.c:224: Ep0Buffer[0] = 0x00;
	mov	dptr,#_Ep0Buffer
	clr	a
	movx	@dptr,a
;	usb_isr.c:225: Ep0Buffer[1] = 0x00;
	mov	dptr,#(_Ep0Buffer + 0x0001)
	movx	@dptr,a
;	usb_isr.c:226: len = SetupLen >= 2 ? 2 : SetupLen;
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r3
	subb	a,#0x02
	mov	a,r4
	subb	a,#0x00
	jc	00180$
	mov	r3,#0x02
	mov	r4,#0x00
	sjmp	00181$
00180$:
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
00181$:
	mov	ar6,r3
	mov	ar7,r4
;	usb_isr.c:227: break;
	ljmp	00149$
;	usb_isr.c:228: default:
00135$:
;	usb_isr.c:229: errflag = 0xFF; break;
	mov	r5,#0xff
;	usb_isr.c:231: break;
	ljmp	00149$
;	usb_isr.c:233: case USB_REQ_TYP_CLASS:
00137$:
;	usb_isr.c:235: switch (SetupReqCode) {
	mov	a,#0x01
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00555$
	sjmp	00141$
00555$:
	mov	a,#0x02
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00556$
	sjmp	00142$
00556$:
	mov	a,#0x09
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00557$
	sjmp	00138$
00557$:
	mov	a,#0x0a
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00558$
	sjmp	00140$
00558$:
	mov	a,#0x0b
;	usb_isr.c:236: case HID_SET_REPORT:
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00143$
	sjmp	00140$
00138$:
;	usb_isr.c:239: len = 0;
	mov	r6,#0x00
	mov	r7,#0x00
;	usb_isr.c:240: break;
;	usb_isr.c:242: case HID_SET_PROTOCOL:
	sjmp	00149$
00140$:
;	usb_isr.c:243: len = 0;
	mov	r6,#0x00
	mov	r7,#0x00
;	usb_isr.c:244: break;
;	usb_isr.c:245: case HID_GET_REPORT:
	sjmp	00149$
00141$:
;	usb_isr.c:246: Ep0Buffer[0] = LedState;
	mov	dptr,#_Ep0Buffer
	mov	a,_LedState
	movx	@dptr,a
;	usb_isr.c:247: len = SetupLen >= 1 ? 1 : SetupLen;
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r3
	subb	a,#0x01
	mov	a,r4
	subb	a,#0x00
	jc	00182$
	mov	r3,#0x01
	mov	r4,#0x00
	sjmp	00183$
00182$:
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
00183$:
	mov	ar6,r3
	mov	ar7,r4
;	usb_isr.c:248: break;
;	usb_isr.c:249: case HID_GET_IDLE:
	sjmp	00149$
00142$:
;	usb_isr.c:250: Ep0Buffer[0] = 0x00;
	mov	dptr,#_Ep0Buffer
	clr	a
	movx	@dptr,a
;	usb_isr.c:251: len = SetupLen >= 1 ? 1 : SetupLen;
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r3
	subb	a,#0x01
	mov	a,r4
	subb	a,#0x00
	jc	00184$
	mov	r3,#0x01
	mov	r4,#0x00
	sjmp	00185$
00184$:
	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
00185$:
	mov	ar6,r3
	mov	ar7,r4
;	usb_isr.c:252: break;
;	usb_isr.c:253: default:
	sjmp	00149$
00143$:
;	usb_isr.c:254: errflag = 0xFF; break;
	mov	r5,#0xff
;	usb_isr.c:256: break;
;	usb_isr.c:258: default:
	sjmp	00149$
00145$:
;	usb_isr.c:259: errflag = 0xFF; break;
	mov	r5,#0xff
;	usb_isr.c:260: }
	sjmp	00149$
00148$:
;	usb_isr.c:262: errflag = 0xFF;
	mov	r5,#0xff
00149$:
;	usb_isr.c:265: if (errflag == 0xFF) {
	cjne	r5,#0xff,00151$
;	usb_isr.c:266: UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
	mov	_UEP0_CTRL,#0xcf
	ljmp	00166$
00151$:
;	usb_isr.c:268: UEP0_T_LEN = (len <= THIS_ENDP0_SIZE) ? len : 0;
	clr	c
	mov	a,#0x08
	subb	a,r6
	clr	a
	subb	a,r7
;	free result
	jnc	00187$
	mov	r6,#0x00
00187$:
	mov	_UEP0_T_LEN,r6
;	usb_isr.c:269: UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
	mov	_UEP0_CTRL,#0xc0
;	usb_isr.c:271: break;
	ljmp	00166$
;	usb_isr.c:274: case UIS_TOKEN_IN | 0:
00153$:
;	usb_isr.c:275: switch (SetupReqCode) {
	mov	a,#0x05
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00565$
	sjmp	00155$
00565$:
	mov	a,#0x06
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00156$
;	usb_isr.c:277: len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
	mov	r6,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r7,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	clr	c
	mov	a,r6
	subb	a,#0x08
	mov	a,r7
	subb	a,#0x00
	jc	00188$
	mov	r6,#0x08
	mov	r7,#0x00
	sjmp	00189$
00188$:
	mov	r6,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r7,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
00189$:
;	usb_isr.c:278: memcpy(Ep0Buffer, pDescr, len);
	mov	___memcpy_PARM_2,_USB_DeviceInterrupt_pDescr_10000_78
	mov	(___memcpy_PARM_2 + 1),(_USB_DeviceInterrupt_pDescr_10000_78 + 1)
	mov	(___memcpy_PARM_2 + 2),(_USB_DeviceInterrupt_pDescr_10000_78 + 2)
	mov	___memcpy_PARM_3,r6
	mov	(___memcpy_PARM_3 + 1),r7
	mov	dptr,#_Ep0Buffer
	mov	b, #0x00
	push	ar7
	push	ar6
	mov	psw,#0x00
	lcall	___memcpy
	mov	psw,#0x08
	pop	ar6
	pop	ar7
;	usb_isr.c:279: SetupLen -= len;
	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
	clr	c
	subb	a,r6
	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
	mov	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
	subb	a,r7
	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
;	usb_isr.c:280: pDescr   += len;
	mov	a,r6
	add	a, _USB_DeviceInterrupt_pDescr_10000_78
	mov	_USB_DeviceInterrupt_pDescr_10000_78,a
	mov	a,r7
	addc	a, (_USB_DeviceInterrupt_pDescr_10000_78 + 1)
	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),a
;	usb_isr.c:281: UEP0_T_LEN = len;
	mov	_UEP0_T_LEN,r6
;	usb_isr.c:282: UEP0_CTRL ^= bUEP_T_TOG;
	xrl	_UEP0_CTRL,#0x40
;	usb_isr.c:283: break;
;	usb_isr.c:284: case USB_SET_ADDRESS:
	sjmp	00166$
00155$:
;	usb_isr.c:285: USB_DEV_AD  = (USB_DEV_AD & bUDA_GP_BIT) | (UINT8)SetupLen;
	mov	a,_USB_DEV_AD
	anl	a,#0x80
	mov	r7,a
	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
	mov	r6,a
	orl	a,r7
	mov	_USB_DEV_AD,a
;	usb_isr.c:286: UEP0_CTRL   = UEP_R_RES_ACK | UEP_T_RES_NAK;
	mov	_UEP0_CTRL,#0x02
;	usb_isr.c:287: break;
;	usb_isr.c:288: default:
	sjmp	00166$
00156$:
;	usb_isr.c:289: UEP0_T_LEN = 0;
	mov	_UEP0_T_LEN,#0x00
;	usb_isr.c:290: UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
	mov	_UEP0_CTRL,#0x02
;	usb_isr.c:293: break;
;	usb_isr.c:296: case UIS_TOKEN_OUT | 0:
	sjmp	00166$
00158$:
;	usb_isr.c:297: if (U_TOG_OK) {
	jnb	_U_TOG_OK,00164$
;	usb_isr.c:298: if ((SetupReqType & USB_REQ_TYP_MASK) == USB_REQ_TYP_CLASS
	mov	r7,_USB_DeviceInterrupt_SetupReqType_10000_78
	anl	ar7,#0x60
	cjne	r7,#0x20,00164$
;	usb_isr.c:300: && USB_RX_LEN >= 1) {
	mov	a,#0x09
	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00164$
	mov	a,#0x100 - 0x01
	add	a,_USB_RX_LEN
	jnc	00164$
;	usb_isr.c:301: ApplyLEDs(Ep0Buffer[0]);
	mov	dptr,#_Ep0Buffer
	movx	a,@dptr
	mov	dpl,a
	mov	psw,#0x00
	lcall	_ApplyLEDs
	mov	psw,#0x08
00164$:
;	usb_isr.c:305: UEP0_T_LEN = 0;
	mov	_UEP0_T_LEN,#0x00
;	usb_isr.c:306: UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
	mov	_UEP0_CTRL,#0xc0
;	usb_isr.c:311: }
00166$:
;	usb_isr.c:312: UIF_TRANSFER = 0;
;	assignBit
	clr	_UIF_TRANSFER
	sjmp	00176$
00174$:
;	usb_isr.c:313: } else if (UIF_BUS_RST) {
	jnb	_UIF_BUS_RST,00171$
;	usb_isr.c:314: UEP0_CTRL    = UEP_R_RES_ACK | UEP_T_RES_NAK;
	mov	_UEP0_CTRL,#0x02
;	usb_isr.c:315: UEP1_CTRL    = UEP_T_RES_NAK;
	mov	_UEP1_CTRL,#0x02
;	usb_isr.c:316: Ready        = 0;
;	assignBit
	clr	_Ready
;	usb_isr.c:317: USB_DEV_AD   = 0x00;
	mov	_USB_DEV_AD,#0x00
;	usb_isr.c:318: UIF_SUSPEND  = 0;
;	assignBit
	clr	_UIF_SUSPEND
;	usb_isr.c:319: UIF_TRANSFER = 0;
;	assignBit
	clr	_UIF_TRANSFER
;	usb_isr.c:320: UIF_BUS_RST  = 0;
;	assignBit
	clr	_UIF_BUS_RST
	sjmp	00176$
00171$:
;	usb_isr.c:321: } else if (UIF_SUSPEND) {
;	usb_isr.c:322: UIF_SUSPEND = 0;
;	assignBit
	jbc	_UIF_SUSPEND,00176$
;	usb_isr.c:324: USB_INT_FG = 0xFF;
	mov	_USB_INT_FG,#0xff
00176$:
;	usb_isr.c:326: }
	pop	psw
	pop	(0+0)
	pop	(0+1)
	pop	(0+2)
	pop	(0+3)
	pop	(0+4)
	pop	(0+5)
	pop	(0+6)
	pop	(0+7)
	pop	dph
	pop	dpl
	pop	b
	pop	acc
	pop	bits
	ljmp	sdcc_atomic_maybe_rollback
;------------------------------------------------------------
;Allocation info for local variables in function 'USB_DeviceInit'
;------------------------------------------------------------
;ep0_addr      Allocated to registers r6 r7 
;ep1_addr      Allocated to registers r4 r5 
;------------------------------------------------------------
;	usb_isr.c:328: void USB_DeviceInit(void)
;	-----------------------------------------
;	 function USB_DeviceInit
;	-----------------------------------------
_USB_DeviceInit:
	ar7 = 0x07
	ar6 = 0x06
	ar5 = 0x05
	ar4 = 0x04
	ar3 = 0x03
	ar2 = 0x02
	ar1 = 0x01
	ar0 = 0x00
;	usb_isr.c:330: UINT16 ep0_addr = (UINT16)(UINT8 __xdata *)Ep0Buffer;
	mov	r6,#_Ep0Buffer
	mov	r7,#(_Ep0Buffer >> 8)
;	usb_isr.c:331: UINT16 ep1_addr = (UINT16)(UINT8 __xdata *)Ep1Buffer;
	mov	r4,#_Ep1Buffer
	mov	r5,#(_Ep1Buffer >> 8)
;	usb_isr.c:333: IE_USB     = 0;
;	assignBit
	clr	_IE_USB
;	usb_isr.c:334: USB_CTRL   = 0x00;
	mov	_USB_CTRL,#0x00
;	usb_isr.c:335: UEP4_1_MOD = bUEP1_TX_EN;       /* EP1 仅上传 (IN) */
	mov	_UEP4_1_MOD,#0x40
;	usb_isr.c:336: UEP2_3_MOD = 0x00;
	mov	_UEP2_3_MOD,#0x00
;	usb_isr.c:338: UEP0_DMA_L = (UINT8)(ep0_addr & 0xFF);
	mov	_UEP0_DMA_L,r6
;	usb_isr.c:339: UEP0_DMA_H = (UINT8)(ep0_addr >> 8);
	mov	_UEP0_DMA_H,r7
;	usb_isr.c:340: UEP1_DMA_L = (UINT8)(ep1_addr & 0xFF);
	mov	_UEP1_DMA_L,r4
;	usb_isr.c:341: UEP1_DMA_H = (UINT8)(ep1_addr >> 8);
	mov	_UEP1_DMA_H,r5
;	usb_isr.c:343: UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
	mov	_UEP0_CTRL,#0x02
;	usb_isr.c:344: UEP1_CTRL  = UEP_T_RES_NAK;
	mov	_UEP1_CTRL,#0x02
;	usb_isr.c:346: USB_DEV_AD = 0x00;
	mov	_USB_DEV_AD,#0x00
;	usb_isr.c:347: UDEV_CTRL  = bUD_PD_DIS;
	mov	_UDEV_CTRL,#0x80
;	usb_isr.c:348: USB_CTRL   = bUC_DEV_PU_EN | bUC_INT_BUSY | bUC_DMA_EN;
	mov	_USB_CTRL,#0x29
;	usb_isr.c:349: UDEV_CTRL |= bUD_PORT_EN;
	orl	_UDEV_CTRL,#0x01
;	usb_isr.c:350: USB_INT_FG = 0xFF;
	mov	_USB_INT_FG,#0xff
;	usb_isr.c:351: USB_INT_EN = bUIE_SUSPEND | bUIE_TRANSFER | bUIE_BUS_RST;
	mov	_USB_INT_EN,#0x07
;	usb_isr.c:352: IE_USB     = 1;
;	assignBit
	setb	_IE_USB
;	usb_isr.c:353: }
	ret
	.area CSEG    (CODE)
	.area CONST   (CODE)
	.area XINIT   (CODE)
	.area CABS    (ABS,CODE)
