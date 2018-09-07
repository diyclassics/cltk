"""Tests for Syriac tools"""

import os
import unittest

from cltk.tokenize.syriac import WordTokenizer

__author__ = ['Patrick J. Burns <patrick@diyclassics.org>',]
__license__ = 'MIT License. See LICENSE.'

class TestSyriac(unittest.TestCase):
    """Class for unittest"""
    def setUp(self):
        pass


    def test_syriac_word_tokenizer(self):
        """Word tokenization"""
        text = """ܪܺܫܳܐ ܕ݁ܶܐܘܰܢܓ݁ܶܠܺܝܳܘܢ ܕ݁ܝܶܫܽܘܥ ܡܫܺܝܚܳܐ ܆ ܒ݁ܪܶܗ ܕ݁ܰܐܠܳܗܳܐ    ܀܀"""
        target = ['ܪܺܫܳܐ', 'ܕ݁ܶܐܘܰܢܓ݁ܶܠܺܝܳܘܢ', 'ܕ݁ܝܶܫܽܘܥ', 'ܡܫܺܝܚܳܐ', '܆', 'ܒ݁ܪܶܗ', 'ܕ݁ܰܐܠܳܗܳܐ', '܀܀']
        word_tokenizer = WordTokenizer()
        result = word_tokenizer.tokenize(text)
        self.assertTrue(result == target)


if __name__ == '__main__':
    unittest.main()
