import cv2 #Opencv
import mediapipe as mp #Google
import time
import matplotlib.pyplot as plt
import numpy as np

from Captura import Captura
from MallaFacial import MallaFacial
from AnalisisFacial import AnalisisFacial

def main():
    #tipoEntrada=input("Entrada video:")
    type_video_input="webcam"
    capture_object=Captura(type_video_input)
    capture=capture_object.getCaptura()
    face_mesh_object=MallaFacial()
    mediap_face_mesh,face_mesh=face_mesh_object.getMallaFacial()
    mediap_draw_points,draw_points=face_mesh_object.getPuntosMallaFacial()   
    analize_video(capture,mediap_draw_points,draw_points,mediap_face_mesh,face_mesh) 
    
def analize_video(capture,mediap_draw_points,draw_points,mediap_face_mesh,face_mesh):
    estate_array=[]
    show_mesh=False
    while True:
        #Lectura de frame y el estado (En Python puedo asignar datos a variables de la siguiente forma var1,var2=1,2) 
        estate,frame=capture.read()
        #Efecto espejo
        frame=cv2.flip(frame,1)
        #Procesa el fotograma para entreganos la malla facial
        results=face_mesh.process(frame)
        listaPuntosFaciales=[]
        #Si encuentra un rostro        
        if results.multi_face_landmarks:
            #Para todos los rostros detectados
            for rostros in results.multi_face_landmarks:
                #Dibujamos las conecciones de la malla
                if show_mesh:
                    mediap_draw_points.draw_landmarks(frame,rostros,mediap_face_mesh.FACEMESH_CONTOURS,draw_points,draw_points)
                #Puntos rostro detectado
                for puntoID,puntos in enumerate (rostros.landmark):
                    #Alto y ancho de la ventana
                    altoVentana, anchoVentana,variable=frame.shape
                    posx=int(puntos.x*anchoVentana)
                    posy=int(puntos.y*altoVentana)
                    #Apilamos los puntos faciales en una lista con sus coordenadas
                    listaPuntosFaciales.append([puntoID,posx,posy])
                    if len(listaPuntosFaciales)==468:
                        facial_analysis_object=AnalisisFacial(listaPuntosFaciales,altoVentana,anchoVentana)
                        show_rotation_axes(listaPuntosFaciales,frame,altoVentana)
                        show_emotion_text(frame,facial_analysis_object.getLongitudes()[1].replace("emocion_",""))
                        estate_array.append(str(facial_analysis_object.getLongitudes()[1]).replace("emocion_",""))  
                        time.sleep(0.1)    
                          
        cv2.imshow("Analisis Facial Python",frame)
        key = cv2.waitKey(1) & 0xFF
        if key==ord('q'):
            show_mesh=True
        elif key==ord('w'):  
            show_mesh=False
        #Codigo Ascii ESC es 27 para cerrar frame
        elif key==27:
            break
    #Destruimos cada ventana creada por opencv 
    cv2.destroyAllWindows() 
    analyze_data(estate_array)
               
def analyze_data(vectorEstado):
    tiempo = np.arange(len(vectorEstado)) + 1
    plt.plot(tiempo,vectorEstado)
    plt.title('EMOCIONES')
    plt.xlabel('TIEMPO')
    plt.ylabel('EMOCIÓN')
    plt.show()

def show_rotation_axes(listaPuntosFaciales,frame,altoVentana):
    coordenadaCentralX,coordenadaCentralY=listaPuntosFaciales[9][1:]
    coordenadaQuijadaX,coordenadaQuijadaY=listaPuntosFaciales[152][1:]
    cv2.line(frame,pt1=(coordenadaCentralX,coordenadaCentralY),pt2=(coordenadaCentralX,altoVentana),color=(0,0,255))
    cv2.line(frame,pt1=(coordenadaCentralX,coordenadaCentralY),pt2=(coordenadaQuijadaX,coordenadaQuijadaY),color=(0,0,255))

def show_emotion_text(frame,text):
    posicion = (20, 20) 
    fuente = cv2.FONT_HERSHEY_SIMPLEX
    escala_fuente = 1
    if text=="neutro":
        color = (76,76,76) 
    elif text=="enojo":
        color = (0,0,255) 
    elif text=="feliz":
        color = (0,255,0) 
    elif text=="asombro":
        color = (0,255,255)     
    cv2.putText(frame, text, posicion, fuente, escala_fuente, color, thickness=2)


#Buena practica de programacion en python (Python ejecuta todos los modulos cargados en orden descendente y declara variables internas __name__ se le declara como main al modulo que se encarga de "correr", al trabajar con esta condicional )
if __name__ == "__main__":
    main()
