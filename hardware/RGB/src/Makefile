## CH552 USB-LED — SDCC Makefile
## 用法:
##   make             编译，产物 build/RGB.ihx (+ .hex)
##   make flash       通过 wchisp 烧录
##   make clean

TARGET   := RGB
BUILD    := build

CC       := sdcc
PACKIHX  := packihx
WCHISP   := wchisp

# CH552 8 KB flash / 256 B iram / 1 KB xram
# 0x0000..0x00BF 已被端点 DMA 缓冲占用 (见 usb_isr.c 中的 __at 声明),
# 普通 xdata 变量从 0x00C0 起。
MCU_FLAGS := -mmcs51 \
             --model-small \
             --xram-loc 0x00C0 --xram-size 0x0340 \
             --code-size 0x3800

CFLAGS   := $(MCU_FLAGS) -I.
LDFLAGS  := $(MCU_FLAGS)

SRCS     := main.c sys.c usb_desc.c usb_isr.c
RELS     := $(SRCS:%.c=$(BUILD)/%.rel)

.PHONY: all flash clean
all: $(BUILD)/$(TARGET).hex

$(BUILD):
	@mkdir -p $(BUILD)

$(BUILD)/%.rel: %.c | $(BUILD)
	$(CC) -c $(CFLAGS) -o $@ $<

$(BUILD)/$(TARGET).ihx: $(RELS)
	$(CC) $(LDFLAGS) -o $@ $^

$(BUILD)/$(TARGET).hex: $(BUILD)/$(TARGET).ihx
	$(PACKIHX) $< > $@

flash: $(BUILD)/$(TARGET).hex
	$(WCHISP) flash $<

clean:
	rm -rf $(BUILD)
