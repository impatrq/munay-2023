import socket

def obtener_ip_wlan0():
    try:
        # Creamos un socket para obtener información de red
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Utilizamos el método getsockname() para obtener la dirección IP de la interfaz activa (WLAN0)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        
        return ip
    except Exception as e:
        return str(e)
        
# Configuración del socket
server_ip = obtener_ip_wlan0() #Escuchar en todas las interfaces de red
server_port = 49152

# Crear un socket TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(1)

print("Esperando conexiones...")

# Esperar a que el cliente se conecte
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida desde {client_address}")

# Enviar los datos de GPS
gps_data = "Latitud: 123.456, Longitud: 789.012"  # Cambia esto por tus datos reales de GPS
client_socket.sendall(gps_data.encode())

# Cerrar los sockets
client_socket.close()
server_socket.close()
