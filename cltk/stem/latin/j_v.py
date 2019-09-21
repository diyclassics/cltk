"""Functions for normalize i/I j/J, u/V in Latin"""

__author__ = ['Kyle P. Johnson <kyle@kyle-p-johnson.com>',
              'Patrick J. Burns <patrick@diyclassics.org>',
              ]
__license__ = 'MIT License. See LICENSE.'

import re

ENDINGS_PRESENT_3 = r"o|is|it|imus|itis|unt|ebam|ebas|ebat|ebamus|ebatis|ebant|em|es|et|emus|etis|ent|am|as|at|amus|atis|ant|or|eris|itur|imur|imini|untur|ebar|ebaris|ebatur|ebamur|ebamini|ebantur|ar|eris|etur|emur|emini|entur"
ENDINGS_PERFECT = r"i|isti|it|imus|istis|erunt|eram|eras|erat|eramus|eratis|erant|ero|eris|erit|erimus|eritis|erint|erim|isse|isses|isset|issemus|issetis|issent"
ENDINGS_12_DEC = r"arum|orum|ae|am|as|us|um|is|os|a|i|o"
ENDINGS_3_DEC = r"is|e|i|em|um|ibus|es"

class JVReplacer(object):  # pylint: disable=R0903
    """Replace J/V with I/U."""

    def __init__(self):
        """Initialization for JVReplacer, reads replacement pattern tuple."""
        self.patterns_ = [(r'j', 'i'), (r'v', 'u')] # Simple case
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in self.patterns_]

    # def tokenize(self, text: str, model: object = None):
    #     """
    #     Method for tokenizing sentences with pretrained punkt models; can
    #     be overridden by language-specific tokenizers.
    #
    #     :rtype: list
    #     :param text: text to be tokenized into sentences
    #     :type text: str
    #     :param model: tokenizer object to used # Should be in init?
    #     :type model: object
    #     """
    # language: str = None

    def replace(self, text: str, uv_target: str = 'u', ij_target: str = 'i', keep_capital: bool = False, keep_rns: bool = True):
        """
        Do j/v replacement
        :rtype: string
        :param text: text to be normalized
        :param uv_target: defines the direction of u/v normalization
        :param ij_target: defines the direction of i/j normalization
        :param keep_capital: allows user to leave capital V in u normalization; e.g. 'Vale' not 'Uale'.
        :param keep_rns: allows user to leave roman numerals out of normalization; e,g, 'XVI' not XUI.
        """
        # Finish doc string
        if uv_target not in ['u', 'v']:
            raise ValueError("uv_target can only by 'u' or 'v'")
        if ij_target not in ['i', 'j']:
            raise ValueError("ij_target can only by 'i' or 'j'")

        if uv_target=="u":
            if keep_capital==True:
                self.patterns = [(re.compile(regex), repl) for (regex, repl) in self.patterns_]
        else:
            patterns = [('(?<!car|dir|dur|mer|mal|tur)'
                        '(?<!bl|br|cr|dr|el|ex|fl|fr|gr|il|ll|nr|ol|pl|pr|rl|rr|tr)'
                        '(?<!b|c|d|f|g|h|m|n|p|q|s|t)'
                        'u'
                        '(?=a|i|e|o|u)', 'v')
                        ]
            patterns += [(r'(?<=\bab|\bad|\bex|\bin|\bob)u(?=a|e|i|o|u)','v'),
                         (r'(?<=\bcon|\bper|\bsub)u(?=a|e|i|o|u)','v'),
                         (r'(?<=\btrans)u(?=a|e|i|o|u)','v'),
                         (r'(?<=\bcircum)u(?=a|e|i|o|u)','v'),
                         (r'(?<=\but)ue', 've'),
                         (r'(?<=\bquam|\bquem|\bquid|\bquod)u', 'v'),
                         (r'(?<=\baliud|\bcuius)u', 'v'),
                         (r'(?<=\bquantas)u','v'),
                         (r'(?<=hel)u','v'),
                         (r'(?<=animad)u','v'),
                         ]
            patterns += [(r'vv','uv'),
                         (r'ivv','iuv'),
                         (r'luu','lvu'),
                         (r'muir','mvir'),
                         (r'(?<!a|e|i|o|u)lv','lu'),
                         # (r'(?<!\br)u', 'v')
                         ]
            patterns += [(r'(?<=q)ve\b','ue'),
                         (r'(?<=m|s)ue\b', 've')
                         ]

            # Try to find more generalizations?
            exc_patterns = [(rf'\bexv({ENDINGS_PRESENT_3})(que)?\b','exu\g<1>\g<2>'),
                            (rf'\beserui({ENDINGS_PRESENT_3})(que)?\b','servi\g<1>\g<2>'),
                            (rf'\b(ex)?arv({ENDINGS_PERFECT})(que)?\b', '\g<1>aru\g<2>\g<3>'),
                            (rf'\b(con)?v(a|o)lv({ENDINGS_PERFECT})(que)?\b', '\g<1>v\g<2>lu\g<3>\g<4>'),
                            (rf'\b(a|ad|ap)?p(a|e)rv({ENDINGS_PERFECT})(que)?', '\g<1>p\g<2>ru\g<3>\g<4>'),
                            (rf'\b(con|in|oc|per)?c(a|u)lv({ENDINGS_PERFECT})(que)?', '\g<1>c\g<2>lu\g<3>\g<4>'),
                            (rf'\b(e|pro)?rv({ENDINGS_PERFECT})(que)?','\g<1>ru\g<2>\g<3>'),
                            (rf'\b(ab|dis|per|re)?solu({ENDINGS_PERFECT})(que)?', '\g<1>solv\g<2>\g<3>'),
                            (rf'\b(de)?serv({ENDINGS_PERFECT})(que)?', '\g<1>seru\g<2>\g<3>'),
                            (rf'\balv({ENDINGS_PERFECT})(que)?','alu\g<1>\g<2>'),
                            (r'\bsiluestr(is|e|i|em|um|ibus|es)','silvestr\g<1>'),
                            (rf'\bseruitu(s|t)({ENDINGS_3_DEC})(que)?','servitu\g<1>\g<2>\g<3>'),
                            (rf'\bseruil({ENDINGS_3_DEC})(que)?','servil\g<1>\g<2>'),
                            (rf'\b(ca|pa|se|si|va)(l|r)u({ENDINGS_12_DEC})(que)?\b','\g<1>\g<2>v\g<3>\g<4>'),
                            (rf'\bAdvatuc({ENDINGS_12_DEC})(que)?\b','Aduatuc\g<1>\g<2>'),
                            (rf'\bCaruili({ENDINGS_12_DEC})(que)?\b','Carvili\g<1>\g<2>'),
                            (rf'\bserui(an|re)(m|s|t|mus|tis|nt)(que)?','servi\g<1>\g<2>\g<3>'),
                            # (rf'\b(con|e|in|ob)?v(a|o|u)lu({ENDINGS_PRESENT_3})', '\g<1>v\g<2>lv\g<3>'),
                            ]
            patterns += exc_patterns
            self.patterns += [(re.compile(regex, flags=re.IGNORECASE), repl) for (regex, repl) in patterns]

        for (pattern, repl) in self.patterns:
            if '\g' not in repl:
                text = re.subn(pattern, self.matchcase(repl), text)[0]
            else:
                text = re.subn(pattern, repl, text)[0]

        if keep_capital:
            text = re.sub('U', 'V', text)

        # Should this work on lowercase?
        if keep_rns==True:
            text = re.sub(r'\b(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IU|U?I{0,3})|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IU|U?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IU|U?I{0,3})|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?U|U?I{1,3}))\b','~~~\g<1>~~~', text)
            text = re.sub(r'~~~(.*)(U)(.*)~~~', '\g<1>V\g<3>', text)
            text = re.sub(r'~~~','',text)

        return text

    def matchcase(self, word: str):
        # Move to utils?
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

if __name__ == "__main__":
    r = JVReplacer()
    text_in = """
    Arma virumque cano, Troiae qui primus ab oris
    Italiam, fato profugus, Laviniaque venit
    litora, multum ille et terris iactatus et alto
    vi superum saevae memorem Iunonis ob iram."""
    print('\n')
    print(f'Original:\n{text_in}\n')

    text_temp = r.replace(text_in)
    print(f'Normalized to u:\n{text_temp}\n')

    text_out = r.replace(text_temp, uv_target='v')
    print(f'Returned to consonantal v:\n{text_out}\n')

    print(f'V-version matches original: {text_in == text_out}')

    # diffs = [i for i in range(len(text_in)) if text_in[i] != text_out[i]]
    #
    # for diff in diffs:
    #     warn = text_out[diff-10:diff+10]
    #     print(warn,'\n')
