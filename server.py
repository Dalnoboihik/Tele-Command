from HardView.LiveView import PyTempCpu
import http.server
import socketserver
import subprocess
import psutil
import platform
import json
import winreg 

PORT = 3000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open('index.html', 'r', encoding='utf-8') as file:
                    html_template = file.read()

                cpu = psutil.cpu_percent()
                ram = psutil.virtual_memory()
                
                cpu_temp = PyTempCpu()
                temp = cpu_temp.get_temp()
                
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                    infoCPU = winreg.QueryValueEx(key, "ProcessorNameString")[0]
                except:
                    infoCPU = platform.processor() or "Неизвестно"
                
                infoRAM = round(psutil.virtual_memory().total / (1024**3), 2)

                html = html_template.replace('{CPU}', str(cpu))
                html = html.replace('{RAM}', str(ram.percent))
                html = html.replace('{infoCPU}', infoCPU)  
                html = html.replace('{infoRAM}', str(infoRAM))  
                html = html.replace('{temp:.1f}', str(temp)) 

                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("Файл index.html не найден".encode('utf-8'))
        elif self.path == "/api/cpu":
            cpu = psutil.cpu_percent()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(cpu).encode('utf-8'))
        elif self.path == "/api/ram":
            ram = psutil.virtual_memory()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(ram.percent).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("404 - Страница не найдена".encode('utf-8'))

    def do_POST(self):
        if self.path == "/run_bat":
            subprocess.Popen(["cmd", "/c", "Clean.bat"])
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("BAT файл успешно запущен через POST".encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("404 - Не найдено".encode('utf-8'))

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Сервер запущен на порту {PORT}")
    httpd.serve_forever()