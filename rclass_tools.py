import os
from itertools import product
from music21 import *
import math
from datetime import datetime


"""Para generar todas las combinaciones posibles de figuras, pasar como parametros: la maxima cantidad de figuras en
la célula (rep), los números (en forma de lista) que representan las notas en el diccionario "figuras" en RSeqClass,
finalmente cuanto dura un pulso en negras, (solo para hacer celulas que entren en un pulso, si queres podes hacer celulas
mas grandes o mas chicas haciendo uso de este parametro).
La función devuelve un diccionario a partir del key definido en "dictkey" porque la idea es pegarlo al diccionario de celulas
"cells" en la clase RSeqClass. 
Ejemplo: generate_combinations(8, [8, 9, 10, 11, 16, 17, 22, 23], 1) va a generar celulas de hasta 8 figuras con corcheas
con punto, corcheas, semi, fusas y sus silencios y que duren un pulso"""


figures = {0: note.Note("f5", quarterLength=3), 1: note.Rest("f5", quarterLength=3),
           2: note.Note("f5", quarterLength=2), 3: note.Rest("f5", quarterLength=2),
           4: note.Note("f5", quarterLength=1.5), 5: note.Rest("f5", quarterLength=1.5),
           6: note.Note("f5", quarterLength=1), 7: note.Rest("f5", quarterLength=1),
           8: note.Note("f5", quarterLength=3/4), 9: note.Rest("f5", quarterLength=3/4),
           10: note.Note("f5", quarterLength=1/2), 11: note.Rest("f5", quarterLength=1/2),
           12: note.Note("f5", quarterLength=1/3), 13: note.Note("f5", quarterLength=1/5),
           14: note.Note("f5", quarterLength=3/8), 15: note.Rest("f5", quarterLength=3/8),
           16: note.Note("f5", quarterLength=1/4), 17: note.Rest("f5", quarterLength=1/4),
           18: note.Note("f5", quarterLength=1/7), 19: note.Rest("f5", quarterLength=1/3),
           20: note.Rest("f5", quarterLength=1/5), 21: note.Rest("f5", quarterLength=1/7),
           22: note.Note("f5", quarterLength=1/8), 23: note.Rest("f5", quarterLength=1/8),
           24: note.Note("f5", quarterLength=1/6), 25: note.Note("f5", quarterLength=1.5/4),
           26: note.Rest("f5", quarterLength=1.5/4), 27: note.Note("f5", quarterLength=1.5/5),
           28: note.Rest("f5", quarterLength=1.5/5), 29: note.Note("f5", quarterLength=1.5/7),
           30: note.Rest("f5", quarterLength=1.5/7), 31: note.Nota("f5", quarterlength=1.5/2)}


defdict = {} # Dicc definitivo de celulas (en nros)

# repeticiones, lista de numeros que representan figuras, duracion del pulso en negras
def generate_combinations(rep, numbers, pul, dk, silencios):
    lst = [] # List de combinaciones
    dur = 0 # Para controlar la duracion de las celulas y evaluar solo las que entran en los pulsos pedidos
    count = 0 # cpntador de silencion en la celula
    dictkey = dk # Para escribir el diccionaro a partir del key nro definido
    # Los keys representan objetos nota en el diccionario "figuras" en RseqClass los values son su duracion en negras
    values = {0: 3, 1: 3, 2: 2, 3: 2, 4: 1.5, 5: 1.5, 6: 1, 7: 1, 8: 3/4, 9: 3/4, 10: 1/2, 11: 1/2, 12: 1/3,
              13: 1/5, 14: 3/8, 15: 3/8, 16: 1/4, 17: 1/4, 18: 1/7, 19: 1/3, 20: 1/5, 21: 1/7, 22: 1/8, 23: 1/8,
              24: 1/6, 25: 1.5/4, 26: 1.5/4, 27: 1.5/5, 28: 1.5/5, 29: 1.5/7, 30: 1.5/7}
    # Agregar las figuras que sen necesarias al dicc para las celulas que quieras crear
    for a in range(rep + 1):
        for j in product(numbers, repeat=a):
            lst.append(j)
    print("La cantidad total de combinaciones es: " + str(len(lst)))

    for i in lst:
        for j in i:
            dur += values[j]
        if dur == pul:  # Descarta la combinaciones que no duran el pulso pedido
            for k in (1, 3, 5, 7, 9, 11, 15, 17, 23): # Para ver si hay mas de dos silencios en la celula y descartarla
                count += i.count(k)
            if count <= silencios:
                defdict[dictkey] = i
                dictkey += 1
            count = 0
        dur = 0

    print("Descartando las combinaciones que no cumplen tus requisitos de cantidad de pulsos y de silencios son: " +
          str(len(defdict)) + "\nAcá está tu diccionario")
    print(defdict)


"""Para crear pngs de todas las celulas de un diccionario dado"""
def cell_image_creator(path): # Path, donde va a crear los archivos(demora mucho en crear la imagenes)
    for i in defdict:
        start_time = datetime.now()
        s = stream.Stream()
        tpo = tempo.MetronomeMark(number=80)
        s.append(tpo)
        s.append(clef.PercussionClef())
        s.staffLines = 1
        print("Creando imagen: " + str(i))
        for j in defdict[i]:
            s.repeatAppend(figures[j], 1)
            s.write("musicxml.png", fp=path + "/" + str(i) + ".png")
            #os.remove(path + "/" + str(i) + ".musicxml")
        end_time = datetime.now()
        print('demoré: {}'.format(end_time - start_time))


"""Crea diccionario de nuevas celulas para copiar y pegar al de la clase RSeq,
Se entiende que borramos a mano imagenes de celulas que no son buenas. Reordena la lista y crea un dicc
nuevo para copiar y pegar"""
def clean_lst(path, key):
    ls = os.listdir(path)
    ls2 = []
    for i in range(len(ls)):
        if not ls[i].startswith("."):
            ls2.append(int(ls[i].split("-")[0]))
    d1 = {}
    d2 = {}
    for i in sorted(ls2):
        d1[i] = defdict[i]
    for i, j in zip(range(len(d1)), d1.keys()):
        d2[i + key] = d1[j]
    print(d2)


#generate_combinations(6, [6, 7, 10, 11, 16, 17], 3, 0, 1)