import re

_NON_ENGLISH_LETTERS_RE = re.compile('[^a-z]+', flags=re.IGNORECASE)

class TextAnalyser(object):
    '''
    Class to analyse text and provide insight into its various features.
    Properties are calculated in a lazy fashion.
    '''

    ## Public properties.
    @property
    def text(self):
        return self._text
    @text.setter
    def text(self, t: str):
        self._setText(t)

    @property
    def words(self):
        if self._words is None:
            self._words = self.text.split()
        return self._words

    @property
    def wordCount(self):
        if self._wordCount is None:
            self._wordCount = len(self.words)
        return self._wordCount

    @property
    def characterCount(self):
        if self._characterCount is None:
            self._characterCount = calculateEnglishLetterFrequencies(self.text)
        return self._characterCount

    @property
    def textLength(self):
        if self._textLength is None:
            self._textLength = self._calculateTextLength()
        return self._textLength

    ## Constructor/public methods.
    def __init__(self, text: str=None):
        self.text = text
    
    ## Private methods.
    def _setText(self, text: str):
        self._text = '' if text is None else text
        self._words \
            = self._wordCount \
            = self._characterCount \
            = self._textLength = None

    def _calculateTextLength(self):
        lenWithSpaces = len(self.text)
        lenWithoutSpaces = len(''.join(self.words))
        return TextAnalyserTextLength(lenWithSpaces, lenWithoutSpaces)

def calculateEnglishLetterFrequencies(text: str):
    '''
    For a given text string, calculate the frequency of occurrences of all the English letters
    it contains, and return a list of dict(letter: frequency), sorted alphabetically.

    NB: Case-insensitive, so 'H' counts the same as 'h'.
    '''
    textAsEnglishLetters = re.sub(_NON_ENGLISH_LETTERS_RE, '', text).lower()
    frequencyDict = dict()
    for letter in textAsEnglishLetters:
        frequencyDict[letter] = frequencyDict.get(letter, 0) + 1
    characterCount = []
    for letter, frequency in sorted(frequencyDict.items()):
        characterCount.append({letter: frequency})
    return characterCount

class TextAnalyserTextLength(object):
    '''
    Helper class for encapsulating text length.
    '''

    ## Public properties.
    @property
    def withSpaces(self):
        return self._withSpaces

    @property
    def withoutSpaces(self):
        return self._withoutSpaces
    
    ## Constructor/public methods.
    def __init__(self, lenWithSpaces, lenWithoutSpaces):
        self._withSpaces = lenWithSpaces
        self._withoutSpaces = lenWithoutSpaces
