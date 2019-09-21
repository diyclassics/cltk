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
        patterns = [(r'j', 'i'), (r'v', 'u'), (r'J', 'I'), (r'V', 'U')]
        self.patterns = \
            [(re.compile(regex), repl) for (regex, repl) in patterns]

    def replace(self, text):
        """Do j/v replacement"""
        for (pattern, repl) in self.patterns:
            text = re.subn(pattern, repl, text)[0]
        return text
