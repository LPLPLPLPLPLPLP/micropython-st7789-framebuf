# st7789 framebuf driver for MicroPython
# by LP_OVER
# LICENCE: GPL v3.0
from st7789 import ST7789
from machine import SPI,Pin
import framebuf
from micropython import const
import asyncio
import time
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
    

async def refresh_timer(t):#t (sec)
    tft.show()
    while True:
        await asyncio.sleep(t)
        tft.show()
#=======GUI SETTINGS=====#
OptionConfirm = None
OptionChange = None
#=======GUI BASIC CLASSES======#
class GUIObject:
    def __init__(self, x, y, w, h, text, scr, offset = 17):
        self.x = x + offset
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.scr = scr


    def Draw(self):pass

    def Logic(self):pass


class Screen(ST7789):
    def __init__(self):
        super().__init__(SCR_WIDTH, SCR_HEIGHT, spi, dc, rst, cs)
        self.ObjectLayer = []
        self.BackGroundColor = 0x0000
        self.display:ST7789 = super()
        self.ChangeableObjects = []
        self.SelsetLabel:GUIObject = None
        self.SelsetIndex = 0
        self.OptionConfirm = OptionConfirm
        self.OptionChange = OptionChange

    
    def AddObject(self, obj:GUIObject):
        self.ObjectLayer.append(obj)
    
    def SwapObjectsLayer(self, obj1:GUIObject, obj2:GUIObject) -> None:
        tmp = self.ObjectLayer.index(obj1)
        self.ObjectLayer[tmp] = obj2
        self.ObjectLayer[self.ObjectLayer.index(obj2)] = obj1

    def RegisterChangeableObjects(self,gui_obj:GUIObject) -> None:
        self.ChangeableObjects.append(gui_obj)
        if self.SelsetLabel is None:
            self.SelsetLabel = self.ChangeableObjects[0]

    def UnregisterChangeableObjects(self,gui_obj:GUIObject) -> None:
        try:
            if self.SelsetLabel == gui_obj:
                self.SelsetLabel = self.ChangeableObjects[0]
        except:
            self.SelsetLabel = None
        self.ChangeableObjects.pop(self.ChangeableObjects.index(gui_obj))

    def SetBackGroundColor(self, color:int) -> None:
        self.BackGroundColor = color

    def GUILogic(self) -> None:
        for i in self.ChangeableObjects:
            i.Logic(self)
            if self.OptionChange():
                self.SelsetIndex += 1
                if self.SelsetIndex >= len(self.ChangeableObjects) - 1:
                    self.SelsetIndex = 0

                self.SelsetLabel = self.ChangeableObjects[self.SelsetIndex]

    def Update(self) -> None:
        OL = self.ObjectLayer
        self.display.fill(self.BackGroundColor)
        for i in range(len(OL) - 1, -1, -1):
            OL[i].Draw()
        self.display.show()


gui = Screen()
tft = gui.display

# GUI LABEL CLASSES #

class Button(GUIObject):
    def __init__(self,x,y,w,h,text,bg_color,text_color,trigger):
        super().__init__(x, y, w, h, gui, text)
        self.bg_color = bg_color
        self.text_color = text_color
        self.trigger = trigger
        self.scr.RegisterChangeableObjects(self)
    def Draw(self,scr:Screen = gui):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        offset = 17
        scr.display.fill_round_rect(x+offset, y, w, h, 4, self.bg_color)
        scr.display.DrawText(self.text, x + 1, y + 2, self.text_color)

    def Logic(self,scr:Screen = gui):
        if scr.OptionConfirm() and scr.SelsetLabel == self:
            self.trigger()


class Label(GUIObject):
    def __init__(self, x, y, w, h, text, bg_color, text_color, offset=17):
        super().__init__(x, y, w, h, text, gui, offset)
        self.bg_color = bg_color
        self.text_color = text_color

    def Update(self,text:str,scr:Screen = gui):
        self.text = text
        scr.display.fill_rect(self.x, self.y, self.w, self.h, self.bg_color)
        scr.display.DrawText(self.text, self.x, self.y + 1, self.text_color, w = self.w)


    def Draw(self,scr:Screen = gui):
        scr.display.fill_rect(self.x, self.y, self.w, self.h, self.bg_color)
        scr.display.DrawText(self.text, self.x, self.y + 1, self.text_color, w = self.w)

class TextArea(GUIObject):
    def __init__(self, x, y, w, h, text,
                bg_color, text_color, side_color, offset = 17):
        super().__init__(x, y, w, h, gui, text, offset)
        self.bg_color = bg_color
        self.text_color = text_color
        self.side_color = side_color

    def Draw(self,scr:Screen = gui):
        scr.display.fill_round_rect(self.x, self.y, self.w, self.h, 4, self.bg_color)
        scr.display.fill_round_rect(self.x - 1 ,self.y - 1, self.w + 2, self.h + 2, 6, self.side_color)
        scr.display.DrawText(self.text, self.x, self.y + 1, self.text_color)

    def Update(self,text:str, scr:Screen = gui):
        self.text = text
        scr.display.fill_round_rect(self.x, self.y, self.w, self.h, 4, self.bg_color)
        scr.display.fill_round_rect(self.x - 1 ,self.y - 1, self.w + 2, self.h + 2, 6, self.side_color)
        scr.display.DrawText(self.text, self.x, self.y + 1, self.text_color)

class Switch(GUIObject):
    def __init__(self, x, y, w, h, bg_color, color, offset = 17):
        super().__init__(x, y, w, h, "", gui, offset)
        self.bg_color = bg_color
        self.color = color
        self.state = False
        self.scr.RegisterChangeableObjects(self)
        self.r = h // 2
        r = self.r
        side_space = h // 10 if (h // 10) else 1
        self.circle_location_on = [x + w - r - 1,y + r,r - side_space]
        self.circle_location_off = [x + r - 1,y + r,r - side_space]


    def GetSwitchStatus(self) -> bool:
        return self.state

    def Draw(self,scr:Screen = gui) -> None:
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        r = self.r
        tft.curved_side_rect(x - (2 * r), y, w, h, self.bg_color if self.state else 0xaa7a)
        draw_state = self.circle_location_on if self.state else self.circle_location_off
        if self.state:
            scr.display.fill_circle(draw_state[0], draw_state[1], draw_state[2], self.color)
        else:
            scr.display.fill_circle(draw_state[0], draw_state[1], draw_state[2], self.color)

    def Logic(self,scr:Screen) -> None:
        if scr.OptionConfirm() and scr.SelsetLabel == self:
            self.state = not self.state
            time.sleep(0.1)
