from VoidEngine import *

# 在屏幕上显示Hello World
# Show "Hello World" on st7789 screen

tft.fill(0x0000)
tft.DrawText("Hello World", 0, 0, 0xFFFF)
tft.show()