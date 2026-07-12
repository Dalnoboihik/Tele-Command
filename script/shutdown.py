import os

KeyBoard = (input("1- Выключение, 2- Перезапуск 1/2: "))

if KeyBoard == ("1"):
    os.system("shutdown /s /t 0") 

elif KeyBoard == ("2"):
    ("shutdown -r") 