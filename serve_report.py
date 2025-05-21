import http.server
import socketserver
import os
import webbrowser
import socket
import threading

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

PORT = find_free_port()
DIRECTORY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "allure_report")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def run_server():
    try:
        server = socketserver.TCPServer(("", PORT), Handler)
        url = f"http://localhost:{PORT}"
        print(f"正在启动 Allure 报告服务器...")
        print(f"请在浏览器中访问: {url}")
        
        # 在新线程中启动服务器
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # 打开浏览器
        webbrowser.open(url)
        print("服务器已启动，请按 Ctrl+C 停止")
        
        try:
            while True:
                input()  # 保持程序运行直到按 Ctrl+C
        except KeyboardInterrupt:
            print("\n正在停止服务器...")
            server.shutdown()
            server.server_close()
            print("服务器已停止")
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")

if __name__ == '__main__':
    run_server()
