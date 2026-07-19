import http.server
import socketserver
import subprocess
import psutil
import json

PORT = 3000

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open('index.html', 'r', encoding='utf-8') as file:
                    html_template = file.read()


                cpu = psutil.cpu_percent()
                html = html_template.replace('{CPU}', str(cpu))

                ram = psutil.virtual_memory()
                html = html_template.replace('{RAM}', str(ram))


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
        elif self.path == "/api/cpu":
            ram = psutil.virtual_memory()
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(str(ram).encode('utf-8'))
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