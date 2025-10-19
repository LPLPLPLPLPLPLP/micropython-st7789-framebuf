# micropython-st7789-framebuf

A st7789 framebuf driver for micropython-esp32s3 ヾ(≧▽≦*)o


## Main Features

- Support RGB565 color format
- SPI Support
- Using framebuf
- Support GUI Label
- Chinese / English Text Support (Font:https://github.com/adobe-fonts/source-han-sans, Drawing Support:https://github.com/peterhinch/micropython-font-to-py/blob/master/font_to_py.py)

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

## Lite Driver

If you just want to use the basic st7789 framebuffer driver, you can go to the ./Lite/ directory to view the light driver file. This file only contains the basic functions.