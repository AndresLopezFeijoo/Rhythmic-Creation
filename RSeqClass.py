from music21 import *
import random as rd
from midi2audio import FluidSynth
import os
import json
from FigureCreator import get_note
from pydub import AudioSegment

cell_by_lvl = json.load(open("CellByLvl.json"))
cells = json.load(open("cells.json"))
levels = {"Audio": "Audio", "I": "1", "II": "2", "III": "3", "IV": "4"}


class Rsequence:

    def __init__(self, lvl, pie, pulses):
        self.level = levels[lvl]  # nivel en nros
        self.pie = pie  # binario ternario
        self.pulses = pulses  # cantidad de pulsos
        self.num = self.get_num  # numerador
        self.tkey = meter.TimeSignature(self.get_num() + "/" + self.get_den())  # indicacion de compas
        self.clef = clef.PercussionClef()  # clave de percusion
        self.quarterlength = self.get_quarterlength()
        self.length = 0
        self.cell_lst = self.cell_list_lvl()
        self.sequence = self.create_seq()
        self.name = self.get_name()

    def get_quarterlength(self):
        if self.pie == "Binario":
            return self.pulses
        else:
            return self.pulses * 1.5

    def get_num(self):
        if self.pie == "Binario":
            if self.pulses == 6:
                return str(round(self.pulses/2))
            else:
                return str(self.pulses)
        else:
            return str(self.pulses * 3)

    def get_den(self):
        if self.pie == "Binario":
            return "4"
        else:
            return "8"

    def counter(self, *args):
        values = {0: 3, 1: 3, 2: 2, 3: 2, 4: 1.5, 5: 1.5, 6: 1, 7: 1, 8: 3 / 4, 9: 3 / 4, 10: 1 / 2, 11: 1 / 2,
                  12: 1 / 3,
                  13: 1 / 5, 14: 3 / 8, 15: 3 / 8, 16: 1 / 4, 17: 1 / 4, 18: 1 / 7, 19: 1 / 3, 20: 1 / 5, 21: 1 / 7,
                  22: 1 / 8, 23: 1 / 8,
                  24: 1 / 6, 25: 1.5 / 4, 26: 1.5 / 4, 27: 1.5 / 5, 28: 1.5 / 5, 29: 1.5 / 7, 30: 1.5 / 7, 31: 1.5}
        for i in cells[self.pie][str(args[0])]:
            self.length += values[i]

    def reset_counter(self):
        self.length = 0

    def pulse_voice(self):
        p = stream.Voice()
        tpo = tempo.MetronomeMark("slow")
        i = instrument.SnareDrum()
        p.append(tpo)
        p.append(self.tkey)
        p.append(self.clef)
        p.staffLines = 1
        p.append(i)
        for j in range(self.pulses):
            n2 = note.Note("a4", quarterLength=self.quarterlength/self.pulses)
            n2.stemDirection = "down"
            p.repeatAppend(n2, 1)
        return p

    def cell_list_lvl(self):  # lista de celulas segun nivel
        levels = {"a": ["Audio", "1", "2"], "b": ["3", "4"]}
        while round(self.length, 2) != self.quarterlength:
            nota = False  # Indica si la secuencia empieza con una nota. False = empieza con silencio
            while nota is False:
                lst = [[], []]
                self.length = 0
                if self.level in levels["a"]:
                    while round(self.length, 2) < self.quarterlength:
                        n = rd.choice(cell_by_lvl[self.pie][self.level])
                        lst[0].append(n)
                        self.counter(n)
                        if round(self.length, 2) > self.quarterlength:
                            lst[0].pop(0)

                if self.level in levels["b"]:
                    for o in range(2):
                        self.reset_counter()
                        while round(self.length, 2) < self.quarterlength:
                            n = rd.choice(cell_by_lvl[self.pie][self.level])
                            lst[o].append(n)
                            self.counter(n)
                            if round(self.length, 2) > self.quarterlength:
                                lst[o].pop(0)

                if get_note(cells[self.pie][json.dumps(lst[0][0])][0], "1", self.pie).isNote:
                #if self.get_note(cells[self.pie][json.dumps(lst[0][0])][0], "1").isNote:
                    nota = True
        return lst


    def create_seq(self):
        score = stream.Score(id='mainScore')
        p0 = stream.Part(id='part0')
        p1 = stream.Part(id='part1')
        i = instrument.SnareDrum()
        tpo = tempo.MetronomeMark("slow")
        p1.append(tpo)
        p0.append(self.tkey)
        p1.append(self.tkey)
        p0.append(self.clef)
        p1.append(self.clef)
        p0.staffLines = 1
        p1.staffLines = 1
        p0.append(i)
        p1.append(i)

        for i in self.cell_lst[0]:
            for j in cells[self.pie][str(i)]:
                n = get_note(int(j), "1", self.pie)
                n.stemDirection = "up"
                p0.repeatAppend(n, 1)
        score.insert(0, p0)

        if self.level == "3" or self.level == "4":
            for i in self.cell_lst[1]:
                for j in cells[self.pie][str(i)]:
                    n = get_note(int(j), "2", self.pie)
                    n.stemDirection = "down"
                    p1.repeatAppend(n, 1)
            score.insert(0, p1)
        else:
            score.insert(self.pulse_voice())

        return score


    def get_name(self):
        n = ""
        for i in self.cell_lst:
            n += str(i) + ","
        return n[:-1]

    def show_image(self):
        self.sequence.show()

    def get_image(self, path):
        self.sequence.write("musicxml.png", fp=path + "/" + self.name + ".png")
        os.remove(path + "/" + self.name + ".musicxml")
        os.rename(path + "/" + self.name + "-1.png", path + "/" + self.name + ".png")

    def get_seq_audio(self, path):
        self.sequence.write("midi", path + "/" + self.name + ".mid")
        fs = FluidSynth(sound_font="/Users/andreslopezfeijoo/PycharmProjects/Telegram-Bot/sound fonts/Arachno.sf2")
        fs.midi_to_audio(path + "/" + self.name + ".mid", path + "/" + self.name + ".flac")
        os.remove(path + "/" + self.name + ".mid")


#for i in range(1):
#    a = Rsequence("III", "Binario", 4)
#    a.show_image()
#    a.get_image("/Users/andreslopezfeijoo/PycharmProjects/RythmicCreation")
#    a.get_seq_audio("/Users/andreslopezfeijoo/PycharmProjects/RythmicCreation")
