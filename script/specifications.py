import psutil
print(f"Загрузка CPU: {psutil.cpu_percent()}%")
print(f"Использование RAM: {psutil.virtual_memory().percent}%")