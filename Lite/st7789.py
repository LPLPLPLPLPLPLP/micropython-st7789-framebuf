# st7789 framebuf driver for MicroPython
# by LP_OVER
# LICENCE: GPL v3.0
from machine import Pin,SPI
from micropython import const
import framebuf
import time
# ST7789命令定义 / ST7789 COMMAND DEFINITION
ST7789_SWRESET = const(0x01)
ST7789_SLPOUT = const(0x11)
ST7789_NORON = const(0x13)
ST7789_INVOFF = const(0x20)
ST7789_INVON = const(0x21)
ST7789_DISPON = const(0x29)
ST7789_CASET = const(0x2A)
ST7789_RASET = const(0x2B)
ST7789_RAMWR = const(0x2C)
ST7789_MADCTL = const(0x36)
ST7789_COLMOD = const(0x3A)

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
        dc.init(dc.OUT, value=0)
        rst.init(rst.OUT, value=1)
        if cs:
            cs.init(cs.OUT, value=1)
        # INIT DISPLAY
        # 初始化屏幕
        self.reset()

        # 初始化序列 / INITIALIZATION SEQUENCE
        init_cmds = [
            (ST7789_SWRESET,None),                          # 软件复位 / SOFTWARE RESET
            (ST7789_SLPOUT,None),                           # 退出睡眠模式 / EXIT SLEEP MODE
            (ST7789_COLMOD,bytearray([COLOR_MODE_16BIT])),  # 设置颜色模式 (16位RGB565) / SET COLOR MODE (16BIT RGB565)
            (ST7789_INVOFF,None),                           # 关闭反色显示 / INVERT OFF
            (ST7789_NORON,None),                            # 正常显示模式 / NORMAL DISPLAY MODE
            (ST7789_DISPON,None),                           # 开启显示 / DISPLAY ON
            (ST7789_MADCTL,bytearray([MADCTL_MODE]))        # 设置屏幕方向 / SET SCREEN ORIENTATION
        ]
        
        for cmd, data in init_cmds:
            self.write_cmd(cmd)
            if data:
                self.write_data(data)
            time.sleep_ms(100)

        # CREATE FRAMEBUF
        # 创建帧缓冲区
        self.buffer = bytearray(self.width * self.height * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        # OPEN BACKLIGHT
        # 开启背光
        self.bl = Pin(45, Pin.OUT)  # 根据实际连接修改引脚
        self.bl(1)
        self.init_window(0, 0, self.width - 1, self.height - 1)
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
    
    def init_window(self, x0:int, y0:int, x1:int, y1:int) -> None:
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
        
    def show(self):
        self.write_cmd(ST7789_RAMWR)
        if self.cs:
            self.cs(0)
        self.dc(1)
        self.spi.write(self.buffer)
        if self.cs:
            self.cs(1)