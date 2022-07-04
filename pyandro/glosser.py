from typing import List
import unidecode
import unicodedata
import pyandro.dictionary as dictionary


def compare_caseless(s1, s2):
    """
    Compares two strings caseless and with Unicode normalization, so accents
    are flatted, for example.
    """
    def NFD(s):
        return unicodedata.normalize('NFD', s)

    return NFD(NFD(s1).casefold()) == NFD(NFD(s2).casefold())


class AndroGlosser():
    def __init__(self):
        self.dictio = dictionary.read_dictionary('dictionary.csv')
        self.names = dictionary.read_dictionary(
            'names.csv', type='names')

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

    def __description_to_gloss(self, desc: str, type: str, variant="") -> str:
        desc = desc.strip()

        sc = desc.find("(<sc>")
        if sc != -1:
            return desc[sc+5:desc.find("</sc>")].upper()

        comma = desc.find(",")
        if comma != -1:
            desc = desc[:comma].strip()

        parentheses = desc.find('(')
        if parentheses != -1:
            desc = desc[:parentheses].strip()

        to = desc.startswith('to ')
        if to:
            desc = desc[3:]
            if variant == 'pst':
                desc = desc + '-PST'
            else:
                desc = desc + '.PRS'

        if type == 'adj':
            desc += '-ADJ'

        if variant != 'pst' and variant != '':
            if variant == 'fem':
                variant = 'f'

            desc += f"-{variant.upper()}"

        return desc.replace(" ", ".")

    def gloss(self, word: str) -> str:
        """
        Glosses a word -- changes a word into its glossing

        Returns "[!]" if no proper glossing can be analyzed, may return [!]
        also when some of the glosses were not inferred properly
        """
        results = []

        for x in self.dictio:
            if compare_caseless(word, x['word']):
                if 'redirect' in x:
                    results.append('[REDIRECT!]')
                else:
                    results.append(self.__description_to_gloss(
                        x['english_description'], x['type']))
            if 'pl' in x and compare_caseless(word, x['pl']):
                results.append(self.__description_to_gloss(
                    x['english_description'], x['type'], 'pl'))
            if 'pst' in x and compare_caseless(word, x['pst']):
                results.append(self.__description_to_gloss(
                    x['english_description'], x['type'], 'pst'))
            if 'fem' in x and x['fem'] != 'FEM' and compare_caseless(word, x['fem']):
                results.append(self.__description_to_gloss(
                    x['english_description'], x['type'], 'fem'))
            if 'supl' in x and compare_caseless(word, x['supl']):
                results.append(self.__description_to_gloss(
                    x['english_description'], x['type'], 'supl'))
            if 'comp' in x and compare_caseless(word, x['comp']):
                results.append(self.__description_to_gloss(
                    x['english_description'], x['type'], 'comp'))

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            # if the word is ending with possesive suffix
            if word.endswith("yi"):
                basic = self.gloss(word[:-2])

                # return basic form with ʏ added, and mark
                # as potentially problematic
                return basic + "-POSS"

            # returns "[!]" as a marker something went wrong
            return word + "[!]"
        else:
            return "/".join(results)

    def __prepare(self, text):
        chars = [',', '.', ';', '?', '!']

        for i in chars:
            text = text.replace(i, '')

        return text.lower().strip()

    def sentence(self, text: str) -> str:
        """
        Glosses the whole sentence word by word
        """
        text = self.__prepare(text)
        words = text.split(" ")
        return " ".join(self.sentence_as_list(text))

    def sentence_as_list(self, text: str) -> List[str]:
        """
        Glosses the whole sentence word by word and returns a list
        """
        text = self.__prepare(text)
        words = text.split(" ")

        return [self.gloss(x) for x in words]
