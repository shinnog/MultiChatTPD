import socket
import threading

clientes_conectados = []

def broadcast(mensaje, nombre):
    """Envía un mensaje a todos los clientes conectados."""
    for cliente in clientes_conectados:
        try:
            cliente.sendall(f"{nombre}: {mensaje}".encode('utf-8'))
        except:
            
            clientes_conectados.remove(cliente)

def handle_client(conn, addr):

    nombre = conn.recv(1024).decode('utf-8')
    print(f"Conexión establecida con {nombre} ({addr[0]}:{addr[1]})")
    broadcast(f"{nombre} se ha unido al chat.", "Servidor") 
    
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                mensaje = data.decode('utf-8')
                print(f"Mensaje de {nombre}: {mensaje}")
                broadcast(mensaje, nombre)  # Reenviar el mensaje a todos
            except:
                break

    
    print(f"{nombre} ({addr[0]}:{addr[1]}) se ha desconectado.")
    broadcast(f"{nombre} ha abandonado el chat.", "Servidor")
    clientes_conectados.remove(conn)
    conn.close()

def start_server(host='192.168.100.48', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Servidor escuchando en {host}:{port}...")
        
        while True:
            conn, addr = server_socket.accept()
            clientes_conectados.append(conn) 
        
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
            print(f"Conexión aceptada. Clientes conectados: {len(clientes_conectados)}")

if __name__ == "__main__":
    start_server()