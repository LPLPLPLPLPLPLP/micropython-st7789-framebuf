# VoidUI

## 控件概念
```
Screen(控件显示、事件处理在此类进行管理)
|
├──GUIObject(全部控件的基类，包含控件的基本属性和方法)
    |
    ├──不可变控件(Label()等类，这些类不会影响到或者触发某些事件)
    |
    └──可变控件(Button()等类，这些类会改变某些变量或触发某些事件)
```

## 函数/类

### Thumbnail

```python
def Thumbnail(SourceFrame:framebuf.FrameBuffer, TargetWidth:int, TargetHeight:int) -> framebuf.FrameBuffer:
```

缩略图函数，通过传入一个FrameBuffer来输出最终压缩后的FrameBuffer

- `SourceFrame` 原FrameBuffer
- `TargetWidth` 目标宽度
- `TargetHeight` 目标高度

返回值：
- `TargetFrame` 目标FrameBuffer

### GUIObject

#### 参数

```python
class GUIObject:
    def __init__(self, x, y, w, h, text, scr, offset = 0):
```

GUIObject类，为所有GUI控件的基类，包含以下属性:

- `x`: X坐标
- `y`: Y坐标
- `w`: 控件宽度
- `h`: 控件高度
- `text`: 控件文本（绘制位置由具体控件决定）
- `scr`: 控件所在的Screen对象
- `offset`: 控件位移量


#### 方法

```python
GUIObject.SetLocation(self, x:int, y:int)
```

设置控件位置

```python
GUIObject.SetSize(self, w:int, h:int)
```
设置控件大小

```python
GUIObject.RemoveObject(self)
```
删除控件

```python
GUIObject.Draw(display)
```
在屏幕上绘制控件

#### class Label(GUIObject)

Label类，继承自GUIObject，用于绘制文本标签

init:
```python
label1 = Label(x, y, w, h, text, bg_color, text_color, offset=17)
```
- `bg_color`: 背景颜色
- `text_color`: 文本颜色

#### class Button(GUIObject)

初始化：
```python
from voidui import Button

tg = lambda a:a == 1

button1 = Button(x,y,w,h,text,bg_color,text_color,tg)
```

方法：

```python
button1.trigger()
```
当tg为True时，按钮被触发。

示例：
```python
from voidui import Button

tg = lambda a:a == 1

button1 = Button(tg)
while True:
    if button1.trigger():
        print("Button Pressed")
```
