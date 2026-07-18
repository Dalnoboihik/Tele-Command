import psutil
import time
import os

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Загрузка CPU: {psutil.cpu_percent()}%')
    print(f'Использование RAM: {psutil.virtual_memory().percent}%')
    time.sleep(1)