finalData = []
backupString = []
import math
#import astropy
#zampar radianes, esta función convierte a radiantes tanto la declinación como la ascensión recta. Se divide dentro de 15 la salida de la función para hacer ascensión recta
def radian(hourTemp):
    radianOut = 15*math.pi*hourTemp/180
    return radianOut
#diferencia de pasos, se restan los puntos inicial y final para el desplazamiento
def coorSubstract(ascF,ascI,decF,decI,sign):
    if sign == "+": #movimiento en sentido positivo
        finalStep = [(ascF-ascI),(decF-decI)]
    elif sign == "-": #movimiento en sentido negativo
        finalStep = [(ascF-ascI),(decF-decI)]
    if finalStep[0] <= 0: #movimiento en sentido positivo
        finalStep.append("-")
        finalStep[0] = finalStep[0]*-1
    else:
        finalStep.append("+") #movimiento en sentido negativo
    if finalStep[1] <= 0:
        finalStep.append("-")
        finalStep[1] = finalStep[1]*-1
    else:
        finalStep.append("+")
    return finalStep
#Llenado de ceros en string, esta rutina hace que los números tengan los mismos dígitos, llenando con ceros los que falten a la izquierda
def fillZeros(number,length): #pide el número y la longitud del número final
    counter = len(str(number))
    x = 0
    backupString = ""
    while x < (length - counter):
        backupString = backupString + "0"
        x = x+1
    backupString = backupString + str(number)
    return backupString
#Conversión ascensión recta Esto convierte la ascensión recta a grados o a horas, dependiendo de selec
def rectaConver(hora,minut,segundos,selec): #selec = 1 pasa a grados, selec = 2 pasa a horas
    minutTemp = float(minut) + float(segundos)/60
    horaTemp = float(hora) + float(minutTemp)/60
    if selec == 1:
        degFinal = float(horaTemp)*15
    elif selec == 2:
        degFinal = float(horaTemp)
    return degFinal
#conversor de declinación, convierte la declinación a grados
def decliConver(deg,minutes,second):
    minutesTemp = float(minutes) + float(second)/60
    degFinal = float(deg) + float(minutesTemp)/60
    return degFinal
#conversor a pasos del stepper, pasos del stepper
def pasos(grados,motor): #1 es ascensión recta, 2 es declinación
    if motor == 1:
        finalSteps = grados*96/0.8
    elif motor ==2:
        finalSteps = grados*20/0.8
    return finalSteps
#FUNCION PARA CONVERTIR DE ECUATORIALES A HORIZONTALES, SOLO TENELE FE
def horizontal(latitude,rightAsc,dec,decSign):
    if decSign == "-":
        dec = dec*-1
    param1 = math.sin(dec)*math.sin(latitude)+math.cos(dec)*math.cos(latitude)*math.cos(rightAsc)
    altitude = math.asin(param1)
    param2 = (math.sin(dec)-math.sin(latitude)*math.sin(altitude))/(math.cos(latitude)*math.cos(altitude))
    azimut = math.acos(param2)
    #param2 = -1*math.sin(rightAsc)*math.cos(dec)/math.cos(altitude)
    #azimut = math.asin(param2)
    altitudeDeg = altitude*180/math.pi
    #print decSign
    if rightAsc >= 0:
        azimutDeg = azimut*180/math.pi
    elif rightAsc < 0:
        azimutDeg = 360 - azimut*180/math.pi
    #print azimutDeg
    coordinates = [altitudeDeg,azimutDeg]
    print coordinates
    return coordinates
#lectura del archivito de texto
def readTxt(nameStar):
    fileRead=open('Lista Estrellas.txt','r')
    lineRead = fileRead.readline()
    ban = 0
    while lineRead !="":
            lineRead = lineRead.rstrip("\n")
            #print lineRead
            dataTemp = lineRead.split(',')
            #print dataTemp
            if nameStar.lower() == dataTemp[0].lower():
                ban = 1
                for x in range(1,8):
                    finalData.append(dataTemp[x])
                lineRead = ""
            else:
                lineRead = fileRead.readline()
            
    fileRead.close()
    if ban == 0:
        finalData.append("nada")
    return finalData
ascHome = pasos(42.625,1)
decHome = pasos(89.328,2)
prevAsc = ascHome
prevDec = decHome
#ascTest = rectaConver(12,30,30,2)
latitude = 14.613333*math.pi/180
#print ascTest
#prueba1 = fillZeros(1)
#prueba = fillZeros(35)
#prueba2 = fillZeros(353)
#prueba3 = fillZeros(5514)
#prueba4 = fillZeros(12345)
#print prueba + " " + prueba1 + " " + prueba2 + " " + prueba3 + " " + prueba4
#test = cuadrantes(5)
#print test
while True:
    nombreEstrella = raw_input("Ingrese el nombre de la estrella a ubicar\n")
    coorEstrella = readTxt(nombreEstrella)
    #print coorEstrella
    if coorEstrella[0] == "nada":
        print("No se encuentra dentro de la base de datos")
    else:
        #print(coorEstrella)
        siderHoras = raw_input("Ingrese la hora de la hora sideral")
        siderMinutos = raw_input("Ingrese los minutos de hora sideral")
        siderSegundos = raw_input ("Ingrese los segundos")
        tiempoSideral = rectaConver(siderHoras,siderMinutos,siderSegundos,2)
        absoluteAscention = rectaConver(coorEstrella[0],coorEstrella[1],coorEstrella[2],2)
        horaSideral = tiempoSideral - absoluteAscention
        #print horaSideral
        radianSideral = radian(horaSideral)
        radianDecli = radian(decliConver(coorEstrella[4],coorEstrella[5],coorEstrella[6])/15)
        #print radianSideral
        #print radianDecli
        #coordenadas horizontales
        horizontales = horizontal(latitude,radianSideral,radianDecli,coorEstrella[3])
        #print horizontales
        #trama en ecuatoriales
        currentDec = pasos(decliConver(coorEstrella[4],coorEstrella[5],coorEstrella[6]),2)
        currentAsc = pasos(rectaConver(coorEstrella[0],coorEstrella[1],coorEstrella[2],1),1)
        finalSteps = coorSubstract(currentAsc,prevAsc,currentDec,prevDec,coorEstrella[3])
        tramaFinal = "a"+"," + (finalSteps[2]) + "," + fillZeros(int(finalSteps[0]),5)+","+"b"+","+str(finalSteps[3])+","+fillZeros(int(finalSteps[1]),5)
        prevAsc = currentAsc
        prevDec = currentDec
        #print tramaFinal
    del coorEstrella[:]
