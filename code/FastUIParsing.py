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
        in_style = False
        for i in f.readlines():
            if i == '}':
                in_style = False

            pattern_style = r'Row\((.*?)\):{'
            pattern_label = r'^([^(]+)\(([^)]+)\)'
            match_style = re.match(pattern_style, i)
            match_label = re.match(pattern_label, i)
            
            if match_style:
                RowX,RowY = match_style.group(1).split(",")
                RowX,RowY = int(RowX),int(RowY)
                print(repr(RowX), repr(RowY))

                in_style = True
            elif match_label:
                if in_style:
                    UIObject = match_label.group(1)
                    args = match_label.group(2)
                    code = f"""gui_obj = {UIObject}({RowX},{RowY},{args})\ngui_obj.Draw()
                    """
                    exec(code)
                    RowX += int(args.split(",")[0])
                else:
                    raise SyntaxError("Invalid XUP syntax")
                
        gui.show()
        f.close()
            

if __name__ == "__main__":
    with open("test.xup", "r") as file:
        parser = ParsingUI(file)
        result = asyncio.run(parser.run())
