/********************************************************************
 * usb_desc.c — HID 设备描述符
 * 厂商定义页 HID，输出一个 1 字节的 Output Report 控制 3 个 LED。
 * Windows / Linux / macOS 全部走系统内置 HID 驱动，无需任何安装。
 ********************************************************************/
#include "ch552.h"
#include "usb_config.h"
#include "usb_desc.h"

#define THIS_ENDP0_SIZE     DEFAULT_ENDP0_SIZE
#define ENDP1_IN_SIZE       8

/*--------- HID Report Descriptor ----------
 * Usage Page: Vendor Defined (0xFF00)
 * Usage 1   : Application Collection
 * Usage 2   : Output, 1 byte
 *   bits[1:0] = LED0 state, [3:2] = LED1, [5:4] = LED2
 *   每路：0=灭, 1=亮, 2=呼吸
 */
UINT8C MyReportDescr[] = {
    0x06, 0x00, 0xFF,
    0x09, 0x01,
    0xA1, 0x01,
        0x09, 0x02,
        0x15, 0x00,
        0x26, 0xFF, 0x00,
        0x75, 0x08,
        0x95, 0x01,
        0x91, 0x02,
    0xC0
};

/*--------- 设备描述符 ----------*/
UINT8C MyDevDescr[] = {
    0x12, 0x01, 0x10, 0x01,
    0x00, 0x00, 0x00, THIS_ENDP0_SIZE,  /* class 由 interface 指定 */
    USB_VID_L, USB_VID_H,
    USB_PID_L, USB_PID_H,
    0x00, 0x10,                          /* bcdDevice = 0x1000 */
    0x01, 0x02, 0x00,
    0x01
};

/*--------- 配置 + HID 接口 + Interrupt IN ----------
 *  9 (config) + 9 (interface) + 9 (HID) + 7 (endpoint) = 34
 */
#define HID_REPORT_DESCR_LEN 21  /* sizeof(MyReportDescr); 必须为常量 */

UINT8C MyCfgDescr[] = {
    /* Configuration */
    0x09, 0x02, 34, 0x00, 0x01, 0x01, 0x00, 0x80, 0x32,
    /* Interface 0 : HID, 1 endpoint */
    0x09, 0x04, 0x00, 0x00, 0x01, 0x03, 0x00, 0x00, 0x00,
    /* HID descriptor */
    0x09, 0x21, 0x11, 0x01, 0x00, 0x01, 0x22,
        HID_REPORT_DESCR_LEN, 0x00,
    /* Endpoint 1 IN, Interrupt, max packet 8, 10 ms */
    0x07, 0x05, 0x81, 0x03, ENDP1_IN_SIZE, 0x00, 0x0A
};

UINT8C MyLangDescr[] = { 0x04, 0x03, 0x09, 0x04 };

UINT8C MyManuInfo[] = { USB_VENDOR_STR_LEN,  0x03, USB_VENDOR_STR  };
UINT8C MyProdInfo[] = { USB_PRODUCT_STR_LEN, 0x03, USB_PRODUCT_STR };

const UINT8 MyDevDescrLen     = sizeof(MyDevDescr);
const UINT8 MyCfgDescrLen     = sizeof(MyCfgDescr);
const UINT8 MyLangDescrLen    = sizeof(MyLangDescr);
const UINT8 MyManuInfoLen     = sizeof(MyManuInfo);
const UINT8 MyProdInfoLen     = sizeof(MyProdInfo);
const UINT8 MyReportDescrLen  = sizeof(MyReportDescr);
