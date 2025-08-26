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
#============FUNCTIONS============#
def Thumbnail(SourceFrame:framebuf.FrameBuffer, TargetWidth:int, TargetHeight:int) -> framebuf.FrameBuffer:
    src_width = SourceFrame.width
    src_height = SourceFrame.height
    
    buffer = bytearray(TargetWidth * TargetHeight * 2)
    target_fb = framebuf.FrameBuffer(buffer, TargetWidth, TargetHeight, framebuf.RGB565)
    
    scale_x = src_width / TargetWidth
    scale_y = src_height / TargetHeight
    
    for y in range(TargetHeight):
        src_y = int(y * scale_y)
        for x in range(TargetWidth):
            src_x = int(x * scale_x)
            color = SourceFrame.pixel(src_x, src_y)
            target_fb.pixel(x, y, color)
    
    return target_fb
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
        self.Refresh = True
        self.Hidden = False

    async def SpecialDrawingRules(self,scr):pass

    def SetLocation(self, x:int, y:int) -> None:
        self.x = x
        self.y = y
        self.Refresh = True
    
    def SetSize(self, w:int, h:int) -> None:
        self.w = w
        self.h = h
        self.Refresh = True

    def RemoveObject(self):
        try:
            self.scr.ObjectLayer.remove(self)
            try:
                self.scr.UnregisterChangeableObjects(self)
            except:
                pass
            self.Hidden = True
            self.Refresh = True
            asyncio.create_task(self.Draw(self.scr))
            del self
        except:
            pass

    def HideObject(self, mode:bool = True):
        self.Hidden = mode
        self.Refresh = True

    async def Draw(self, scr):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        tmp = framebuf.FrameBuffer(bytearray(w*h*2),w,h,framebuf.RGB565)
        scr.display.blit(tmp,x,y)
        if self.Hidden:
            return
        asyncio.create_task(self.SpecialDrawingRules(scr))

    def Logic(self):pass


class Screen(ST7789):
    def __init__(self):
        super().__init__(SCR_WIDTH, SCR_HEIGHT, spi, dc, rst, cs)
        self.ObjectLayer = []
        self.BackgroundColor = 0x0000
        self.display:ST7789 = super()
        self.ChangeableObjects = []
        self.Focus:GUIObject = None
        self.SelsetIndex = 0
        self.OptionConfirm = OptionConfirm
        self.OptionChange = OptionChange
        self.OptionChangeActive = False
        self.HighLightLoc = (0,0)
        self.HighLightAttr = (0,0)
        self.HighLightRefresh = True

    
    def AddObject(self, obj:GUIObject):
        self.ObjectLayer.append(obj)
    
    def SwapObjectsLayer(self, obj1:GUIObject, obj2:GUIObject) -> None:
        tmp = self.ObjectLayer.index(obj1)
        self.ObjectLayer[tmp] = obj2
        self.ObjectLayer[self.ObjectLayer.index(obj2)] = obj1

    def RegisterChangeableObjects(self,gui_obj:GUIObject) -> None:
        self.ChangeableObjects.append(gui_obj)
        if self.Focus is None:
            self.Focus = self.ChangeableObjects[0]

    def UnregisterChangeableObjects(self,gui_obj:GUIObject) -> None:
        try:
            if self.Focus == gui_obj:
                self.Focus = self.ChangeableObjects[0]
        except:
            self.Focus = None
        self.ChangeableObjects.pop(self.ChangeableObjects.index(gui_obj))

    def SetBackgroundColor(self, color:int) -> None:
        self.BackgroundColor = color

    def GUILogic(self) -> None:
        for i in self.ChangeableObjects:
            asyncio.create_task(i.Logic(self))
            if self.OptionChange() :
                if not self.OptionChangeActive:
                    GUIObj = self.Focus
                    self.display.rect(GUIObj.x-2,GUIObj.y-2,GUIObj.w+4,GUIObj.h+4,self.BackgroundColor)
                    self.SelsetIndex += 1
                    if self.SelsetIndex >= len(self.ChangeableObjects):
                        self.SelsetIndex = 0
                    self.Focus = self.ChangeableObjects[self.SelsetIndex]
                self.OptionChangeActive = True
                self.HighLightRefresh = True
            else:
                self.OptionChangeActive = False

    def Update(self) -> None:
        OL = self.ObjectLayer
        self.GUILogic()
        for i in range(len(OL) - 1, -1, -1):
            GUIObj = OL[i]
            if GUIObj.Refresh:
                asyncio.create_task(GUIObj.Draw(self))
            if GUIObj == self.Focus and self.HighLightRefresh:
                self.HighLightLoc = (GUIObj.x-2,GUIObj.y-2)
                self.HighLightAttr = (GUIObj.w+4,GUIObj.h+4)
                self.display.rect(self.HighLightLoc[0],self.HighLightLoc[1],self.HighLightAttr[0],self.HighLightAttr[1],0x3333)
                self.HighLightRefresh = False
        self.display.show()


gui = Screen()
tft = gui.display

# GUI LABEL CLASSES #

class Button(GUIObject):
    def __init__(self, x:int, y:int, text:str,
                 bg_color:int, text_color:int, trigger:function):
        
        super().__init__(x, y, gui.display.GetTextWidth(text)+4, 20, text, gui)
        self.bg_color = bg_color
        self.text_color = text_color
        self.trigger = trigger
        self.scr.RegisterChangeableObjects(self)
        self.scr.AddObject(self)
        self.active = False

    async def SpecialDrawingRules(self, scr:Screen = gui):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        scr.display.fill_round_rect(x, y, w, h, 4, self.bg_color)
        scr.display.DrawText(self.text, x + 1, y + 2, self.text_color)
        self.Refresh = False

    async def Logic(self, scr:Screen = gui):
        if scr.OptionConfirm() and scr.Focus == self:
            if not self.active:
                self.trigger()
            self.active = True
        else:
            self.active = False

class Label(GUIObject):
    def __init__(self, x:int, y:int, text:str,
                 bg_color:int, text_color:int, offset=17):
        super().__init__(x, y, gui.display.GetTextWidth(text), 20, text, gui, offset)
        self.scr.AddObject(self)
        self.bg_color = bg_color
        self.text_color = text_color

    def Update(self,text:str):
        self.text = text
        self.Refresh = True

    async def SpecialDrawingRules(self, scr:Screen = gui):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        scr.display.fill_rect(x, y, w, h, self.bg_color)
        scr.display.DrawText(self.text, x, y + 1, self.text_color, w = w)
        self.Refresh = False

class TextArea(GUIObject):
    def __init__(self, x, y, w, h, text,
                bg_color, text_color, side_color, offset = 17):
        super().__init__(x, y, w, h, gui, text, offset)
        self.scr.AddObject(self)
        self.bg_color = bg_color
        self.text_color = text_color
        self.side_color = side_color

    async def SpecialDrawingRules(self,scr:Screen = gui):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        scr.display.fill_round_rect(x, y, w, h, 4, self.bg_color)
        scr.display.fill_round_rect(x-2 ,y-2, w+4, h+4, 6, self.side_color)
        scr.display.DrawText(self.text, x, y + 1, self.text_color)
        self.Refresh = False

    def Update(self,text:str, scr:Screen = gui):
        self.text = text
        self.Refresh = True
        scr.NeedRefresh = True

class Switch(GUIObject):
    def __init__(self, x:int, y:int, w:int, h:int, bg_color:int, color:int, offset = 17):
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

    async def SpecialDrawingRules(self,scr:Screen = gui) -> None:
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        scr.display.curved_side_rect(x, y, w, h, self.bg_color if self.state else 0xaa7a)
        draw_state = self.circle_location_on if self.state else self.circle_location_off
        scr.display.fill_circle(draw_state[0], draw_state[1], draw_state[2], self.color)
        self.Refresh = True

    async def Logic(self,scr:Screen) -> None:
        if scr.OptionConfirm() and scr.Focus == self:
            x = self.x
            y = self.y
            w = self.w
            h = self.h
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
                now_c_B += (tg_c[0] - ((now_c//256)*256)) // 2
                now_c_G += (tg_c[1] - ((now_c - now_c_B)//16 * 16)) // 2
                now_c_R += (tg_c[2] - ((now_c - now_c_B - now_c_G))) // 2
                now_c = (now_c_B + now_c_G + now_c_R)
                now_x += (tg_x - now_x) // 2
                scr.display.show()
            self.Refresh = False