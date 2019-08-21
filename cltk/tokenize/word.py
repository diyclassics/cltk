"""Language-specific word tokenizers. Primary purpose is to handle enclitics."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',
              'Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Natasha Voake <natashavoake@gmail.com>',
              'Clément Besnier <clemsciences@gmail.com>',
              'Andrew Deloucas <adeloucas@g.harvard.edu>']
# Author info for Arabic?

__license__ = 'MIT License. See LICENSE.'

from typing import List, Dict, Tuple, Set, Any, Generator
from abc import abstractmethod

import re

from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

from nltk.tokenize.treebank import TreebankWordTokenizer

import cltk.corpus.arabic.utils.pyarabic.araby as araby
from cltk.tokenize.latin.sentence import LatinPunktSentenceTokenizer
from cltk.tokenize.greek.sentence import GreekRegexSentenceTokenizer

from cltk.tokenize.latin.params import ABBREVIATIONS, latin_exceptions, latin_replacements

from cltk.tokenize.akkadian.word import tokenize_akkadian_words, tokenize_akkadian_signs

from cltk.tokenize.middle_english.params import MiddleEnglishTokenizerPatterns
from cltk.tokenize.middle_high_german.params import MiddleHighGermanTokenizerPatterns
from cltk.tokenize.old_norse.params import OldNorseTokenizerPatterns
from cltk.tokenize.old_french.params import OldFrenchTokenizerPatterns

class WordTokenizer:  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to a given language."""

    def __init__(self, language):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        self.available_languages = ['akkadian',
                                    'arabic',
                                    'french', # deprecate
                                    'greek',
                                    'latin',
                                    'middle_english',
                                    'middle_french',
                                    'middle_high_german',
                                    'old_french',
                                    'old_norse',
                                    'sanskrit',
                                    'multilingual'
                                    ]
        assert self.language in self.available_languages, \
            "Specific tokenizer not available for '{0}'. Only available for: '{1}'.".format(self.language,  # pylint: disable=line-too-long
            self.available_languages)  # pylint: disable=line-too-long

    def tokenize(self, string):
        """Tokenize incoming string."""
        if self.language == 'akkadian':
            tokens = tokenize_akkadian_words(string)
        elif self.language == 'arabic':
            tokenizer = BaseArabyWordTokenizer('arabic')
            tokens = tokenizer.tokenize(string)
        elif self.language == 'french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'greek':
            tokenizer = BasePunktWordTokenizer('greek', GreekRegexSentenceTokenizer)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'latin':
            tokenizer = LatinPunktWordTokenizer()
            tokens = tokenizer.tokenize(string)
        elif self.language == 'old_norse':
            tokenizer = BaseRegexWordTokenizer('old_norse', OldNorseTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_english':
            tokenizer = BaseRegexWordTokenizer('middle_english', MiddleEnglishTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'middle_high_german':
            tokenizer = BaseRegexWordTokenizer('middle_high_german', MiddleHighGermanTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        elif self.language == 'old_french':
            tokenizer = BaseRegexWordTokenizer('old_french', OldFrenchTokenizerPatterns)
            tokens = tokenizer.tokenize(string)
        else:
            tokenizer = TreebankWordTokenizer() # Should else have warning that default is used?
            tokens = tokenizer.tokenize(string)
        return tokens

    def tokenize_sign(self, word):
        """This is for tokenizing cuneiform signs."""
        if self.language == 'akkadian':
            sign_tokens = tokenize_akkadian_signs(word)
        else:
            sign_tokens = 'Language must be written using cuneiform.'
        return sign_tokens


class BaseWordTokenizer:
    """ Base class for word tokenization"""

    def __init__(self, language: str = None):
        """
        :param language : language for word tokenization
        :type language: str
        """
        if language:
            self.language = language.lower()

    @abstractmethod
    def tokenize(self, text: str, model: object = None):
        """
        Create a list of tokens from a string.
        This method should be overridden by subclasses of BaseWordTokenizer.
        """
        pass


class BasePunktWordTokenizer(BaseWordTokenizer):
    """Base class for punkt word tokenization"""

    def __init__(self, language: str = None, sent_tokenizer:object = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        super().__init__(language=self.language)
        if sent_tokenizer:
            self.sent_tokenizer = sent_tokenizer()
        else:
            punkt_param = PunktParameters()
            self.sent_tokenizer = PunktSentenceTokenizer(punkt_param)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        sents = self.sent_tokenizer.tokenize(text)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]


class BaseRegexWordTokenizer(BaseWordTokenizer):
    """Base class for regex word tokenization"""

    def __init__(self, language:str = None, patterns:List[str] = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        :param patterns: regex patterns for word tokenization
        :type patterns: list of strings
        """
        self.language = language
        self.patterns = patterns
        super().__init__(language=self.language)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        for pattern in self.patterns:
            text = re.sub(pattern[0], pattern[1], text)
        return text.split()


class BaseArabyWordTokenizer(BaseWordTokenizer):
    """
    Base class for word tokenizer using the pyarabic package:
    https://pypi.org/project/PyArabic/
    """

    def __init__(self, language:str = None):
        """
        :param language : language for sentence tokenization
        :type language: str
        """
        self.language = language
        super().__init__(language=self.language)

    def tokenize(self, text: str):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        """
        return araby.tokenize(text)

class LatinPunktWordTokenizer(BasePunktWordTokenizer):
    """
    PunktSentenceTokenizer trained on Latin
    """
    def __init__(self: object, language:str = 'latin', sent_tokenizer=LatinPunktSentenceTokenizer):
        """
        :param language : language for word tokenization
        :type language: str
        """
        super().__init__(language='latin')
        self.sent_tokenizer = sent_tokenizer()
        self._latin_replacements = latin_replacements

    def tokenize(self, text: str, split_enclitics:list = ['ne', 'n', 'que', 've', 'ue', 'st'],
                                  split_words:list = []):
        """
        :rtype: list
        :param text: text to be tokenized into sentences
        :type text: str
        :param model: tokenizer object to used # Should be in init?
        :type model: object
        """
        if self._latin_replacements:
            split_words = self._latin_replacements
        if split_words:
            text = self._replace_patterns(text, split_words)
        text = text.replace(' \'', ' \' ') # Handle lead apostrophe problem
        sents = self.sent_tokenizer.tokenize(text)
        if split_enclitics:
            sents = self._split_enclitics(sents, split_enclitics)
        tokenizer = TreebankWordTokenizer()
        return [item for sublist in tokenizer.tokenize_sents(sents) for item in sublist]

    def _split_enclitics(self:object, sents:list, enclitics: list):
        import string
        exclude_flag = '~'
        if 'ne' in enclitics and 'n' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)([n]e?)[%s]?\b'%re.escape(string.punctuation))
        elif 'ne' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)(ne)[%s]?\b'%re.escape(string.punctuation))
        elif 'n' in enclitics:
            ne_compile = re.compile(r'^\b(\w+?)(n)[%s]?\b'%re.escape(string.punctuation))

        enclitics_ = [enc for enc in enclitics if enc is not 'ne' and enc is not 'n']
        if len(enclitics_) > 1:
            if "que" in enclitics_ and 'ue' in enclitics_:
                enclitics_.remove('que')
                enclitics_.remove('ue')
                enclitics_.append('q?ue')
            enclitics_string = "|".join(enclitics_)
            enc_compile = re.compile(r'\b(?<!~)(\w+?)(%s)[%s]?\b'%(enclitics_string, re.escape(string.punctuation)))

        sent_tokens_ = []
        for sent in sents:
            for word in latin_exceptions:
                sent = re.sub(rf'\b{word}\b', self._matchcase(rf'~{word}~'), sent, flags=re.IGNORECASE)
            sent = " ".join(filter(None, ne_compile.split(sent)))
            sent = " ".join(filter(None, enc_compile.split(sent)))
            for enclitic in enclitics:
                if enclitic == 'st':
                    sent = sent.replace('u st ', 'us st ')
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' e{enclitic}', sent)
                elif enclitic == 'n':
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' -{enclitic}e', sent)
                else:
                    sent = re.sub(rf'[^%s]\b{enclitic}\b'%(exclude_flag), f' -{enclitic}', sent)
            sent = sent.replace('~','')
            sent_tokens_.append(" ".join(sent.split()))
        return sent_tokens_

    def _matchcase(self, word):
        # From Python Cookbook, p. 47
        def replace(m):
            text = m.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.title()
            else:
                return word
        return replace

    def _replace_patterns(self, text: str, patterns: list):
        for pattern in patterns:
            text = re.sub(pattern[0], self._matchcase(pattern[1]), text, flags=re.IGNORECASE)
        return text

if __name__ == "__main__":
    word_tokenizer = WordTokenizer('latin')
    tests = ['Arma virumque cano, Troiae qui primus ab oris.',
                 'Hoc verumst, tota te ferri, Cynthia, Roma, et non ignota vivere nequitia?',
                 'Nec te decipiant veteres circum atria cerae. Tolle tuos tecum, pauper amator, avos!',
                 'Neque enim, quod quisque potest, id ei licet, nec, si non obstatur, propterea etiam permittitur.',
                 'Quid opust verbis? lingua nullast qua negem quidquid roges.',
                 'Textile post ferrumst, quia ferro tela paratur, nec ratione alia possunt tam levia gigni insilia ac fusi, radii, scapique sonantes.',
                 # pylint: disable=line-too-long
                 'Dic sodes mihi, bellan videtur specie mulier?',
                 'Cenavin ego heri in navi in portu Persico?',
                 'quae ripas Ubiorum contingebat in longitudinem pedum ducentorum rescindit']

    results = []

    for test in tests:
        result = word_tokenizer.tokenize(test)
        results.append(result)

    target = [
        ['Arma', 'virum', '-que', 'cano', ',', 'Troiae', 'qui', 'primus', 'ab', 'oris', '.'],
        ['Hoc', 'verum', 'est', ',', 'tota', 'te', 'ferri', ',', 'Cynthia', ',', 'Roma', ',',
         'et', 'non', 'ignota', 'vivere', 'nequitia', '?'],
        ['Nec', 'te', 'decipiant', 'veteres', 'circum', 'atria', 'cerae', '.', 'Tolle', 'tuos',
         'cum', 'te', ',', 'pauper', 'amator', ',', 'avos', '!'],
        ['Neque', 'enim', ',', 'quod', 'quisque', 'potest', ',', 'id', 'ei', 'licet', ',',
         'nec', ',', 'si', 'non', 'obstatur', ',', 'propterea', 'etiam', 'permittitur', '.'],
        ['Quid', 'opus', 'est', 'verbis', '?', 'lingua', 'nulla', 'est', 'qua', 'negem',
         'quidquid', 'roges', '.'],
        ['Textile', 'post', 'ferrum', 'est', ',', 'quia', 'ferro', 'tela', 'paratur', ',',
         'nec', 'ratione', 'alia', 'possunt', 'tam', 'levia', 'gigni', 'insilia', 'ac', 'fusi',
         ',', 'radii', ',', 'scapi', '-que', 'sonantes', '.'],
        ['Dic', 'si', 'audes', 'mihi', ',', 'bella', '-ne', 'videtur', 'specie', 'mulier', '?'],
        ['Cenavi', '-ne', 'ego', 'heri', 'in', 'navi', 'in', 'portu', 'Persico', '?'],
        ['quae', 'ripas', 'Ubiorum', 'contingebat', 'in', 'longitudinem', 'pedum', 'ducentorum',
         'rescindit']]

    for i, item in enumerate(zip(results, target)):
        print(f'{i}:\n{item[0]}\n{item[1]}')
