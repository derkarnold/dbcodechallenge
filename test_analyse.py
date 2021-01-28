import unittest
from analyse import TextAnalyser, calculateEnglishLetterFrequencies

class SharedAnalyserTestCaseMixin(object):
    def _commonSetUp(self, *, text, lenWithSpaces, lenWithoutSpaces,
                     wordCount, characterCount):
        self.analyser = TextAnalyser(text)
        self.text = text
        self.lenWithSpaces = lenWithSpaces
        self.lenWithoutSpaces = lenWithoutSpaces
        self.wordCount = wordCount
        self.characterCount = characterCount
    
    def test_text_is_unchanged(self):
        self.assertEqual(self.text, self.analyser.text)

    def test_text_length(self):
        textLength = self.analyser.textLength
        self.assertEqual(textLength.withSpaces, self.lenWithSpaces)
        self.assertEqual(textLength.withoutSpaces, self.lenWithoutSpaces)

    def test_word_count(self):
        self.assertEqual(self.analyser.wordCount, self.wordCount)

    def test_character_count(self):
        self.assertListEqual(self.analyser.characterCount, self.characterCount)


class BaseAnalyserTestCase(SharedAnalyserTestCaseMixin, unittest.TestCase):
    def setUp(self):
        self._commonSetUp(
            text='hello 2 times  ',
            lenWithSpaces=15,
            lenWithoutSpaces=11,
            wordCount=3,
            characterCount=[
                {'e': 2}, {'h': 1}, {'i': 1}, {'l':2}, {'m':1}, {'o':1}, {'s':1}, {'t':1}
        ],)
    
class EmptyTextTestCase(SharedAnalyserTestCaseMixin, unittest.TestCase):
    def setUp(self):
        self._commonSetUp(
            text='',
            lenWithSpaces=0,
            lenWithoutSpaces=0,
            wordCount=0,
            characterCount=[],
        )
    
class JustWhitespaceTextTestCase(SharedAnalyserTestCaseMixin, unittest.TestCase):
    def setUp(self):
        self._commonSetUp(
            text='  \n \r \t \u2007',
            lenWithSpaces=9,
            lenWithoutSpaces=0,
            wordCount=0,
            characterCount=[],
        )
    
class CalculateEnglishLetterFrequenciesTestCase(unittest.TestCase):
    def test_just_lowercase(self):
        result = calculateEnglishLetterFrequencies('blahblahblahblahhello')
        self.assertListEqual(result, [{'a': 4}, {'b': 4}, {'e': 1}, {'h': 5}, {'l': 6}, {'o': 1}])
    
    def test_just_numbers(self):
        result = calculateEnglishLetterFrequencies('1234559801234814823741829347823014')
        self.assertListEqual(result, [])

    def test_mixed(self):
        result = calculateEnglishLetterFrequencies('BlahBlah blah blah 1 2 3 4 5')
        self.assertListEqual(result, [{'a': 4}, {'b': 4}, {'h': 4}, {'l': 4}])
