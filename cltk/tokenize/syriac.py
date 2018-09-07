"""Syriac tokenizers."""

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',]
__license__ = 'MIT License. See LICENSE.'

from cltk.tokenize.tokenizers import StringWordTokenizer

class SentenceTokenizer():
    pass

class WordTokenizer(StringWordTokenizer):  # pylint: disable=too-few-public-methods
    """Tokenize according to rules specific to Syriac"""

    def __init__(self, language='syriac'):
        """Take language as argument to the class. Check availability and
        setup class variables."""
        self.language = language
        StringWordTokenizer.__init__(self, self.language)


if __name__ == '__main__':
    t = WordTokenizer()
    test = """ܪܺܫܳܐ ܕ݁ܶܐܘܰܢܓ݁ܶܠܺܝܳܘܢ ܕ݁ܝܶܫܽܘܥ ܡܫܺܝܚܳܐ ܆ ܒ݁ܪܶܗ ܕ݁ܰܐܠܳܗܳܐ    ܀܀"""
    tokens = t.tokenize(test)
    print(tokens)
