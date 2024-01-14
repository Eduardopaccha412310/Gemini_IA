import tkinter as tk  #Interfaz
from PIL import Image
from io import BytesIO
import os
import cv2
from PIL import Image, ImageTk
import pyttsx3    #Texto a Audio
import re #texto
from rich.console import Console #HTMLtexto consola
from rich.syntax import Syntax
from docx import Document
import html2text 
import textwrap
import google.generativeai as genai  #GEMINI-1
from markdown import Markdown
import os
import azure.cognitiveservices.speech as speechsdk #Azure-1

class VentanaPrincipal:
    
    def cerrar_ventana(self, event):
        self.master.destroy()

    def cerrar_ventana_chat(self, ventana_chat):
        ventana_chat.destroy()

    def cerrar_ventana_foto(self, ventana_chat):
        ventana_chat.destroy()
    
    def focus_next_widget(self, event, current_widget, next_widget, prev_widget):
        next_widget.focus_set()
        if isinstance(next_widget, tk.Button):
            # Si el próximo widget es un botón, hablar su texto
            self.hablarpy(next_widget["text"])
        elif isinstance(prev_widget, tk.Button):
            # Si el widget anterior es un botón, revertir el cambio
            prev_widget.focus_set()
        return "break"  # Para evitar que se realice la acción predeterminada de la tecla "Tab"

    def leer_texto_boton(self, boton):
        # Esta función será llamada cuando se presiona la tecla "Tab" en un botón y leerá el texto del botón
       self.master.after(100, lambda: self.hablarpy(boton["text"]))

    def cambiar_foco_boton(self, event):
            # Cambiar el foco entre los botones al presionar "Tab"
            if self.master.focus_get() == self.boton_chat:
                self.boton_foto.focus_set()
            elif self.master.focus_get() == self.boton_foto:
                self.boton_cerrar.focus_set()
            elif self.master.focus_get() == self.boton_cerrar:
                self.boton_chat.focus_set()

    def to_markdown(self,text):
        return Markdown().convert(textwrap.indent(text, '> ', predicate=lambda _: True)) 
    
    def to_plain_string(self,text):
        # Eliminar caracteres especiales excepto letras, números y tildes
        cleaned_text = re.sub(r'[^\w\sáéíóúÁÉÍÓÚ.,;:?!¡¿]', '', text)
        return cleaned_text 
    
    def contiene_palabra(self,cadena, palabra):
    # Verificar si la cadena no es None antes de intentar la comparación
        if cadena is not None:
            return palabra in cadena
        else:
            return False
        
    def html_to_docx( text, output_path):
        # Verificar si el archivo ya existe
        original_output_path = output_path
        counter = 1
        while os.path.exists(output_path):
            # Si el archivo ya existe, agregar un número al final del nombre
            output_path = original_output_path.replace('.docx', f'_{counter}.docx')
            counter += 1

        # Crear un nuevo documento de Word
        doc = Document() 
        text_content = html2text.html2text(text) 
        doc.add_paragraph(text_content) 
        doc.save(output_path) 
        print(f'Documento Word guardado en: {output_path}')

    def hablar(self,texto):
        console = Console()
        syntax = Syntax(texto, "html", theme="monokai", line_numbers=True)
        console.print(syntax)

        #Azure-2                    AQUI Tu KEY DE AZURE
        
        speech_config = speechsdk.SpeechConfig(subscription='d214b416ed6542d1875694d4e84b4ad0', region="brazilsouth")
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True) 
        speech_config.speech_synthesis_voice_name='es-EC-AndreaNeural' #definimos la voz a utilizar
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(texto).get()
        stream = speechsdk.AudioDataStream(speech_synthesis_result)  

    def hablarpy(self,texto):
        print(texto)
        engine = pyttsx3.init()
        engine.say(texto)
        engine.startLoop(False)
        engine.iterate()
        engine.endLoop()

    def __init__(self, master):
                
        #GEMINI-2                       AQUI Tu KEY DE GOOGLE      
        GOOGLE_API_KEY='AIzaSyCIWr5RYw8Oewzzr99Xg4jLlLh6_Ux2TmM'
        genai.configure(api_key=GOOGLE_API_KEY)
    
        self.master = master
        master.title("Gemini + AzureCognitionServices") 
        # Ocultar barra de título y botones de ventana
        #master.overrideredirect(True)
        
        # Personalizar color de fondo
        master.configure(bg='#000000')  # Puedes usar cualquier código de color hexadecimal

        # Personalizar tamaño de fuente

        # Personalizar color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(master, text="Bienvenido: \n \n     Selecciona una opcion:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=20)  
        # Centrar la ventana en la pantalla
        self.centra_ventana()
  
        # Agregar botones con el mismo tamaño
        self.boton_chat = tk.Button(master, text="Chat", command=self.abrir_ventana_chat, bg='#333333', fg='#ffffff', width=12, height=2)
        self.boton_chat.pack()
        

        self.boton_foto = tk.Button(master, text="Foto", command=self.abrir_ventana_foto, bg='#333333', fg='#ffffff', width=12, height=2)
        self.boton_foto.pack()
        

        # Agregar un botón para cerrar la ventana
        self.boton_cerrar = tk.Button(master, text="Cerrar", command=master.destroy, bg='#500', fg='#ffffff', width=12, height=2)
        self.boton_cerrar.pack()
        
        master.bind("<Escape>", self.cerrar_ventana)

         # Vincular la tecla "Tab" al primer botón (Chat) cuando se inicia la aplicación
        self.master.bind("<Tab>", self.cambiar_foco_boton)
        #self.boton_chat.focus_set()  # Establecer el foco en el botón "Chat" al inicio
         
         # Vincular la tecla "Tab" a la función leer_texto_boton cuando los botones tienen el foco
        self.boton_chat.bind("<FocusIn>", lambda event: self.leer_texto_boton(self.boton_chat))
        self.boton_foto.bind("<FocusIn>", lambda event: self.leer_texto_boton(self.boton_foto))
        self.boton_cerrar.bind("<FocusIn>", lambda event: self.leer_texto_boton(self.boton_cerrar))

    def centra_ventana(self):
        ancho_ventana = 600
        alto_ventana = 300  

        # Obtener el tamaño de la pantalla
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Calcular la posición para centrar la ventana
        x = (ancho_pantalla - ancho_ventana) // 2
        y = (alto_pantalla - alto_ventana) // 2

        # Establecer la geometría de la ventana para centrarla
        self.master.geometry(f'{ancho_ventana}x{alto_ventana}+{x}+{y-90}')

##                CHAT#                CHAT#                CHAT#                CHAT#                CHAT#                CHAT#                CHAT
    def abrir_ventana_chat(self): 
        ventana_chat = tk.Toplevel(self.master)
        ventana_chat.title("Chat")

             # Obtener el tamaño de la pantalla principal
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Centrar la ventana de chat
        ancho_ventana_chat = 600  
        alto_ventana_chat = 300
        x = (ancho_pantalla - ancho_ventana_chat) // 2
        y = (alto_pantalla - alto_ventana_chat) // 2
        #TAMAÑO
        ventana_chat.geometry(f'{ancho_ventana_chat}x{alto_ventana_chat}+{x}+{y}') 
        ventana_chat.configure(bg='#000000')  #Color d fondo

        # Personalizar color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(ventana_chat, text="Ingresa un mensaje:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=12)  
        
        #ENtrada de texto
        entrada = tk.Text(ventana_chat, font=("Arial", 10), bg='#eeeeee', height=4,  width=40, wrap="word")
        entrada.pack(pady=9)
        # Establecer autofocus en la entrada de texto
        entrada.focus_set() 


        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])
        chat     
        

        self.resultado_label = tk.Label(ventana_chat, text="",font=("Arial", 8),bg='#333333', fg='#ffffff', width=90, height=4)
        self.resultado_label.pack() 
        boton_enviar2 = tk.Button(ventana_chat, text="Enviar", command=lambda: mostrar_resultado_chat(entrada.get("1.0", tk.END), chat), bg='#333333', fg='#ffffff', width=12, height=2,takefocus=True)
        boton_enviar2.pack(side=tk.LEFT, padx=(145, 5))

        # Agregar el botón "Cerrar" en la ventana de chat
        boton_cerrar_chat = tk.Button(ventana_chat, text="Cerrar", command=lambda: self.cerrar_ventana_chat(ventana_chat), bg='#500', fg='#ffffff', width=12, height=2,takefocus=True)
        boton_cerrar_chat.pack(side=tk.LEFT, padx=(0, 5))
        #boton_enviar2.focus_set()
        
        # Agregar el botón "Por voz" en la ventana de chat
        boton_comando_voz = tk.Button(ventana_chat, text="Comando de voz", command=lambda: on_boton_icono_click(), bg='#500', fg='#ffffff', width=16, height=2,takefocus=True)
        boton_comando_voz.pack(side=tk.LEFT)

        # Vincular la tecla "Esc" al método cerrar_ventana_chat
        ventana_chat.bind("<Escape>", lambda event: self.cerrar_ventana_chat(ventana_chat))
        #entrada.bind("<Tab>", lambda event: focus_next_widget(event, boton_enviar2))
        #entrada.bind("<Tab>", lambda event: self.focus_next_widget(event, entrada, boton_enviar2))

        # Vincular la tecla "Tab" al primer botón (Enviar)
        #entrada.focus_set()                                                                   
        #boton_enviar2.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_enviar2, boton_cerrar_chat))
        #entrada.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_enviar2, boton_cerrar_chat))
        #boton_cerrar_chat.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_cerrar_chat, boton_comando_voz))
        #boton_comando_voz.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_comando_voz, boton_enviar2))
        #boton_enviar2.focus_set() 
        # En el método abrir_ventana_chat, después de establecer el enlace de la tecla "Tab" en la entrada de texto
        ##Se puede establecer un comando antes de  TAB
        entrada.bind("<Control-Tab>", lambda event: self.focus_next_widget(event, entrada, boton_enviar2, boton_cerrar_chat))
        #self.hablarpy("Enviar")
        boton_enviar2.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_enviar2, boton_cerrar_chat, boton_comando_voz))
        boton_cerrar_chat.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_cerrar_chat, boton_comando_voz, boton_enviar2))
        boton_comando_voz.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_comando_voz, boton_enviar2, boton_cerrar_chat))
        
        # Vincular la tecla "Tab" a la función leer_texto_boton cuando los botones tienen el foco
        #boton_enviar2.bind("<FocusIn>", lambda event: self.leer_texto_boton(boton_enviar2))

        def on_boton_icono_click():
        # Aquí puedes poner la lógica que deseas ejecutar cuando se haga clic en el botón con icono
            console = Console()
            console.log('Hola')

        #def focus_next_widget(event, widget):
        #    widget.focus_set()
        #   return "break"  # Para evitar que se realice la acción predeterminada de la tecla "Tab"
        
                
        def mostrar_resultado_chat(mensaje, chat): 
            
            boton_enviar2.config(state=tk.DISABLED)
            entrada.delete("1.0", tk.END)

            if mensaje=="salir": 
                exit()    
            try:
                response = chat.send_message(mensaje).text 
                print(response)  
                self.hablarpy(response)
                #html_to_docx(response, "respuestas/texto_escanneado.docx")
                     
                self.resultado_label.config(text=response)  
                entrada.focus_set() 
                boton_enviar2.config(state=tk.NORMAL)

                #Voz con azure
                #self.hablarpy(a)  

            except Exception as e:
                print(f'{type(e).__name__}: {e}')  

## FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO                   # FOTO         
    def abrir_ventana_foto(self):
        # Lógica de la Foto aquí
        # messagebox.showinfo("Foto", "Lógica de la Foto")
        ventana_foto = tk.Toplevel(self.master)
        ventana_foto.title("Prompt con Foto")

        # Obtener el tamaño de la pantalla principal
        ancho_pantalla = self.master.winfo_screenwidth()
        alto_pantalla = self.master.winfo_screenheight()

        # Centrar la ventana de chat
        ancho_ventana_foto = 600  
        alto_ventana_foto = 300
        x = (ancho_pantalla - ancho_ventana_foto) // 2
        y = (alto_pantalla - alto_ventana_foto) // 2
        #TAMAÑO
        ventana_foto.geometry(f'{ancho_ventana_foto}x{alto_ventana_foto}+{x}+{y}') 
        ventana_foto.configure(bg='#000000')  #Color d fondo 

        # Función para actualizar la vista de la cámara en la ventana 
        def tomar_foto():
            # Inicializar la cámara
            camara = cv2.VideoCapture(0)

            if not camara.isOpened():
                print("Error al abrir la cámara.")
                return None

            # Capturar un solo cuadro (foto)
            ret, frame = camara.read()
            retval, buffer = cv2.imencode('.jpg', frame)
            # Crear un objeto BytesIO para almacenar la imagen en memoria
            img_bytes = BytesIO(buffer.tobytes())

            # Abrir la imagen desde BytesIO usando PIL
            img_pil = Image.open(img_bytes)

            # Puedes mostrar la imagen si lo deseas
            #img_pil.show()
            
            camara.release()

            if ret:
                return img_pil
            else:
                print("Error al capturar la foto.")
                return None
          

        #Color de fondo de la etiqueta y color del texto
        etiqueta = tk.Label(ventana_foto, text="Ingresa un mensaje:", font=("Arial", 12), bg='#000000', fg='#ffffff')
        etiqueta.pack(pady=12)  
        
 
        #ENtrada de texto
        entry_mensaje = tk.Text(ventana_foto, font=("Arial", 10), bg='#eeeeee', height=4, width=40, wrap="word")
        entry_mensaje.pack(pady=10)

        # Establecer autofocus en la entrada de texto
        entry_mensaje.focus_set()  


        #Salida Respuesta
        self.resultado_label = tk.Label(ventana_foto, text="",font=("Arial", 8),bg='#222222', fg='#ffffff', width=90, height=4)
        self.resultado_label.pack() 
        #Boton ENVIAR
        boton_enviar_pic = tk.Button(ventana_foto, text="Enviar", command=lambda: mostrar_resultado_foto(entry_mensaje.get("1.0", tk.END)), bg='#333333', fg='#ffffff', width=12, height=2)
        boton_enviar_pic.pack(side=tk.LEFT, padx=(145, 5))

         # Agregar el botón "Cerrar" en la ventana de chat
        boton_cerrar_pic = tk.Button(ventana_foto, text="Cerrar", command=lambda: self.cerrar_ventana_foto(ventana_foto), bg='#500', fg='#ffffff', width=12, height=2)
        boton_cerrar_pic.pack(side=tk.LEFT, padx=(0, 5))

        # Agregar el botón "Por voz" en la ventana de chat
        boton_comando_voz_pic = tk.Button(ventana_foto, text="Comando de voz", command=lambda: on_boton_icono_click(), bg='#500', fg='#ffffff', width=16, height=2)
        boton_comando_voz_pic.pack(side=tk.LEFT)

        # Vincular la tecla "Esc" al método cerrar_ventana_chat
        #ventana_foto.bind("<Escape>", lambda event: self.cerrar_ventana_foto(ventana_foto))
        #entry_mensaje.bind("<Tab>", lambda event: focus_next_widget(event, boton_enviar))

        #alternar_enfoque = True

        #def cambiar_enfoque(event):
        #    nonlocal alternar_enfoque
        #    if alternar_enfoque:
         #       boton_enviar_pic.focus_set()
        #        # Leer el texto del botón "Enviar" cuando obtiene el enfoque
        #        self.hablarpy(boton_enviar_pic["text"])
        #    else:
        #        entry_mensaje.focus_set()
        #    alternar_enfoque = not alternar_enfoque
        # Vincular la tecla "Tab" para cambiar el enfoque entre botón "Enviar" y la entrada de texto
        #entry_mensaje.bind("<Control-Tab>", cambiar_enfoque)
        entry_mensaje.bind("<Control-Tab>", lambda event: self.focus_next_widget(event, entry_mensaje, boton_enviar_pic, boton_cerrar_pic))
        #self.hablarpy("Enviar")
        boton_enviar_pic.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_enviar_pic, boton_cerrar_pic, boton_comando_voz_pic))
        boton_cerrar_pic.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_cerrar_pic, boton_comando_voz_pic, boton_enviar_pic))
        boton_comando_voz_pic.bind("<Tab>", lambda event: self.focus_next_widget(event, boton_comando_voz_pic, boton_enviar_pic, boton_cerrar_pic))

        def on_boton_icono_click():
        # Aquí puedes poner la lógica que deseas ejecutar cuando se haga clic en el botón con icono
            console = Console()
            console.log('Hola')
    
        def mostrar_resultado_foto(mensaje):   
            foto =tomar_foto()  
            print(" mensaje ",mensaje)  
            print(" foto ",foto)   
            boton_enviar_pic.config(state=tk.DISABLED)
            entry_mensaje.delete("1.0", tk.END)

            if mensaje=="salir": 
                exit()    
            else: 
                model = genai.GenerativeModel('gemini-pro-vision')  
                response = model.generate_content([mensaje, foto], stream=True)
                response.resolve()
                print(response) 
                        
                if response.candidates[0].content.parts : 
                    testo= response.candidates[0].content.parts[0].text
                    self.resultado_label.config(text=testo)
                    self.hablarpy(testo)
                    try:
                        self.html_to_docx(response, "respuestas/respuesta.docx")
                    except Exception as e:
                        print('Error al guardar!')    
                else: 
                    try:  
                        a=response.text
                        self.html_to_docx(response, "respuestas/respuesta.docx")
                        self.resultado_label.config(text=a)
                        self.hablarpy(a) 

                    except Exception as e:
                        print(f'{type(e).__name__}: {e}')    

                # Reactivar el botón después de completar la función  
                entry_mensaje.focus_set() 
                boton_enviar_pic.config(state=tk.NORMAL)
                 
if __name__ == "__main__":
    root = tk.Tk()
    ventana_principal = VentanaPrincipal(root)
    root.mainloop()
