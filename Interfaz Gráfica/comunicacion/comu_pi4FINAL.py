import socket

# Configuración del socket
server_hostname = 'pimunay'  # Nombre de hostname de tu Raspberry Pi
server_port = 49152

# Resuelve el hostname a una dirección IP
try:
    server_ip = socket.gethostbyname(server_hostname)

    # Crear un socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    # Recibir los datos de GPS
    gps_data = client_socket.recv(1024).decode()
    print(f"Datos de GPS recibidos: {gps_data}")

    # Cerrar el socket del cliente
    client_socket.close()
except socket.gaierror:
    print(f"No se pudo resolver el hostname {server_hostname}. Asegúrate de que el nombre de hostname sea correcto.")
except ConnectionRefusedError:
    print(f"No se pudo conectar al servidor en {server_hostname}:{server_port}. Asegúrate de que el servidor esté en ejecución.")
