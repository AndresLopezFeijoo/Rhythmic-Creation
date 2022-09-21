import json
import os
from FigureCreator import get_note
from music21 import *
from midi2audio import FluidSynth
import random as rd

cells = json.load(open("cells.json"))

"""Function that reads the list of sequences and returns a list o their names,
    Those numbers are the cells that forms the sequences"""
def cell_name_lst(path):
    l = []
    for i in os.listdir(path):
        if i.split(".")[1] == "png":
            l.append(list(eval(i.split(".")[0])))
    return l


""" Function that substitutes a cell in a sequence for an irregular value for a given level """
def irregular_v_cheat(seq, year, pie):  # Sequence to modify, level in years (int) , Bin / Ter
    aBin = [15, 113]  # List of irregular cells for first and second year, binary compass
    aTer = [55, 56, 58]  # List of irregular cells for first and second year, compound compass
    bBin = [15, 113, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]  # Similar for third and fourth year
    bTer = [55, 56, 58, 57]  # Similar
    if year < 3:
        seq[0].pop(0)
        if pie == "Binario":
            seq[0].append(rd.choice(aBin))
        else:
            seq[0].append(rd.choice(aTer))
        rd.shuffle(seq[0])
    else:
        #seq[0].pop(0)
        seq[1].pop(0)
        if pie == "Binario":
            #seq[0].append(rd.choice(bBin))
            seq[1].append(rd.choice(bBin))
        else:
            #eq[0].append(rd.choice(bTer))
            seq[1].append(rd.choice(bTer))
        #rd.shuffle(seq[0])
        rd.shuffle(seq[1])

    return seq


class CheatRitSeq:
    """A class that chats and creates a rhythmic sequence from a given list of cells"""

    def __init__(self, list, pie, time):  # List of two list one for each voice, containing cells numbers, Bin/Tern, "2/4"
        self.time = time
        self.pie = pie
        self.pulses = self.get_pulse()
        self.quarterlength = self.get_quarterlength()
        self.timek = meter.TimeSignature(time)
        self.cell_lst1 = list[0]
        self.cell_list2 = list[1]
        self.name = list
        self.sequence = self.create_seq()


    def get_pulse(self):
        if self.pie == "Binario":
            return int(self.time.split("/")[0])
        else:
            return int(self.time.split("/")[0]) / 3

    def create_seq(self):
        score = stream.Score(id='mainScore')
        p0 = stream.Part(id='part0')
        p1 = stream.Part(id='part1')
        i = instrument.SnareDrum()
        tpo = tempo.MetronomeMark("slow")
        p1.append(tpo)
        p0.append(self.timek)
        p1.append(self.timek)
        p0.append(clef.PercussionClef())
        p1.append(clef.PercussionClef())
        p0.staffLines = 1
        p1.staffLines = 1
        p0.append(i)
        p1.append(i)

        for i in self.cell_lst1:
            for j in cells[self.pie][str(i)]:
                n = get_note(int(j), "1", self.pie)
                n.stemDirection = "up"
                p0.repeatAppend(n, 1)
        score.insert(0, p0)


        if len(self.cell_list2) > 0:
            for i in self.cell_list2:
                for j in cells[self.pie][str(i)]:
                    n = get_note(int(j), "2", self.pie)
                    n.stemDirection = "down"
                    p1.repeatAppend(n, 1)
            score.insert(0, p1)
        else:
            score.insert(0, self.pulse_voice())

        return score

    def get_quarterlength(self):
        if self.pie == "Binario":
            return self.pulses
        else:
            return self.pulses * 1.5

    def pulse_voice(self):
        p = stream.Voice()
        tpo = tempo.MetronomeMark("slow")
        i = instrument.SnareDrum()
        p.append(tpo)
        p.append(self.timek)
        p.append(clef.PercussionClef())
        p.staffLines = 1
        p.append(i)
        for j in range(int(self.pulses)):
            n2 = note.Note("a4", quarterLength=1.5)
            n2.stemDirection = "down"
            p.repeatAppend(n2, 1)
        return p

    def insert_irr_values(self, year):  # Year that the irregular values belongs to (int)
        new_lst = irregular_v_cheat(self.name, year, self.pie)
        self.cell_lst1 = new_lst[0]
        self.cell_lst2 = new_lst[1]
        self.name = new_lst
        self.sequence = self.create_seq()


    def show_image(self):
        self.sequence.show()

    def get_image(self, path):
            self.sequence.write("musicxml.png", fp=path + "/" + str(self.name) + ".png")
            os.remove(path + "/" + str(self.name) + ".musicxml")
            os.rename(path + "/" + str(self.name) + "-1.png", path + "/" + str(self.name) + ".png")

    def get_seq_audio(self, path):
            self.sequence.write("midi", path + "/" + str(self.name) + ".mid")
            fs = FluidSynth(sound_font="/Users/andreslopezfeijoo/PycharmProjects/Telegram-Bot/sound fonts/Arachno.sf2")
            fs.midi_to_audio(path + "/" + str(self.name) + ".mid", path + "/" + str(self.name) + ".flac")
            os.remove(path + "/" + str(self.name) + ".mid")



def clear_lst(path):
    lst = []
    for i in os.listdir(path):
        if not i.startswith("."):
            if i.split(".")[0] + ".png" not in os.listdir(path):
                os.remove(path + "/" + i.split(".")[0] + ".flac")

def doit(pathin, pathout, tkey, year):
    for i in cell_name_lst(pathin):
        a = CheatRitSeq(i, "Ternario", tkey)
        a.insert_irr_values(year)
        a.get_seq_audio(pathout)
        a.get_image(pathout)

#doit("/Users/andreslopezfeijoo/PycharmProjects/RhythmicCreation/Secuencias/Rítmicas/Ternario/IV/4", "/Users/andreslopezfeijoo/Desktop/carpeta sin título", "12/8", 4)

#clear_lst("/Users/andreslopezfeijoo/Desktop/carpeta sin título")

#irregular_v_cheat([[23, 22, 112, 30, 28, 37, 48, 15, 17, 18, 37, 32, 28, 11],
#                   [23, 22, 112, 30, 28, 37, 48, 15, 17, 18, 37, 32, 28, 11]], 3, "Binario")
#cell_name_lst("/Users/andreslopezfeijoo/PycharmProjects/RhythmicCreation/Secuencias/Rítmicas/Binario/I/2")

#a = CheatRitSeq([[19, 15, 23, 5, 37, 16, 20, 16, 16, 18], [8, 23, 16, 18, 10, 9, 4, 15, 12, 13, 10, 6, 9, 2]], "Binario", "2/4")
#a.show_image()

#a.insert_irr_values(3)
#print(a.name)
#a.show_image()