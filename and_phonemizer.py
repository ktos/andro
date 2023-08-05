from typing import Dict
import pyandro.phonemizer

from TTS.tts.utils.text.phonemizers.base import BasePhonemizer

_DEF_AND_PUNCS = ".,[]()?!"

_TRANS_TABLE = {"、": ","}


def trans(text):
    for i, j in _TRANS_TABLE.items():
        text = text.replace(i, j)
    return text


class AND_Phonemizer(BasePhonemizer):
    """🐸TTS Andro phonemizer using pyandro`    

    Example:

        >>> from TTS.tts.utils.text.phonemizers import AND_Phonemizer
        >>> phonemizer = AND_Phonemizer()
        >>> phonemizer.phonemize("Mi esi Seja!", separator="|")


    """

    language = "and"

    def __init__(self, punctuations=_DEF_AND_PUNCS, keep_puncs=True, **kwargs):  # pylint: disable=unused-argument
        super().__init__(self.language, punctuations=punctuations, keep_puncs=keep_puncs)
        self.ap = pyandro.phonemizer.AndroPhonemizer()

    @staticmethod
    def name():
        return "and_phonemizer"

    def _phonemize(self, text: str, separator: str = "|") -> str:
        words = text.split(" ")
        pho = []

        for i in words:
            result = ""
            for j in _DEF_AND_PUNCS:
                if i.endswith(j):
                    result = i[:-1]
                    result = separator.join(list(self.ap.phonemize(
                        result).replace('.', '').replace('ˈ', '')))
                    result += j
                    break

            if result == "":
                result = separator.join(
                    list(self.ap.phonemize(i).replace('.', '').replace('ˈ', '')))

            pho.append(result)

        pho = [x + ' ' for x in pho]

        if separator is not None or separator != "":
            return separator.join(pho).strip()
        return "".join(pho).strip()

    def phonemize(self, text: str, separator="|") -> str:
        """Custom phonemize for AND

        Skip pre-post processing steps used by the other phonemizers.
        """
        return self._phonemize(text, separator)

    @staticmethod
    def supported_languages() -> Dict:
        return {"and": "Andro (And́royas)"}

    def version(self) -> str:
        return "0.0.1"

    def is_available(self) -> bool:
        return True


# if __name__ == "__main__":
#     text = "Mi nomi Seja, ti nomi no."
#     e = AND_Phonemizer()
#     print(e.supported_languages())
#     print(e.version())
#     print(e.language)
#     print(e.name())
#     print(e.is_available())
#     print("`" + e.phonemize(text) + "`")
