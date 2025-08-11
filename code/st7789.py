# st7789 framebuf driver for MicroPython
# by LP_OVER
# LICENCE: GPL v3.0
from machine import Pin,SPI
from micropython import const
import SourceHanSans as font_20
import framebuf
import time
# ST7789命令定义 / ST7789 COMMAND DEFINITION
ST7789_NOP = 0x00
ST7789_SWRESET = 0x01
ST7789_SLPIN = 0x10
ST7789_SLPOUT = 0x11
ST7789_NORON = 0x13
ST7789_INVOFF = 0x20
ST7789_INVON = 0x21
ST7789_DISPON = 0x29
ST7789_CASET = 0x2A
ST7789_RASET = 0x2B
ST7789_RAMWR = 0x2C
ST7789_MADCTL = 0x36
ST7789_COLMOD = 0x3A

# 颜色模式/COLOR MODE
COLOR_MODE_16BIT = 0b00011101

# 屏幕方向控制
MADCTL_MY  = const(0b10000000)  # 行地址顺序 / ROW ADDRESS ORDER
MADCTL_MX  = const(0b01000000)  # 列地址顺序 / COLUMN ADDRESS ORDER
MADCTL_MV  = const(0b00100000)  # 行列交换   / SWAP ROW/COLUMN
MADCTL_ML  = const(0b00010000)  # 左右交换   / SWAP LEFT/RIGHT
MADCTL_MODE = MADCTL_MY | MADCTL_MV | 0b00001010
class ST7789(framebuf.FrameBuffer):
    def __init__(self, width, height, spi, dc, rst, cs=None):
        self.width = width
        self.height = height
        self.spi = spi
        self.dc = dc
        self.rst = rst
        self.cs = cs
        # INIT CONTROL PINS
        # 初始化控制引脚
        dc.init(dc.OUT, value=0)
        rst.init(rst.OUT, value=1)
        if cs:
            cs.init(cs.OUT, value=1)
        # INIT DISPLAY
        # 初始化屏幕
        self.reset()
        self._init_display()
        # CREATE FRAMEBUF
        # 创建帧缓冲区
        self.buffer = bytearray(self.width * self.height * 2)
        # INIT FRAMEBUF
        # 初始化FrameBuffer (RGB565格式)
        self.fbuf = super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        # OPEN BACKLIGHT
        # 开启背光
        self.bl = Pin(45, Pin.OUT)  # 根据实际连接修改引脚
        self.bl(1)
        # 设置全屏窗口 / SET FULL SCREEN WINDOW
        self.init_window(0, 0, self.width - 1, self.height - 1)
        # CLEAR SCREEN
        # 清屏并显示
        self.fill(0)
        self.show()

    def reset(self):
        self.rst(0)
        time.sleep_ms(50)
        self.rst(1)
        time.sleep_ms(150)
    
    def write_cmd(self, cmd):
        self.cs(0)
        self.dc(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
    
    def write_data(self, buf):
        self.cs(0)
        self.dc(1)
        self.spi.write(buf)
        self.cs(1)
    
    def _init_display(self):
        # 初始化序列 / INITIALIZATION SEQUENCE
        init_cmds = [
            (ST7789_SWRESET,None),                          # 软件复位 / SOFTWARE RESET
            (ST7789_SLPOUT,None),                           # 退出睡眠模式 / EXIT SLEEP MODE
            (ST7789_COLMOD,bytearray([COLOR_MODE_16BIT])),  # 设置颜色模式 (16位RGB565) / SET COLOR MODE (16BIT RGB565)
            (ST7789_INVOFF,None),                           # 关闭反色显示 / INVERT OFF
            (ST7789_NORON,None),                            # 正常显示模式 / NORMAL DISPLAY MODE
            (ST7789_DISPON,None),                           # 开启显示 / DISPLAY ON
            (ST7789_MADCTL,bytearray([MADCTL_MODE]))               # 设置屏幕方向 / SET SCREEN ORIENTATION
        ]
        
        for cmd, data in init_cmds:
            self.write_cmd(cmd)
            if data:
                self.write_data(data)
            time.sleep_ms(100)
    def init_window(self, x0, y0, x1, y1):
        # 设置列地址范围 / SET COLUMN ADDRESS RANGE
        self.write_cmd(ST7789_CASET)
        self.write_data(bytearray([
            x0 >> 8, x0 & 0xFF, 
            x1 >> 8, x1 & 0xFF
        ]))
        
        # 设置行地址范围 / SET ROW ADDRESS RANGE
        self.write_cmd(ST7789_RASET)
        self.write_data(bytearray([
            y0 >> 8, y0 & 0xFF, 
            y1 >> 8, y1 & 0xFF
        ]))

    def set_window(self):
        # 准备写入显示数据 / PREPARE TO WRITE DISPLAY DATA
        self.write_cmd(ST7789_RAMWR)
        
    def invert(self,mode:bool):
        self.write_cmd(ST7789_INVON if mode else ST7789_INVOFF)
    
    def DrawText(self, text, x, y, color, offset=17, wrap=False, w = None, buffer = None):
        orig_x = x + offset 
        curr_x = orig_x
        curr_y = y
        if buffer is None:
            fbuf = super()
        else:
            fbuf = buffer
        get_ch = font_20.get_ch
        memviews = b''
        total_width = 0
        for char in text:
            if char == " ":
                curr_x += 12
                continue
            elif char == '\n' and wrap:
                curr_x = orig_x
                curr_y += 20
                continue
            mv, height, width = get_ch(char)
            memviews += mv
            row_bytes = (width + 7) // 8
            for ny in range(height):
                row_start = ny * row_bytes
                for nx in range(width):
                    byte_idx = row_start + (nx // 8)
                    bit_mask = 1 << (7 - (nx % 8))
                    if mv[byte_idx] & bit_mask:
                        fbuf.pixel(curr_x + nx, curr_y + ny, color)
            curr_x += width
            total_width += width
            if w is not None and total_width + 20 > w:
                return memviews,total_width,20
            if wrap and curr_x >= 300:
                curr_x = orig_x
                curr_y += 20
        return memviews,total_width,20
    
    
    def fill_round_rect(self, x, y, w, h, r, color):
        # Draw a filled rounded rectangle
        # 绘制填充圆角矩形
        self.fill_circle(x + r, y + r, r, color)
        self.fill_circle(x + w - r, y + r, r, color)
        self.fill_rect(x + r, y, w - (2 * r), h + 1, color)
        self.fill_circle(x + r, y + h - r, r, color)
        self.fill_circle(x + w - r, y + h - r, r, color)
        self.fill_rect(x, y + r, w + 1, h - (2 * r), color)

    def show(self):
        self.set_window()
        if self.cs:
            self.cs(0)
        self.dc(1)
        # 填充未使用缓冲区(可选)
        # FILL UNUSED BUFFER (OPTIONAL).IF YOU FOUND THAT THE DISPLAY IS NOT WORKING PROPERLY, YOU CAN TRY THIS.
        for _ in range(70):
            self.spi.write(bytearray(320))
        #写入有效数据 WRITE VALID DATA
        self.spi.write(self.buffer)
        if self.cs:
            self.cs(1)
