#ifndef __USB_DESC_H__
#define __USB_DESC_H__

#include "ch552.h"

extern UINT8C MyDevDescr[];
extern UINT8C MyCfgDescr[];
extern UINT8C MyLangDescr[];
extern UINT8C MyManuInfo[];
extern UINT8C MyProdInfo[];
extern UINT8C MyReportDescr[];

extern const UINT8 MyDevDescrLen;
extern const UINT8 MyCfgDescrLen;
extern const UINT8 MyLangDescrLen;
extern const UINT8 MyManuInfoLen;
extern const UINT8 MyProdInfoLen;
extern const UINT8 MyReportDescrLen;

/* MyCfgDescr 中 HID descriptor 的偏移，方便从 GET_DESCRIPTOR(HID) 取出 */
#define HID_DESCR_OFFSET_IN_CFG 18
#define HID_DESCR_LEN           9

#endif
