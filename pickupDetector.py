
from music21.exceptions21 import AnalysisException
from music21 import stream



class PickupDetectorException(AnalysisException):
    pass


class PickupDetector:
    """
    Initialized with a stream s. Once initialized, a number of methods are available to give information about pickups
    in the Score and their locations.

    # TODO:
        Need to add proper exception handling routines.
    # TODO:
        Make sure indicies in "detectPickups" work for All cases, and clarify docs.
    # TODO:
        Anacrusis matcher? Find the bar which completes the first part of the anacrusis (usually at end of piece/movt.)

    """
    def __init__(self, s:stream.Score):

        if s is None:
            raise PickupDetectorException('Need a Stream to initialize')

        self.currentStream = s
        self.measures = list(self.currentStream.getElementsByClass(stream.Part)[0].getElementsByClass(stream.Measure))
        self.lastBar = self.measures[len(self.measures)-1]
        self.firstBar = self.measures[0]

    def hasMeasureZero(self):
        """
        Returns true if the first measure has measure 0. This is a detail of encoding, but if the first measure is
        numbered zero, it should be a pickup.
        :return: bool
        """
        firstMeasuresNumber = self.measures[0].number
        if firstMeasuresNumber == 0:
            return True
        return False


    def detectPickups(self):
        """
        Checks every measure's actual contents/length against the barDuration established by its contextual key signature.
        Returns a list of indices corresponding to the measure numbers which contain less duration than the key signature.
        :return: list
        """
        count = []
        i = 0
        for m in self.measures:
            size = m.duration.quarterLength
            timeSig = m.barDuration.quarterLength
            if timeSig > size:
                count.append(i)
            i += 1
        return count


    @staticmethod
    def hasFrontPickup(self):
        """
        Returns True if the first measure has a smaller amount of duration than the key signature, else: False.
        :return: bool
        """
        size = self.firstBar.duration.quarterLength
        timeSig = self.firstBar.barDuration.quarterLength
        return timeSig < size


    @staticmethod
    def detectEndPickup(self):
        """
        Returns True if the last measure has less duration than the key signature, else: False.
        :return: bool
        """
        size = self.lastBar.duration.quarterLength
        timeSig = self.lastBar.barDuration.quarterLength
        if timeSig > size:
            return True
        else:
            return False

    def countTotalPickups(self):
        """
        Returns the number of pickups found by calling the detectPickups method.
        :return: int
        """
        return len(self.detectPickups())








