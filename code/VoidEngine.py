# st7789 framebuf driver for MicroPython
# by LP_OVER
# LICENCE: GPL v3.0
from st7789 import ST7789
from machine import SPI,Pin
import framebuf
from micropython import const
import asyncio
#======CHANGE THESE SETTINGS========#
TFT_RST_PIN = const(0)  # Pin RST
TFT_LED_PIN = const(12) 
TFT_DC_PIN = const(35)  # Pin DC
TFT_CS_PIN = const(34)  # Pin CS
TFT_CLK_PIN = const(36) # Pin Clock
TFT_MISO_PIN = const(2) 
TFT_MOSI_PIN = const(37)

SCR_WIDTH = const(320)
SCR_HEIGHT = const(206)
#===================================#
spi = SPI(2,
                baudrate=80000000,
                polarity=0,
                phase=0,
                sck=Pin(TFT_CLK_PIN),
                mosi=Pin(TFT_MOSI_PIN),
                miso=Pin(TFT_MISO_PIN))

dc = Pin(TFT_DC_PIN,Pin.OUT)
cs = Pin(TFT_CS_PIN,Pin.OUT)
rst= Pin(TFT_RST_PIN,Pin.OUT)
    
gui = ST7789(SCR_WIDTH, SCR_HEIGHT, spi, dc, rst, cs)

async def refresh_timer(t):#t (sec)
    gui.show()
    while True:
        await asyncio.sleep(t)
        gui.show()
#=======GUI CLASSES======#
class GUIObject:
    def __init__(self,x,y,w,h,text,offset = 17):
        self.x = x + offset
        self.y = y
        self.w = w
        self.h = h
        self.text = text

    def Draw():pass
        
class Button:# It doesn't belong to GUIObject/不属于GUIObject
    def __init__(self,trigger):
        self.trigger = trigger

    def Draw(self,x,y,w,h,text,bg_color,text_color,offset = 17):
        gui.fill_round_rect(x+offset, y, w, h, 4, bg_color)
        gui.DrawText(text, x + 1, y + 2, text_color)

class Label(GUIObject):
    def __init__(self,x,y,w,h,text,bg_color,text_color,offset=17):
        super().__init__(x,y,w,h,text,offset)
        self.bg_color = bg_color
        self.text_color = text_color

    def Draw(self):
        gui.fill_rect(self.x, self.y, self.w, self.h, self.bg_color)
        gui.DrawText(self.text, self.x, self.y + 1, self.text_color, w = self.w)

class TextArea(GUIObject):
    def __init__(self,x,y,w,h,text,bg_color,text_color,side_color,offset = 17):
        super().__init__(x,y,w,h,text,offset)
        self.bg_color = bg_color
        self.text_color = text_color
        self.side_color = side_color

    def Draw(self):
        gui.fill_round_rect(self.x, self.y, self.w, self.h, 4, self.bg_color)
        gui.fill_round_rect(self.x - 1 ,self.y - 1, self.w + 2, self.h + 2, 6, self.side_color)
        gui.DrawText(self.text, self.x, self.y + 1, self.text_color)

    def Update(self,text):
        self.text = text
        gui.fill_round_rect(self.x, self.y, self.w, self.h, 4, self.bg_color)
        gui.fill_round_rect(self.x - 1 ,self.y - 1, self.w + 2, self.h + 2, 6, self.side_color)
        gui.DrawText(self.text, self.x, self.y + 1, self.text_color)
