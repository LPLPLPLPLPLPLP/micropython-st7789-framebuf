# micropython-st7789-framebuf
基于MicroPython的ST7789显示屏驱动和GUI库
[English Docs HERE!](https://github.com/LPLPLPLPLPLPLP/micropython-st7789-framebuf/blob/main/README_EN.md)
## 主要功能

- RGB565颜色格式支持
- SPI支持
- FrameBuffer支持
- GUI控件支持
- 中/英文显示 (字体来源:https://github.com/adobe-fonts/source-han-sans)

## 文件结构

```
micropython-st7789-framebuf
├── code
│   ├── st7789.py(主要显示驱动)
│   └── VoidEngine.py(GUI库)
└── font
    ├── SourceHanSans.mpy(字体文件,字体大小 20)
```

## 注意事项

1.若您使用 ```VoidEngine.py``` 作为您的驱动库，您需要修改

```VoidEngine``` Line 8 (写有CHANGE THESE SETTINGS的那一行)

来匹配您的实际设置

2.你需要在```st7789.py```的 Line 32处更改 MADCTL_MODE 常量来匹配您的显示屏设置

## 函数/类

### 显示屏驱动 (st7789.py)

#### class ST7789(framebuf.FrameBuffer)
```python
display = ST7789(width, height, spi, dc, rst, cs=None)
```
- `width`: 显示屏宽
- `height`: 显示屏高
- `spi`: SPI对象
- `dc`: 数据/命令引脚
- `rst`: 复位引脚
- `cs`: 片选引脚


· 方法:

```python
display.show()
```
在屏幕上显示FrameBuffer的内容

```python
display.invert(mode:bool)
```
反转屏幕颜色

```python
display.DrawText(x, y, text, color, offset = 17, wrap = False, w = None)
```
在屏幕上绘制文本（你必须下载字体文件SourceHanSans.mpy到你的esp32s3设备上）

- `x`: X坐标
- `y`: Y坐标
- `text`: 要绘制的文本
- `color`: 文本颜色
- `offset`: 字体偏移量
- `wrap`: 是否换行
- `w`: 文本宽度（如果文本过长，将会被切断）

```python
display.fill_round_rect(x, y, w, h, r, color)
```
在屏幕上绘制填充圆角矩形

- `x`: X坐标
- `y`: Y坐标
- `w`: 宽度
- `h`: 高度
- `r`: 圆角半径
- `color`: 颜色

### GUI库 (VoidEngine.py)

#### GUIObject(x,y,w,h,text,offset=17)

GUIObject类，所有GUI控件都继承自这个类,并且包含以下属性:

- `x`: X坐标
- `y`: Y坐标
- `w`: 控件宽度
- `h`: 控件高度
- `text`: 控件文本（绘制位置由具体控件决定）
- `offset`: 控件位移量

与以下方法：

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
from VoidEngine import Button

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
from VoidEngine import Button

tg = lambda a:a == 1

button1 = Button(tg)
while True:
    if button1.trigger():
        print("Button Pressed")
```


