"""Functions for normalize i/I j/J, u/V in Latin"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Patrick J. Burns <patrick@diyclassics.org>',
              ]
__license__ = 'MIT License. See LICENSE.'

import re

class JVReplacer(object):  # pylint: disable=R0903
    """Replace J/V with I/U."""

    def __init__(self):
        """Initialization for JVReplacer, reads replacement pattern tuple."""
        patterns = [(r'j', 'i'), (r'v', 'u')] # Simple case
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text, uv_target='u', keep_capital=False, keep_rns=True):
        """Do j/v replacement"""
        # Finish doc string
        # Add typing

        return text

    def matchcase(self, word):
        """helper function From Python Cookbook"""
        def replace(matching):
            text = matching.group()
            if text.isupper():
                return word.upper()
            elif text.islower():
                return word.lower()
            elif text[0].isupper():
                return word.capitalize()
            return word
        return replace


# class JVReplacer(object):  # pylint: disable=R0903
#     """Replace J/V with I/U."""
#
#     def __init__(self):
#         """Initialization for JVReplacer, reads replacement pattern tuple."""
#         patterns = [(r'j', 'i'), (r'v', 'u'), (r'J', 'I'), (r'V', 'U')]
#         self.patterns = \
#             [(re.compile(regex), repl) for (regex, repl) in patterns]
#
#     def replace(self, text, uv_target='u', keep_capital=False, keep_rns=True):
#         """Do j/v replacement"""
#         if uv_target=='u':
#             patterns = [(r'v', 'u')]
#             if keep_capital==True:
#                 self.patterns = [(re.compile(regex), repl) for (regex, repl) in patterns]
#             else:
#                 self.patterns = [(re.compile(regex, flags=re.IGNORECASE), repl) for (regex, repl) in patterns]
#
#         elif uv_target=='v':
#             patterns = [(r'(?<!b|c|d|f|g|h|m|n|p|q|s|t)(?<!bl|br|cr|el|ex|fl|fr|gr|il|ll|nr|ol|pl|pr|rl|rr|tr)(?<!\br|\bl)(?<!\ber)(?<!car|dir|dur|mer|mal|tur)u(?=a|i|e|o|u)', 'v')]
#             patterns += [
#                         (r'(?<=\bab|\bad|\bin|\bob)u(?=a|e|i|o|u)','v'),
#                          (r'(?<=\bcon|\bsub)u(?=a|e|i|o|u)','v'),
#                          (r'(?<=\btrans)u(?=a|e|i|o|u)','v'),
#                          (r'(?<=\bcircum)u(?=a|e|i|o|u)','v'),
#
#                          (r'(?<=\bquam|\bquid|\bquod)u', 'v'),
#                          (r'(?<=\baliud)u', 'v'),
#                          ]
#             exc_patterns = [
#                             (r'(<=q)ve\b','ue'),
#                             (r'(?<!d|g|n|p|t)ue\b', 've'),
#                             (r'(?<!ll)ue', 've'),
#                             (r'brv', 'bru'),
#                             (r'vv','uv'),
#                             (r'a(d|p)parv','a\g<1>paru'),
#                             (r'aperv', 'aperu'),
#                             (r'volveri','volueri'),
#                             (r'comparv','comparu'),
#                             (r'convoluit','convolvit'),
#                             (r'resolua','resolva'),
#                             (r'seruitu', 'servitu'),
#                             (r'\bdeservit\b', 'deseruit'),
#                             (r'convalv','convalu'),
#                             (r'c(a|o|u)lv','c\g<1>lu'),
#                             (r'\brevolu','revolv'),
#                             (r'\bsilua', 'silva'),
#                             (r'\bsilui', 'silvi'),
#                             (r'caluis(.+)', 'Calvis\g<1>'),
#                             (r'v(a|o)lv(e|i)', 'v\g<1>lu\g<2>'),
#                             (r'\bvolue\b', 'volve'),
#
#
#
#                             ]  #Try to generalize exceptions?
#             patterns += exc_patterns
#
#             self.patterns = [(re.compile(regex, flags=re.IGNORECASE), repl) for (regex, repl) in patterns]
#         else:
#             patterns = [] # should throw error
#         for (pattern, repl) in self.patterns:
#             if '\g' not in repl:
#                 text = re.subn(pattern, self.matchcase(repl), text)[0]
#             else:
#                 text = re.subn(pattern, repl, text)[0]
#
#         if keep_rns==True:
#             text = re.sub(r'\b(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IU|U?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IU|U?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IU|U?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?U|U?I{1,3}))\b','~~~\g<1>~~~', text)
#             text = re.sub(r'~~~(.*)(U)(.*)~~~', '\g<1>V\g<3>', text)
#             text = re.sub(r'~~~','',text)
#
#         return text
#

#
# if __name__ == "__main__":
#     r = JVReplacer()
#     with open('./test.txt') as file:
#         text_in = file.read()
#
#     test = r.replace(text_in, keep_capital=True)
#     # print(f'All u:\n{test}\n\n')
#     text_out = r.replace(test, uv_target='v')
#     print(text_out)
#     print(text_in == text_out)
#
#     diffs = [i for i in range(len(text_in)) if text_in[i] != text_out[i]]
#
#     for diff in diffs:
#         warn = text_out[diff-10:diff+10]
#         if 'olu' not in warn and 'ser' not in warn and 'Ser' not in warn and 'sil' not in warn:
#             print(warn,'\n')
#             pass
#     # #
#     # import difflib
#     #
#     # cases = [(text_in, text_out)]
#     #
#     # for a,b in cases:
#     #     for i,s in enumerate(difflib.ndiff(a, b)):
#     #         if s[0]==' ': continue
#     #         elif s[0]=='-':
#     #             print(u'Delete "{}" from position {}'.format(s[-1],i))
#     #             print(b[i-5:i+5])
#     #         elif s[0]=='+':
#     #             print(u'Add "{}" to position {}'.format(s[-1],i))
