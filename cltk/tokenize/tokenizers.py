""" Code for building and working with tokenizers
"""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>']
__license__ = 'MIT License. See LICENSE.'

from abc import abstractmethod
# from collections import Counter

from cltk.utils.cltk_logger import logger

class WordTokenizer():
    """Abstract class for word tokenization"

    def __init__(self, language=None):
        """ Initialize WordTokenizer with option for language specific parameters
        :type language: str
        :param language : text from which to build the stoplist
        """
        if language:
            self.language = language.lower()


    @abstractmethod
    def tokenize(self, text):
        """
        Build a stoplist based on string or list of strings. This method
        should be overridden by subclasses of Stoplist.
        """

class StringWordTokenizer(WordTokenizer):

    def __init__(self, language=None):
        WordTokenizer.__init__(self, language)

    def tokenize(self, text):
        return text.split()
        

if __name__ == "__main__":
    pass
