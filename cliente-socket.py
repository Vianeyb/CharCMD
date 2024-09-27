import socket
import threading
import sys
import os

class Cliente():
    def __init__(self, host="localhost", port=7000, DOWNLOAD_DIR='./download'):
        try:
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))

             # Crear el directorio de descarga si no existe
            self.DOWNLOAD_DIR = DOWNLOAD_DIR
            if not os.path.exists(self.DOWNLOAD_DIR):
                os.makedirs(self.DOWNLOAD_DIR)

            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True 
            msg_recv.start()

            while True:
                msg = input('-> ')
                if msg.startswith('get '):  # Si es un comando para obtener un archivo
                    filename = msg.split(' ', 1)[1]  # Extraer el nombre del archivo
                    self.request_file(filename)  # Solicitar el archivo al servidor
                elif msg != 'salir':
                    self.send_msg(msg)
                else:
                    self.sock.close()
                    sys.exit()
        except Exception as e:
            print(f"Error al conectar el socket: {e}")
            
    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(4096).decode('utf-8')
                if data:
                    print(data)
            except:
                pass


    def send_msg(self,msg):
        try:
            self.sock.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar mensaje: {e}")

    def request_file(self, filename):
        """Solicitar un archivo al servidor"""
        try:
            # Enviar el comando `get` para pedir el archivo
            self.sock.send(f"get {filename}".encode('utf-8'))
            
            # Recibir el archivo en bloques de 4096 bytes
            with open(os.path.join(self.DOWNLOAD_DIR, filename), 'wb') as f:
                while True:
                    data = self.sock.recv(4096)
                    if not data:
                        break
                    f.write(data)

            print(f"Archivo '{filename}' descargado en {self.DOWNLOAD_DIR}")
        except Exception as e:
            print(f"Error al recibir el archivo: {e}")
            
cliente = Cliente()
