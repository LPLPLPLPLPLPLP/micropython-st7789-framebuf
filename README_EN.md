# micropython-st7789-framebuf
A st7789 framebuf driver for micropython-esp32s3

## Main Features

- Support RGB565 color format
- SPI Support
- Using framebuf
- Support GUI Label
- Chinese / English Font Support (Font:https://github.com/adobe-fonts/source-han-sans)

## File Structure

```
micropython-st7789-framebuf
├── code
│   ├── st7789.py(Display driver)
│   └── VoidEngine.py(GUI Library)
└── font
    ├── SourceHanSans.mpy(Font file,size 20)
```

## Warning

1. If you use `VoidEngine.py` as your driver library, you need to modify

```VoidEngine``` Settings under Line 8(the line with CHANGE THESE SETTINGS)

2. You need to change `MADCTL_MODE` constant in `st7789.py` Line 32 to match your display settings
## Functions/Classes

### Display Driver (st7789.py)

#### class ST7789(framebuf.FrameBuffer)
```python
display = ST7789(width, height, spi, dc, rst, cs=None)
```
- `width`: Display width
- `height`: Display height
- `spi`: SPI object
- `dc`: DC pin
- `rst`: RST pin
- `cs`: CS pin

· Methods:

```python
display.show()
```
Write framebuf to the display

```python
display.invert(mode:bool)
```
Invert display color

```python
display.DrawText(x, y, text, color, offset = 17, wrap = False, w = None)
```
Draw text on the display(You must download fonts/SourceHanSans.mpy in your esp32s3 device)

- `x`: X coordinate
- `y`: Y coordinate
- `text`: Text to be drawn
- `color`: Text color
- `offset`: Offset of the font
- `wrap`: Whether to wrap the text
- `w`: Width of the text(if the letter are too long, it will be cut off)

```python
display.fill_round_rect(x, y, w, h, r, color)
```
Draw a round rectangle on the display

- `x`: X coordinate
- `y`: Y coordinate
- `w`: Width of the rectangle
- `h`: Height of the rectangle
- `r`: Radius of the rectangle
- `color`: Color of the rectangle

### GUI Library (VoidEngine.py)

#### GUIObject(x,y,w,h,text,offset=17)

Basic GUI class , If a Label inherits from this class, it always have these attributes:

- `x`: X coordinate
- `y`: Y coordinate
- `w`: Width of the label
- `h`: Height of the label
- `text`: Text of the label
- `offset`: Offset of the font

and this method:

```python
GUIObject.Draw(display)
```
Draw the label on the display

#### class Label(GUIObject)

Label class, inherits from GUIObject

init:
```python
label1 = Label(x, y, w, h, text, bg_color, text_color, offset=17)
```
- `bg_color`: Background color of the label
- `text_color`: Text color of the label

#### class Button(trigger)
Warning: This class is not inherited from GUIObject.

init:
```python
from VoidEngine import Button
from machine import Pin
button1 = Button(Pin(0).value)
```

Methods:

```python
button1.trigger()
```
Return True if the "trigger" is True

For example:
```python
from VoidEngine import Button

tg = lambda a:a == 1

button1 = Button(tg)
while True:
    if button1.trigger():
        print("Button Pressed")
```

