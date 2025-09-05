# micropython-st7789-framebuf
基于MicroPython的ST7789显示屏驱动和GUI库
[English Docs HERE!](https://github.com/LPLPLPLPLPLPLP/micropython-st7789-framebuf/blob/main/README_EN.md)
## 主要功能

- 基于MicroPython的ST7789显示屏驱动
- 支持RGB565颜色格式
- SPI接口支持
- 支持FrameBuffer接口
- 附带的基础UI控件
- 中/英文显示 (字体来源:https://github.com/adobe-fonts/source-han-sans)

## 文件结构

```
micropython-st7789-framebuf
├── code
│   ├── st7789.py(主要显示驱动)
│   └── voidui.py(GUI库)
└── font
    ├── SourceHanSans.mpy(字体文件,字体大小 20)
```

## 注意事项

1.若您使用 ```voidui.py``` 作为您的驱动库，您需要修改

```voidui.py``` Line 9 (写有CHANGE THESE SETTINGS的那一行)

来匹配您的实际设置

2.你需要在```st7789.py```的 Line 32处更改 MADCTL_MODE 常量来匹配您的显示屏设置

## 详细文档介绍

[st7789.py 显示屏驱动](https://github.com/LPLPLPLPLPLPLP/micropython-st7789-framebuf/blob/main/docs/st7789-EN.md)
[voidui.py GUI库](https://github.com/LPLPLPLPLPLPLP/micropython-st7789-framebuf/blob/main/docs/voidui-EN.md)

