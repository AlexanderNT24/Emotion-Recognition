import math

class AnalisisFacial:
     
    longitudes=None
    altoVentana=None
    anchoVentana=None
    listaPuntosFaciales=None
    longitudBoca=None
    longitudOjoIzquierdo=None
    longitudOjoDerecho=None
    longitudCejaIzquierda=None
    longitudCejaDerecha=None
    longitudBocaHorizontal=None
    emocion=None

    def __init__(self,listaPuntosFaciales,altoVentana,anchoVentana) :  
       self.listaPuntosFaciales=listaPuntosFaciales
       self.altoVentana=altoVentana
       self.anchoVentana=anchoVentana

    def getLongitudes(self):
        xpuntaRostro1,yPuntaRostro1=self.listaPuntosFaciales[93][1:]
        xpuntaRostro2,yPuntaRostro2=self.listaPuntosFaciales[323][1:]
        self.longitudRostro=math.hypot(xpuntaRostro1-xpuntaRostro2,yPuntaRostro1-yPuntaRostro2)
        #print(f"Longitud Rostro {longitudRostro}")
        #Trabajamos con proporciones 240 es el 100%
        porcentaje=self.longitudRostro/240
        #print(f"Porcentaje {int(porcentaje*100)}% Decimal {int(porcentaje*100)}")
        #print(f"Tamaño rostro proporcional {self.longitudRostro/porcentaje}")
        #Segun el identificador tomamos coordenadas en x,y ([n:] desde la posicion n en adelante)
        x1Boca,y1Boca=self.listaPuntosFaciales[13][1:]
        x2Boca,y2Boca=self.listaPuntosFaciales[14][1:]
        #Devuelve la norma de un vector es decir distancia entre dos puntos
        self.longitudBoca=abs(int(math.hypot(x2Boca-x1Boca,y2Boca-y1Boca)/porcentaje))
        #print(f"Longitud Boca:{self.longitudBoca}")
        x1OjoIzquierdo,y1OjoIzquierdo=self.listaPuntosFaciales[159][1:]
        x2OjoIzquierdo,y2OjoIzquierdo=self.listaPuntosFaciales[145][1:]
        #Devuelve la norma de un vector es decir distancia entre dos puntos
        self.longitudOjoIzquierdo=abs(math.hypot(x2OjoIzquierdo-x1OjoIzquierdo,y2OjoIzquierdo-y1OjoIzquierdo)/porcentaje)
        #print(f"Longitud Ojo Izquierdo:{self.longitudOjoIzquierdo}")
        x1OjoDerecho,y1OjoDerecho=self.listaPuntosFaciales[374][1:]
        x2OjoDerecho,y2OjoDerecho=self.listaPuntosFaciales[386][1:]
        #Devuelve la norma de un vector es decir distancia entre dos puntos
        self.longitudOjoDerecho=abs(math.hypot(x2OjoDerecho-x1OjoDerecho,y2OjoDerecho-y1OjoDerecho)/porcentaje)
        #print(f"Longitud Ojo Derecho:{self.longitudOjoDerecho}")
        xCejaIzquierda,yCejaIzquierda=self.listaPuntosFaciales[52][1:]
        self.longitudCejaIzquierda=abs(math.hypot(xCejaIzquierda-x1OjoIzquierdo,yCejaIzquierda-y1OjoIzquierdo)/porcentaje)      
        #print(f"Long ceja izquierda: {self.longitudCejaIzquierda}")
        xCejaDerecha,yCejaDerecha=self.listaPuntosFaciales[282][1:]
        self.longitudCejaDerecha=abs(math.hypot(xCejaDerecha-x2OjoDerecho,yCejaDerecha-y2OjoDerecho)/porcentaje)
        #print(f"Long ceja derecha: {longitudCejaDerecha}")
        #print(f"Ceja Derecha {escalaLongitudCejaDerecha} Ceja izquierda {escalaLongitudCejaIzquierda}")              
        xbocaIzq,yBocaIzq=self.listaPuntosFaciales[61][1:]
        xbocaDer,yBocaDer=self.listaPuntosFaciales[291][1:]
        self.longitudBocaHorizontal=abs(math.hypot(xbocaIzq-xbocaDer,yBocaIzq-yBocaDer)/porcentaje)
        #print(f" Boca {self.longitudBocaHorizontal}")
        coordenadaCentralX,coordenadaCentralY=self.listaPuntosFaciales[9][1:]
        coordenadaQuijadaX,coordenadaQuijadaY=self.listaPuntosFaciales[152][1:]
        eje=self.altoVentana-coordenadaCentralY
        rotacion="rotacion_nula"
        if (coordenadaCentralX-coordenadaQuijadaX)!=0:
            pendiente=(coordenadaCentralY-coordenadaQuijadaY)/(coordenadaCentralX-coordenadaQuijadaX)  
            if pendiente<-0.1 and pendiente>-4:
                rotacion="rotacion_izquierda"
            elif pendiente>0.1 and pendiente<4:
                rotacion="rotacion_derecha"   

        if self.longitudBoca<=8:
            escalaLongitudBoca="boca_cerrada"
        elif self.longitudBoca>8:
            escalaLongitudBoca="boca_abierta"   
 
        if self.longitudOjoIzquierdo<=10:
            escalaLongitudOjoIzquierdo="ojoI_cerrado" 
        elif  self.longitudOjoIzquierdo>10:  
             escalaLongitudOjoIzquierdo="ojoI_abierto"    

        if self.longitudOjoDerecho<=10:
            escalaLongitudOjoDerecho="ojoD_cerrado"  
        elif self.longitudOjoDerecho>10:  
             escalaLongitudOjoDerecho="ojoD_abierto"

        if self.longitudCejaDerecha<=35:
            escalaLongitudCejaDerecha="cejaD_normal"
        elif self.longitudCejaDerecha>35:    
            escalaLongitudCejaDerecha="cejaD_levantada"
        
        if self.longitudCejaIzquierda<=35:
            escalaLongitudCejaIzquierda="cejaI_normal"
        elif self.longitudCejaIzquierda>35:    
            escalaLongitudCejaIzquierda="cejaI_levantada"  
        
        longitudesEscala=[escalaLongitudBoca,escalaLongitudOjoIzquierdo,escalaLongitudOjoDerecho,escalaLongitudCejaIzquierda,escalaLongitudCejaDerecha,self.getEmocion(),rotacion]
        #print(f"Estado: Boca({longitudesEscala[0]}) Ojo Izquierdo({longitudesEscala[1]}) Ojo Derecho({longitudesEscala[2]})")
        longitudesEscala=str(longitudesEscala).replace("[","")
        longitudesEscala=longitudesEscala.replace("]","")
        longitudesEscala=longitudesEscala.replace("'","")
        longitudesEscala=longitudesEscala.replace(",","")
        longitudesEscala=longitudesEscala.replace(" ","\n")
        return longitudesEscala,self.getEmocion()

    def getEmocion(self):
        #print(f"Ceja derecha: {self.longitudCejaDerecha}")
        #print(f"Ceja derecha: {self.longitudCejaIzquierda}")
        #print(f"Boca: {self.longitudBoca}")  
        self.emocion="emocion_neutro" 
        #Enojo
        if (self.longitudCejaDerecha<=24 or self.longitudCejaIzquierda<=24) and (self.longitudBoca<=7) and (self.longitudOjoIzquierdo<=14 or self.longitudOjoDerecho<=14):
            self.emocion="emocion_enojo"

        #Felicidad
        if (self.longitudCejaDerecha>26 and self.longitudCejaDerecha<=37 and self.longitudBocaHorizontal>100) or (self.longitudCejaIzquierda>26 and self.longitudCejaIzquierda<=37 and self.longitudBocaHorizontal>100):
            self.emocion="emocion_feliz"
       
        #Asombro
        if (self.longitudCejaDerecha>37 and self.longitudBoca>=9) or (self.longitudCejaIzquierda>37 and self.longitudBoca>=9):
            self.emocion="emocion_asombro"
    
        #print(f"La emocion es :{self.emocion}")
        return self.emocion
