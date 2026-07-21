import http.server
import socketserver
import subprocess
import psutil
import platform
import json
import winreg
from urllib.parse import urlparse, parse_qs

PORT = 3000

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

            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory()
            
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

            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "Файл index.html не найден")
    
    def serve_cpu_api(self):
        cpu = psutil.cpu_percent()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(cpu).encode('utf-8'))
    
    def serve_ram_api(self):
        ram = psutil.virtual_memory()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(str(ram.percent).encode('utf-8'))
    
    def send_error(self, code, message):
        self.send_response(code)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

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
        else:
            self.send_error(404, "404 - Страница не найдена")

    def do_POST(self):
        if self.path == "/run_bat":
            subprocess.Popen(["cmd", "/c", "Clean.bat"])
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("BAT файл успешно запущен через POST".encode('utf-8'))
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
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write("Неверный логин или пароль".encode('utf-8'))
        else:
            self.send_error(404, "404 - Не найдено")

if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"Сервер запущен на порту {PORT}")
        print("http://localhost:3000")
        httpd.serve_forever()