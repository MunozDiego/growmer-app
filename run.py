import os
import sys
import subprocess
from multiprocessing import Process
from app import create_app, db
import threading
from werkzeug.serving import make_server

class ServerThread(threading.Thread):

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 7481, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

def start_server(app):
    global server
    server = ServerThread(app)
    server.start()

def stop_server():
    global server
    server.shutdown()

def StartGrowmer():
    #Abrir Google Chrome en modo debug
    os.system('cmd /c "start chrome.exe --remote-debugging-port=5351 --start-maximized"')

    #verificar si existe la base de datos en la carpeta AppData
    dir_path = os.path.join(os.environ['APPDATA'], 'GROWMER APP BETA')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    file_path = os.path.join(dir_path, 'growmer.db')

    #Nos aseguramos que encuentre CEF en las carpetas temp que crea pyinstaller
    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path

    path = resource_path(relative_path='cefsimple/Debug/cefsimple.exe')
    app = create_app(os.getenv('FLASK_CONFIG') or 'production')
    
    #se crea la db en caso que no exista
    if not os.path.exists(file_path):
            db.create_all(app=app)
    #inicia flask en un subproceso
    start_server(app=app)

    process = app.cef_process
    #cuando se cierre CEF, parar el server
    while True:
        output = process.stdout.readline()
        return_code = process.poll()
        if return_code is not None:
            stop_server()
            break
        
if __name__ == "__main__":
    StartGrowmer()
    sys.exit()