from music21 import *


def get_note(n, voice, pie):  # Number that represents the note, one or two voices, Bin or Tern
    note_data = {0: [1, "half", 0, 1, 1, 3],  # Blanca con punto //
                 1: [0, "half", 1, 1, 1, 3],  # Silencio Blanca con punto
                 2: [1, "half", 0, 1, 1, 2],  # Blanca
                 3: [0, "half", 0, 1, 1, 2],  # Sil de Blanca
                 4: [1, "quarter", 1, 1, 1, 1.5],  # Negra con punto
                 5: [0, "quarter", 1, 1, 1, 1.5],  # Sil de negra con punto
                 6: [1, "quarter", 0, 1, 1, 1],  # Negra
                 7: [0, "quarter", 0, 1, 1, 1],  # Sil de Negra
                 8: [1, "eighth", 1, 1, 1, 3 / 4],  # Corchea con punto
                 9: [0, "eighth", 1, 1, 1, 3 / 4],  # Sil de Corchea con punto
                 10: [1, "eighth", 0, 1, 1, 1 / 2],  # Corchea
                 11: [0, "eighth", 0, 1, 1, 1 / 2],  # Sil de Corchea
                 12: [1, "eighth", 0, 3, 2, 1 / 3],  # Corchea de Tresillo
                 13: [1, "16th", 0, 5, 4, 1 / 5],  # Semi de Quintillo
                 14: [1, "16th", 1, 1, 1, 3 / 8],  # Semi con punto
                 15: [0, "16th", 1, 1, 1, 3 / 8],  # Sil de semi con punto
                 16: [1, "16th", 0, 1, 1, 1 / 4],  # Semi
                 17: [0, "16th", 0, 1, 1, 1 / 4],  # Sil de Semi
                 18: [1, "16th", 0, 7, 4, 1 / 7],  # Semi de septisillo
                 19: [0, "eighth", 0, 3, 2, 1 / 3],  # Sil de Corche de Tresillo
                 20: [0, "16th", 0, 5, 4, 1 / 5],  # Sil de semi de quintillo
                 21: [0, "16th", 0, 7, 4, 1 / 7],  # Sil de semi de septisillo
                 22: [1, "32nd", 0, 1, 1, 1 / 8],  # Fusa
                 23: [0, "32nd", 0, 1, 1, 1 / 8],  # Sil de Fusa
                 24: [1, "16th", 0, 6, 4, 1 / 6],  # Semi de Seisillo
                 25: [1, "eighth", 0, 4, 3, 1.5 / 4],  # Corchea de Cuatrillo CC
                 26: [0, "eighth", 0, 4, 3, 1.5 / 4],  # Sil de Corche de Cuatrillo CC
                 27: [1, "eighth", 0, 5, 3, 0],  # Corchea de Quintillo CC
                 28: [0, "eighth", 0, 5, 3, 0],  # Sil de Corchea de Qintillo CC
                 29: [1, "16th", 0, 7, 6, 0],  # Semi de Septisillo CC
                 30: [0, "16th", 0, 7, 6, 0],  # Sil de Semi de Septisillo CC
                 31: [1, "eighth", 0, 2, 3, 1.5 / 2]}  # Corchea de dosillo
    # # Silencio o figura / nombre / puntillo o no / cantidad de figuras... / donde entran x figuras / quarterlength
    if note_data[n][0] == 0:
        a = note.Rest()
    if note_data[n][0] == 1:
        if voice == "1":
            a = note.Note("f5")
        else:
            a = note.Note("a4")
    a.duration.type = note_data[n][1]
    a.duration.dots = note_data[n][2]
    t = duration.Tuplet(note_data[n][3], note_data[n][4])
    a.duration.appendTuplet(t)
    if pie == "Binario":
        a.quarterLength = note_data[n][5]
    return a