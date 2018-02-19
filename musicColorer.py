# @author Bronnie C Stroud
# @version 1
# TODO: Add support for all chromatic and altered pitches (#4, b6, etc.). Currently only supports modal diatonic pitches
# TODO: Better handling of minor key Leading Tones. Currently LT are treated as "non-mode" tones and left black.
# TODO: Rework  or replace analysis.floatingKey module for more modulation-detection precision. Currently uses 4 measure window.
# TODO: Allow the user to bypass analysis and to assert a key to be used for coloring.

import os
import sys
from music21 import stream
from music21 import analysis
from music21 import note
from colour import Color
import pickupDetector

class MusicColorer:
    """
    This class is initialized with a list of colors and a music21 Score object. It analyzes each measure with the
    floatingKey method, then colors the noteheads, matching colors to scale degrees relative to the prevailing key.
    The recolored Score is returned.

    # TODO:
        Add support for all chromatic pitches (#4, b6, etc.). Currently only supports modal diatonic pitches.
    # TODO:
        Better handling of minor key Leading Tones. Currently LT are treated as "non-mode" tones and left black.
    # TODO:
        Rework analysis.floatingKey module for more modulation-detection precision. Currently uses 4 measure window.
    # TODO:
        Allow the user to bypass analysis and to assert a key to be used for coloring. Score analysis is the default
        option.
    """
    currentScore = None
    colors = []
    keys = []

    def __init__(self, argv:list):
        """
            Initializes the colorer by initializing arguments and analyzing the score with analysis.floatingKey.
        """
        if argv is None:
            argv = sys.argv

        self.argv = argv
        self.destroyOldLogFile()
        self.initializeArgs(self.argv)
        self.analyzeKeys()

    def run(self):
        """
        This method steps through the Score's structures recursively: Score -> Part -> Measure. At the Measure level, a
        "currentKey" is looked up in the list of keys from the analysis step of the initialization. Each note is
        contextualized within this key to give a matching scale degree. Finally, this scale degree is looked up in the
        list of colors and the notehead is colored accordingly. When every note has been colored, the score is returned
        to the caller.
        :return: stream.Score
        """
        self.logger("changeNoteColors", "Recoloring notes...")
        parts = list(self.currentScore.getElementsByClass(stream.Part))
        currentPart = 0
        self.logger("changeNoteColors", "There are " + str(len(parts)) + " parts in this score")
        for thisPart in parts:
            self.logger("changeNoteColors", "PART starting # " + str(currentPart + 1) + " of " + str(len(parts)) + "")
            measures = list(thisPart.getElementsByClass(stream.Measure))
            currentPart += 1
            currentMeasure = 0
            for thisMeasure in measures:
                # self.logger("changeNoteColors",
                #            "MEASURE starting # " + str(currentMeasure+1) + " of " + str(len(measures)))
                currentKey = self.keys[currentMeasure]
                notes = list(thisMeasure.getElementsByClass(note.Note))
                # self.logger("changeNoteColors", "There are " + str(len(notes)) + " notes in this measure")
                for thisNote in notes:
                    scaleDegree = currentKey.getScaleDegreeFromPitch(thisNote)
                    thisNote.color = self.getMatchingColor(scaleDegree)
                currentMeasure += 1
        return self.currentScore

    def initializeArgs(self, argv: list):
        """
        This method unpacks argv arguments and either assigns them globally or calls the appropriate methods to process
        or initialize them.
        These are...
        1. argv[0] is the score to edit.
        2. argv[1] is a list of 7 comma-separated supported color representations
        (e.g., '"blue", "black", "black", "black", "red", "pink","black"'). These are parsed by processColors into actual
        color objects.
        """
        self.logger("initializeArgs", "Initializing...")
        self.currentScore = argv[0]
        colorStringList = argv[1].split(',')  # argv[1] should be a string of colors separated by commas
        self.colors = self.processColors(colorStringList)
        return

    def processColors(self, colorStringList: list):
        """
        Accepts a string of comma-separated color names, rgb values, or other representations of colors accepted by the
        Colour package and converts them to a list of Color objects
        :return: list
        """
        self.logger("processColors", "Processing colors...")
        localColors = []
        for thisString in colorStringList:
            c = Color(thisString)
            localColors.append(c)
        return localColors

    def analyzeKeys(self):
        """
        Analyzes the score with analysis.floatingKey, which returns a list of key objects with the same length as the
        number of measures found in the piece. If there is NOT a pickup, the end of this list must be padded the end
        with an extra Key object. This is due to a glitch in floatingKey module which causes the last measure of Scores
        without a pickup to be left unanalyzed.
        """
        ka = analysis.floatingKey.KeyAnalyzer(self.currentScore)
        self.logger("analyzeKeys", "Analyzing Score...")
        self.keys = ka.run()
        detector = pickupDetector.PickupDetector(self.currentScore)
        # If no pickup, pad end of keys[]
        if not detector.detectPickups():
            self.padEndKeys()
        return

    def padEndKeys(self):
        """
        Copies the last key in the keys[] list and adds it to the end of keys[].

        For some reason, if there is NOT a pickup in the score, the floatingKey module doesn't analyze the last measure.
        Because of this, we have to replicate the last measure it DOES analyze so an error doesn't occur when iterating
        through in the run() method.

        Should only be called when the current score does NOT have a pickup in it.
        """
        self.keys.insert(len(self.keys), self.keys[len(self.keys)-1])
        self.logger("padEndKeys", "Padding keys...")
        return

    def getMatchingColor(self, scaleDegree: int):  # returns the color matching a given scale degree
        """
        Looks up the color to match a given scale degree referencing colors[]. Returns a hexadecimal representation of
        it. If a note is not diatonic to the key center established by floatingKey, it will not have an integer
        representing its scale degree. In these cases, the note is colored black by default.
        :return: Color
        """
        if scaleDegree is None:  # This occurs when a note is not in the analyzed key for that measure
            # self.logger("getMatchingColor", "The note passed in was of type NoneType")
            return Color("black").hex
        returnColor = self.colors[int(scaleDegree) - 1].hex
        return returnColor

    @staticmethod
    def destroyOldLogFile():
        """
        Deletes the old log-file.
        """
        log_file = open("musicColorerLOGFILE.txt", "w")
        log_file.write("")
        log_file.close()

    @staticmethod
    def logger(currentMethod: str, message: str):
        """
        Simple logger method. Prints & writes formatted strings with the following information:
        Current Working Directory
        Method originating message
        Message
        """
        log_file = open("musicColorerLOGFILE.txt", "a")
        cwd = os.getcwd()
        cwd = '{: <50}'.format(cwd)
        currentMethod = '{: <20}'.format(currentMethod)  # Makes this left aligned, 20 characters or fill with space
        message = '{: <30}'.format(message)
        messageString = "CWD: " + cwd + "From Method: " + currentMethod + "Message: " + message
        print(messageString)
        log_file.write(messageString + "\n")
        log_file.close()

if __name__ == "__main__":
    colorer = MusicColorer(sys.argv)
    colorer.run()

"""
PSEUDOCODE:

def __init__(currentScore, colorStringList):
    processColors()
    analyzeKeys()

def processColors():
    for colorString in colorStringList:
        colorList.append(Color(colorString))
    return colorList

def analyzeKeys():
    analyzer = floatingKey.KeyAnalyzer(currentScore)
    keys = analyzer.run()
    if NO PICKUP
        padKeyListEnd()
    return

def padKeyListEnd():
    keyList.insert(-1, keyList[-1])
    return

def run():
    for currentPart in currentScore
        for currentMeasure in currentPart
            currentKey = keyList[currentMeasureNumber]
            for currentNote in currentMeasure
                scaleDegree = currentKey.scaleDegree(currentNote)
                note.color = getMatchingColor(scaleDegree)
    return currentScore

def getMatchingColor(scaleDegree):
    return colorList[scaleDegree].hex
"""