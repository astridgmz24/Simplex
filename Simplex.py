#24 ene
import numpy as np
import os
np.set_printoptions(suppress=True)

def Portada():
    print("          Universidad Nacional Autonoma de Mexico")
    print("             Optimizacion 1")
    print("             Metodo Simplex \n")

    print("          Gomez Gonzalez Astrid Yoatziry")
    print("           Navarro Ramos Karen Lizbeth")
    input("\n Presiona una tecla para continuar...")
    os.system("cls")

def Instrucciones():
    print(" \n\nInstrucciones:")
    print("1. Ingresar total de variables")
    print("2. Ingresar total de restricciones")
    print("3. Maximizar o Minimizar")
    print("  Maximizar=max Minimizar=min")
    print("4. Vector Funcion Objetivo")
    print("5. Restricciones")
    print("  No es necesario ingresar la no negatividad")
    input("\n Presiona una tecla para continuar...")
    os.system("cls")

def LeerFOB(c):
    FUNOBJ=np.zeros(c)
    for m in range (0,c):
        FUNOBJ[m]=input("X"+str(m+1)+": ")
    #Cambio signos
    if MAXMIN=="max":
        FUNOBJ=FUNOBJ
    elif MAXMIN=="min":
        FUNOBJ=FUNOBJ*-1
    return FUNOBJ

def Leer(r,c):
    MAT=np.zeros((r,c))
    LD=np.zeros(r+1)
    SGN=[None]*r 

    for n in range (0,r):
        print("\n Restriccion "+str(n+1))
        for m in range (0,c):
            MAT[n,m]=input("X"+str(m+1)+": ")

    #Validar entrada de signo
        while True: 
            SGN[n]=str(input("Signo ('<=' '>=' '='): "))
            if SGN[n]=='<=' or SGN[n]=='>=' or SGN[n]=='=':
                break
            else:
                print("Entra invalida. Ingrese nuevamente...")
        LD[n+1]=input("LD: ")

    return MAT, LD, SGN

def Factibilidad(r):
    a=0
    for i in range (0,r):
        if LD[i]<0:
            a=a+1
        else:
            a=a
        if a==0:
            return True
        else:
            return False

def Revision(r):
    a=0
    for i in range (0,r):
        if SGN[i]=="<=":
            a=a
        else:
            a=a+1

    if a==0:
        return "Facil"
    else:
        return "Dificil"

def CrearMaV(r):
    MATs=np.zeros((r+1,r))
    MATa=np.zeros((r+1,r))

    for i in range (0,r):
        if SGN[i]=="<=":
            MATs[i+1,i]=1
        elif SGN[i]==">=":
            MATs[i+1,i]=-1
            MATa[0,i]=-M
            MATa[i+1,i]=1
        else:
            MATa[0,i]=-M
            MATa[i+1,i]=1
    #Eliminar columnas de MATs
    numfil= len(MATs)    #Numero de filas en matriz s 
    numcol= len(MATs[0]) #Numero de columnas en matriz a
    nueva_fila=[]
    for j in range(numcol):
        sumacols= sum([numfil[j] for numfil in MATs]) #sumar columnas
        nueva_fila.append(sumacols)
    for k in range(numcol):
        if nueva_fila[k]==0:
            MATs=np.delete(MATs, k, axis=1)

    #Eliminar columnas de MATa
    numfila= len(MATa)    #Numero de filas en matriz s 
    numcola= len(MATa[0]) #Numero de columnas en matriz a
    nueva_filaa=[]
    for f in range(numcola):
        sumacola= sum([numfila[f] for numfila in MATa]) #sumar columnas
        nueva_filaa.append(sumacola)
    for h in range(numcola):
        if nueva_filaa[h]==0:
            MATa=np.delete(MATa, h, axis=1)
    return MATs, MATa

def VecBN(COL):
    #No Basicos
    VNB=np.zeros((COL,1))
    k=1
    for i in range (0,COL):
        VNB[i]=k
        k=k+1

    #Basicos
    MATz=np.hstack((MATs, MATa))
    CZ=len(MATz)
    VB=np.zeros((TOTSA,1))
    for n in range (1,TOTSA+1): #renglon
        for m in range (0,CZ):#columna
            if MATz[n,m]==1:
                VB[n-1]=TOTVAR+m+1

    return(VNB, VB)

def CrearTableau(r,c):
    LDT=np.zeros((r,1))
    TABLEAU=np.vstack((FUNOBJ, MAT))
    TABLEAU=np.hstack((TABLEAU, MATs))

    if FASE=="Dificil":
        TABLEAU=np.hstack((TABLEAU, MATa))
            
    for i in range (0,r):
        LDT[i,0]=LD[i]
    TABLEAU=np.hstack((TABLEAU, LDT))

    SHAPE=TABLEAU.shape
    ROW=SHAPE[0]
    COL=SHAPE[1]
    return TABLEAU, ROW, COL

def ElegirM():
    a=np.amax(MAT)
    b=np.amax(LD)
    c=np.amax(FUNOBJ)
    big=max(a,b,c)
    M=big*100
    return int(M)

def BigM(r,c):
    COPIA=TABLEAU.copy()
    for i in range (1,r):
        SUMA=sum(MATa[i])
        if SUMA >0:
            TABLEAU[0,:]=TABLEAU[0,:]+(M*COPIA[i,:])
    return TABLEAU

def Simplex(r,c):
    global TABLEAU
    global VB
    global VNB
    while True:
        MAY=TABLEAU[0,:c-1].argmax()
        NUM=TABLEAU[0,:c-1].max()
    
        TABLEAU=TABLEAU.astype(float)
        if NUM<=0:
            #print("OPTIMO")
            break
        else:
            DIV=TABLEAU[1:,c-1]/TABLEAU[1:,MAY]
            DIV=DIV.astype(float)
        
            for j in range (0,r-1):
                if DIV[j]<0:
                    DIV[j]=M
        
            MEN=DIV.argmin()+1
        
        #Siguiente Iteracion
            print("Siguiente Iteracion:")
            COPIA=TABLEAU.copy()
            TABLEAU[MEN,:]=COPIA[MEN,:]/COPIA[MEN,MAY]
            for i in [x for x in range(0,r) if x != MEN]:
                TABLEAU[i,:]=COPIA[i,:]-COPIA[i,MAY]*TABLEAU[MEN,:]
            VB[MEN-1]=VNB[MAY]

            RESULTADO=TABLEAU.copy()
            print(RESULTADO)
    return RESULTADO, VB


#MAIN////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
Portada()
Instrucciones()

TOTVAR=int(input("\n\n\nTotal de Variables: ")) #Columnas m c
TOTSA=int(input("Total de Restricciones: ")) #Renglones n r 

#Leer Funcion Objetivo
print("\n ->Funcion Objetivo:")
while True:
    MAXMIN=input("Maximizar o Minimizar (max/min): ")
    MAXMIN = MAXMIN.lower()
    if MAXMIN=='max' or MAXMIN=='min':
        break
    else:
        print("Entrada invalida ----> Debería ser: max o min")
        print("Ingrese nuevamente...")
FUNOBJ=LeerFOB(TOTVAR)

#Leer Restricciones
print(" \n -> Sujeto a:")
MAT, LD, SGN=Leer(TOTSA, TOTVAR)

#Factibilidad y Fase
FAC=Factibilidad(TOTSA+1)
FASE=Revision(TOTSA)

if FAC==True:
    M=ElegirM()
    #Matriz Holgura y artificiales
    MATs, MATa=CrearMaV(TOTSA)
    #Tableau
    TABLEAU, ROW, COL=CrearTableau(TOTSA+1, (TOTVAR+(2*TOTSA)+1))
    print("\n\n\nTableau:")
    print(TABLEAU)
    
    if FASE=="Dificil":
        TABLEAU=BigM(ROW,COL)
    
    #Vectores Basicos y No Basicos
    VNB, VB=VecBN(COL)
    #SIMPLEX :)
    print("\n\n\nSIMPLEX")
    TABLEAU=TABLEAU.astype(float)
    RESULTADO, VB=Simplex(ROW, COL)


    print("\n\n\nSOLUCION OPTIMA: ")
    print(RESULTADO)

    resu= RESULTADO[0,COL-1]
    resuF= resu*-1
    print("Funcion Objetivo= ", resuF)
    
    print("\nVariables Basicas")
    FINAL=np.zeros((TOTSA,1))
    for k in range (1,ROW):
        FINAL[k-1]=RESULTADO[k,COL-1]
    NOMBRE=np.zeros((TOTSA,1))
    NOMBRE=NOMBRE.astype(str)
    for j in range (0, TOTSA):
        NOMBRE[j]="X"+str(VB[j])+"->"+str(FINAL[j])
    print(NOMBRE)
    
else:
    print("Problema NO FACTIBLE, en LD existen negativos")

input()#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
'''NOTAS:
TOTVAR: total de variables (int)
TOTSA: total de restricciones (int)
MAXMIN: si es maximizar o minimizar (string)

FUNOBJ: vector funcion objetivo
MAT: matriz coeficientes de restricciones
LD: vector lado derecho
SGN: vector signos de restricciones
TABLEAU: matriz todo unido

MATs: matriz de "s", variables de holgura
MATa: matriz de "a", variables artificiales

M=bigM
FAC= revisar si es factible o no (boolean)
FASE= si todos son menor o igual que o no 
ROW, COL= renglones y columnas totales del tableau 

RESULTADO= Tabla con el optimo
VNB=vector no basico
VB= vector basico
'''