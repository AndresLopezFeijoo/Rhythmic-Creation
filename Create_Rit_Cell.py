from rclass_tools import generate_combinations, cell_image_creator, clean_lst
from datetime import datetime

print("####################################################################################################\n"
      "####################################################################################################\n")
print("-->> Vamos a generar celulas rítmicas para alimentar el diccionario ""cells"" de la clase RSeqClass\n\n"
      "-->> Primero vas a elegir con que figuras vas a armar esas celulas y me lo vas a decir en números\n\n"
      "     0 = Blanca con punto     1 = Silencio de Blanca con punto\n"
      "     2 = Blanca               3 = Silencio de Blanca\n"
      "     4 = Negra con punto      5 = Silencio de Negra con punto\n"
      "     6 = Negra                7 = Silencio de Negra\n"
      "     8 = Corchea con punto    9 = Silencio de corchea con punto\n"
      "     10 = Corchea             11 = Silencio de corchea\n"
      "     12 = Corchea de tresillo 13 = Semi de quintillo\n"
      "     14 = Semi con punto      15 = Silencio de semi con punto\n"
      "     16 = Semi                17 = Silencio de semi\n"
      "     22 = Fusa                23 = Silencio de fusa\n"
      "     24 = Semi de seisillo    25 = Corchea de Cuatrillo\n"
      "     26 = Sil cor cuatrillo   27 = Corchea de Quintillo en CC \n"
      "     28 = Sil cor Quint       29 = Corchea septisillo CC \n"
      "     30 = Sil corch septisillo\n    ")

figures = input("Ingresa que figuras queres usar separadas por coma y espacio\n"
                "Por ejemplo: 0, 1, 2, 3\n"
                "Tu lista: ")
fg = []
for i in figures.split(", "):
    fg.append(int(i))

pie = (input("-->> Decime si vas a armar celulas de pulsos binarios o ternarios2\n"
                    "binario / ternario: "))

pulse = float(input("-->> Decime cuantos pulsos queres que ocupe tu celula como maximo.\n"
                    "El pulso de Negra vale 1 y el de negra con punto 1.5\n"
                    "Por ejemplo, si queres que te devuelva una negra con punto y dos semis, me vas a tener que "
                    "decir 2\n"
                    "Tu cantidad de pulsos: "))

if pie == "ternario":
    pulse = pulse * 1.5


repetitions = int(input("-->> Ahora necesito saber cuantas figuras queres como maximo en tu celula.\n"
             "Por ejemplo, si estas trabajando con fusas sobre pulso de negra y queres que aparezcan 8 fusas en algun"
             "momento tu número mágico es 8.\n"
             "Tu número mágico: "))

silences = int(input("-->> Muy bien, ahora pensa en esto: Si elegiste silencios para que yo combine, te voy a devolver muchas " \
           "células con muchos silencios,\nincluso algunas completas de silencios y te van a quedar secuencias " \
           "espantosas.\n" \
           "Para que no te pase eso decime cuantos silencios por celula como maximo vas a querer\n" \
           "Tus silencios por celula: "))

dictk = int(input("-->> Por último y super importante, yo te voy a devolver un diccionario de celulas para que copies y pegues" \
        " en el diccionadio cells de la clase RSeqClass.\n" \
        "Probablemente ese diccionario ya tenga alguna cosa ahi entonces la pregunta es: " \
        "Desde que Key del diccionario queres que arme tu nuevo diccionario para copiar y pegar?\n" \
        "Por ejemplo si vas por el 23 y queres agregar al final decime 24\n" \
        "Tu key: "))

print("Dejame hacer los cálculos")
generate_combinations(repetitions, fg, pulse, dictk, silences)
print("Así como está no te va a servir de mucho, hay combinaciones que nos muy musicales, soy una computadora.\n"
          "Lo que voy a hacer es exportar imagenes para que vos revises las células.\n"
          "Tranqui, te voy diciendo que hacer")

path = input("Dame un path donde quieras recibir las imagenes que voy a exportar para que revises.\n"
             "Por ejemplo: secuencias/ritmicas/pngs\n"
             "Ojo que si generaste muchas celulas me va a llevar un rato\n"
             "Tu path: ")

start_time = datetime.now()
cell_image_creator(path)
end_time = datetime.now()
print('Uff demoré en total: {}'.format(end_time - start_time))

print("Ahora lo que tenes que hacer es ir a esa carpeta donde generé las imagenes y revisarlas.\n"
      "Previsualizalas y anda borrando las que no te gustan, cuando estes listo apretá <enter> y te voy a dar"
      "tu ansiado diccionario, limpio y listo para que copies y pegues!!")
fin = input("Cuando vos digas <enter>.......")

clean_lst(path, dictk)

