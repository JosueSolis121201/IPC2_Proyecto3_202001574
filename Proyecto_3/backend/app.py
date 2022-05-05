from ast import alias
import random
from flask import Flask, jsonify, request
from tkinter import Tk                               #Libreria para explorador de archivos (Se usara para leer data e instrucciones)
from tkinter.filedialog import askopenfilename
app = Flask(__name__) #iniciar la ruta básica del flask
from xml.dom import minidom
from xml.dom.minidom import parse, parseString
import re


#diccionario de datos
listaEstudiates = []
listaEstudiates.append({"carnet": "201800001", "nombre": "Estudiante Viany"})
listaEstudiates.append({"carnet": "201800002", "nombre": "Estudiante 2"})
listaEstudiates.append({"carnet": "201800003", "nombre": "Estudiante 3"})
listaEstudiates.append({"carnet": "201800004", "nombre": "Estudiante 4"})
listaEstudiates.append({"carnet": "201800005", "nombre": "Estudiante 5"})
listaEstudiates.append({"carnet": "201800006", "nombre": "Estudiante 6"})
listaEstudiates.append({"carnet": "201800007", "nombre": "Estudiante 7"})
listaEstudiates.append({"carnet": "201800008", "nombre": "Estudiante 8"})
listaEstudiates.append({"carnet": "201800009", "nombre": "Estudiante 9"})
listaEstudiates.append({"carnet": "201800010", "nombre": "Estudiante 10"})
listaEstudiates.append({"carnet": "201800011", "nombre": "Paola"})




class analizardor():
    def __init__(self) -> None:
        self.asdasd00=0


        self.mensajes_positivos=[]
        self.mensajes_negativos=[]
        self.mensaje_txt=[]
        

        self.contador_mensajes_total=0
        self.contador_sentimientos_positivos_total=0
        self.contador_sentimientos_negativos_total=0
        self.contador_mensajes_neutros_total=0




    def analizador_xml(self,string_xml):
        dom3 = parseString(string_xml)
        doc=dom3
        x=0
        
       

        solicitud = doc.getElementsByTagName("solicitud_clasificacion")
        print("//////////")
        for dic in solicitud:
            
            print(x)
            sentimientos_positivos = dic.getElementsByTagName("sentimientos_positivos")
            sentimientos_negativos = dic.getElementsByTagName("sentimientos_negativos")
            empresa=dic.getElementsByTagName("empresa")
            servicios=dic.getElementsByTagName("servicio")
            mensaje=dic.getElementsByTagName("lista_mensajes")


            #!Sentimiento_positivo
            for sent in sentimientos_positivos:
                sent_text=sent.getElementsByTagName("palabra")
                for exprecion_positiva in sent_text:
                    nombre = doc.getElementsByTagName("palabra")[x].firstChild.data
                    self.mensajes_positivos.append(nombre)
                    x=x+1

                    print("palabras_positiva:%s" % nombre)      #TODO: Resp_sent_positivo
            x=0
            #!Sentimiento_Negativo
            for sent in sentimientos_negativos:
                sent_text=sent.getElementsByTagName("palabra")
                for exprecion_positiva in sent_text:
                    nombre = doc.getElementsByTagName("palabra")[x].firstChild.data
                    self.mensajes_negativos.append(nombre)
                    x=x+1               
                    print("palabras_negativa:%s" % nombre)      #TODO: Resp_sent_Negativo
            x=0
            #!nombre
            for sent in empresa:
                nombre=sent.getElementsByTagName("nombre")[0].firstChild.data
                print("nombre_empresa:%s" % nombre)#TODO: nombre
            x=0
            #!servicio
            for sent in servicios:
                sent_text=sent.getElementsByTagName("alias")
                sent_text_id=sent.getAttribute("nombre")
                print("sent_text_id:%s" % sent_text_id)
                for exprecion_positiva in sent_text:
                    nombre = doc.getElementsByTagName("alias")[x].firstChild.data
                    x=x+1               
                    print("servicios:%s" % nombre)      #TODO: Resp_sent_positivo
                x=0

            #!mensaje
            for sent in mensaje:
                sent_text=sent.getElementsByTagName("mensaje")
                for exprecion_positiva in sent_text:
                    nombre = doc.getElementsByTagName("mensaje")[x].firstChild.data
                    self.mensaje_txt.append(nombre) 
                    x=x+1
                    print("mensaje:%s" % nombre)      #TODO: Resp_sent_positivo
            x=0  
        x=0 
        print("//////////")

    def lectura_de_texto(self):
        for mensaje in self.mensaje_txt:
            for mensaje_pos in self.mensajes_positivos:
                cantidad = mensaje.count(mensaje_pos.strip())
                self.contador_sentimientos_positivos_total= self.contador_sentimientos_positivos_total + cantidad 
        
            for mensaje_nega in self.mensajes_negativos:
                cantidad = mensaje.count(mensaje_nega.strip())
                self.contador_sentimientos_negativos_total= self.contador_sentimientos_negativos_total + cantidad


        if (self.contador_sentimientos_positivos_total == self.contador_sentimientos_negativos_total) or self.contador_sentimientos_positivos_total + self.contador_sentimientos_negativos_total ==0:
            self.contador_sentimientos_positivos_total=0
            self.contador_sentimientos_negativos_total=0
            self.contador_mensajes_neutros_total=self.contador_mensajes_neutros_total+1

        self.contador_mensajes_total = self.contador_mensajes_neutros_total+self.contador_sentimientos_negativos_total+self.contador_sentimientos_positivos_total
        retorno = "Contador_sent_pos: " + str(self.contador_sentimientos_positivos_total) + "\n"
        retorno = retorno + "Contador_sent_nega: " + str(self.contador_sentimientos_negativos_total)+ "\n"
        retorno = retorno + "Contador_sent_neutrales: " + str(self.contador_mensajes_neutros_total)+ "\n"
        retorno = retorno + "Contador_sent_Totales: " + str(self.contador_mensajes_total)+ "\n"
        return retorno



        
        

        


        

        




@app.route('/estudiante', methods=['GET','POST'])
def getEstudiante():
    if request.method == 'POST':
        string_xml= request.json.get("texto")
        nuevo_analizador =  analizardor()
        
        nuevo_analizador.analizador_xml(string_xml)
        valor = nuevo_analizador.lectura_de_texto()
       
        return jsonify({"texto":valor})
    else:
        estudiante = random.choice(listaEstudiates)
        return jsonify(estudiante)



if __name__ == '__main__':
    app.run(debug=True)














