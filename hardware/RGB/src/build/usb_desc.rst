                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ISO C Compiler
                                      3 ; Version 4.6.0 #16555 (MINGW64)
                                      4 ;--------------------------------------------------------
                                      5 	.module usb_desc
                                      6 	
                                      7 	.optsdcc -mmcs51 --model-small
                                      8 ;--------------------------------------------------------
                                      9 ; Public variables in this module
                                     10 ;--------------------------------------------------------
                                     11 	.globl _MyReportDescrLen
                                     12 	.globl _MyProdInfoLen
                                     13 	.globl _MyManuInfoLen
                                     14 	.globl _MyLangDescrLen
                                     15 	.globl _MyCfgDescrLen
                                     16 	.globl _MyDevDescrLen
                                     17 	.globl _MyProdInfo
                                     18 	.globl _MyManuInfo
                                     19 	.globl _MyLangDescr
                                     20 	.globl _MyCfgDescr
                                     21 	.globl _MyDevDescr
                                     22 	.globl _MyReportDescr
                                     23 	.globl _U_IS_NAK
                                     24 	.globl _U_TOG_OK
                                     25 	.globl _U_SIE_FREE
                                     26 	.globl _UIF_FIFO_OV
                                     27 	.globl _UIF_SUSPEND
                                     28 	.globl _UIF_TRANSFER
                                     29 	.globl _UIF_BUS_RST
                                     30 	.globl _TF0
                                     31 	.globl _TR0
                                     32 	.globl _IE_USB
                                     33 	.globl _EA
                                     34 	.globl _ET0
                                     35 	.globl _UEP1_DMA_H
                                     36 	.globl _UEP1_DMA_L
                                     37 	.globl _UEP0_DMA_H
                                     38 	.globl _UEP0_DMA_L
                                     39 	.globl _UEP2_3_MOD
                                     40 	.globl _UEP4_1_MOD
                                     41 	.globl _UEP2_DMA_H
                                     42 	.globl _UEP2_DMA_L
                                     43 	.globl _USB_DEV_AD
                                     44 	.globl _USB_CTRL
                                     45 	.globl _USB_INT_EN
                                     46 	.globl _UEP0_T_LEN
                                     47 	.globl _UEP0_CTRL
                                     48 	.globl _USB_RX_LEN
                                     49 	.globl _USB_MIS_ST
                                     50 	.globl _USB_INT_ST
                                     51 	.globl _USB_INT_FG
                                     52 	.globl _UEP3_T_LEN
                                     53 	.globl _UEP3_CTRL
                                     54 	.globl _UEP2_T_LEN
                                     55 	.globl _UEP2_CTRL
                                     56 	.globl _UEP1_T_LEN
                                     57 	.globl _UEP1_CTRL
                                     58 	.globl _UDEV_CTRL
                                     59 	.globl _P3_DIR_PU
                                     60 	.globl _P3_MOD_OC
                                     61 	.globl _P3
                                     62 	.globl _P1_DIR_PU
                                     63 	.globl _P1_MOD_OC
                                     64 	.globl _P1
                                     65 	.globl _TH0
                                     66 	.globl _TL0
                                     67 	.globl _TMOD
                                     68 	.globl _TCON
                                     69 	.globl _IE_EX
                                     70 	.globl _IE
                                     71 	.globl _CLOCK_CFG
                                     72 	.globl _WAKE_CTRL
                                     73 	.globl _SAFE_MOD
                                     74 	.globl _PCON
                                     75 ;--------------------------------------------------------
                                     76 ; special function registers
                                     77 ;--------------------------------------------------------
                                     78 	.area RSEG    (ABS,DATA)
      000000                         79 	.org 0x0000
                           000087    80 _PCON	=	0x0087
                           0000A1    81 _SAFE_MOD	=	0x00a1
                           0000A9    82 _WAKE_CTRL	=	0x00a9
                           0000B9    83 _CLOCK_CFG	=	0x00b9
                           0000A8    84 _IE	=	0x00a8
                           0000E8    85 _IE_EX	=	0x00e8
                           000088    86 _TCON	=	0x0088
                           000089    87 _TMOD	=	0x0089
                           00008A    88 _TL0	=	0x008a
                           00008C    89 _TH0	=	0x008c
                           000090    90 _P1	=	0x0090
                           000092    91 _P1_MOD_OC	=	0x0092
                           000093    92 _P1_DIR_PU	=	0x0093
                           0000B0    93 _P3	=	0x00b0
                           000096    94 _P3_MOD_OC	=	0x0096
                           000097    95 _P3_DIR_PU	=	0x0097
                           0000D1    96 _UDEV_CTRL	=	0x00d1
                           0000D2    97 _UEP1_CTRL	=	0x00d2
                           0000D3    98 _UEP1_T_LEN	=	0x00d3
                           0000D4    99 _UEP2_CTRL	=	0x00d4
                           0000D5   100 _UEP2_T_LEN	=	0x00d5
                           0000D6   101 _UEP3_CTRL	=	0x00d6
                           0000D7   102 _UEP3_T_LEN	=	0x00d7
                           0000D8   103 _USB_INT_FG	=	0x00d8
                           0000D9   104 _USB_INT_ST	=	0x00d9
                           0000DA   105 _USB_MIS_ST	=	0x00da
                           0000DB   106 _USB_RX_LEN	=	0x00db
                           0000DC   107 _UEP0_CTRL	=	0x00dc
                           0000DD   108 _UEP0_T_LEN	=	0x00dd
                           0000E1   109 _USB_INT_EN	=	0x00e1
                           0000E2   110 _USB_CTRL	=	0x00e2
                           0000E3   111 _USB_DEV_AD	=	0x00e3
                           0000E4   112 _UEP2_DMA_L	=	0x00e4
                           0000E5   113 _UEP2_DMA_H	=	0x00e5
                           0000EA   114 _UEP4_1_MOD	=	0x00ea
                           0000EB   115 _UEP2_3_MOD	=	0x00eb
                           0000EC   116 _UEP0_DMA_L	=	0x00ec
                           0000ED   117 _UEP0_DMA_H	=	0x00ed
                           0000EE   118 _UEP1_DMA_L	=	0x00ee
                           0000EF   119 _UEP1_DMA_H	=	0x00ef
                                    120 ;--------------------------------------------------------
                                    121 ; special function bits
                                    122 ;--------------------------------------------------------
                                    123 	.area RSEG    (ABS,DATA)
      000000                        124 	.org 0x0000
                           0000A9   125 _ET0	=	0x00a9
                           0000AF   126 _EA	=	0x00af
                           0000EA   127 _IE_USB	=	0x00ea
                           00008C   128 _TR0	=	0x008c
                           00008D   129 _TF0	=	0x008d
                           0000D8   130 _UIF_BUS_RST	=	0x00d8
                           0000D9   131 _UIF_TRANSFER	=	0x00d9
                           0000DA   132 _UIF_SUSPEND	=	0x00da
                           0000DC   133 _UIF_FIFO_OV	=	0x00dc
                           0000DD   134 _U_SIE_FREE	=	0x00dd
                           0000DE   135 _U_TOG_OK	=	0x00de
                           0000DF   136 _U_IS_NAK	=	0x00df
                                    137 ;--------------------------------------------------------
                                    138 ; overlayable register banks
                                    139 ;--------------------------------------------------------
                                    140 	.area REG_BANK_0	(REL,OVR,DATA)
      000000                        141 	.ds 8
                                    142 ;--------------------------------------------------------
                                    143 ; internal ram data
                                    144 ;--------------------------------------------------------
                                    145 	.area DSEG    (DATA)
                                    146 ;--------------------------------------------------------
                                    147 ; overlayable items in internal ram
                                    148 ;--------------------------------------------------------
                                    149 ;--------------------------------------------------------
                                    150 ; indirectly addressable internal ram data
                                    151 ;--------------------------------------------------------
                                    152 	.area ISEG    (DATA)
                                    153 ;--------------------------------------------------------
                                    154 ; absolute internal ram data
                                    155 ;--------------------------------------------------------
                                    156 	.area IABS    (ABS,DATA)
                                    157 	.area IABS    (ABS,DATA)
                                    158 ;--------------------------------------------------------
                                    159 ; bit data
                                    160 ;--------------------------------------------------------
                                    161 	.area BSEG    (BIT)
                                    162 ;--------------------------------------------------------
                                    163 ; paged external ram data
                                    164 ;--------------------------------------------------------
                                    165 	.area PSEG    (PAG,XDATA)
                                    166 ;--------------------------------------------------------
                                    167 ; uninitialized external ram data
                                    168 ;--------------------------------------------------------
                                    169 	.area XSEG    (XDATA)
                                    170 ;--------------------------------------------------------
                                    171 ; absolute external ram data
                                    172 ;--------------------------------------------------------
                                    173 	.area XABS    (ABS,XDATA)
                                    174 ;--------------------------------------------------------
                                    175 ; initialized external ram data
                                    176 ;--------------------------------------------------------
                                    177 	.area XISEG   (XDATA)
                                    178 	.area HOME    (CODE)
                                    179 	.area GSINIT0 (CODE)
                                    180 	.area GSINIT1 (CODE)
                                    181 	.area GSINIT2 (CODE)
                                    182 	.area GSINIT3 (CODE)
                                    183 	.area GSINIT4 (CODE)
                                    184 	.area GSINIT5 (CODE)
                                    185 	.area GSINIT  (CODE)
                                    186 	.area GSFINAL (CODE)
                                    187 	.area CSEG    (CODE)
                                    188 ;--------------------------------------------------------
                                    189 ; global & static initialisations
                                    190 ;--------------------------------------------------------
                                    191 	.area HOME    (CODE)
                                    192 	.area GSINIT  (CODE)
                                    193 	.area GSFINAL (CODE)
                                    194 	.area GSINIT  (CODE)
                                    195 ;--------------------------------------------------------
                                    196 ; Home
                                    197 ;--------------------------------------------------------
                                    198 	.area HOME    (CODE)
                                    199 	.area HOME    (CODE)
                                    200 ;--------------------------------------------------------
                                    201 ; code
                                    202 ;--------------------------------------------------------
                                    203 	.area CSEG    (CODE)
                                    204 	.area CSEG    (CODE)
                                    205 	.area CONST   (CODE)
                                    206 	.area CONST   (CODE)
      00077B                        207 _MyReportDescr:
      00077B 06                     208 	.db #0x06	; 6
      00077C 00                     209 	.db #0x00	; 0
      00077D FF                     210 	.db #0xff	; 255
      00077E 09                     211 	.db #0x09	; 9
      00077F 01                     212 	.db #0x01	; 1
      000780 A1                     213 	.db #0xa1	; 161
      000781 01                     214 	.db #0x01	; 1
      000782 09                     215 	.db #0x09	; 9
      000783 02                     216 	.db #0x02	; 2
      000784 15                     217 	.db #0x15	; 21
      000785 00                     218 	.db #0x00	; 0
      000786 26                     219 	.db #0x26	; 38
      000787 FF                     220 	.db #0xff	; 255
      000788 00                     221 	.db #0x00	; 0
      000789 75                     222 	.db #0x75	; 117	'u'
      00078A 08                     223 	.db #0x08	; 8
      00078B 95                     224 	.db #0x95	; 149
      00078C 01                     225 	.db #0x01	; 1
      00078D 91                     226 	.db #0x91	; 145
      00078E 02                     227 	.db #0x02	; 2
      00078F C0                     228 	.db #0xc0	; 192
                                    229 	.area CSEG    (CODE)
                                    230 	.area CONST   (CODE)
      000790                        231 _MyDevDescr:
      000790 12                     232 	.db #0x12	; 18
      000791 01                     233 	.db #0x01	; 1
      000792 10                     234 	.db #0x10	; 16
      000793 01                     235 	.db #0x01	; 1
      000794 00                     236 	.db #0x00	; 0
      000795 00                     237 	.db #0x00	; 0
      000796 00                     238 	.db #0x00	; 0
      000797 08                     239 	.db #0x08	; 8
      000798 09                     240 	.db #0x09	; 9
      000799 12                     241 	.db #0x12	; 18
      00079A 52                     242 	.db #0x52	; 82	'R'
      00079B C5                     243 	.db #0xc5	; 197
      00079C 00                     244 	.db #0x00	; 0
      00079D 10                     245 	.db #0x10	; 16
      00079E 01                     246 	.db #0x01	; 1
      00079F 02                     247 	.db #0x02	; 2
      0007A0 00                     248 	.db #0x00	; 0
      0007A1 01                     249 	.db #0x01	; 1
                                    250 	.area CSEG    (CODE)
                                    251 	.area CONST   (CODE)
      0007A2                        252 _MyCfgDescr:
      0007A2 09                     253 	.db #0x09	; 9
      0007A3 02                     254 	.db #0x02	; 2
      0007A4 22                     255 	.db #0x22	; 34
      0007A5 00                     256 	.db #0x00	; 0
      0007A6 01                     257 	.db #0x01	; 1
      0007A7 01                     258 	.db #0x01	; 1
      0007A8 00                     259 	.db #0x00	; 0
      0007A9 80                     260 	.db #0x80	; 128
      0007AA 32                     261 	.db #0x32	; 50	'2'
      0007AB 09                     262 	.db #0x09	; 9
      0007AC 04                     263 	.db #0x04	; 4
      0007AD 00                     264 	.db #0x00	; 0
      0007AE 00                     265 	.db #0x00	; 0
      0007AF 01                     266 	.db #0x01	; 1
      0007B0 03                     267 	.db #0x03	; 3
      0007B1 00                     268 	.db #0x00	; 0
      0007B2 00                     269 	.db #0x00	; 0
      0007B3 00                     270 	.db #0x00	; 0
      0007B4 09                     271 	.db #0x09	; 9
      0007B5 21                     272 	.db #0x21	; 33
      0007B6 11                     273 	.db #0x11	; 17
      0007B7 01                     274 	.db #0x01	; 1
      0007B8 00                     275 	.db #0x00	; 0
      0007B9 01                     276 	.db #0x01	; 1
      0007BA 22                     277 	.db #0x22	; 34
      0007BB 15                     278 	.db #0x15	; 21
      0007BC 00                     279 	.db #0x00	; 0
      0007BD 07                     280 	.db #0x07	; 7
      0007BE 05                     281 	.db #0x05	; 5
      0007BF 81                     282 	.db #0x81	; 129
      0007C0 03                     283 	.db #0x03	; 3
      0007C1 08                     284 	.db #0x08	; 8
      0007C2 00                     285 	.db #0x00	; 0
      0007C3 0A                     286 	.db #0x0a	; 10
                                    287 	.area CSEG    (CODE)
                                    288 	.area CONST   (CODE)
      0007C4                        289 _MyLangDescr:
      0007C4 04                     290 	.db #0x04	; 4
      0007C5 03                     291 	.db #0x03	; 3
      0007C6 09                     292 	.db #0x09	; 9
      0007C7 04                     293 	.db #0x04	; 4
                                    294 	.area CSEG    (CODE)
                                    295 	.area CONST   (CODE)
      0007C8                        296 _MyManuInfo:
      0007C8 0E                     297 	.db #0x0e	; 14
      0007C9 03                     298 	.db #0x03	; 3
      0007CA 6D                     299 	.db #0x6d	; 109	'm'
      0007CB 00                     300 	.db #0x00	; 0
      0007CC 69                     301 	.db #0x69	; 105	'i'
      0007CD 00                     302 	.db #0x00	; 0
      0007CE 74                     303 	.db #0x74	; 116	't'
      0007CF 00                     304 	.db #0x00	; 0
      0007D0 74                     305 	.db #0x74	; 116	't'
      0007D1 00                     306 	.db #0x00	; 0
      0007D2 69                     307 	.db #0x69	; 105	'i'
      0007D3 00                     308 	.db #0x00	; 0
      0007D4 66                     309 	.db #0x66	; 102	'f'
      0007D5 00                     310 	.db #0x00	; 0
                                    311 	.area CSEG    (CODE)
                                    312 	.area CONST   (CODE)
      0007D6                        313 _MyProdInfo:
      0007D6 10                     314 	.db #0x10	; 16
      0007D7 03                     315 	.db #0x03	; 3
      0007D8 52                     316 	.db #0x52	; 82	'R'
      0007D9 00                     317 	.db #0x00	; 0
      0007DA 47                     318 	.db #0x47	; 71	'G'
      0007DB 00                     319 	.db #0x00	; 0
      0007DC 42                     320 	.db #0x42	; 66	'B'
      0007DD 00                     321 	.db #0x00	; 0
      0007DE 2D                     322 	.db #0x2d	; 45
      0007DF 00                     323 	.db #0x00	; 0
      0007E0 4C                     324 	.db #0x4c	; 76	'L'
      0007E1 00                     325 	.db #0x00	; 0
      0007E2 45                     326 	.db #0x45	; 69	'E'
      0007E3 00                     327 	.db #0x00	; 0
      0007E4 44                     328 	.db #0x44	; 68	'D'
      0007E5 00                     329 	.db #0x00	; 0
                                    330 	.area CSEG    (CODE)
                                    331 	.area CONST   (CODE)
      0007E6                        332 _MyDevDescrLen:
      0007E6 12                     333 	.db #0x12	; 18
                                    334 	.area CSEG    (CODE)
                                    335 	.area CONST   (CODE)
      0007E7                        336 _MyCfgDescrLen:
      0007E7 22                     337 	.db #0x22	; 34
                                    338 	.area CSEG    (CODE)
                                    339 	.area CONST   (CODE)
      0007E8                        340 _MyLangDescrLen:
      0007E8 04                     341 	.db #0x04	; 4
                                    342 	.area CSEG    (CODE)
                                    343 	.area CONST   (CODE)
      0007E9                        344 _MyManuInfoLen:
      0007E9 0E                     345 	.db #0x0e	; 14
                                    346 	.area CSEG    (CODE)
                                    347 	.area CONST   (CODE)
      0007EA                        348 _MyProdInfoLen:
      0007EA 10                     349 	.db #0x10	; 16
                                    350 	.area CSEG    (CODE)
                                    351 	.area CONST   (CODE)
      0007EB                        352 _MyReportDescrLen:
      0007EB 15                     353 	.db #0x15	; 21
                                    354 	.area CSEG    (CODE)
                                    355 	.area XINIT   (CODE)
                                    356 	.area CABS    (ABS,CODE)
