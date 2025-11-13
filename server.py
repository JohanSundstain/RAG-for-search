import socket
import json
import threading
import signal
import sys

from search import search  

class SearchServer:
    """
    TCP-сервер для вызова функции search(query) через сокет.
    Работает на AF_INET (TCP), поддерживает несколько клиентов.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080, max_clients: int = 5):
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.server_socket = None
        self.running = False
        self.lock = threading.Lock()
        self.threads = []

    def start(self):
        """Запуск сервера."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.max_clients)
        self.running = True

        print(f"🔌 SearchServer запущен на {self.host}:{self.port}")

        # Установка обработчика Ctrl+C
        signal.signal(signal.SIGINT, self._signal_handler)

        try:
            while self.running:
                conn, addr = self.server_socket.accept()
                thread = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                thread.start()
                self.threads.append(thread)
        finally:
            self.stop()

    def _handle_client(self, conn: socket.socket, addr):
        """Обработка одного клиента."""
        print(f"📩 Клиент подключён: {addr}")
        try:
            data = conn.recv(10**6).decode('utf-8')
            if not data:
                return
            query = json.loads(data)

            with self.lock:
                result = search(query['query'])

            conn.sendall(result)
        except Exception as e:
            conn.sendall(json.dumps({"error": str(e)}).encode('utf-8'))
        finally:
            conn.close()
            print(f"❌ Клиент отключён: {addr}")

    def stop(self):
        """Остановка сервера."""
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass
        print("🛑 Сервер остановлен.")

    def _signal_handler(self, signum, frame):
        """Перехват Ctrl+C."""
        print("\n⚙️ Получен сигнал завершения.")
        self.stop()
        sys.exit(0)


if __name__ == "__main__":
    server = SearchServer(host="127.0.0.1", port=8080)
    server.start()
