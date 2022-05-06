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
        self.fecha_total=""


        self.mensajes_positivos=[]
        self.mensajes_negativos=[]
        self.mensaje_txt=[]
        self.empresas=[]
        self.servicios=[]
        self.servicios_id=[]
        

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
            
            #!Sentimiento_Negativo
            for sent in sentimientos_negativos:
                sent_text=sent.getElementsByTagName("palabra")
                for exprecion_negativa in sent_text:
                    nombre = doc.getElementsByTagName("palabra")[x].firstChild.data
                    self.mensajes_negativos.append(nombre)
                    x=x+1               
                    print("palabras_negativa:%s" % nombre)      #TODO: Resp_sent_Negativo
            x=0
            #!nombre_empresa
            for sent in empresa:
                sent_text=sent.getElementsByTagName("nombre")
                for exprecion_positiva in sent_text:
                    nombre = doc.getElementsByTagName("nombre")[x].firstChild.data
                    self.empresas.append(nombre)
                    x=x+1               
                    print("nombre:%s" % nombre)#TODO: nombre_empresa
            x=0
            #!servicio
            for sent in servicios:
                
                sent_text=sent.getElementsByTagName("alias")
                sent_text_id=sent.getAttribute("nombre")
                self.servicios_id.append(sent_text_id)
                print("sent_text_id:%s" % sent_text_id)
                for exprecion_positiva in sent_text:
                    print(x)
                    nombre = doc.getElementsByTagName("alias")[x].firstChild.data
                    self.servicios.append(nombre)
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


    def lectura_individual(self):
        retorno=""
        
        for empresa in self.empresas:               #?Empresas
            #print(empresa)
            num_total_por_mensaje_positivo=0
            num_total_por_mensaje_negativo=0
            num_total_por_mensaje_neutro=0
            num_menciones_servicio=0
            iteracion=0
            retorno=retorno+  "\t"+"<empresa nombre=\""+empresa+"\">" + "\n"
            retorno=retorno+   "\t"+"\t"+"<mensajes>" + "\n"
            for mensaje in self.mensaje_txt:        #?mensajes_emocion
                iteracion=iteracion+1
                for mensaje_pos in self.mensajes_positivos:
                    cantidad = mensaje.count(mensaje_pos.strip())
                    num_total_por_mensaje_positivo=num_total_por_mensaje_positivo+cantidad
        
                for mensaje_nega in self.mensajes_negativos:
                    #print(self.mensajes_negativos)
                    cantidad = mensaje.count(mensaje_nega.strip())
                    num_total_por_mensaje_negativo=num_total_por_mensaje_negativo+cantidad

                if (num_total_por_mensaje_positivo == num_total_por_mensaje_negativo) or num_total_por_mensaje_positivo + num_total_por_mensaje_negativo ==0:
                    num_total_por_mensaje_positivo=0
                    num_total_por_mensaje_negativo=0
                    num_total_por_mensaje_neutro=num_total_por_mensaje_neutro+1
                

                retorno=retorno+ "\t"+ "\t"+ "\t" +"<positivos No.Mensaje: "+str(iteracion)+">"+ str(num_total_por_mensaje_positivo) +"</positivos>" + "\n"
                retorno=retorno+  "\t"+ "\t"+ "\t"+ "<negativo No.Mensaje: "+str(iteracion)+">"+ str(num_total_por_mensaje_negativo) +"</negativo>" + "\n"
                retorno=retorno+  "\t"+ "\t"+ "\t"+ "<neutro No.Mensaje: "+str(iteracion)+">"+ str(num_total_por_mensaje_neutro) +"</neutro>" + "\n"
                retorno=retorno+  "\t"+ "\t"+ "</mensajes>" + "\n"
                retorno=retorno+  "\t"+ "\t"+ "<mensajes>" + "\n"
                num_total_por_mensaje_positivo=0
                num_total_por_mensaje_negativo=0
                iteracion=0
            retorno=retorno+self.lecutra_servicios()
        return retorno 
        

    def lecutra_servicios(self):
        retorno=""
        contador=0
        num_menciones_servicio=0
        for mensaje in self.mensaje_txt:
            
            for servicio in self.servicios_id:        #?Servicios
                contador=contador+1
                retorno=retorno+"\t"+"\t"+ "\t"+"\t"+ "<servicio nombre=\""+servicio+"\">" + "\n"
                print("////////////////////////////////////")
                    
            for alia in self.servicios:
                        
                    cantidad = mensaje.count(alia.strip())
                     
                    num_menciones_servicio=num_menciones_servicio+cantidad
                        
                    print(mensaje)
                    print(alia)
                    print(cantidad)
                    
                

            retorno=retorno+ "\t"+"\t"+"\t"+"\t" + "\t" +"<Total del mensaje>"+ str(num_menciones_servicio) +"</Total>" + "\n"
        contador=0
        return retorno

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
        pattern = '\d+'
        match = re.search(r'(\d+/\d+/\d+)', mensaje)
        fecha=match.group(1)
        






        #!xml
        self.contador_mensajes_total = self.contador_mensajes_neutros_total+self.contador_sentimientos_negativos_total+self.contador_sentimientos_positivos_total
        retorno="<?xml version=\"1.0\"?>"  + "\n"
        retorno=retorno+"<lista_respuestas>"  + "\n"
        retorno=retorno+"<respuesta>"  + "\n"
        retorno=retorno+"<fecha>" +fecha+ "</fecha>" + "\n"
        retorno=retorno+" <mensajes>" + "\n"
        retorno = retorno + "<total>" + str(self.contador_mensajes_total)+ "</total>" "\n"
        retorno = retorno+ "<positivos>" + str(self.contador_sentimientos_positivos_total) + "</positivos> \n"
        retorno = retorno + "<negativos>" + str(self.contador_sentimientos_negativos_total)+ "</negativos> \n"
        retorno = retorno + "<neutros>" + str(self.contador_mensajes_neutros_total)+ "</neutros> \n"
        retorno=retorno+" </mensajes>" + "\n"
        retorno=retorno+" <analisis>" + "\n"
        retorno=retorno+ self.lectura_individual()
        retorno=retorno+ "\t"+"\t"+"\t"" </mensaje>" + "\n"
        retorno=retorno+ "\t"+"\t"" </empresa>" + "\n"
        retorno=retorno+ "\t"+" </analisis>" + "\n"
        retorno=retorno+" </respuesta>" + "\n"
        retorno=retorno+" </lista_respuesta>" + "\n"

        
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














