import os

KeyBoard = (input("Выключить сервер? Y/N: "))

if KeyBoard == ("Y"):
    os.system("shutdown /s /t 0") 

elif KeyBoard == ("N"):
    print("Стоп")