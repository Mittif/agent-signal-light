                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (MINGW64)
                                      4 ;--------------------------------------------------------
                                      5 	.module usb_isr
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-small
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _USB_DeviceInit
                                     12 	.globl _USB_DeviceInterrupt
                                     13 	.globl _Timer0Interrupt
                                     14 	.globl _LEDs_Init
                                     15 	.globl ___memcpy
                                     16 	.globl _U_IS_NAK
                                     17 	.globl _U_TOG_OK
                                     18 	.globl _U_SIE_FREE
                                     19 	.globl _UIF_FIFO_OV
                                     20 	.globl _UIF_SUSPEND
                                     21 	.globl _UIF_TRANSFER
                                     22 	.globl _UIF_BUS_RST
                                     23 	.globl _TF0
                                     24 	.globl _TR0
                                     25 	.globl _IE_USB
                                     26 	.globl _EA
                                     27 	.globl _ET0
                                     28 	.globl _UEP1_DMA_H
                                     29 	.globl _UEP1_DMA_L
                                     30 	.globl _UEP0_DMA_H
                                     31 	.globl _UEP0_DMA_L
                                     32 	.globl _UEP2_3_MOD
                                     33 	.globl _UEP4_1_MOD
                                     34 	.globl _UEP2_DMA_H
                                     35 	.globl _UEP2_DMA_L
                                     36 	.globl _USB_DEV_AD
                                     37 	.globl _USB_CTRL
                                     38 	.globl _USB_INT_EN
                                     39 	.globl _UEP0_T_LEN
                                     40 	.globl _UEP0_CTRL
                                     41 	.globl _USB_RX_LEN
                                     42 	.globl _USB_MIS_ST
                                     43 	.globl _USB_INT_ST
                                     44 	.globl _USB_INT_FG
                                     45 	.globl _UEP3_T_LEN
                                     46 	.globl _UEP3_CTRL
                                     47 	.globl _UEP2_T_LEN
                                     48 	.globl _UEP2_CTRL
                                     49 	.globl _UEP1_T_LEN
                                     50 	.globl _UEP1_CTRL
                                     51 	.globl _UDEV_CTRL
                                     52 	.globl _P3_DIR_PU
                                     53 	.globl _P3_MOD_OC
                                     54 	.globl _P3
                                     55 	.globl _P1_DIR_PU
                                     56 	.globl _P1_MOD_OC
                                     57 	.globl _P1
                                     58 	.globl _TH0
                                     59 	.globl _TL0
                                     60 	.globl _TMOD
                                     61 	.globl _TCON
                                     62 	.globl _IE_EX
                                     63 	.globl _IE
                                     64 	.globl _CLOCK_CFG
                                     65 	.globl _WAKE_CTRL
                                     66 	.globl _SAFE_MOD
                                     67 	.globl _PCON
                                     68 	.globl _Ep1Buffer
                                     69 	.globl _Ep0Buffer
                                     70 	.globl _Ready
                                     71 	.globl _LedState
                                     72 ;--------------------------------------------------------
                                     73 ; special function registers
                                     74 ;--------------------------------------------------------
                                     75 	.area RSEG    (ABS,DATA)
      000000                         76 	.org 0x0000
                           000087    77 _PCON	=	0x0087
                           0000A1    78 _SAFE_MOD	=	0x00a1
                           0000A9    79 _WAKE_CTRL	=	0x00a9
                           0000B9    80 _CLOCK_CFG	=	0x00b9
                           0000A8    81 _IE	=	0x00a8
                           0000E8    82 _IE_EX	=	0x00e8
                           000088    83 _TCON	=	0x0088
                           000089    84 _TMOD	=	0x0089
                           00008A    85 _TL0	=	0x008a
                           00008C    86 _TH0	=	0x008c
                           000090    87 _P1	=	0x0090
                           000092    88 _P1_MOD_OC	=	0x0092
                           000093    89 _P1_DIR_PU	=	0x0093
                           0000B0    90 _P3	=	0x00b0
                           000096    91 _P3_MOD_OC	=	0x0096
                           000097    92 _P3_DIR_PU	=	0x0097
                           0000D1    93 _UDEV_CTRL	=	0x00d1
                           0000D2    94 _UEP1_CTRL	=	0x00d2
                           0000D3    95 _UEP1_T_LEN	=	0x00d3
                           0000D4    96 _UEP2_CTRL	=	0x00d4
                           0000D5    97 _UEP2_T_LEN	=	0x00d5
                           0000D6    98 _UEP3_CTRL	=	0x00d6
                           0000D7    99 _UEP3_T_LEN	=	0x00d7
                           0000D8   100 _USB_INT_FG	=	0x00d8
                           0000D9   101 _USB_INT_ST	=	0x00d9
                           0000DA   102 _USB_MIS_ST	=	0x00da
                           0000DB   103 _USB_RX_LEN	=	0x00db
                           0000DC   104 _UEP0_CTRL	=	0x00dc
                           0000DD   105 _UEP0_T_LEN	=	0x00dd
                           0000E1   106 _USB_INT_EN	=	0x00e1
                           0000E2   107 _USB_CTRL	=	0x00e2
                           0000E3   108 _USB_DEV_AD	=	0x00e3
                           0000E4   109 _UEP2_DMA_L	=	0x00e4
                           0000E5   110 _UEP2_DMA_H	=	0x00e5
                           0000EA   111 _UEP4_1_MOD	=	0x00ea
                           0000EB   112 _UEP2_3_MOD	=	0x00eb
                           0000EC   113 _UEP0_DMA_L	=	0x00ec
                           0000ED   114 _UEP0_DMA_H	=	0x00ed
                           0000EE   115 _UEP1_DMA_L	=	0x00ee
                           0000EF   116 _UEP1_DMA_H	=	0x00ef
                                    117 ;--------------------------------------------------------
                                    118 ; special function bits
                                    119 ;--------------------------------------------------------
                                    120 	.area RSEG    (ABS,DATA)
      000000                        121 	.org 0x0000
                           0000A9   122 _ET0	=	0x00a9
                           0000AF   123 _EA	=	0x00af
                           0000EA   124 _IE_USB	=	0x00ea
                           00008C   125 _TR0	=	0x008c
                           00008D   126 _TF0	=	0x008d
                           0000D8   127 _UIF_BUS_RST	=	0x00d8
                           0000D9   128 _UIF_TRANSFER	=	0x00d9
                           0000DA   129 _UIF_SUSPEND	=	0x00da
                           0000DC   130 _UIF_FIFO_OV	=	0x00dc
                           0000DD   131 _U_SIE_FREE	=	0x00dd
                           0000DE   132 _U_TOG_OK	=	0x00de
                           0000DF   133 _U_IS_NAK	=	0x00df
                                    134 ;--------------------------------------------------------
                                    135 ; overlayable register banks
                                    136 ;--------------------------------------------------------
                                    137 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        138 	.ds 8
                                    139 	.area REG_BANK_1	(REL,OVR,DATA)
      000008                        140 	.ds 8
                                    141 	.area REG_BANK_2	(REL,OVR,DATA)
      000010                        142 	.ds 8
                                    143 ;--------------------------------------------------------
                                    144 ; overlayable bit register bank
                                    145 ;--------------------------------------------------------
                                    146 	.area BIT_BANK	(REL,OVR,DATA)
      000021                        147 bits:
      000021                        148 	.ds 1
                           008000   149 	b0 = bits[0]
                           008100   150 	b1 = bits[1]
                           008200   151 	b2 = bits[2]
                           008300   152 	b3 = bits[3]
                           008400   153 	b4 = bits[4]
                           008500   154 	b5 = bits[5]
                           008600   155 	b6 = bits[6]
                           008700   156 	b7 = bits[7]
                                    157 ;--------------------------------------------------------
                                    158 ; internal ram data
                                    159 ;--------------------------------------------------------
                                    160 	.area DSEG    (DATA)
      000022                        161 _LedState::
      000022                        162 	.ds 1
      000023                        163 _LedMode:
      000023                        164 	.ds 3
      000026                        165 _PwmTick:
      000026                        166 	.ds 1
      000027                        167 _BreathLevel:
      000027                        168 	.ds 1
      000028                        169 _USB_DeviceInterrupt_SetupReqCode_10000_78:
      000028                        170 	.ds 1
      000029                        171 _USB_DeviceInterrupt_SetupReqType_10000_78:
      000029                        172 	.ds 1
      00002A                        173 _USB_DeviceInterrupt_SetupLen_10000_78:
      00002A                        174 	.ds 2
      00002C                        175 _USB_DeviceInterrupt_pDescr_10000_78:
      00002C                        176 	.ds 3
                                    177 ;--------------------------------------------------------
                                    178 ; overlayable items in internal ram
                                    179 ;--------------------------------------------------------
                                    180 	.area	OSEG    (OVR,DATA)
      00002F                        181 _DriveStatic_PARM_2:
      00002F                        182 	.ds 1
                                    183 	.area	OSEG    (OVR,DATA)
                                    184 ;--------------------------------------------------------
                                    185 ; indirectly addressable internal ram data
                                    186 ;--------------------------------------------------------
                                    187 	.area ISEG    (DATA)
                                    188 ;--------------------------------------------------------
                                    189 ; absolute internal ram data
                                    190 ;--------------------------------------------------------
                                    191 	.area IABS    (ABS,DATA)
                                    192 	.area IABS    (ABS,DATA)
                                    193 ;--------------------------------------------------------
                                    194 ; bit data
                                    195 ;--------------------------------------------------------
                                    196 	.area BSEG    (BIT)
      000000                        197 _Ready::
      000000                        198 	.ds 1
      000001                        199 _BreathRising:
      000001                        200 	.ds 1
                                    201 ;--------------------------------------------------------
                                    202 ; paged external ram data
                                    203 ;--------------------------------------------------------
                                    204 	.area PSEG    (PAG,XDATA)
                                    205 ;--------------------------------------------------------
                                    206 ; uninitialized external ram data
                                    207 ;--------------------------------------------------------
                                    208 	.area XSEG    (XDATA)
                           000000   209 _Ep0Buffer	=	0x0000
                           000040   210 _Ep1Buffer	=	0x0040
                                    211 ;--------------------------------------------------------
                                    212 ; absolute external ram data
                                    213 ;--------------------------------------------------------
                                    214 	.area XABS    (ABS,XDATA)
                                    215 ;--------------------------------------------------------
                                    216 ; initialized external ram data
                                    217 ;--------------------------------------------------------
                                    218 	.area XISEG   (XDATA)
                                    219 	.area HOME    (CODE)
                                    220 	.area GSINIT0 (CODE)
                                    221 	.area GSINIT1 (CODE)
                                    222 	.area GSINIT2 (CODE)
                                    223 	.area GSINIT3 (CODE)
                                    224 	.area GSINIT4 (CODE)
                                    225 	.area GSINIT5 (CODE)
                                    226 	.area GSINIT  (CODE)
                                    227 	.area GSFINAL (CODE)
                                    228 	.area CSEG    (CODE)
                                    229 ;--------------------------------------------------------
                                    230 ; global & static initialisations
                                    231 ;--------------------------------------------------------
                                    232 	.area HOME    (CODE)
                                    233 	.area GSINIT  (CODE)
                                    234 	.area GSFINAL (CODE)
                                    235 	.area GSINIT  (CODE)
                                    236 ;	usb_isr.c:47: volatile UINT8 LedState = 0;             /* 主机最近一次写入的原字节，用于 GET_REPORT */
      000111 75 22 00         [24]  237 	mov	_LedState,#0x00
                                    238 ;	usb_isr.c:48: static   volatile UINT8 LedMode[3] = {0,0,0};
      000114 75 23 00         [24]  239 	mov	_LedMode,#0x00
      000117 75 24 00         [24]  240 	mov	(_LedMode + 0x0001),#0x00
      00011A 75 25 00         [24]  241 	mov	(_LedMode + 0x0002),#0x00
                                    242 ;	usb_isr.c:51: static volatile UINT8 PwmTick      = 0;
      00011D 75 26 00         [24]  243 	mov	_PwmTick,#0x00
                                    244 ;	usb_isr.c:52: static volatile UINT8 BreathLevel  = 0;
      000120 75 27 00         [24]  245 	mov	_BreathLevel,#0x00
                                    246 ;	usb_isr.c:46: volatile __bit Ready    = 0;
                                    247 ;	assignBit
      000123 C2 00            [12]  248 	clr	_Ready
                                    249 ;	usb_isr.c:53: static volatile __bit BreathRising = 1;
                                    250 ;	assignBit
      000125 D2 01            [12]  251 	setb	_BreathRising
                                    252 ;--------------------------------------------------------
                                    253 ; Home
                                    254 ;--------------------------------------------------------
                                    255 	.area HOME    (CODE)
                                    256 	.area HOME    (CODE)
                                    257 ;--------------------------------------------------------
                                    258 ; code
                                    259 ;--------------------------------------------------------
                                    260 	.area CSEG    (CODE)
                                    261 ;------------------------------------------------------------
                                    262 ;Allocation info for local variables in function 'DriveStatic'
                                    263 ;------------------------------------------------------------
                                    264 ;mode          Allocated with name '_DriveStatic_PARM_2'
                                    265 ;i             Allocated to registers r7 
                                    266 ;------------------------------------------------------------
                                    267 ;	usb_isr.c:55: static void DriveStatic(UINT8 i, UINT8 mode)
                                    268 ;	-----------------------------------------
                                    269 ;	 function DriveStatic
                                    270 ;	-----------------------------------------
      000184                        271 _DriveStatic:
                           000007   272 	ar7 = 0x07
                           000006   273 	ar6 = 0x06
                           000005   274 	ar5 = 0x05
                           000004   275 	ar4 = 0x04
                           000003   276 	ar3 = 0x03
                           000002   277 	ar2 = 0x02
                           000001   278 	ar1 = 0x01
                           000000   279 	ar0 = 0x00
      000184 AF 82            [24]  280 	mov	r7, dpl
                                    281 ;	usb_isr.c:58: if (mode == LED_ON) {
      000186 74 01            [12]  282 	mov	a,#0x01
      000188 B5 2F 12         [24]  283 	cjne	a,_DriveStatic_PARM_2,00134$
                                    284 ;	usb_isr.c:59: if (i == 0) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
      00018B EF               [12]  285 	mov	a,r7
      00018C 70 04            [24]  286 	jnz	00114$
      00018E 53 90 EF         [24]  287 	anl	_P1,#0xef
      000191 22               [24]  288 	ret
      000192                        289 00114$:
                                    290 ;	usb_isr.c:60: else if (i == 1) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
      000192 BF 01 04         [24]  291 	cjne	r7,#0x01,00107$
      000195 53 90 DF         [24]  292 	anl	_P1,#0xdf
                                    293 ;	usb_isr.c:61: else LED_DRIVE_ON(LED2_PORT, LED2_BIT);
      000198 22               [24]  294 	ret
      000199                        295 00107$:
      000199 53 90 BF         [24]  296 	anl	_P1,#0xbf
      00019C 22               [24]  297 	ret
      00019D                        298 00134$:
                                    299 ;	usb_isr.c:62: } else if (mode == LED_OFF) {
      00019D E5 2F            [12]  300 	mov	a,_DriveStatic_PARM_2
      00019F 70 11            [24]  301 	jnz	00136$
                                    302 ;	usb_isr.c:63: if (i == 0) LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
      0001A1 EF               [12]  303 	mov	a,r7
      0001A2 70 04            [24]  304 	jnz	00129$
      0001A4 43 90 10         [24]  305 	orl	_P1,#0x10
      0001A7 22               [24]  306 	ret
      0001A8                        307 00129$:
                                    308 ;	usb_isr.c:64: else if (i == 1) LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
      0001A8 BF 01 04         [24]  309 	cjne	r7,#0x01,00122$
      0001AB 43 90 20         [24]  310 	orl	_P1,#0x20
                                    311 ;	usb_isr.c:65: else LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
      0001AE 22               [24]  312 	ret
      0001AF                        313 00122$:
      0001AF 43 90 40         [24]  314 	orl	_P1,#0x40
      0001B2                        315 00136$:
                                    316 ;	usb_isr.c:67: }
      0001B2 22               [24]  317 	ret
                                    318 ;------------------------------------------------------------
                                    319 ;Allocation info for local variables in function 'ApplyLEDs'
                                    320 ;------------------------------------------------------------
                                    321 ;raw           Allocated to registers r7 
                                    322 ;m0            Allocated to registers r6 
                                    323 ;m1            Allocated to registers r5 
                                    324 ;m2            Allocated to registers r7 
                                    325 ;------------------------------------------------------------
                                    326 ;	usb_isr.c:69: static void ApplyLEDs(UINT8 raw)
                                    327 ;	-----------------------------------------
                                    328 ;	 function ApplyLEDs
                                    329 ;	-----------------------------------------
      0001B3                        330 _ApplyLEDs:
      0001B3 AF 82            [24]  331 	mov	r7, dpl
                                    332 ;	usb_isr.c:71: UINT8 m0 = (raw >> 0) & 0x03;
      0001B5 8F 06            [24]  333 	mov	ar6,r7
      0001B7 53 06 03         [24]  334 	anl	ar6,#0x03
                                    335 ;	usb_isr.c:72: UINT8 m1 = (raw >> 2) & 0x03;
      0001BA EF               [12]  336 	mov	a,r7
      0001BB 03               [12]  337 	rr	a
      0001BC 03               [12]  338 	rr	a
      0001BD 54 3F            [12]  339 	anl	a,#0x3f
      0001BF FD               [12]  340 	mov	r5,a
      0001C0 53 05 03         [24]  341 	anl	ar5,#0x03
                                    342 ;	usb_isr.c:73: UINT8 m2 = (raw >> 4) & 0x03;
      0001C3 EF               [12]  343 	mov	a,r7
      0001C4 C4               [12]  344 	swap	a
      0001C5 54 0F            [12]  345 	anl	a,#0x0f
      0001C7 FF               [12]  346 	mov	r7,a
      0001C8 53 07 03         [24]  347 	anl	ar7,#0x03
                                    348 ;	usb_isr.c:75: if (m0 > LED_BREATHE) m0 = LED_OFF;
      0001CB EE               [12]  349 	mov	a,r6
      0001CC 24 FD            [12]  350 	add	a,#0xff - 0x02
      0001CE 50 02            [24]  351 	jnc	00102$
                                    352 ;	free result
      0001D0 7E 00            [12]  353 	mov	r6,#0x00
      0001D2                        354 00102$:
                                    355 ;	usb_isr.c:76: if (m1 > LED_BREATHE) m1 = LED_OFF;
      0001D2 ED               [12]  356 	mov	a,r5
      0001D3 24 FD            [12]  357 	add	a,#0xff - 0x02
      0001D5 50 02            [24]  358 	jnc	00104$
                                    359 ;	free result
      0001D7 7D 00            [12]  360 	mov	r5,#0x00
      0001D9                        361 00104$:
                                    362 ;	usb_isr.c:77: if (m2 > LED_BREATHE) m2 = LED_OFF;
      0001D9 EF               [12]  363 	mov	a,r7
      0001DA 24 FD            [12]  364 	add	a,#0xff - 0x02
      0001DC 50 02            [24]  365 	jnc	00106$
                                    366 ;	free result
      0001DE 7F 00            [12]  367 	mov	r7,#0x00
      0001E0                        368 00106$:
                                    369 ;	usb_isr.c:79: LedState = (m2 << 4) | (m1 << 2) | m0;
      0001E0 EF               [12]  370 	mov	a,r7
      0001E1 C4               [12]  371 	swap	a
      0001E2 54 F0            [12]  372 	anl	a,#0xf0
      0001E4 FC               [12]  373 	mov	r4,a
      0001E5 ED               [12]  374 	mov	a,r5
      0001E6 2D               [12]  375 	add	a,r5
      0001E7 25 E0            [12]  376 	add	a,acc
      0001E9 4C               [12]  377 	orl	a,r4
      0001EA 4E               [12]  378 	orl	a,r6
      0001EB F5 22            [12]  379 	mov	_LedState,a
                                    380 ;	usb_isr.c:81: LedMode[0] = m0; DriveStatic(0, m0);
      0001ED 8E 23            [24]  381 	mov	_LedMode,r6
      0001EF 8E 2F            [24]  382 	mov	_DriveStatic_PARM_2,r6
      0001F1 75 82 00         [24]  383 	mov	dpl, #0x00
      0001F4 C0 07            [24]  384 	push	ar7
      0001F6 C0 05            [24]  385 	push	ar5
      0001F8 12 01 84         [24]  386 	lcall	_DriveStatic
      0001FB D0 05            [24]  387 	pop	ar5
                                    388 ;	usb_isr.c:82: LedMode[1] = m1; DriveStatic(1, m1);
      0001FD 8D 24            [24]  389 	mov	(_LedMode + 0x0001),r5
      0001FF 8D 2F            [24]  390 	mov	_DriveStatic_PARM_2,r5
      000201 75 82 01         [24]  391 	mov	dpl, #0x01
      000204 12 01 84         [24]  392 	lcall	_DriveStatic
      000207 D0 07            [24]  393 	pop	ar7
                                    394 ;	usb_isr.c:83: LedMode[2] = m2; DriveStatic(2, m2);
      000209 8F 25            [24]  395 	mov	(_LedMode + 0x0002),r7
      00020B 8F 2F            [24]  396 	mov	_DriveStatic_PARM_2,r7
      00020D 75 82 02         [24]  397 	mov	dpl, #0x02
                                    398 ;	usb_isr.c:84: }
      000210 02 01 84         [24]  399 	ljmp	_DriveStatic
                                    400 ;------------------------------------------------------------
                                    401 ;Allocation info for local variables in function 'LEDs_Init'
                                    402 ;------------------------------------------------------------
                                    403 ;	usb_isr.c:86: void LEDs_Init(void)
                                    404 ;	-----------------------------------------
                                    405 ;	 function LEDs_Init
                                    406 ;	-----------------------------------------
      000213                        407 _LEDs_Init:
                                    408 ;	usb_isr.c:88: LED0_MOD_OC &= ~(1 << LED0_BIT); LED0_DIR_PU |= (1 << LED0_BIT);
      000213 53 92 EF         [24]  409 	anl	_P1_MOD_OC,#0xef
      000216 43 93 10         [24]  410 	orl	_P1_DIR_PU,#0x10
                                    411 ;	usb_isr.c:89: LED1_MOD_OC &= ~(1 << LED1_BIT); LED1_DIR_PU |= (1 << LED1_BIT);
      000219 53 92 DF         [24]  412 	anl	_P1_MOD_OC,#0xdf
      00021C 43 93 20         [24]  413 	orl	_P1_DIR_PU,#0x20
                                    414 ;	usb_isr.c:90: LED2_MOD_OC &= ~(1 << LED2_BIT); LED2_DIR_PU |= (1 << LED2_BIT);
      00021F 53 92 BF         [24]  415 	anl	_P1_MOD_OC,#0xbf
      000222 43 93 40         [24]  416 	orl	_P1_DIR_PU,#0x40
                                    417 ;	usb_isr.c:91: ApplyLEDs(0);
      000225 75 82 00         [24]  418 	mov	dpl, #0x00
      000228 12 01 B3         [24]  419 	lcall	_ApplyLEDs
                                    420 ;	usb_isr.c:96: TMOD = (TMOD & 0xF0) | 0x02;
      00022B E5 89            [12]  421 	mov	a,_TMOD
      00022D 54 F0            [12]  422 	anl	a,#0xf0
      00022F 44 02            [12]  423 	orl	a,#0x02
      000231 F5 89            [12]  424 	mov	_TMOD,a
                                    425 ;	usb_isr.c:97: TH0  = 0xDB;
      000233 75 8C DB         [24]  426 	mov	_TH0,#0xdb
                                    427 ;	usb_isr.c:98: TL0  = 0xDB;
      000236 75 8A DB         [24]  428 	mov	_TL0,#0xdb
                                    429 ;	usb_isr.c:99: TR0  = 1;
                                    430 ;	assignBit
      000239 D2 8C            [12]  431 	setb	_TR0
                                    432 ;	usb_isr.c:100: ET0  = 1;
                                    433 ;	assignBit
      00023B D2 A9            [12]  434 	setb	_ET0
                                    435 ;	usb_isr.c:101: }
      00023D 22               [24]  436 	ret
                                    437 ;------------------------------------------------------------
                                    438 ;Allocation info for local variables in function 'Timer0Interrupt'
                                    439 ;------------------------------------------------------------
                                    440 ;tick          Allocated to registers r7 
                                    441 ;------------------------------------------------------------
                                    442 ;	usb_isr.c:103: void Timer0Interrupt(void) __interrupt(INT_NO_TMR0) __using(2)
                                    443 ;	-----------------------------------------
                                    444 ;	 function Timer0Interrupt
                                    445 ;	-----------------------------------------
      00023E                        446 _Timer0Interrupt:
                           000017   447 	ar7 = 0x17
                           000016   448 	ar6 = 0x16
                           000015   449 	ar5 = 0x15
                           000014   450 	ar4 = 0x14
                           000013   451 	ar3 = 0x13
                           000012   452 	ar2 = 0x12
                           000011   453 	ar1 = 0x11
                           000010   454 	ar0 = 0x10
      00023E C0 E0            [24]  455 	push	acc
      000240 C0 D0            [24]  456 	push	psw
      000242 75 D0 10         [24]  457 	mov	psw,#0x10
                                    458 ;	usb_isr.c:105: UINT8 tick = ++PwmTick;
      000245 E5 26            [12]  459 	mov	a,_PwmTick
      000247 04               [12]  460 	inc	a
                                    461 ;	usb_isr.c:107: if (tick == 0) {
      000248 FF               [12]  462 	mov	r7,a
      000249 8F 26            [24]  463 	mov	_PwmTick,r7
      00024B 70 1E            [24]  464 	jnz	00111$
                                    465 ;	usb_isr.c:109: if (BreathRising) {
      00024D 30 01 0F         [24]  466 	jnb	_BreathRising,00108$
                                    467 ;	usb_isr.c:110: if (BreathLevel == 0xFF) { BreathRising = 0; --BreathLevel; }
      000250 74 FF            [12]  468 	mov	a,#0xff
      000252 B5 27 06         [24]  469 	cjne	a,_BreathLevel,00102$
                                    470 ;	assignBit
      000255 C2 01            [12]  471 	clr	_BreathRising
      000257 15 27            [12]  472 	dec	_BreathLevel
      000259 80 10            [24]  473 	sjmp	00111$
      00025B                        474 00102$:
                                    475 ;	usb_isr.c:111: else                       ++BreathLevel;
      00025B 05 27            [12]  476 	inc	_BreathLevel
      00025D 80 0C            [24]  477 	sjmp	00111$
      00025F                        478 00108$:
                                    479 ;	usb_isr.c:113: if (BreathLevel == 0x00) { BreathRising = 1; ++BreathLevel; }
      00025F E5 27            [12]  480 	mov	a,_BreathLevel
      000261 70 06            [24]  481 	jnz	00105$
                                    482 ;	assignBit
      000263 D2 01            [12]  483 	setb	_BreathRising
      000265 05 27            [12]  484 	inc	_BreathLevel
      000267 80 02            [24]  485 	sjmp	00111$
      000269                        486 00105$:
                                    487 ;	usb_isr.c:114: else                       --BreathLevel;
      000269 15 27            [12]  488 	dec	_BreathLevel
      00026B                        489 00111$:
                                    490 ;	usb_isr.c:118: if (LedMode[0] == LED_BREATHE) {
      00026B 74 02            [12]  491 	mov	a,#0x02
      00026D B5 23 0E         [24]  492 	cjne	a,_LedMode,00122$
                                    493 ;	usb_isr.c:119: if (tick < BreathLevel) LED_DRIVE_ON(LED0_PORT, LED0_BIT);
      000270 C3               [12]  494 	clr	c
      000271 EF               [12]  495 	mov	a,r7
      000272 95 27            [12]  496 	subb	a,_BreathLevel
      000274 50 05            [24]  497 	jnc	00115$
      000276 53 90 EF         [24]  498 	anl	_P1,#0xef
                                    499 ;	usb_isr.c:120: else                    LED_DRIVE_OFF(LED0_PORT, LED0_BIT);
      000279 80 03            [24]  500 	sjmp	00122$
      00027B                        501 00115$:
      00027B 43 90 10         [24]  502 	orl	_P1,#0x10
      00027E                        503 00122$:
                                    504 ;	usb_isr.c:122: if (LedMode[1] == LED_BREATHE) {
      00027E 74 02            [12]  505 	mov	a,#0x02
      000280 B5 24 0E         [24]  506 	cjne	a,(_LedMode + 0x0001),00133$
                                    507 ;	usb_isr.c:123: if (tick < BreathLevel) LED_DRIVE_ON(LED1_PORT, LED1_BIT);
      000283 C3               [12]  508 	clr	c
      000284 EF               [12]  509 	mov	a,r7
      000285 95 27            [12]  510 	subb	a,_BreathLevel
      000287 50 05            [24]  511 	jnc	00126$
      000289 53 90 DF         [24]  512 	anl	_P1,#0xdf
                                    513 ;	usb_isr.c:124: else                    LED_DRIVE_OFF(LED1_PORT, LED1_BIT);
      00028C 80 03            [24]  514 	sjmp	00133$
      00028E                        515 00126$:
      00028E 43 90 20         [24]  516 	orl	_P1,#0x20
      000291                        517 00133$:
                                    518 ;	usb_isr.c:126: if (LedMode[2] == LED_BREATHE) {
      000291 74 02            [12]  519 	mov	a,#0x02
      000293 B5 25 0E         [24]  520 	cjne	a,(_LedMode + 0x0002),00145$
                                    521 ;	usb_isr.c:127: if (tick < BreathLevel) LED_DRIVE_ON(LED2_PORT, LED2_BIT);
      000296 C3               [12]  522 	clr	c
      000297 EF               [12]  523 	mov	a,r7
      000298 95 27            [12]  524 	subb	a,_BreathLevel
      00029A 50 05            [24]  525 	jnc	00137$
      00029C 53 90 BF         [24]  526 	anl	_P1,#0xbf
                                    527 ;	usb_isr.c:128: else                    LED_DRIVE_OFF(LED2_PORT, LED2_BIT);
      00029F 80 03            [24]  528 	sjmp	00145$
      0002A1                        529 00137$:
      0002A1 43 90 40         [24]  530 	orl	_P1,#0x40
      0002A4                        531 00145$:
                                    532 ;	usb_isr.c:130: }
      0002A4 D0 D0            [24]  533 	pop	psw
      0002A6 D0 E0            [24]  534 	pop	acc
      0002A8 32               [24]  535 	reti
                                    536 ;	eliminated unneeded push/pop dpl
                                    537 ;	eliminated unneeded push/pop dph
                                    538 ;	eliminated unneeded push/pop b
                                    539 ;------------------------------------------------------------
                                    540 ;Allocation info for local variables in function 'USB_DeviceInterrupt'
                                    541 ;------------------------------------------------------------
                                    542 ;SetupReqCode  Allocated with name '_USB_DeviceInterrupt_SetupReqCode_10000_78'
                                    543 ;SetupReqType  Allocated with name '_USB_DeviceInterrupt_SetupReqType_10000_78'
                                    544 ;SetupLen      Allocated with name '_USB_DeviceInterrupt_SetupLen_10000_78'
                                    545 ;pDescr        Allocated with name '_USB_DeviceInterrupt_pDescr_10000_78'
                                    546 ;errflag       Allocated to registers r5 
                                    547 ;len           Allocated to registers r6 r7 
                                    548 ;------------------------------------------------------------
                                    549 ;	usb_isr.c:132: void USB_DeviceInterrupt(void) __interrupt(INT_NO_USB) __using(1)
                                    550 ;	-----------------------------------------
                                    551 ;	 function USB_DeviceInterrupt
                                    552 ;	-----------------------------------------
      0002A9                        553 _USB_DeviceInterrupt:
                           00000F   554 	ar7 = 0x0f
                           00000E   555 	ar6 = 0x0e
                           00000D   556 	ar5 = 0x0d
                           00000C   557 	ar4 = 0x0c
                           00000B   558 	ar3 = 0x0b
                           00000A   559 	ar2 = 0x0a
                           000009   560 	ar1 = 0x09
                           000008   561 	ar0 = 0x08
      0002A9 C0 21            [24]  562 	push	bits
      0002AB C0 E0            [24]  563 	push	acc
      0002AD C0 F0            [24]  564 	push	b
      0002AF C0 82            [24]  565 	push	dpl
      0002B1 C0 83            [24]  566 	push	dph
      0002B3 C0 07            [24]  567 	push	(0+7)
      0002B5 C0 06            [24]  568 	push	(0+6)
      0002B7 C0 05            [24]  569 	push	(0+5)
      0002B9 C0 04            [24]  570 	push	(0+4)
      0002BB C0 03            [24]  571 	push	(0+3)
      0002BD C0 02            [24]  572 	push	(0+2)
      0002BF C0 01            [24]  573 	push	(0+1)
      0002C1 C0 00            [24]  574 	push	(0+0)
      0002C3 C0 D0            [24]  575 	push	psw
      0002C5 75 D0 08         [24]  576 	mov	psw,#0x08
                                    577 ;	usb_isr.c:141: if (UIF_TRANSFER) {
      0002C8 20 D9 03         [24]  578 	jb	_UIF_TRANSFER,00526$
      0002CB 02 06 7A         [24]  579 	ljmp	00174$
      0002CE                        580 00526$:
                                    581 ;	usb_isr.c:142: switch (USB_INT_ST & (MASK_UIS_TOKEN | MASK_UIS_ENDP)) {
      0002CE 74 3F            [12]  582 	mov	a,#0x3f
      0002D0 55 D9            [12]  583 	anl	a,_USB_INT_ST
      0002D2 FF               [12]  584 	mov	r7,a
      0002D3 FE               [12]  585 	mov	r6,a
      0002D4 70 03            [24]  586 	jnz	00527$
      0002D6 02 06 4B         [24]  587 	ljmp	00158$
      0002D9                        588 00527$:
      0002D9 BF 20 03         [24]  589 	cjne	r7,#0x20,00528$
      0002DC 02 05 D0         [24]  590 	ljmp	00153$
      0002DF                        591 00528$:
      0002DF BF 21 02         [24]  592 	cjne	r7,#0x21,00529$
      0002E2 80 08            [24]  593 	sjmp	00101$
      0002E4                        594 00529$:
      0002E4 BF 30 02         [24]  595 	cjne	r7,#0x30,00530$
      0002E7 80 11            [24]  596 	sjmp	00102$
      0002E9                        597 00530$:
      0002E9 02 06 76         [24]  598 	ljmp	00166$
                                    599 ;	usb_isr.c:145: case UIS_TOKEN_IN | 1:
      0002EC                        600 00101$:
                                    601 ;	usb_isr.c:146: UEP1_CTRL ^= bUEP_T_TOG;
      0002EC 63 D2 40         [24]  602 	xrl	_UEP1_CTRL,#0x40
                                    603 ;	usb_isr.c:147: UEP1_CTRL  = (UEP1_CTRL & ~MASK_UEP_T_RES) | UEP_T_RES_NAK;
      0002EF 74 FC            [12]  604 	mov	a,#0xfc
      0002F1 55 D2            [12]  605 	anl	a,_UEP1_CTRL
      0002F3 44 02            [12]  606 	orl	a,#0x02
      0002F5 F5 D2            [12]  607 	mov	_UEP1_CTRL,a
                                    608 ;	usb_isr.c:148: break;
      0002F7 02 06 76         [24]  609 	ljmp	00166$
                                    610 ;	usb_isr.c:151: case UIS_TOKEN_SETUP | 0:
      0002FA                        611 00102$:
                                    612 ;	usb_isr.c:152: UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
      0002FA 75 DC C0         [24]  613 	mov	_UEP0_CTRL,#0xc0
                                    614 ;	usb_isr.c:153: len = USB_RX_LEN;
      0002FD AE DB            [24]  615 	mov	r6,_USB_RX_LEN
      0002FF 7F 00            [12]  616 	mov	r7,#0x00
                                    617 ;	usb_isr.c:154: if (len == sizeof(USB_SETUP_REQ)) {
      000301 BE 08 05         [24]  618 	cjne	r6,#0x08,00531$
      000304 BF 00 02         [24]  619 	cjne	r7,#0x00,00531$
      000307 80 03            [24]  620 	sjmp	00532$
      000309                        621 00531$:
      000309 02 05 B3         [24]  622 	ljmp	00148$
      00030C                        623 00532$:
                                    624 ;	usb_isr.c:155: SetupLen     = ((UINT16)UsbSetupBuf->wLengthH << 8) | UsbSetupBuf->wLengthL;
      00030C 90 00 07         [24]  625 	mov	dptr,#(_Ep0Buffer + 0x0007)
      00030F E0               [24]  626 	movx	a,@dptr
      000310 FC               [12]  627 	mov	r4,a
      000311 7D 00            [12]  628 	mov	r5,#0x00
      000313 90 00 06         [24]  629 	mov	dptr,#(_Ep0Buffer + 0x0006)
      000316 E0               [24]  630 	movx	a,@dptr
      000317 7A 00            [12]  631 	mov	r2,#0x00
      000319 4D               [12]  632 	orl	a,r5
      00031A F5 2A            [12]  633 	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
      00031C EA               [12]  634 	mov	a,r2
      00031D 4C               [12]  635 	orl	a,r4
      00031E F5 2B            [12]  636 	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
                                    637 ;	usb_isr.c:156: len          = 0;
      000320 7E 00            [12]  638 	mov	r6,#0x00
      000322 7F 00            [12]  639 	mov	r7,#0x00
                                    640 ;	usb_isr.c:157: errflag      = 0;
                                    641 ;	usb_isr.c:158: SetupReqCode = UsbSetupBuf->bRequest;
      000324 90 00 01         [24]  642 	mov	dptr,#(_Ep0Buffer + 0x0001)
      000327 E0               [24]  643 	movx	a,@dptr
      000328 F5 28            [12]  644 	mov	_USB_DeviceInterrupt_SetupReqCode_10000_78,a
                                    645 ;	usb_isr.c:159: SetupReqType = UsbSetupBuf->bRequestType;
      00032A 90 00 00         [24]  646 	mov	dptr,#_Ep0Buffer
      00032D E0               [24]  647 	movx	a,@dptr
      00032E F5 29            [12]  648 	mov	_USB_DeviceInterrupt_SetupReqType_10000_78,a
                                    649 ;	usb_isr.c:161: switch (SetupReqType & USB_REQ_TYP_MASK) {
      000330 AC 29            [24]  650 	mov	r4,_USB_DeviceInterrupt_SetupReqType_10000_78
      000332 74 60            [12]  651 	mov	a,#0x60
      000334 5C               [12]  652 	anl	a,r4
      000335 FB               [12]  653 	mov	r3,a
      000336 60 09            [24]  654 	jz	00103$
      000338 BB 20 03         [24]  655 	cjne	r3,#0x20,00534$
      00033B 02 05 37         [24]  656 	ljmp	00137$
      00033E                        657 00534$:
      00033E 02 05 AF         [24]  658 	ljmp	00145$
                                    659 ;	usb_isr.c:163: case USB_REQ_TYP_STANDARD:
      000341                        660 00103$:
                                    661 ;	usb_isr.c:164: switch (SetupReqCode) {
      000341 E5 28            [12]  662 	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
      000343 24 F5            [12]  663 	add	a,#0xff - 0x0a
      000345 50 03            [24]  664 	jnc	00535$
      000347 02 05 32         [24]  665 	ljmp	00135$
      00034A                        666 00535$:
                                    667 ;	free result
      00034A E5 28            [12]  668 	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
      00034C 24 0B            [12]  669 	add	a,#(00536$-3-.)
      00034E 83               [24]  670 	movc	a,@a+pc
      00034F F5 82            [12]  671 	mov	dpl,a
      000351 E5 28            [12]  672 	mov	a,_USB_DeviceInterrupt_SetupReqCode_10000_78
      000353 24 0F            [12]  673 	add	a,#(00537$-3-.)
      000355 83               [24]  674 	movc	a,@a+pc
      000356 F5 83            [12]  675 	mov	dph,a
      000358 E4               [12]  676 	clr	a
      000359 73               [24]  677 	jmp	@a+dptr
      00035A                        678 00536$:
      00035A 0B                     679 	.db	00134$
      00035B CC                     680 	.db	00124$
      00035C 32                     681 	.db	00135$
      00035D 32                     682 	.db	00135$
      00035E 32                     683 	.db	00135$
      00035F 94                     684 	.db	00119$
      000360 70                     685 	.db	00104$
      000361 32                     686 	.db	00135$
      000362 A1                     687 	.db	00120$
      000363 C0                     688 	.db	00123$
      000364 EF                     689 	.db	00131$
      000365                        690 00537$:
      000365 05                     691 	.db	00134$>>8
      000366 04                     692 	.db	00124$>>8
      000367 05                     693 	.db	00135$>>8
      000368 05                     694 	.db	00135$>>8
      000369 05                     695 	.db	00135$>>8
      00036A 04                     696 	.db	00119$>>8
      00036B 03                     697 	.db	00104$>>8
      00036C 05                     698 	.db	00135$>>8
      00036D 04                     699 	.db	00120$>>8
      00036E 04                     700 	.db	00123$>>8
      00036F 04                     701 	.db	00131$>>8
                                    702 ;	usb_isr.c:165: case USB_GET_DESCRIPTOR:
      000370                        703 00104$:
                                    704 ;	usb_isr.c:166: switch (UsbSetupBuf->wValueH) {
      000370 90 00 03         [24]  705 	mov	dptr,#(_Ep0Buffer + 0x0003)
      000373 E0               [24]  706 	movx	a,@dptr
      000374 FB               [12]  707 	mov	r3,a
      000375 BB 01 02         [24]  708 	cjne	r3,#0x01,00538$
      000378 80 19            [24]  709 	sjmp	00105$
      00037A                        710 00538$:
      00037A BB 02 02         [24]  711 	cjne	r3,#0x02,00539$
      00037D 80 28            [24]  712 	sjmp	00106$
      00037F                        713 00539$:
      00037F BB 03 02         [24]  714 	cjne	r3,#0x03,00540$
      000382 80 36            [24]  715 	sjmp	00107$
      000384                        716 00540$:
      000384 BB 21 03         [24]  717 	cjne	r3,#0x21,00541$
      000387 02 04 08         [24]  718 	ljmp	00113$
      00038A                        719 00541$:
      00038A BB 22 03         [24]  720 	cjne	r3,#0x22,00542$
      00038D 02 04 17         [24]  721 	ljmp	00114$
      000390                        722 00542$:
      000390 02 04 2A         [24]  723 	ljmp	00115$
                                    724 ;	usb_isr.c:167: case 1:  /* device */
      000393                        725 00105$:
                                    726 ;	usb_isr.c:168: pDescr = (PUINT8)MyDevDescr; len = MyDevDescrLen; break;
      000393 75 2C 90         [24]  727 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyDevDescr
      000396 75 2D 07         [24]  728 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyDevDescr >> 8)
      000399 75 2E 80         [24]  729 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
      00039C 90 07 E6         [24]  730 	mov	dptr,#_MyDevDescrLen
      00039F E4               [12]  731 	clr	a
      0003A0 93               [24]  732 	movc	a,@a+dptr
      0003A1 FE               [12]  733 	mov	r6,a
      0003A2 7F 00            [12]  734 	mov	r7,#0x00
      0003A4 02 04 2C         [24]  735 	ljmp	00116$
                                    736 ;	usb_isr.c:169: case 2:  /* configuration */
      0003A7                        737 00106$:
                                    738 ;	usb_isr.c:170: pDescr = (PUINT8)MyCfgDescr; len = MyCfgDescrLen; break;
      0003A7 75 2C A2         [24]  739 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyCfgDescr
      0003AA 75 2D 07         [24]  740 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyCfgDescr >> 8)
      0003AD 75 2E 80         [24]  741 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
      0003B0 90 07 E7         [24]  742 	mov	dptr,#_MyCfgDescrLen
      0003B3 E4               [12]  743 	clr	a
      0003B4 93               [24]  744 	movc	a,@a+dptr
      0003B5 FE               [12]  745 	mov	r6,a
      0003B6 7F 00            [12]  746 	mov	r7,#0x00
                                    747 ;	usb_isr.c:171: case 3:  /* string */
      0003B8 80 72            [24]  748 	sjmp	00116$
      0003BA                        749 00107$:
                                    750 ;	usb_isr.c:172: switch (UsbSetupBuf->wValueL) {
      0003BA 90 00 02         [24]  751 	mov	dptr,#(_Ep0Buffer + 0x0002)
      0003BD E0               [24]  752 	movx	a,@dptr
      0003BE FB               [12]  753 	mov	r3,a
      0003BF 60 0A            [24]  754 	jz	00108$
      0003C1 BB 01 02         [24]  755 	cjne	r3,#0x01,00544$
      0003C4 80 18            [24]  756 	sjmp	00109$
      0003C6                        757 00544$:
                                    758 ;	usb_isr.c:173: case 0: pDescr = (PUINT8)MyLangDescr; len = MyLangDescrLen; break;
      0003C6 BB 02 3B         [24]  759 	cjne	r3,#0x02,00111$
      0003C9 80 26            [24]  760 	sjmp	00110$
      0003CB                        761 00108$:
      0003CB 75 2C C4         [24]  762 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyLangDescr
      0003CE 75 2D 07         [24]  763 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyLangDescr >> 8)
      0003D1 75 2E 80         [24]  764 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
      0003D4 90 07 E8         [24]  765 	mov	dptr,#_MyLangDescrLen
      0003D7 E4               [12]  766 	clr	a
      0003D8 93               [24]  767 	movc	a,@a+dptr
      0003D9 FE               [12]  768 	mov	r6,a
      0003DA 7F 00            [12]  769 	mov	r7,#0x00
                                    770 ;	usb_isr.c:174: case 1: pDescr = (PUINT8)MyManuInfo;  len = MyManuInfoLen;  break;
      0003DC 80 4E            [24]  771 	sjmp	00116$
      0003DE                        772 00109$:
      0003DE 75 2C C8         [24]  773 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyManuInfo
      0003E1 75 2D 07         [24]  774 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyManuInfo >> 8)
      0003E4 75 2E 80         [24]  775 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
      0003E7 90 07 E9         [24]  776 	mov	dptr,#_MyManuInfoLen
      0003EA E4               [12]  777 	clr	a
      0003EB 93               [24]  778 	movc	a,@a+dptr
      0003EC FE               [12]  779 	mov	r6,a
      0003ED 7F 00            [12]  780 	mov	r7,#0x00
                                    781 ;	usb_isr.c:175: case 2: pDescr = (PUINT8)MyProdInfo;  len = MyProdInfoLen;  break;
      0003EF 80 3B            [24]  782 	sjmp	00116$
      0003F1                        783 00110$:
      0003F1 75 2C D6         [24]  784 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyProdInfo
      0003F4 75 2D 07         [24]  785 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyProdInfo >> 8)
      0003F7 75 2E 80         [24]  786 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
      0003FA 90 07 EA         [24]  787 	mov	dptr,#_MyProdInfoLen
      0003FD E4               [12]  788 	clr	a
      0003FE 93               [24]  789 	movc	a,@a+dptr
      0003FF FE               [12]  790 	mov	r6,a
      000400 7F 00            [12]  791 	mov	r7,#0x00
                                    792 ;	usb_isr.c:176: default: errflag = 0xFF; break;
      000402 80 28            [24]  793 	sjmp	00116$
      000404                        794 00111$:
      000404 7D FF            [12]  795 	mov	r5,#0xff
                                    796 ;	usb_isr.c:178: break;
                                    797 ;	usb_isr.c:179: case USB_DESCR_TYP_HID:       /* 0x21 */
      000406 80 24            [24]  798 	sjmp	00116$
      000408                        799 00113$:
                                    800 ;	usb_isr.c:180: pDescr = (PUINT8)&MyCfgDescr[HID_DESCR_OFFSET_IN_CFG];
      000408 75 2C B4         [24]  801 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#(_MyCfgDescr + 0x0012)
      00040B 75 2D 07         [24]  802 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#((_MyCfgDescr + 0x0012) >> 8)
      00040E 75 2E 80         [24]  803 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
                                    804 ;	usb_isr.c:181: len    = HID_DESCR_LEN;
      000411 7E 09            [12]  805 	mov	r6,#0x09
      000413 7F 00            [12]  806 	mov	r7,#0x00
                                    807 ;	usb_isr.c:182: break;
                                    808 ;	usb_isr.c:183: case USB_DESCR_TYP_REPORT:    /* 0x22 */
      000415 80 15            [24]  809 	sjmp	00116$
      000417                        810 00114$:
                                    811 ;	usb_isr.c:184: pDescr = (PUINT8)MyReportDescr;
      000417 75 2C 7B         [24]  812 	mov	_USB_DeviceInterrupt_pDescr_10000_78,#_MyReportDescr
      00041A 75 2D 07         [24]  813 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),#(_MyReportDescr >> 8)
      00041D 75 2E 80         [24]  814 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 2),#0x80
                                    815 ;	usb_isr.c:185: len    = MyReportDescrLen;
      000420 90 07 EB         [24]  816 	mov	dptr,#_MyReportDescrLen
      000423 E4               [12]  817 	clr	a
      000424 93               [24]  818 	movc	a,@a+dptr
      000425 FE               [12]  819 	mov	r6,a
      000426 7F 00            [12]  820 	mov	r7,#0x00
                                    821 ;	usb_isr.c:186: break;
                                    822 ;	usb_isr.c:187: default: errflag = 0xFF; break;
      000428 80 02            [24]  823 	sjmp	00116$
      00042A                        824 00115$:
      00042A 7D FF            [12]  825 	mov	r5,#0xff
                                    826 ;	usb_isr.c:188: }
      00042C                        827 00116$:
                                    828 ;	usb_isr.c:189: if (SetupLen > len) SetupLen = len;
      00042C C3               [12]  829 	clr	c
      00042D EE               [12]  830 	mov	a,r6
      00042E 95 2A            [12]  831 	subb	a,_USB_DeviceInterrupt_SetupLen_10000_78
      000430 EF               [12]  832 	mov	a,r7
      000431 95 2B            [12]  833 	subb	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000433 50 04            [24]  834 	jnc	00118$
                                    835 ;	free result
      000435 8E 2A            [24]  836 	mov	_USB_DeviceInterrupt_SetupLen_10000_78,r6
      000437 8F 2B            [24]  837 	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),r7
      000439                        838 00118$:
                                    839 ;	usb_isr.c:190: len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
      000439 AA 2A            [24]  840 	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
      00043B AB 2B            [24]  841 	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      00043D C3               [12]  842 	clr	c
      00043E EA               [12]  843 	mov	a,r2
      00043F 94 08            [12]  844 	subb	a,#0x08
      000441 EB               [12]  845 	mov	a,r3
      000442 94 00            [12]  846 	subb	a,#0x00
      000444 40 06            [24]  847 	jc	00178$
      000446 7A 08            [12]  848 	mov	r2,#0x08
      000448 7B 00            [12]  849 	mov	r3,#0x00
      00044A 80 04            [24]  850 	sjmp	00179$
      00044C                        851 00178$:
      00044C AA 2A            [24]  852 	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
      00044E AB 2B            [24]  853 	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000450                        854 00179$:
      000450 8A 0E            [24]  855 	mov	ar6,r2
      000452 8B 0F            [24]  856 	mov	ar7,r3
                                    857 ;	usb_isr.c:191: memcpy(Ep0Buffer, pDescr, len);
      000454 85 2C 2F         [24]  858 	mov	___memcpy_PARM_2,_USB_DeviceInterrupt_pDescr_10000_78
      000457 85 2D 30         [24]  859 	mov	(___memcpy_PARM_2 + 1),(_USB_DeviceInterrupt_pDescr_10000_78 + 1)
      00045A 85 2E 31         [24]  860 	mov	(___memcpy_PARM_2 + 2),(_USB_DeviceInterrupt_pDescr_10000_78 + 2)
      00045D 8E 32            [24]  861 	mov	___memcpy_PARM_3,r6
      00045F 8F 33            [24]  862 	mov	(___memcpy_PARM_3 + 1),r7
      000461 90 00 00         [24]  863 	mov	dptr,#_Ep0Buffer
      000464 75 F0 00         [24]  864 	mov	b, #0x00
      000467 C0 0F            [24]  865 	push	ar7
      000469 C0 0E            [24]  866 	push	ar6
      00046B C0 0D            [24]  867 	push	ar5
      00046D 75 D0 00         [24]  868 	mov	psw,#0x00
      000470 12 06 EB         [24]  869 	lcall	___memcpy
      000473 75 D0 08         [24]  870 	mov	psw,#0x08
      000476 D0 0D            [24]  871 	pop	ar5
      000478 D0 0E            [24]  872 	pop	ar6
      00047A D0 0F            [24]  873 	pop	ar7
                                    874 ;	usb_isr.c:192: SetupLen -= len;
      00047C E5 2A            [12]  875 	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
      00047E C3               [12]  876 	clr	c
      00047F 9E               [12]  877 	subb	a,r6
      000480 F5 2A            [12]  878 	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
      000482 E5 2B            [12]  879 	mov	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000484 9F               [12]  880 	subb	a,r7
      000485 F5 2B            [12]  881 	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
                                    882 ;	usb_isr.c:193: pDescr   += len;
      000487 EE               [12]  883 	mov	a,r6
      000488 25 2C            [12]  884 	add	a, _USB_DeviceInterrupt_pDescr_10000_78
      00048A F5 2C            [12]  885 	mov	_USB_DeviceInterrupt_pDescr_10000_78,a
      00048C EF               [12]  886 	mov	a,r7
      00048D 35 2D            [12]  887 	addc	a, (_USB_DeviceInterrupt_pDescr_10000_78 + 1)
      00048F F5 2D            [12]  888 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),a
                                    889 ;	usb_isr.c:194: break;
      000491 02 05 B5         [24]  890 	ljmp	00149$
                                    891 ;	usb_isr.c:196: case USB_SET_ADDRESS:
      000494                        892 00119$:
                                    893 ;	usb_isr.c:197: SetupLen = UsbSetupBuf->wValueL;
      000494 90 00 02         [24]  894 	mov	dptr,#(_Ep0Buffer + 0x0002)
      000497 E0               [24]  895 	movx	a,@dptr
      000498 FB               [12]  896 	mov	r3,a
      000499 8B 2A            [24]  897 	mov	_USB_DeviceInterrupt_SetupLen_10000_78,r3
      00049B 75 2B 00         [24]  898 	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),#0x00
                                    899 ;	usb_isr.c:198: break;
      00049E 02 05 B5         [24]  900 	ljmp	00149$
                                    901 ;	usb_isr.c:199: case USB_GET_CONFIGURATION:
      0004A1                        902 00120$:
                                    903 ;	usb_isr.c:200: Ep0Buffer[0] = Ready;
      0004A1 A2 00            [12]  904 	mov	c,_Ready
      0004A3 E4               [12]  905 	clr	a
      0004A4 33               [12]  906 	rlc	a
      0004A5 90 00 00         [24]  907 	mov	dptr,#_Ep0Buffer
      0004A8 F0               [24]  908 	movx	@dptr,a
                                    909 ;	usb_isr.c:201: if (SetupLen >= 1) len = 1;
      0004A9 AA 2A            [24]  910 	mov	r2,_USB_DeviceInterrupt_SetupLen_10000_78
      0004AB AB 2B            [24]  911 	mov	r3,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      0004AD C3               [12]  912 	clr	c
      0004AE EA               [12]  913 	mov	a,r2
      0004AF 94 01            [12]  914 	subb	a,#0x01
      0004B1 EB               [12]  915 	mov	a,r3
      0004B2 94 00            [12]  916 	subb	a,#0x00
      0004B4 50 03            [24]  917 	jnc	00548$
      0004B6 02 05 B5         [24]  918 	ljmp	00149$
      0004B9                        919 00548$:
      0004B9 7E 01            [12]  920 	mov	r6,#0x01
      0004BB 7F 00            [12]  921 	mov	r7,#0x00
                                    922 ;	usb_isr.c:202: break;
      0004BD 02 05 B5         [24]  923 	ljmp	00149$
                                    924 ;	usb_isr.c:203: case USB_SET_CONFIGURATION:
      0004C0                        925 00123$:
                                    926 ;	usb_isr.c:204: Ready = UsbSetupBuf->wValueL ? 1 : 0;
      0004C0 90 00 02         [24]  927 	mov	dptr,#(_Ep0Buffer + 0x0002)
      0004C3 E0               [24]  928 	movx	a,@dptr
                                    929 ;	assignBit
      0004C4 FB               [12]  930 	mov	r3,a
      0004C5 24 FF            [12]  931 	add	a,#0xff
      0004C7 92 00            [24]  932 	mov	_Ready,c
                                    933 ;	usb_isr.c:205: break;
      0004C9 02 05 B5         [24]  934 	ljmp	00149$
                                    935 ;	usb_isr.c:206: case USB_CLEAR_FEATURE:
      0004CC                        936 00124$:
                                    937 ;	usb_isr.c:207: if ((SetupReqType & USB_REQ_RECIP_MASK) == USB_REQ_RECIP_ENDP) {
      0004CC 53 0C 1F         [24]  938 	anl	ar4,#0x1f
      0004CF BC 02 18         [24]  939 	cjne	r4,#0x02,00129$
                                    940 ;	usb_isr.c:208: switch (UsbSetupBuf->wIndexL) {
      0004D2 90 00 04         [24]  941 	mov	dptr,#(_Ep0Buffer + 0x0004)
      0004D5 E0               [24]  942 	movx	a,@dptr
      0004D6 FC               [12]  943 	mov	r4,a
      0004D7 BC 81 0B         [24]  944 	cjne	r4,#0x81,00126$
                                    945 ;	usb_isr.c:210: UEP1_CTRL = (UEP1_CTRL & ~(bUEP_T_TOG | MASK_UEP_T_RES)) | UEP_T_RES_NAK;
      0004DA 74 BC            [12]  946 	mov	a,#0xbc
      0004DC 55 D2            [12]  947 	anl	a,_UEP1_CTRL
      0004DE 44 02            [12]  948 	orl	a,#0x02
      0004E0 F5 D2            [12]  949 	mov	_UEP1_CTRL,a
                                    950 ;	usb_isr.c:211: break;
      0004E2 02 05 B5         [24]  951 	ljmp	00149$
                                    952 ;	usb_isr.c:212: default:
      0004E5                        953 00126$:
                                    954 ;	usb_isr.c:213: errflag = 0xFF; break;
      0004E5 7D FF            [12]  955 	mov	r5,#0xff
                                    956 ;	usb_isr.c:214: }
      0004E7 02 05 B5         [24]  957 	ljmp	00149$
      0004EA                        958 00129$:
                                    959 ;	usb_isr.c:216: errflag = 0xFF;
      0004EA 7D FF            [12]  960 	mov	r5,#0xff
                                    961 ;	usb_isr.c:218: break;
      0004EC 02 05 B5         [24]  962 	ljmp	00149$
                                    963 ;	usb_isr.c:219: case USB_GET_INTERFACE:
      0004EF                        964 00131$:
                                    965 ;	usb_isr.c:220: Ep0Buffer[0] = 0x00;
      0004EF 90 00 00         [24]  966 	mov	dptr,#_Ep0Buffer
      0004F2 E4               [12]  967 	clr	a
      0004F3 F0               [24]  968 	movx	@dptr,a
                                    969 ;	usb_isr.c:221: if (SetupLen >= 1) len = 1;
      0004F4 AB 2A            [24]  970 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      0004F6 AC 2B            [24]  971 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      0004F8 C3               [12]  972 	clr	c
      0004F9 EB               [12]  973 	mov	a,r3
      0004FA 94 01            [12]  974 	subb	a,#0x01
      0004FC EC               [12]  975 	mov	a,r4
      0004FD 94 00            [12]  976 	subb	a,#0x00
      0004FF 50 03            [24]  977 	jnc	00553$
      000501 02 05 B5         [24]  978 	ljmp	00149$
      000504                        979 00553$:
      000504 7E 01            [12]  980 	mov	r6,#0x01
      000506 7F 00            [12]  981 	mov	r7,#0x00
                                    982 ;	usb_isr.c:222: break;
      000508 02 05 B5         [24]  983 	ljmp	00149$
                                    984 ;	usb_isr.c:223: case USB_GET_STATUS:
      00050B                        985 00134$:
                                    986 ;	usb_isr.c:224: Ep0Buffer[0] = 0x00;
      00050B 90 00 00         [24]  987 	mov	dptr,#_Ep0Buffer
      00050E E4               [12]  988 	clr	a
      00050F F0               [24]  989 	movx	@dptr,a
                                    990 ;	usb_isr.c:225: Ep0Buffer[1] = 0x00;
      000510 90 00 01         [24]  991 	mov	dptr,#(_Ep0Buffer + 0x0001)
      000513 F0               [24]  992 	movx	@dptr,a
                                    993 ;	usb_isr.c:226: len = SetupLen >= 2 ? 2 : SetupLen;
      000514 AB 2A            [24]  994 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      000516 AC 2B            [24]  995 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000518 C3               [12]  996 	clr	c
      000519 EB               [12]  997 	mov	a,r3
      00051A 94 02            [12]  998 	subb	a,#0x02
      00051C EC               [12]  999 	mov	a,r4
      00051D 94 00            [12] 1000 	subb	a,#0x00
      00051F 40 06            [24] 1001 	jc	00180$
      000521 7B 02            [12] 1002 	mov	r3,#0x02
      000523 7C 00            [12] 1003 	mov	r4,#0x00
      000525 80 04            [24] 1004 	sjmp	00181$
      000527                       1005 00180$:
      000527 AB 2A            [24] 1006 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      000529 AC 2B            [24] 1007 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      00052B                       1008 00181$:
      00052B 8B 0E            [24] 1009 	mov	ar6,r3
      00052D 8C 0F            [24] 1010 	mov	ar7,r4
                                   1011 ;	usb_isr.c:227: break;
      00052F 02 05 B5         [24] 1012 	ljmp	00149$
                                   1013 ;	usb_isr.c:228: default:
      000532                       1014 00135$:
                                   1015 ;	usb_isr.c:229: errflag = 0xFF; break;
      000532 7D FF            [12] 1016 	mov	r5,#0xff
                                   1017 ;	usb_isr.c:231: break;
      000534 02 05 B5         [24] 1018 	ljmp	00149$
                                   1019 ;	usb_isr.c:233: case USB_REQ_TYP_CLASS:
      000537                       1020 00137$:
                                   1021 ;	usb_isr.c:235: switch (SetupReqCode) {
      000537 74 01            [12] 1022 	mov	a,#0x01
      000539 B5 28 02         [24] 1023 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00555$
      00053C 80 28            [24] 1024 	sjmp	00141$
      00053E                       1025 00555$:
      00053E 74 02            [12] 1026 	mov	a,#0x02
      000540 B5 28 02         [24] 1027 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00556$
      000543 80 44            [24] 1028 	sjmp	00142$
      000545                       1029 00556$:
      000545 74 09            [12] 1030 	mov	a,#0x09
      000547 B5 28 02         [24] 1031 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00557$
      00054A 80 0E            [24] 1032 	sjmp	00138$
      00054C                       1033 00557$:
      00054C 74 0A            [12] 1034 	mov	a,#0x0a
      00054E B5 28 02         [24] 1035 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00558$
      000551 80 0D            [24] 1036 	sjmp	00140$
      000553                       1037 00558$:
      000553 74 0B            [12] 1038 	mov	a,#0x0b
                                   1039 ;	usb_isr.c:236: case HID_SET_REPORT:
      000555 B5 28 53         [24] 1040 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00143$
      000558 80 06            [24] 1041 	sjmp	00140$
      00055A                       1042 00138$:
                                   1043 ;	usb_isr.c:239: len = 0;
      00055A 7E 00            [12] 1044 	mov	r6,#0x00
      00055C 7F 00            [12] 1045 	mov	r7,#0x00
                                   1046 ;	usb_isr.c:240: break;
                                   1047 ;	usb_isr.c:242: case HID_SET_PROTOCOL:
      00055E 80 55            [24] 1048 	sjmp	00149$
      000560                       1049 00140$:
                                   1050 ;	usb_isr.c:243: len = 0;
      000560 7E 00            [12] 1051 	mov	r6,#0x00
      000562 7F 00            [12] 1052 	mov	r7,#0x00
                                   1053 ;	usb_isr.c:244: break;
                                   1054 ;	usb_isr.c:245: case HID_GET_REPORT:
      000564 80 4F            [24] 1055 	sjmp	00149$
      000566                       1056 00141$:
                                   1057 ;	usb_isr.c:246: Ep0Buffer[0] = LedState;
      000566 90 00 00         [24] 1058 	mov	dptr,#_Ep0Buffer
      000569 E5 22            [12] 1059 	mov	a,_LedState
      00056B F0               [24] 1060 	movx	@dptr,a
                                   1061 ;	usb_isr.c:247: len = SetupLen >= 1 ? 1 : SetupLen;
      00056C AB 2A            [24] 1062 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      00056E AC 2B            [24] 1063 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000570 C3               [12] 1064 	clr	c
      000571 EB               [12] 1065 	mov	a,r3
      000572 94 01            [12] 1066 	subb	a,#0x01
      000574 EC               [12] 1067 	mov	a,r4
      000575 94 00            [12] 1068 	subb	a,#0x00
      000577 40 06            [24] 1069 	jc	00182$
      000579 7B 01            [12] 1070 	mov	r3,#0x01
      00057B 7C 00            [12] 1071 	mov	r4,#0x00
      00057D 80 04            [24] 1072 	sjmp	00183$
      00057F                       1073 00182$:
      00057F AB 2A            [24] 1074 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      000581 AC 2B            [24] 1075 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000583                       1076 00183$:
      000583 8B 0E            [24] 1077 	mov	ar6,r3
      000585 8C 0F            [24] 1078 	mov	ar7,r4
                                   1079 ;	usb_isr.c:248: break;
                                   1080 ;	usb_isr.c:249: case HID_GET_IDLE:
      000587 80 2C            [24] 1081 	sjmp	00149$
      000589                       1082 00142$:
                                   1083 ;	usb_isr.c:250: Ep0Buffer[0] = 0x00;
      000589 90 00 00         [24] 1084 	mov	dptr,#_Ep0Buffer
      00058C E4               [12] 1085 	clr	a
      00058D F0               [24] 1086 	movx	@dptr,a
                                   1087 ;	usb_isr.c:251: len = SetupLen >= 1 ? 1 : SetupLen;
      00058E AB 2A            [24] 1088 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      000590 AC 2B            [24] 1089 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      000592 C3               [12] 1090 	clr	c
      000593 EB               [12] 1091 	mov	a,r3
      000594 94 01            [12] 1092 	subb	a,#0x01
      000596 EC               [12] 1093 	mov	a,r4
      000597 94 00            [12] 1094 	subb	a,#0x00
      000599 40 06            [24] 1095 	jc	00184$
      00059B 7B 01            [12] 1096 	mov	r3,#0x01
      00059D 7C 00            [12] 1097 	mov	r4,#0x00
      00059F 80 04            [24] 1098 	sjmp	00185$
      0005A1                       1099 00184$:
      0005A1 AB 2A            [24] 1100 	mov	r3,_USB_DeviceInterrupt_SetupLen_10000_78
      0005A3 AC 2B            [24] 1101 	mov	r4,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      0005A5                       1102 00185$:
      0005A5 8B 0E            [24] 1103 	mov	ar6,r3
      0005A7 8C 0F            [24] 1104 	mov	ar7,r4
                                   1105 ;	usb_isr.c:252: break;
                                   1106 ;	usb_isr.c:253: default:
      0005A9 80 0A            [24] 1107 	sjmp	00149$
      0005AB                       1108 00143$:
                                   1109 ;	usb_isr.c:254: errflag = 0xFF; break;
      0005AB 7D FF            [12] 1110 	mov	r5,#0xff
                                   1111 ;	usb_isr.c:256: break;
                                   1112 ;	usb_isr.c:258: default:
      0005AD 80 06            [24] 1113 	sjmp	00149$
      0005AF                       1114 00145$:
                                   1115 ;	usb_isr.c:259: errflag = 0xFF; break;
      0005AF 7D FF            [12] 1116 	mov	r5,#0xff
                                   1117 ;	usb_isr.c:260: }
      0005B1 80 02            [24] 1118 	sjmp	00149$
      0005B3                       1119 00148$:
                                   1120 ;	usb_isr.c:262: errflag = 0xFF;
      0005B3 7D FF            [12] 1121 	mov	r5,#0xff
      0005B5                       1122 00149$:
                                   1123 ;	usb_isr.c:265: if (errflag == 0xFF) {
      0005B5 BD FF 06         [24] 1124 	cjne	r5,#0xff,00151$
                                   1125 ;	usb_isr.c:266: UEP0_CTRL = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_STALL | UEP_T_RES_STALL;
      0005B8 75 DC CF         [24] 1126 	mov	_UEP0_CTRL,#0xcf
      0005BB 02 06 76         [24] 1127 	ljmp	00166$
      0005BE                       1128 00151$:
                                   1129 ;	usb_isr.c:268: UEP0_T_LEN = (len <= THIS_ENDP0_SIZE) ? len : 0;
      0005BE C3               [12] 1130 	clr	c
      0005BF 74 08            [12] 1131 	mov	a,#0x08
      0005C1 9E               [12] 1132 	subb	a,r6
      0005C2 E4               [12] 1133 	clr	a
      0005C3 9F               [12] 1134 	subb	a,r7
                                   1135 ;	free result
      0005C4 50 02            [24] 1136 	jnc	00187$
      0005C6 7E 00            [12] 1137 	mov	r6,#0x00
      0005C8                       1138 00187$:
      0005C8 8E DD            [24] 1139 	mov	_UEP0_T_LEN,r6
                                   1140 ;	usb_isr.c:269: UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
      0005CA 75 DC C0         [24] 1141 	mov	_UEP0_CTRL,#0xc0
                                   1142 ;	usb_isr.c:271: break;
      0005CD 02 06 76         [24] 1143 	ljmp	00166$
                                   1144 ;	usb_isr.c:274: case UIS_TOKEN_IN | 0:
      0005D0                       1145 00153$:
                                   1146 ;	usb_isr.c:275: switch (SetupReqCode) {
      0005D0 74 05            [12] 1147 	mov	a,#0x05
      0005D2 B5 28 02         [24] 1148 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00565$
      0005D5 80 5C            [24] 1149 	sjmp	00155$
      0005D7                       1150 00565$:
      0005D7 74 06            [12] 1151 	mov	a,#0x06
      0005D9 B5 28 67         [24] 1152 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00156$
                                   1153 ;	usb_isr.c:277: len = SetupLen >= THIS_ENDP0_SIZE ? THIS_ENDP0_SIZE : SetupLen;
      0005DC AE 2A            [24] 1154 	mov	r6,_USB_DeviceInterrupt_SetupLen_10000_78
      0005DE AF 2B            [24] 1155 	mov	r7,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      0005E0 C3               [12] 1156 	clr	c
      0005E1 EE               [12] 1157 	mov	a,r6
      0005E2 94 08            [12] 1158 	subb	a,#0x08
      0005E4 EF               [12] 1159 	mov	a,r7
      0005E5 94 00            [12] 1160 	subb	a,#0x00
      0005E7 40 06            [24] 1161 	jc	00188$
      0005E9 7E 08            [12] 1162 	mov	r6,#0x08
      0005EB 7F 00            [12] 1163 	mov	r7,#0x00
      0005ED 80 04            [24] 1164 	sjmp	00189$
      0005EF                       1165 00188$:
      0005EF AE 2A            [24] 1166 	mov	r6,_USB_DeviceInterrupt_SetupLen_10000_78
      0005F1 AF 2B            [24] 1167 	mov	r7,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      0005F3                       1168 00189$:
                                   1169 ;	usb_isr.c:278: memcpy(Ep0Buffer, pDescr, len);
      0005F3 85 2C 2F         [24] 1170 	mov	___memcpy_PARM_2,_USB_DeviceInterrupt_pDescr_10000_78
      0005F6 85 2D 30         [24] 1171 	mov	(___memcpy_PARM_2 + 1),(_USB_DeviceInterrupt_pDescr_10000_78 + 1)
      0005F9 85 2E 31         [24] 1172 	mov	(___memcpy_PARM_2 + 2),(_USB_DeviceInterrupt_pDescr_10000_78 + 2)
      0005FC 8E 32            [24] 1173 	mov	___memcpy_PARM_3,r6
      0005FE 8F 33            [24] 1174 	mov	(___memcpy_PARM_3 + 1),r7
      000600 90 00 00         [24] 1175 	mov	dptr,#_Ep0Buffer
      000603 75 F0 00         [24] 1176 	mov	b, #0x00
      000606 C0 0F            [24] 1177 	push	ar7
      000608 C0 0E            [24] 1178 	push	ar6
      00060A 75 D0 00         [24] 1179 	mov	psw,#0x00
      00060D 12 06 EB         [24] 1180 	lcall	___memcpy
      000610 75 D0 08         [24] 1181 	mov	psw,#0x08
      000613 D0 0E            [24] 1182 	pop	ar6
      000615 D0 0F            [24] 1183 	pop	ar7
                                   1184 ;	usb_isr.c:279: SetupLen -= len;
      000617 E5 2A            [12] 1185 	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
      000619 C3               [12] 1186 	clr	c
      00061A 9E               [12] 1187 	subb	a,r6
      00061B F5 2A            [12] 1188 	mov	_USB_DeviceInterrupt_SetupLen_10000_78,a
      00061D E5 2B            [12] 1189 	mov	a,(_USB_DeviceInterrupt_SetupLen_10000_78 + 1)
      00061F 9F               [12] 1190 	subb	a,r7
      000620 F5 2B            [12] 1191 	mov	(_USB_DeviceInterrupt_SetupLen_10000_78 + 1),a
                                   1192 ;	usb_isr.c:280: pDescr   += len;
      000622 EE               [12] 1193 	mov	a,r6
      000623 25 2C            [12] 1194 	add	a, _USB_DeviceInterrupt_pDescr_10000_78
      000625 F5 2C            [12] 1195 	mov	_USB_DeviceInterrupt_pDescr_10000_78,a
      000627 EF               [12] 1196 	mov	a,r7
      000628 35 2D            [12] 1197 	addc	a, (_USB_DeviceInterrupt_pDescr_10000_78 + 1)
      00062A F5 2D            [12] 1198 	mov	(_USB_DeviceInterrupt_pDescr_10000_78 + 1),a
                                   1199 ;	usb_isr.c:281: UEP0_T_LEN = len;
      00062C 8E DD            [24] 1200 	mov	_UEP0_T_LEN,r6
                                   1201 ;	usb_isr.c:282: UEP0_CTRL ^= bUEP_T_TOG;
      00062E 63 DC 40         [24] 1202 	xrl	_UEP0_CTRL,#0x40
                                   1203 ;	usb_isr.c:283: break;
                                   1204 ;	usb_isr.c:284: case USB_SET_ADDRESS:
      000631 80 43            [24] 1205 	sjmp	00166$
      000633                       1206 00155$:
                                   1207 ;	usb_isr.c:285: USB_DEV_AD  = (USB_DEV_AD & bUDA_GP_BIT) | (UINT8)SetupLen;
      000633 E5 E3            [12] 1208 	mov	a,_USB_DEV_AD
      000635 54 80            [12] 1209 	anl	a,#0x80
      000637 FF               [12] 1210 	mov	r7,a
      000638 E5 2A            [12] 1211 	mov	a,_USB_DeviceInterrupt_SetupLen_10000_78
      00063A FE               [12] 1212 	mov	r6,a
      00063B 4F               [12] 1213 	orl	a,r7
      00063C F5 E3            [12] 1214 	mov	_USB_DEV_AD,a
                                   1215 ;	usb_isr.c:286: UEP0_CTRL   = UEP_R_RES_ACK | UEP_T_RES_NAK;
      00063E 75 DC 02         [24] 1216 	mov	_UEP0_CTRL,#0x02
                                   1217 ;	usb_isr.c:287: break;
                                   1218 ;	usb_isr.c:288: default:
      000641 80 33            [24] 1219 	sjmp	00166$
      000643                       1220 00156$:
                                   1221 ;	usb_isr.c:289: UEP0_T_LEN = 0;
      000643 75 DD 00         [24] 1222 	mov	_UEP0_T_LEN,#0x00
                                   1223 ;	usb_isr.c:290: UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
      000646 75 DC 02         [24] 1224 	mov	_UEP0_CTRL,#0x02
                                   1225 ;	usb_isr.c:293: break;
                                   1226 ;	usb_isr.c:296: case UIS_TOKEN_OUT | 0:
      000649 80 2B            [24] 1227 	sjmp	00166$
      00064B                       1228 00158$:
                                   1229 ;	usb_isr.c:297: if (U_TOG_OK) {
      00064B 30 DE 22         [24] 1230 	jnb	_U_TOG_OK,00164$
                                   1231 ;	usb_isr.c:298: if ((SetupReqType & USB_REQ_TYP_MASK) == USB_REQ_TYP_CLASS
      00064E AF 29            [24] 1232 	mov	r7,_USB_DeviceInterrupt_SetupReqType_10000_78
      000650 53 0F 60         [24] 1233 	anl	ar7,#0x60
      000653 BF 20 1A         [24] 1234 	cjne	r7,#0x20,00164$
                                   1235 ;	usb_isr.c:300: && USB_RX_LEN >= 1) {
      000656 74 09            [12] 1236 	mov	a,#0x09
      000658 B5 28 15         [24] 1237 	cjne	a,_USB_DeviceInterrupt_SetupReqCode_10000_78,00164$
      00065B 74 FF            [12] 1238 	mov	a,#0x100 - 0x01
      00065D 25 DB            [12] 1239 	add	a,_USB_RX_LEN
      00065F 50 0F            [24] 1240 	jnc	00164$
                                   1241 ;	usb_isr.c:301: ApplyLEDs(Ep0Buffer[0]);
      000661 90 00 00         [24] 1242 	mov	dptr,#_Ep0Buffer
      000664 E0               [24] 1243 	movx	a,@dptr
      000665 F5 82            [12] 1244 	mov	dpl,a
      000667 75 D0 00         [24] 1245 	mov	psw,#0x00
      00066A 12 01 B3         [24] 1246 	lcall	_ApplyLEDs
      00066D 75 D0 08         [24] 1247 	mov	psw,#0x08
      000670                       1248 00164$:
                                   1249 ;	usb_isr.c:305: UEP0_T_LEN = 0;
      000670 75 DD 00         [24] 1250 	mov	_UEP0_T_LEN,#0x00
                                   1251 ;	usb_isr.c:306: UEP0_CTRL  = bUEP_R_TOG | bUEP_T_TOG | UEP_R_RES_ACK | UEP_T_RES_ACK;
      000673 75 DC C0         [24] 1252 	mov	_UEP0_CTRL,#0xc0
                                   1253 ;	usb_isr.c:311: }
      000676                       1254 00166$:
                                   1255 ;	usb_isr.c:312: UIF_TRANSFER = 0;
                                   1256 ;	assignBit
      000676 C2 D9            [12] 1257 	clr	_UIF_TRANSFER
      000678 80 1C            [24] 1258 	sjmp	00176$
      00067A                       1259 00174$:
                                   1260 ;	usb_isr.c:313: } else if (UIF_BUS_RST) {
      00067A 30 D8 13         [24] 1261 	jnb	_UIF_BUS_RST,00171$
                                   1262 ;	usb_isr.c:314: UEP0_CTRL    = UEP_R_RES_ACK | UEP_T_RES_NAK;
      00067D 75 DC 02         [24] 1263 	mov	_UEP0_CTRL,#0x02
                                   1264 ;	usb_isr.c:315: UEP1_CTRL    = UEP_T_RES_NAK;
      000680 75 D2 02         [24] 1265 	mov	_UEP1_CTRL,#0x02
                                   1266 ;	usb_isr.c:316: Ready        = 0;
                                   1267 ;	assignBit
      000683 C2 00            [12] 1268 	clr	_Ready
                                   1269 ;	usb_isr.c:317: USB_DEV_AD   = 0x00;
      000685 75 E3 00         [24] 1270 	mov	_USB_DEV_AD,#0x00
                                   1271 ;	usb_isr.c:318: UIF_SUSPEND  = 0;
                                   1272 ;	assignBit
      000688 C2 DA            [12] 1273 	clr	_UIF_SUSPEND
                                   1274 ;	usb_isr.c:319: UIF_TRANSFER = 0;
                                   1275 ;	assignBit
      00068A C2 D9            [12] 1276 	clr	_UIF_TRANSFER
                                   1277 ;	usb_isr.c:320: UIF_BUS_RST  = 0;
                                   1278 ;	assignBit
      00068C C2 D8            [12] 1279 	clr	_UIF_BUS_RST
      00068E 80 06            [24] 1280 	sjmp	00176$
      000690                       1281 00171$:
                                   1282 ;	usb_isr.c:321: } else if (UIF_SUSPEND) {
                                   1283 ;	usb_isr.c:322: UIF_SUSPEND = 0;
                                   1284 ;	assignBit
      000690 10 DA 03         [24] 1285 	jbc	_UIF_SUSPEND,00176$
                                   1286 ;	usb_isr.c:324: USB_INT_FG = 0xFF;
      000693 75 D8 FF         [24] 1287 	mov	_USB_INT_FG,#0xff
      000696                       1288 00176$:
                                   1289 ;	usb_isr.c:326: }
      000696 D0 D0            [24] 1290 	pop	psw
      000698 D0 00            [24] 1291 	pop	(0+0)
      00069A D0 01            [24] 1292 	pop	(0+1)
      00069C D0 02            [24] 1293 	pop	(0+2)
      00069E D0 03            [24] 1294 	pop	(0+3)
      0006A0 D0 04            [24] 1295 	pop	(0+4)
      0006A2 D0 05            [24] 1296 	pop	(0+5)
      0006A4 D0 06            [24] 1297 	pop	(0+6)
      0006A6 D0 07            [24] 1298 	pop	(0+7)
      0006A8 D0 83            [24] 1299 	pop	dph
      0006AA D0 82            [24] 1300 	pop	dpl
      0006AC D0 F0            [24] 1301 	pop	b
      0006AE D0 E0            [24] 1302 	pop	acc
      0006B0 D0 21            [24] 1303 	pop	bits
      0006B2 02 00 8E         [24] 1304 	ljmp	sdcc_atomic_maybe_rollback
                                   1305 ;------------------------------------------------------------
                                   1306 ;Allocation info for local variables in function 'USB_DeviceInit'
                                   1307 ;------------------------------------------------------------
                                   1308 ;ep0_addr      Allocated to registers r6 r7 
                                   1309 ;ep1_addr      Allocated to registers r4 r5 
                                   1310 ;------------------------------------------------------------
                                   1311 ;	usb_isr.c:328: void USB_DeviceInit(void)
                                   1312 ;	-----------------------------------------
                                   1313 ;	 function USB_DeviceInit
                                   1314 ;	-----------------------------------------
      0006B5                       1315 _USB_DeviceInit:
                           000007  1316 	ar7 = 0x07
                           000006  1317 	ar6 = 0x06
                           000005  1318 	ar5 = 0x05
                           000004  1319 	ar4 = 0x04
                           000003  1320 	ar3 = 0x03
                           000002  1321 	ar2 = 0x02
                           000001  1322 	ar1 = 0x01
                           000000  1323 	ar0 = 0x00
                                   1324 ;	usb_isr.c:330: UINT16 ep0_addr = (UINT16)(UINT8 __xdata *)Ep0Buffer;
      0006B5 7E 00            [12] 1325 	mov	r6,#_Ep0Buffer
      0006B7 7F 00            [12] 1326 	mov	r7,#(_Ep0Buffer >> 8)
                                   1327 ;	usb_isr.c:331: UINT16 ep1_addr = (UINT16)(UINT8 __xdata *)Ep1Buffer;
      0006B9 7C 40            [12] 1328 	mov	r4,#_Ep1Buffer
      0006BB 7D 00            [12] 1329 	mov	r5,#(_Ep1Buffer >> 8)
                                   1330 ;	usb_isr.c:333: IE_USB     = 0;
                                   1331 ;	assignBit
      0006BD C2 EA            [12] 1332 	clr	_IE_USB
                                   1333 ;	usb_isr.c:334: USB_CTRL   = 0x00;
      0006BF 75 E2 00         [24] 1334 	mov	_USB_CTRL,#0x00
                                   1335 ;	usb_isr.c:335: UEP4_1_MOD = bUEP1_TX_EN;       /* EP1 仅上传 (IN) */
      0006C2 75 EA 40         [24] 1336 	mov	_UEP4_1_MOD,#0x40
                                   1337 ;	usb_isr.c:336: UEP2_3_MOD = 0x00;
      0006C5 75 EB 00         [24] 1338 	mov	_UEP2_3_MOD,#0x00
                                   1339 ;	usb_isr.c:338: UEP0_DMA_L = (UINT8)(ep0_addr & 0xFF);
      0006C8 8E EC            [24] 1340 	mov	_UEP0_DMA_L,r6
                                   1341 ;	usb_isr.c:339: UEP0_DMA_H = (UINT8)(ep0_addr >> 8);
      0006CA 8F ED            [24] 1342 	mov	_UEP0_DMA_H,r7
                                   1343 ;	usb_isr.c:340: UEP1_DMA_L = (UINT8)(ep1_addr & 0xFF);
      0006CC 8C EE            [24] 1344 	mov	_UEP1_DMA_L,r4
                                   1345 ;	usb_isr.c:341: UEP1_DMA_H = (UINT8)(ep1_addr >> 8);
      0006CE 8D EF            [24] 1346 	mov	_UEP1_DMA_H,r5
                                   1347 ;	usb_isr.c:343: UEP0_CTRL  = UEP_R_RES_ACK | UEP_T_RES_NAK;
      0006D0 75 DC 02         [24] 1348 	mov	_UEP0_CTRL,#0x02
                                   1349 ;	usb_isr.c:344: UEP1_CTRL  = UEP_T_RES_NAK;
      0006D3 75 D2 02         [24] 1350 	mov	_UEP1_CTRL,#0x02
                                   1351 ;	usb_isr.c:346: USB_DEV_AD = 0x00;
      0006D6 75 E3 00         [24] 1352 	mov	_USB_DEV_AD,#0x00
                                   1353 ;	usb_isr.c:347: UDEV_CTRL  = bUD_PD_DIS;
      0006D9 75 D1 80         [24] 1354 	mov	_UDEV_CTRL,#0x80
                                   1355 ;	usb_isr.c:348: USB_CTRL   = bUC_DEV_PU_EN | bUC_INT_BUSY | bUC_DMA_EN;
      0006DC 75 E2 29         [24] 1356 	mov	_USB_CTRL,#0x29
                                   1357 ;	usb_isr.c:349: UDEV_CTRL |= bUD_PORT_EN;
      0006DF 43 D1 01         [24] 1358 	orl	_UDEV_CTRL,#0x01
                                   1359 ;	usb_isr.c:350: USB_INT_FG = 0xFF;
      0006E2 75 D8 FF         [24] 1360 	mov	_USB_INT_FG,#0xff
                                   1361 ;	usb_isr.c:351: USB_INT_EN = bUIE_SUSPEND | bUIE_TRANSFER | bUIE_BUS_RST;
      0006E5 75 E1 07         [24] 1362 	mov	_USB_INT_EN,#0x07
                                   1363 ;	usb_isr.c:352: IE_USB     = 1;
                                   1364 ;	assignBit
      0006E8 D2 EA            [12] 1365 	setb	_IE_USB
                                   1366 ;	usb_isr.c:353: }
      0006EA 22               [24] 1367 	ret
                                   1368 	.area CSEG    (CODE)
                                   1369 	.area CONST   (CODE)
                                   1370 	.area XINIT   (CODE)
                                   1371 	.area CABS    (ABS,CODE)
