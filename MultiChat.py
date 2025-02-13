import socket
import threading
import tkinter as tk
from tkinter import scrolledtext

def recibir_mensajes(cliente_socket, chat_area):
    """Función para recibir mensajes del servidor."""
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if not mensaje:
                break
            chat_area.config(state=tk.NORMAL)  # Habilitar edición del área de chat
            chat_area.insert(tk.END, mensaje + "\n")  # Mostrar el mensaje
            chat_area.config(state=tk.DISABLED)  # Deshabilitar edición del área de chat
            chat_area.yview(tk.END)  # Desplazar al final del chat
        except:
            print("Conexión con el servidor perdida.")
            break

def enviar_mensaje(cliente_socket, entrada_texto, chat_area):
    """Función para enviar mensajes al servidor."""
    mensaje = entrada_texto.get()  # Obtener el texto del campo de entrada
    if mensaje.strip():  # Verificar que el mensaje no esté vacío
        if mensaje.lower() == 'salir':
            cliente_socket.sendall(mensaje.encode('utf-8'))
            cliente_socket.close()
            ventana.quit()  # Cerrar la ventana
        else:
            cliente_socket.sendall(mensaje.encode('utf-8'))
            entrada_texto.delete(0, tk.END)  # Limpiar el campo de entrada

def iniciar_cliente(host='192.168.100.48', port=65432):
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((host, port))

    # Solicitar al usuario que ingrese su nombre
    nombre = input("Ingresa tu nombre: ")
    cliente_socket.sendall(nombre.encode('utf-8'))  # Enviar el nombre al servidor

    # Configurar la interfaz gráfica
    global ventana
    ventana = tk.Tk()
    ventana.title(f"Chat - {nombre}")

    # Área de chat
    chat_area = scrolledtext.ScrolledText(ventana, state=tk.DISABLED)
    chat_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Campo de entrada de texto
    entrada_texto = tk.Entry(ventana, font=("Arial", 12))
    entrada_texto.pack(padx=20, pady=10, fill=tk.X)

    # Vincular la tecla "Enter" al envío de mensajes
    entrada_texto.bind(
        "<Return>",
        lambda event: enviar_mensaje(cliente_socket, entrada_texto, chat_area),
    )

    # Botón para enviar mensajes
    boton_enviar = tk.Button(
        ventana,
        text="Enviar",
        command=lambda: enviar_mensaje(cliente_socket, entrada_texto, chat_area),
    )
    boton_enviar.pack(padx=20, pady=10)

    # Hilo para recibir mensajes
    threading.Thread(target=recibir_mensajes, args=(cliente_socket, chat_area)).start()

    # Iniciar la interfaz gráfica
    ventana.mainloop()

if __name__ == "__main__":
    iniciar_cliente()