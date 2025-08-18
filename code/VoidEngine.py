# st7789 framebuf driver for MicroPython
# VoidEngineby LP_OVER
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
        self.OptionChangeActive = False
        self.HighLightLocation = (0,0)
        self.HighLightAttr = (0,0)

    
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
            if self.OptionChange() :
                if not self.OptionChangeActive:
                    self.SelsetIndex += 1
                    if self.SelsetIndex >= len(self.ChangeableObjects):
                        self.SelsetIndex = 0
                    self.SelsetLabel = self.ChangeableObjects[self.SelsetIndex]
                self.OptionChangeActive = True
            else:
                self.OptionChangeActive = False

    def Update(self) -> None:
        OL = self.ObjectLayer
        self.display.fill(self.BackGroundColor)
        self.GUILogic()
        for i in range(len(OL) - 1, -1, -1):
            Guiobj = OL[i]
            Guiobj.Draw()
            if Guiobj == self.SelsetLabel:
                self.display.rect(Guiobj.x - 2,Guiobj.y - 2,Guiobj.w + 4,Guiobj.h + 4,0x3333)
                self.HighLightLocation = (Guiobj.x - 2,Guiobj.y - 2)
                self.HighLightAttr = (Guiobj.w + 4,Guiobj.h + 4)
        self.display.show()


gui = Screen()
tft = gui.display

# GUI LABEL CLASSES #

class Button(GUIObject):
    def __init__(self,x,y,w,h,text,bg_color,text_color,trigger):
        super().__init__(x, y, w, h, text, gui)
        self.bg_color = bg_color
        self.text_color = text_color
        self.trigger = trigger
        self.scr.RegisterChangeableObjects(self)
        self.scr.AddObject(self)
        self.active = False

    def Draw(self,scr:Screen = gui):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        scr.display.fill_round_rect(x, y, w, h, 4, self.bg_color)
        scr.display.DrawText(self.text, x + 1, y + 2, self.text_color)

    def Logic(self,scr:Screen = gui):
        if scr.OptionConfirm() and scr.SelsetLabel == self:
            if not self.active:
                self.trigger()
            self.active = True
        else:
            self.active = False




class Label(GUIObject):
    def __init__(self, x, y, w, h, text, bg_color, text_color, offset=17):
        super().__init__(x, y, w, h, text, gui, offset)
        self.scr.AddObject(self)
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
        self.scr.AddObject(self)
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
        self.scr.AddObject(self)
        self.r = h // 2
        r = self.r
        side_space = h // 10 if (h // 10) else 1
        self.circle_location_on = [x + w - side_space + r,y + r,r - side_space]
        self.circle_location_off = [x - side_space + (3 * r),y + r,r - side_space]

    def GetSwitchStatus(self) -> bool:
        return self.state

    def Draw(self,scr:Screen = gui) -> None:
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        r = self.r
        scr.display.curved_side_rect(x, y, w, h, self.bg_color if self.state else 0xaa7a)
        draw_state = self.circle_location_on if self.state else self.circle_location_off
        if self.state:
            scr.display.fill_circle(draw_state[0], draw_state[1], draw_state[2], self.color)
        else:
            scr.display.fill_circle(draw_state[0], draw_state[1], draw_state[2], self.color)

    def Logic(self,scr:Screen) -> None:
        if scr.OptionConfirm() and scr.SelsetLabel == self:
            x = self.x
            y = self.y
            w = self.w
            h = self.h
            r = self.r
            now_c = self.color if self.state else self.bg_color
            now_x = self.circle_location_on[0] if self.state else self.circle_location_off[0]
            self.state = not self.state
            draw_state = self.circle_location_on if self.state else self.circle_location_off

            B = (self.bg_color//256)*256
            G = (self.bg_color - B)//16 * 16
            R = (self.bg_color - B - G)
        
            tg_c = [B,G,R] if self.state else [0xaa00,0x0070,0x000a]
            tg_x = draw_state[0] if self.state else draw_state[0]
            for _ in range(8):
                scr.display.curved_side_rect(x, y, w, h, now_c)
                scr.display.fill_circle(now_x, draw_state[1], draw_state[2], self.color)
                now_c_B = (now_c//256)*256
                now_c_G = (now_c - now_c_B)//16 * 16
                now_c_R = (now_c - now_c_B - now_c_G)
                now_c_B = (now_c_B + (tg_c[0] - now_c_B)) // 2
                now_c_G = (now_c_G + (tg_c[1] - now_c_G)) // 2
                now_c_R = (now_c_R + (tg_c[2] - now_c_R)) // 2
                now_c = (now_c_B + now_c_G + now_c_R)
                now_x += (tg_x - now_x) // 2
                scr.display.show()