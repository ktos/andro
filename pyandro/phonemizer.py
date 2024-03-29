from typing import List
import unidecode
import unicodedata
import pyandro.dictionary as dictionary
import os


def compare_caseless(s1, s2):
    """
    Compares two strings caseless and with Unicode normalization, so accents
    are flatted, for example.
    """
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(NFD(s1).casefold()) == NFD(NFD(s2).casefold())


class AndroPhonemizer():
    def __init__(self, dictionary_path=None, names_path=None):
        if dictionary_path is None:
            dictionary_path = os.path.normpath(os.path.join(
                os.path.realpath(__file__), '../../dictionary.csv'))
            names_path = os.path.normpath(os.path.join(
                os.path.realpath(__file__), '../../names.csv'))

        self.dictio = dictionary.read_dictionary(dictionary_path)
        self.names = dictionary.read_dictionary(names_path, type='names')

        # read and parse dictionary file
        self.basic = (x['word'] for x in filter(lambda x: x['type']
                                                not in ['name', 'phraseology', 'proper'], self.dictio))
        self.pl = (x['pl'] for x in filter(lambda x: 'pl' in x, self.dictio))
        self.pst = (x['pst']
                    for x in filter(lambda x: 'pst' in x, self.dictio))
        self.fem = (x['fem']
                    for x in filter(lambda x: 'fem' in x and x['fem'] != 'FEM', self.dictio))
        self.supl = (x['supl']
                     for x in filter(lambda x: 'supl' in x, self.dictio))
        self.comp = (x['comp']
                     for x in filter(lambda x: 'comp' in x, self.dictio))

    def romanization(self, word: str, remove_accents=False) -> str:
        vowels = {'yi': 'ʏ', 'a': 'a', 'e': 'ɛ', 'o': 'ɔ', 'u': 'u'}
        consonants = {'ch': 'ʈ͡ʂ', 'b': 'b', 'p': 'p', 't': 't', 'd': 'd', 'k': 'k', 'g': 'g', 'm': 'm', 'n': 'n',
                      'f': 'f', 'v': 'v', 's': 's', 'z': 'z', 'j': 'ʐ', 'h': 'x', 'y': 'j', 'l': 'l', 'w': 'w', 'r': 'r'}

        word = word.lower()

        if remove_accents:
            word = word.replace('ś', 's')
            word = word.replace('é', 'ɛ')
            word = word.replace('á', 'a')
            word = word.replace('ó', 'ɔ')
            word = word.replace('ḱ', 'k')
            word = word.replace('ú', 'u')
            word = word.replace('í', 'i')
            word = word.replace('ń', 'n')
            word = word.replace('ḿ', 'm')
            word = word.replace('ý', 'y')
            word = word.replace('j́', 'j')
            word = word.replace('ĺ', 'l')
            word = word.replace('ćh', 'ʈ͡ʂ')
            word = word.replace('\u035e', '')
            word = word.replace('\u0301', '')

        for i in vowels:
            word = word.replace(i, vowels[i])

        for i in consonants:
            word = word.replace(i, consonants[i])

        return word

    def phonemize(self, word: str) -> str:
        """
        Phonemizes a word -- changes a word into its IPA representation

        Returns "[!]" if no proper phonemization can be found in the dictionary,
        may return also [!] attached to phonemization in special cases not yet
        supported.        
        """
        for x in self.dictio:
            if compare_caseless(word, x['word']):
                return x['speech']
            if 'pl' in x and compare_caseless(word, x['pl']):
                return x['pl_speech']
            if 'pst' in x and compare_caseless(word, x['pst']):
                return x['pst_speech']
            if 'fem' in x and x['fem'] != 'FEM' and compare_caseless(word, x['fem']):
                return x['fem_speech']
            if 'supl' in x and compare_caseless(word, x['supl']):
                return x['supl_speech']
            if 'comp' in x and compare_caseless(word, x['comp']):
                return x['comp_speech']

        # if the word is ending with possesive suffix
        if word.endswith("yi"):
            basic = self.phonemize(word[:-2])

            # return basic form with ʏ added, and mark
            # as potentially problematic
            if basic is not None:
                return basic + "ʏ[!]"

        # try searching for a name
        for x in self.names:
            if compare_caseless(word, x['word']):
                return x['speech']

        # if everything failed, try pure romanization
        word = self.romanization(word)

        # returns "[!]" as a marker something went wrong
        return word + "[!]"

    def __prepare(self, text):
        chars = [',', '.', ';', '?', '!']

        for i in chars:
            text = text.replace(i, '')

        return text.lower().strip()

    def sentence(self, text: str, include_front_accent=False) -> str:
        """
        Phonemizes whole sentence word by word and returns the whole text
        with / signs
        """
        text = self.__prepare(text)
        words = text.split(" ")
        return "/" + " ".join(self.sentence_as_list(text, include_front_accent=include_front_accent)) + "/"

    def sentence_as_list(self, text: str, include_front_accent=False) -> List[str]:
        """
        Phonemizes whole sentence word by word and returns a list of IPA
        representations
        """
        text = self.__prepare(text)
        words = text.split(" ")

        if not include_front_accent:
            return [self.__remove_initial_accent(self.phonemize(x)) for x in words]
        else:
            return [self.phonemize(x) for x in words]

    def __remove_initial_accent(self, word: str) -> str:
        if word.startswith('ˈ'):
            return word[1:]
        else:
            return word

    def ipa_to_arpabet(self, text: str) -> str:
        """
        Changes IPA into an ARPABET representation, approximating some things
        similarly to the South-Eastern Dialect
        """
        # <yi> is [ɪ]
        arpabet_vowels = {'a': "AH0", 'ɛ': 'EH0',
                          'i': 'IY0', 'ɔ': 'AO0', 'ʏ': 'IH0', 'u': 'UW0'}

        # <j> [ʐ] is [ʒ], <h> [x] is [h], as in South-Eastern Dialect and <ch> [ʈ͡ʂ] is [tʃ]
        arpabet_conson = {'b': 'B', 'p': 'P', 't': 'T', 'd': 'D', 'k': 'K', 'g': 'G', 'm': 'M', 'n': 'N',
                          'f': 'F', 'v': 'V', 's': 'S', 'z': 'Z', 'ʐ': 'ZH', 'x': 'HH', 'j': 'Y', 'l': 'L', 'w': 'W', 'ʈ͡ʂ': 'CH', 'r': 'R'}

        text = text.replace('.', '')
        text = text.replace('ˈ', '')

        for k in arpabet_vowels:
            text = text.replace(k, arpabet_vowels[k] + ' ')

        for k in arpabet_conson:
            text = text.replace(k, arpabet_conson[k] + ' ')

        return "{" + text.rstrip() + "}"

    def sentence_arpabet(self, text: str) -> str:
        """
        Returns ARPABET phonemization for a whole sentence
        """
        text = self.__prepare(text)
        return " ".join([self.ipa_to_arpabet(self.phonemize(x)) for x in text.split(' ')])
