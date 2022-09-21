import json
from music21 import *
import os
from FigureCreator import get_note

cells = json.load(open("Cells.json"))


def print_all_cells(pie, path):
    for i in cells[pie]:
        s = stream.Stream()
        t = stream.Voice()
        if pie == "Binario":
            s.append(meter.TimeSignature("2/4"))
        else:
            s.append(meter.TimeSignature("6/8"))

        ex = expressions.TextExpression(str(i))
        ex.style.fontSize = 24.0
        ex.style.fontStyle = 'italic'
        ex.style.fontWeight = 'bold'
        ex.placement = "above"
        s.append(clef.PercussionClef())
        s.staffLines = 1
        lst = [a for a in cells[pie][i]]
        print(i)
        print(lst)
        for j in lst:
            n = get_note(int(j), "1", pie)
            n.stemDirection = "up"
            t.repeatAppend(n, 1)

        t.append(ex)
        s.insert(t)
        s.write("musicxml.png", fp=path + "/" + str(i) + ".png")
        os.remove(path + "/" + str(i) + ".musicxml")
        os.rename(path + "/" + str(i) + "-1.png", path + "/" + str(i) + ".png")
        s.clear()
        t.clear()


def key_remover(list, pie): # List of keys to remove (in strings), Pie from cells dictionary
    counter = 0
    new_dict = {}
    print(cells[pie])
    for i in list:
        cells[pie].pop(str(i))
    for i in cells[pie]:
        new_dict[str(counter)] = []
        for j in cells[pie][i]:
            new_dict[str(counter)].append(j)
        counter += 1
    print(cells[pie])
    print(json.dumps(new_dict))

#key_remover([101, 102], "Binario")
print_all_cells("Ternario", "/Users/andreslopezfeijoo/PycharmProjects/RhythmicCreation/TerCellList")
