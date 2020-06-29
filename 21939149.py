"""Ejecicio extraordinario Programacion Concurrente y Distribuida
   Autor: Pablo Pascual Garcia
   Num.Expediente: 21939149"""

import math
import random
import multiprocessing as mp
import time

#Funcion MergeSort que ordena el array de forma no paralela
def mergeSort(array):
    tam=len(array)#tamaño del array
    #Si el tamaño del array es menor o igual a 1 estará ordenado
    if tam<=1:
        return array
    #Dividimos en dos mitades el array(izquierda y derecha)
    mitad=tam//2
    der=mergeSort(array[mitad:])
    izq=mergeSort(array[:mitad])
    return merge(izq,der)#realizamos el algoritmo de ordenacion

#Funcion la cual usa el mergeSort tanto para el lado derecho como el lado izquierdo
#El argumento *args nos permitirá pasar un numero variable de argumentos
def merge(*args):
    izq,der=args[0] if len(args) == 1 else args
    longIzq=len(izq)
    longDer=len(der)
    indiceIzq=0
    indiceDer=0
    mezcla=[]
    #El bucle irá comparando que valores de las mitades los cuales tendrán un indice para saber
    #su posición y en el caso de que sea menor se añadirá el valor en una lista, la cual
    #una vez terminada de recorrer una de las mitades se concatenará
    while indiceDer<longDer and indiceIzq<longIzq:
        if der[indiceDer]>=izq[indiceIzq]:
            mezcla.append(izq[indiceIzq])
            indiceIzq=indiceIzq+1
        else:
            mezcla.append(der[indiceDer])
            indiceDer=indiceDer+1
    if longIzq == indiceIzq:
        mezcla.extend(der[indiceDer:])
    else:
        mezcla.extend(izq[indiceIzq:])
    return mezcla

#Funcion mergeSort la cual paraleliza el proceso del algoritmo con todos los nucleos de nuestro procesador
def mergeSortP(array):
    #Sacamos el numero de cores del pc
    numCores = mp.cpu_count()
    #Creamos un grupo de trabajo, de tamaño igual y que tenga una distribucion
    #de trabajo igual o similar al los demas
    grupoTrabajo = mp.Pool(processes=numCores)
    tamTrabajo = int(math.ceil(float(len(array))/numCores))
    array = [array[i * tamTrabajo:(i + 1) * tamTrabajo] for i in range(numCores)]
    #Realizamos el mergesort en cada una de las particiones de distribución
    #del trabajo realizadas anteriormente
    array = grupoTrabajo.map(mergeSort, array)
    #Combinamos las particiones ordenadas utilizando la funcion pool, hasta que se reduzca a un array
    while len(array) > 1:
        #Como solo nos interesa que el numero de particiones sea par, en caso contrario sacamos del array
        #el ultimo numero y lo agragamos despues de la iteracion
        extra = array.pop() if len(array) % 2 == 1 else None
        array = [(array[i], array[i + 1]) for i in range(0, len(array), 2)]
        array = grupoTrabajo.map(merge, array) + ([extra] if extra else [])
    return array[0]

#Funcion que hace Fibonacci de forma recurrente
def fibR(num):
    if num<=1: 
        return num
    else: 
        return fibR(num-1)+fibR(num-2)

#Funcion que hace Fibonacci de forma paralela
def fibP(num):
    numCores = mp.cpu_count()#Sacamos el numero de nucleos del ordenador
    #Se reparten las tareas de la forma que hemos especificado en la memoria
    tareas = [num-3, num-4, num-4, num-4, num-5, num-5, num-5, num-6]
    resultados = mp.RawArray('i', numCores)#Array de memoria compartida donde se almacenaran los resultados
    cores = []#Aqui guardamos la tarea de cada nucleo
    for core in range(numCores):  #Se le da a cada nucleo su tarea
        #Se guarda la tarea de cada nucleo en el array
        cores.append(mp.Process(target=tareaCore, args=(core, tareas[core], resultados)))
    #Iniciamos las tareas que cada uno de los nucleos debe realizar
    for core in cores:
        core.start()
    #Bloqueamos llamadas hasta que los nucleos terminen sus tareas
    for core in cores:
        core.join()
    #Obtenemos los numeros que debía obtener cada tarea y los sumamos para obtener el numero requerido
    numF=0
    for i in resultados:
        numF=numF+i
    return numF

#Funcion que hace la tarea de cada nucleo
def tareaCore(indice, tarea, resultado):
    resultado[indice] = fibR(tarea)

#Este es el main el cual nos ejecutará un login y en el caso de que sea correcto
#podremos probar nuestros ejercicios(1.MergeSort y 2.Fibonacci)
#Para hacer el login email=email y contraseña=email
if __name__ == "__main__":
    validar=True
    print("Introduzca su email y contraseña: ")
    email=input("Email: ")
    contr=input("Contraseña: ")
    while validar:
        if (email=="email" and contr=="email"):
            print ("""************UNIVERSIDAD EUROPEA************
Escuela de Ingeniería Arquitectura y Diseño
          
*******************MENU********************

Pablo Pascual García

1.Ejercicio A
2.Ejercicio B
3.Salir\n""")
            elegir=input("¿Que quieres hacer? ")
            if elegir=="1": 
                print("\nHas accedido al ejercicio de MergeSort")
                tam=int(input("Introduce el tamaño del array a ordenar: "))
                #Creamos el array con numeros random y tamaño que se ha introducido por pantalla
                array = [random.randint(0, tam) for i in range(tam)]
                #Ordenamos el array con las nuestras funciones programadas previamente
                #y calculamos el tiempo que tardan
                start = time.time()
                for sort in mergeSort, mergeSortP:
                    arrayOrdenado = sort(array)
                end = time.time() - start
                print("El array ordenado es: ", arrayOrdenado)
                print("El tiempo en ordenarlo ha sido de: ", end)
            elif elegir=="2":
                print("\nHas accedido al ejercicio de Fibonacci")
                num = int(input("Introduzca un numero: "))
                #Una vez introducido el numero, calculamos Fibonacci y el tiempo que tarda en ralizarlo
                start = time.time()
                print("El numero de Fibonacci solicitado es: ",fibP(num))
                end = time.time() - start
                print("El tiempo en ordenarlo ha sido de: ", end)
            elif elegir=="3":
                print("\nAdios")
                validar=False
            else:
                print("\nParametro no valido")
        else:
            print("\nDatos incorrectos")
            validar=False
