import asyncio,framebuf
class GUIObject:
    def __init__(self, x, y, w, h, text, scr, offset = 0):
        self.x = x + offset
        self.y = y
        self.w = w
        self.h = h
        self.r = w
        self.text = text
        self.scr = scr
        self.Refresh = True

    def SpecialDrawingRules(self,scr):pass

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

    def Draw(self, scr):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        tmp = framebuf.FrameBuffer(bytearray(w*h*2),w,h,framebuf.RGB565)
        scr.display.blit(tmp,x,y)
        self.SpecialDrawingRules(scr)
    def Logic(self):pass

