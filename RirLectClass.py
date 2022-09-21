import json
from RSeqClass import Rsequence
import os
from FigureCreator import get_note
from music21 import *
from midi2audio import FluidSynth


cells = json.load(open("cells.json"))
levels = {"Audio": "Audio", "I": "1", "II": "2", "III": "3", "IV": "4"}


def flatten(lst):
    l = []
    for i in lst:
        for j in i:
            l.append(j)

    return l


class RitLectClass:

    def __init__(self, measures, pulses, pie, year): #  Measures to create, Pulses by measure, pie, Year
        self.measures = measures
        self.pulses = pulses
        self.pie = pie
        self.lvl = year
        self.cell_list = self.create_cell_list()
        self.tkey = meter.TimeSignature(str(pulses) + "/" + self.get_den())
        self.clef = clef.PercussionClef()
        self.lecture = self.create_lecture()
        self.name = self.get_name()

    def get_den(self):
        if self.pie == "Binario":
            return "4"
        else:
            return "8"

    def create_cell_list(self):
        lst = []
        v1 = []
        v2 = []

        if self.lvl == "I" or self.lvl == "II" or self.lvl == "Audio":
            for i in range(self.measures):
                s = Rsequence(self.lvl, self.pie, self.pulses)
                for i in s.cell_lst[0]:
                    lst.append(i)

        else:
            for i in range(self.measures):
                s = Rsequence(self.lvl, self.pie, self.pulses)
                v1.append(s.cell_lst[0])
                v2.append(s.cell_lst[1])
            lst.append(flatten(v1))
            lst.append(flatten(v2))

        print(lst)
        return lst

    def create_lecture(self):
        score = stream.Score(id='mainScore')
        p0 = stream.Part(id='part0')
        p1 = stream.Part(id='part1')
        i = instrument.SnareDrum()
        tpo = tempo.MetronomeMark("slow")
        p0.append(tpo)
        p0.append(self.tkey)
        p1.append(self.tkey)
        p0.append(self.clef)
        p1.append(self.clef)
        p0.staffLines = 1
        p1.staffLines = 1
        p0.append(i)
        p1.append(i)

        if self.lvl == "I" or self.lvl == "II" or self.lvl == "Audio":
            for i in self.cell_list:
                for j in cells[self.pie][str(i)]:
                    n = get_note(int(j), "1", self.pie)
                    n.stemDirection = "up"
                    p0.repeatAppend(n, 1)
            score.insert(0, p0)

        else:
            for i in self.cell_list[0]:
                for j in cells[self.pie][str(i)]:
                    n = get_note(int(j), "1", self.pie)
                    n.stemDirection = "up"
                    p0.repeatAppend(n, 1)
            score.insert(0, p0)

            for j in self.cell_list[1]:
                for k in cells[self.pie][str(j)]:
                    n = get_note(int(k), "2", self.pie)
                    n.stemDirection = "down"
                    p1.repeatAppend(n, 1)
            score.insert(0, p1)

        #score.show()
        return score

    def get_name(self):
        n = ""
        for i in self.cell_list:
            n += str(i) + ","
        return n[:-1]

    def show_image(self):
        self.lecture.show()

    def get_image(self, path):
        self.lecture.write("musicxml.png", fp=path + "/" + self.name + ".png")
        os.remove(path + "/" + self.name + ".musicxml")
        os.rename(path + "/" + self.name + "-1.png", path + "/" + self.name + ".png")

    def get_seq_audio(self, path):
        self.lecture.write("midi", path + "/" + self.name + ".mid")
        fs = FluidSynth(sound_font="/Users/andreslopezfeijoo/PycharmProjects/Telegram-Bot/sound fonts/Arachno.sf2")
        fs.midi_to_audio(path + "/" + self.name + ".mid", path + "/" + self.name + ".flac")
        os.remove(path + "/" + self.name + ".mid")


for i in range(5):
    l = RitLectClass(8, 3, "Binario", "III")
    l.show_image()
#l.get_image("/Users/andreslopezfeijoo/PycharmProjects/RythmicCreation")
#l.get_seq_audio("/Users/andreslopezfeijoo/PycharmProjects/RythmicCreation")


