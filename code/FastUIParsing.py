from VoidEngine import *
import io,re
import asyncio
class ParsingUI:
    def __init__(self,_file:io.TextIOWrapper):
        _file.seek(0)
        self._file = _file

    async def run(self):
        f = self._file
        row = 0
        for i in f.readlines():
            ui_object = "text"
            args = "x=0,y={},color=0xFFFF".format(row*20)
            pattern = r'^<([^>]*)>([^<]*)<([^>]*)>\[(\d+)\]$'
            pattern_2 = r'^<([^>]*)>([^<]*)<([^>]*)>'
            match = re.match(pattern, i)
            if match:
                ui_object = match.group(1)
                s = match.group(2)
                args = match.group(3)
                num = int(match.group(4))  # 转换为整数
                print((ui_object, s, args, num))
            else:
                match_2 = re.match(pattern_2, i)
                if match_2:
                    ui_object = match_2.group(1)
                    s = match_2.group(2)
                    args = match_2.group(3)
                    print((ui_object, s, args))
                else:
                    s = i
                    print((ui_object,s))
            ui_object = ui_object.replace("text","DrawText")
            command = """gui.{}('''{}''',{})""".format(ui_object,s,args)
            print(command)
            eval(command,{"gui":gui})
            if ui_object == "DrawText":
                row += 1
        gui.show()
        f.close()

if __name__ == "__main__":
    with open("test.xup", "r") as file:
        parser = ParsingUI(file)
        result = asyncio.run(parser.run())
