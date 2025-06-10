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

# 啟動 Allure 報告伺服器，並自動開啟瀏覽器
# 伺服器啟動後，按 Ctrl+C 可停止

def run_server():
    try:
        server = socketserver.TCPServer(("", PORT), Handler)
        url = f"http://localhost:{PORT}"
        print(f"正在啟動 Allure 報告伺服器...")
        print(f"請在瀏覽器中訪問: {url}")
        
        # 在新執行緒中啟動伺服器
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # 開啟瀏覽器
        webbrowser.open(url)
        print("伺服器已啟動，請按 Ctrl+C 停止")
        
        try:
            while True:
                input()  # 保持程式運行直到按 Ctrl+C
        except KeyboardInterrupt:
            print("\n正在停止伺服器...")
            server.shutdown()
            server.server_close()
            print("伺服器已停止")
    except Exception as e:
        print(f"啟動伺服器時發生錯誤: {e}")

if __name__ == '__main__':
    run_server()
