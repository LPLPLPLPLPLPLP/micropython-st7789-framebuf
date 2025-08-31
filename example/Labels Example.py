from VoidEngine import *

# 基础的VoidEngine 控件使用
# Basic VoidEning Label usage

label1 = Label(0, 0, "Hello VoidEngine", 0x00F0, 0xFFFF)

gui.fill(0)
# label1会在update()内刷新在屏幕上
# label1 will be refreshed on the screen within update().
gui.update()