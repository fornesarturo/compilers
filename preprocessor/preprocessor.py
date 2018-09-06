'''
Process Char by Char
store space/linejump/tab as just one space

Abriendo Archivo: Nombre \n
Path: \n
salida \n
<eof>
Cerrando Archivo
'''
import time
import os


filename = input("Nombre del archivo: ")
if len(filename) == 0:
    filename = "file"

with open(filename, 'r') as f:
    print("Abriendo archivo =" + filename)
    print("Path: ", os.path.dirname(os.path.abspath(__file__)) + "/" + filename)
    can_print_whitespace = False
    whitespace_flag = False
    while True:
        c = f.read(1)
        if not c:
            print()
            break
        if c in ['\n', '\t', '\r', ' ']:
            whitespace_flag = True
        else:
            if whitespace_flag:
                if can_print_whitespace:
                    whitespace_flag = False
                    print(" ", end = "", flush = True)
                else:
                    can_print_whitespace = True
            print(c, end = "", flush = True)
        time.sleep(0.1)
    print("<EOF>")
    print("Cerrando archivo...")