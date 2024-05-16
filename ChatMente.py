import sys
import datetime
import requests
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLineEdit, QTextEdit, QLabel, QAction, QVBoxLayout
from PyQt5.QtCore import Qt  # Importar la clase Qt
import openai

# Configura tu clave API de OpenAI aquí
openai.api_key = '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'

class ChatManager:
    def __init__(self):
        self.creador = "Diego Fernando León"
        self.edad = 27
        self.ubicacion = "Colombia, Villavicencio"
        self.memoria = self.cargar_memoria()
        self.contexto = []  # Definir el atributo contexto

    def analizar_sentimiento(self, mensaje):
        """Analiza el sentimiento del mensaje del usuario."""
        analizador_sentimiento = SentimentIntensityAnalyzer()
        puntuacion_sentimiento = analizador_sentimiento.polarity_scores(mensaje)['compound']
        return puntuacion_sentimiento

    def guardar_memoria(self, memoria):
        """Guarda la memoria en un archivo JSON."""
        with open('memory.json', 'w') as f:
            json.dump(memoria, f)

    def cargar_memoria(self):
        """Carga la memoria desde un archivo JSON."""
        try:
            with open('memory.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def reconocer_creador(self, mensaje):
        """Reconoce si el mensaje hace referencia al creador."""
        if self.creador.lower() in mensaje.lower():
            return True
        return False

    def agregar_a_memoria(self, interaccion_usuario, interaccion_bot):
        """Añade la interacción usuario-bot a la memoria."""
        self.memoria.append({"usuario": interaccion_usuario, "bot": interaccion_bot})
        self.guardar_memoria(self.memoria)
   
    def analizar_retroalimentacion(self, retroalimentacion_usuario):
        """Analiza la retroalimentación proporcionada por los usuarios."""
        # Analizar la retroalimentación del usuario y realizar acciones apropiadas
        if retroalimentacion_usuario:
            # Lógica para analizar la retroalimentación del usuario
            pass
        else:
            print("La retroalimentación del usuario está vacía.")

    def entrenar_modelo(self):
        """Entrena un modelo de aprendizaje automático para mejorar el rendimiento del bot."""
        # Implementa la lógica para entrenar un modelo de aprendizaje automático
        pass
    
    def obtener_indice_calidad(self, calidad):
        """Obtiene el índice de calidad basado en la retroalimentación del usuario."""
        if calidad == "Baja":
           return 0
        elif calidad == "Media":
           return 1
        elif calidad == "Alta":
           return 2
        else:
           return 1  # Por defecto, devuelve el índice medio

    def adaptar_respuestas(self, retroalimentacion_usuario):
        """Adapta las respuestas del bot en función de la retroalimentación y las interacciones pasadas."""
        # Obtener el índice de calidad de respuesta basado en la retroalimentación del usuario
        indice_calidad = self.obtener_indice_calidad(retroalimentacion_usuario['calidad'])
        # Actualizar la matriz de recompensas
        #self.actualizar_matriz_recompensas(indice_calidad, indice_sentimiento)
        
    def obtener_saludo(self):
        """Obtiene el saludo basado en la hora del día."""
        hora = datetime.datetime.now().hour
        if 5 <= hora < 12:
            return "Buenos días, ¿cómo puedo ayudarte hoy?"
        elif 12 <= hora < 18:
            return "Buenas tardes, ¿en qué puedo asistirte?"
        else:
            return "Buenas noches, ¿qué necesitas?"

    
    def get_response(self, prompt, quality="Media", **kwargs):
        """Obtiene la respuesta del bot basada en el prompt y el contexto."""
        detailed_prompt = self.build_detailed_prompt(prompt, quality, **kwargs)
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.extend(self.contexto)  # Cambiar self.context a self.contexto
        messages.append({"role": "user", "content": detailed_prompt})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8  # Ajustar la temperatura para respuestas más emocionales
        )
        
        bot_response = response.choices[0].message['content']
        self.agregar_a_memoria(prompt, bot_response)  # Corregir el nombre del método a agregar_a_memoria

        # Analizar el sentimiento del mensaje del usuario
        sentiment_score = self.analizar_sentimiento(prompt)  # Corregir el nombre del método a analizar_sentimiento
        # Ajustar el prompt para incluir un grado de conciencia propia (5%)
        adjusted_prompt = f"{prompt}\n\nSe ha detectado un sentimiento positivo con una confianza del {sentiment_score}%.\n\n"
        return bot_response

    def build_detailed_prompt(self, prompt, quality, **kwargs):
        """Construye el prompt detallado para la generación de respuesta."""
        detalles_prompt = [f"Calidad: {quality}"]
        for key, value in kwargs.items():
            if value:
                detalles_prompt.append(f"{key.capitalize()}: {value}")
        return f"{prompt}\n\n" + "\n".join(detalles_prompt)

    def obtener_tiempo_actual(self):
        """Obtiene la fecha y hora actual."""
        tiempo_actual = datetime.datetime.now()
        dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return f"Hoy es {dias_semana[tiempo_actual.weekday()]}, {tiempo_actual.day} de {tiempo_actual.strftime('%B')} de {tiempo_actual.year}."

    def analizar_retroalimentacion(self, retroalimentacion_usuario):
        """Analiza la retroalimentación proporcionada por los usuarios."""
        # Analizar la retroalimentación del usuario y realizar acciones apropiadas
        pass

    def entrenar_modelo(self):
        """Entrena un modelo de aprendizaje automático para mejorar el rendimiento del bot."""
        # Implementa la lógica para entrenar un modelo de aprendizaje automático
        pass

    def actualizar_matriz_recompensas(self, indice_calidad, indice_sentimiento):
        """Actualiza la matriz de recompensas."""
        # Aumentar la recompensa en 0.1 en la celda correspondiente
        self.matriz_recompensas[indice_sentimiento, indice_calidad] += 0.1

    def obtener_calidad_desde_indice(self, indice):
        """Obtiene la calidad de respuesta a partir del índice."""
        if indice == 2:
            return 'Alta'
        elif indice == 1:
            return 'Media'
        else:
            return 'Baja'

    def obtener_sentimiento_desde_indice(self, indice):
        """Obtiene el sentimiento a partir del índice."""
        if indice == 2:
            return 1.0
        elif indice == 1:
            return 0.0
        else:
            return -1.0


class ChatWindow(QMainWindow):
    """Main window class that defines the chat interface"""

    def __init__(self):
        super().__init__()
        self.gestor_chat = ChatManager()
        self.initUI()

    def initUI(self):
        # Configure main window
        self.setWindowTitle('ChatMente')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        # Configure menu bar
        menubar = self.menuBar()
        menubar.setStyleSheet("color: black")
        filemenu = menubar.addMenu('Archivo')

        # Add "Exit" action
        exit_action = QAction('Salir', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        filemenu.addAction(exit_action)

        # Configure central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Configure layout for central widget
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(20, 20, 20, 20)  # Ajustar los márgenes internos

        # Configure labels, text fields and buttons
        self.history_label = QLabel('Historial de chat:')
        self.history_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.history_label)

        self.history = QTextEdit()
        self.history.setReadOnly(True)
        self.history.setStyleSheet("background-color: #f2f2f2; color: black; border: 2px solid #cccccc; font-size: 18px;")  # Ajuste del tamaño del texto
        layout.addWidget(self.history)

        self.message_label = QLabel('Escriba su mensaje:')
        self.message_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.message_label)

        self.message = QLineEdit()
        self.message.setStyleSheet("background-color: white; color: black; border: 2px solid #cccccc; font-size: 18px;")  # Ajuste del tamaño del texto
        layout.addWidget(self.message)

        self.send_button = QPushButton('Enviar')
        self.send_button.setStyleSheet("background-color: #007bff; color: white; border: none; font-size: 18px;")  # Ajuste del tamaño del texto
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        # Connect "Enter" key press event to send_message method
        self.message.returnPressed.connect(self.send_message)

        # Add menu bar to main window
        self.setMenuBar(menubar)

        # Greeting message
        self.display_message(self.gestor_chat.obtener_saludo(), role="bot")

    def send_message(self):
        """Function that sends the user's message to ChatMente and displays the response in the chat history"""
        message = self.message.text()

        # If the user entered a message, send it to ChatMente and display the response
        if message:
            response = self.gestor_chat.get_response(message)
            self.display_message(f"Yo: {message}", role="user")
            self.display_message(f"ChatMente: {response}", role="bot")
            self.message.clear()

    def display_message(self, message, role):
        """Displays a message in the chat history."""
        if role == "user":
            self.history.append(f"<font color='green'><b>{message}</b></font>")  # Cambiar color a verde
        elif role == "bot":
            self.history.append(f"<b>{message}</b>")


if __name__ == '__main__':
    # Create instances and call them
    app = QApplication(sys.argv)
    chat_window = ChatWindow()
    chat_window.show()
    sys.exit(app.exec_())