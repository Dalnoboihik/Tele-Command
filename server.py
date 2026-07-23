import http.server
import socketserver
import subprocess
import psutil
import platform
import json
import winreg
import threading
import time
import random
from urllib.parse import urlparse, parse_qs
from datetime import datetime

PORT = 3000

class SystemLogger:
    def __init__(self):
        self.history = []
        self.max_cpu = 0
        self.max_ram = 0
        self.lock = threading.Lock()
        
    def add_record(self, cpu, ram):
        with self.lock:
            record = {
                'time': datetime.now().isoformat(),
                'cpu': round(cpu, 1),
                'ram': round(ram, 1)
            }
            self.history.append(record)
            if len(self.history) > 1000:
                self.history.pop(0)
            
            if cpu > self.max_cpu:
                self.max_cpu = cpu
            if ram > self.max_ram:
                self.max_ram = ram
    
    def get_recent_stats(self, count=100):
        with self.lock:
            return self.history[-count:] if self.history else []
    
    def get_max_values(self):
        with self.lock:
            return {
                'max_cpu': round(self.max_cpu, 1),
                'max_ram': round(self.max_ram, 1)
            }

system_logger = SystemLogger()

def background_logging():
    while True:
        try:
            base_cpu = psutil.cpu_percent(interval=0.5)
            cpu = max(0, min(100, base_cpu + random.uniform(-3, 3)))
            ram = psutil.virtual_memory().percent
            system_logger.add_record(cpu, ram)
        except Exception as e:
            print(f"Ошибка сбора данных: {e}")
        time.sleep(10)

class MyHandler(http.server.BaseHTTPRequestHandler):
    
    def is_authenticated(self):
        cookies = self.headers.get('Cookie', '')
        return 'session=authenticated' in cookies
    
    def serve_login_page(self):
        try:
            with open('login.html', 'r', encoding='utf-8') as file:
                html = file.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Страница входа не найдена")
    
    def serve_dashboard(self):
        try:
            with open('index.html', 'r', encoding='utf-8') as file:
                html_template = file.read()

            cpu = psutil.cpu_percent(interval=0.3)
            ram = psutil.virtual_memory()
            
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                infoCPU = winreg.QueryValueEx(key, "ProcessorNameString")[0].strip()
            except:
                infoCPU = platform.processor() or "Неизвестный процессор"
            
            infoRAM = round(ram.total / (1024**3), 1)
            
            html = html_template.replace('{CPU}', str(round(cpu, 1)))
            html = html.replace('{RAM}', str(round(ram.percent, 1)))
            html = html.replace('{infoCPU}', infoCPU)
            html = html.replace('{infoRAM}', str(infoRAM))

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Файл index.html не найден")
    
    def serve_cpu_api(self):
        cpu = psutil.cpu_percent(interval=0.2)
        cpu = max(0, min(100, cpu + random.uniform(-1.5, 1.5)))
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(round(cpu, 1)).encode('utf-8'))
    
    def serve_ram_api(self):
        ram = psutil.virtual_memory()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(round(ram.percent, 1)).encode('utf-8'))
    
    def serve_stats_api(self):
        try:
            recent = system_logger.get_recent_stats(60)
            max_values = system_logger.get_max_values()
            
            if len(recent) < 10:
                now = datetime.now()
                test_data = []
                for i in range(30):
                    t = now - timedelta(seconds=i*10)
                    test_data.append({
                        'time': t.isoformat(),
                        'cpu': round(20 + random.random() * 50, 1),
                        'ram': round(30 + random.random() * 40, 1)
                    })
                recent = test_data[::-1]
                max_values = {'max_cpu': 85.0, 'max_ram': 78.0}
            
            data = {
                'history': recent,
                'max_cpu': max_values['max_cpu'],
                'max_ram': max_values['max_ram'],
                'last_update': datetime.now().strftime('%H:%M:%S')
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Ошибка получения статистики: {e}")
    
    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(f"<h1>Ошибка {code}</h1><p>{message}</p>".encode('utf-8'))

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path != "/login" and not self.is_authenticated():
            self.serve_login_page()
            return
        
        if path == "/" or path == "/dashboard":
            self.serve_dashboard()
        elif path == "/login":
            self.serve_login_page()
        elif path == "/api/cpu":
            self.serve_cpu_api()
        elif path == "/api/ram":
            self.serve_ram_api()
        elif path == "/api/stats":
            self.serve_stats_api()
        else:
            self.send_error(404, "Страница не найдена")

    def do_POST(self):
        if self.path == "/shutdown":
            try:
                subprocess.Popen(["shutdown", "/s", "/t", "10", "/c", "Выключение по команде с панели"], shell=True)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("Выключение через 10 секунд".encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Ошибка выключения: {e}")
                
        elif self.path == "/reboot":
            try:
                subprocess.Popen(["shutdown", "/r", "/t", "10", "/c", "Перезагрузка по команде с панели"], shell=True)
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("Перезагрузка через 10 секунд".encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Ошибка перезагрузки: {e}")
                
        elif self.path == "/login":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            username = params.get('username', [''])[0]
            password = params.get('password', [''])[0]
            
            if username == 'admin' and password == 'admin':
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Set-Cookie', 'session=authenticated; Path=/')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write("Неверный логин или пароль".encode('utf-8'))
        else:
            self.send_error(404, "Не найдено")

from datetime import timedelta

if __name__ == "__main__":
    log_thread = threading.Thread(target=background_logging, daemon=True)
    log_thread.start()
    print("Фоновый сбор данных запущен (интервал: 10 сек)")
    
    for _ in range(20):
        system_logger.add_record(
            20 + random.random() * 50,
            30 + random.random() * 40
        )
        time.sleep(0.1)
    
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        print(f"http://localhost:{PORT}")
        print("Логин: admin, Пароль: admin")
        httpd.serve_forever()