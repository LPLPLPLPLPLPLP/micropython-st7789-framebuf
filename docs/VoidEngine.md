# VoidEngine 文档

## 关于VoidEngine

基于st7789 framebuf的GUI控件库

## 方法

### ·  gui 方法

用法与st7789.ST7789一致

### ·  Button 类

屏幕按钮类

#### 参数

[**trigger**]传入一个函数指针，且此指针指向的函数返回布尔值，当值为**True**时，按钮触发

#### 方法
```python
Button.trigger() 
```
即传入的trigger指针，当此函数指针返回True时，屏幕按钮被触发

```python
Button.Draw(x,y,w,h,text,bg_color,text_color,offset = 17)
```
在屏幕x,y位置绘制一个按钮，长 w 像素，宽 h 像素，并在按钮上显示文字text，按钮背景颜色为 bg_color , 文字颜色为 text_color , 默认在绘制时偏移 offset像素

#### 示例

```python
from VoidEngine import *
import mpython

button1 = Button(mpython.button_a.is_pressed) #定义一个Button对象，并传入触发函数指针

gui.fill(0x0000) #清空屏幕
button1.Draw(0,0,64,24,"Hello",0xFF33,0xFFFF) #在屏幕上绘制按钮
gui.show() #向屏幕显示缓存数据

while True:
    if button1.trigger(): #当传入的函数指针被触发时
        print("Hello World!") #在控制台打印Hello World!
```

### · GUIObject 类

无实际使用，由此类继承的其他控件都具有以下属性：

```x```:此控件的屏幕x坐标
```y```:此控件的屏幕y坐标
```w```:此控件的长度
```h```:此控件的高度
```text```:控件基础文本 显示位置由实际控件决定
```offset```:此控件绘制时偏移量

### · TextArea 类

继承自GUIObject()，文本框类

#### 参数

```x```:文本框的屏幕x坐标
```y```:文本框的屏幕y坐标
```w```:文本框的长度
```h```:文本框的高度
```text```:文本框基础文本
```bg_color```:文本框背景颜色
```text_color```:文本框文字颜色
```side_color```:文本框边框颜色
```offset```:文本框绘制时偏移量

#### 方法

```python
TextArea.Draw()
```

绘制文本框

```python
TextArea.Update(text)
```

更新文本框内容

#### 示例

```python
from VoidEngine import *
import mpython

text_area1 = TextArea(0,0,128,64,"Hello",0x0000,0xFFFF,0xFFFF,17) #定义一个TextArea对象

gui.fill(0x0000) #清空屏幕
text_area1.Draw() #在屏幕上绘制文本框
gui.show() #向屏幕显示缓存数据

while True:
    if mpython.button_a.is_pressed(): #当按下按钮A时
        text_area1.Update("Hello World!") #更新文本框内容
        gui.show() #向屏幕显示缓存数据
```
