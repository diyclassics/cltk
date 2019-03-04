from cltk.tokenize.word import WordTokenizer
from cltk.lemmatize.french.french import regex
import os
import importlib.machinery

from cltk.utils.file_operations import open_pickle

__author__ = ['Natasha Voake <natashavoake@gmail.com>', 'Patrick J. Burns <patrick@diyclassics.org']
__license__ = 'MIT License. See LICENSE.'


class LemmaReplacer(object):  # pylint: disable=too-few-public-methods
    """Lemmatize French words by replacing input words with corresponding
    values from a replacement list.
    """

    models_path = os.path.expanduser('~/cltk_data/french/text/french_data_cltk')

    def __init__(self):
        """
        """
        self.models_path = LemmaReplacer.models_path

        missing_models_message = "LemmaReplacer requires the ```french_data_cltk``` to be in cltk_data. Please load this corpus."

        try:
            self.entries = open_pickle(os.path.join(self.models_path,'entries.pickle'))
            self.forms_and_lemmas = open_pickle(os.path.join(self.models_path,'forms_and_lemmas.pickle'))
        except FileNotFoundError as err:
            raise type(err)(missing_models_message)

    def lemmatize(self, tokens):
        """define list of lemmas"""
        entries = self.entries
        forms_and_lemmas = self.forms_and_lemmas

        lemma_list = [x[0] for x in entries]
        """Provide a lemma for each token"""
        lemmatized = []
        for token in tokens:
            """check for a match between token and list of lemmas"""
            if token in lemma_list:
                lemmed = (token, token)
                lemmatized.append(lemmed)
            else:
                """if no match check for a match between token and list of lemma forms"""
                lemma = [k for k, v in forms_and_lemmas.items() if token in v]
                if lemma != []:
                    lemmed = (token, lemma)
                    lemmatized.append(lemmed)
                elif lemma == []:
                    """if no match apply regular expressions and check for a match against the list of lemmas again"""
                    regexed = regex(token)
                    if regexed in lemma_list:
                        lemmed = (token, regexed)
                        lemmatized.append(lemmed)
                    else:
                        lemmed = (token, "None")
                        lemmatized.append(lemmed)
        return lemmatized

if __name__ == '__main__':

    from pprint import pprint
    l = LemmaReplacer()
    lemmas = l.lemmatize('ne me mandez nule foiz mais'.split())
    pprint(lemmas)
