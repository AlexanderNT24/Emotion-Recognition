import cv2 #Opencv
import mediapipe as mp #Google
import time
import matplotlib.pyplot as plt

from Captura import Captura
from MallaFacial import MallaFacial
from AnalisisFacial import AnalisisFacial
from Conexion import Conexion

def main():
    #tipoEntrada=input("Entrada video:")
    tipoEntrada="webcam"
    objetoCaptura=Captura(tipoEntrada)
    captura=objetoCaptura.getCaptura()
    objetoMallaFacial=MallaFacial()
    mediapMallaFacial,mallaFacial=objetoMallaFacial.getMallaFacial()
    mediapDibujoPuntos,dibujoPuntos=objetoMallaFacial.getPuntosMallaFacial()   
    analisisVideo(captura,mediapDibujoPuntos,dibujoPuntos,mediapMallaFacial,mallaFacial) 
    
def analisisVideo(captura,mediapDibujoPuntos,dibujoPuntos,mediapMallaFacial,mallaFacial):
    vectorEstado=[]
    verMalla=False
    while True:
        #Lectura de frame y el estado (En Python puedo asignar datos a variables de la siguiente forma var1,var2=1,2) 
        estado,frame=captura.read()
        #Efecto espejo
        frame=cv2.flip(frame,1)
        #Procesa el fotograma para entreganos la malla facial
        resultados=mallaFacial.process(frame)
        listaPuntosFaciales=[]
        #Si encuentra un rostro        
        if resultados.multi_face_landmarks:
            #Para todos los rostros detectados
            for rostros in resultados.multi_face_landmarks:
                #Dibujamos las conecciones de la malla
                if verMalla:
                    mediapDibujoPuntos.draw_landmarks(frame,rostros,mediapMallaFacial.FACEMESH_CONTOURS,dibujoPuntos,dibujoPuntos)
                #Puntos rostro detectado
                for puntoID,puntos in enumerate (rostros.landmark):
                    #Alto y ancho de la ventana
                    altoVentana, anchoVentana,variable=frame.shape
                    posx=int(puntos.x*anchoVentana)
                    posy=int(puntos.y*altoVentana)
                    #print(f"alto{altoVentana} ancho {anchoVentana}")
                    #Apilamos los puntos faciales en una lista con sus coordenadas
                    listaPuntosFaciales.append([puntoID,posx,posy])
                    if len(listaPuntosFaciales)==468:
                        objetoAnalisisFacial=AnalisisFacial(listaPuntosFaciales,altoVentana,anchoVentana)
                        objetoConexion=Conexion(str(objetoAnalisisFacial.getLongitudes()[0]))
                        objetoConexion.enviarDatos()
                        mostrarEjesRotacion(listaPuntosFaciales,frame,altoVentana)
                        vectorEstado.append(str(objetoAnalisisFacial.getLongitudes()[1]).replace("emocion_",""))  
                        time.sleep(0.1)    
                          
        cv2.imshow("Analisis Facial Python",frame)
        tecla = cv2.waitKey(1) & 0xFF
        if tecla==ord('q'):
            verMalla=True
        elif tecla==ord('w'):  
            verMalla=False
        #Codigo Ascii ESC es 27 para cerrar frame
        elif tecla==27:
            break
    #Destruimos cada ventana creada por opencv 
    cv2.destroyAllWindows() 
    analizarDatos(vectorEstado)
               
def analizarDatos(vectorEstado):
    plt.plot(vectorEstado)
    plt.title('EMOCIONES')
    plt.xlabel('TIEMPO')
    plt.ylabel('EMOCIÓN')
    plt.show()

def mostrarEjesRotacion(listaPuntosFaciales,frame,altoVentana):
    coordenadaCentralX,coordenadaCentralY=listaPuntosFaciales[9][1:]
    coordenadaQuijadaX,coordenadaQuijadaY=listaPuntosFaciales[152][1:]
    cv2.line(frame,pt1=(coordenadaCentralX,coordenadaCentralY),pt2=(coordenadaCentralX,altoVentana),color=(0,0,255))
    cv2.line(frame,pt1=(coordenadaCentralX,coordenadaCentralY),pt2=(coordenadaQuijadaX,coordenadaQuijadaY),color=(0,0,255))

#Buena practica de programacion en python (Python ejecuta todos los modulos cargados en orden descendente y declara variables internas __name__ se le declara como main al modulo que se encarga de "correr", al trabajar con esta condicional )
if __name__ == "__main__":
    main()
