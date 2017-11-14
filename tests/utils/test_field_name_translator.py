# coding=utf-8

import unittest
from sixquant.utils.field_name_translator import translate_field_name


class TestMethods(unittest.TestCase):
    def test_translate_field_name(self):
        self.assertEqual((None, False), translate_field_name(None))
        self.assertEqual(([], False), translate_field_name([]))
        self.assertEqual(('close', False), translate_field_name('close'))
        self.assertEqual(('pt_close', True), translate_field_name('pt_price'))
        self.assertEqual((['close', 'pt_close'], True), translate_field_name(['close', 'pt_price']))

        reverse = False
        self.assertEqual((None, False), translate_field_name(None, reverse=reverse))
        self.assertEqual(([], False), translate_field_name([], reverse=reverse))
        self.assertEqual(('close', False), translate_field_name('close', reverse=reverse))
        self.assertEqual(('pt_close', True), translate_field_name('pt_price', reverse=reverse))
        self.assertEqual((['close', 'pt_close'], True), translate_field_name(['close', 'pt_price'], reverse=reverse))

        reverse = True
        self.assertEqual((None, False), translate_field_name(None, reverse=reverse))
        self.assertEqual(([], False), translate_field_name([], reverse=reverse))
        self.assertEqual(('price', True), translate_field_name('close', reverse=reverse))
        self.assertEqual(('pt_price', True), translate_field_name('pt_close', reverse=reverse))
        self.assertEqual((['price', 'pt_price'], True), translate_field_name(['close', 'pt_close'], reverse=reverse))

        self.assertEqual(('close', True), translate_field_name('price'))
        self.assertEqual(('prev_close', True), translate_field_name('prev_price'))
        self.assertEqual(('pt_close', True), translate_field_name('pt_price'))
        self.assertEqual(('amount', True), translate_field_name('money'))


if __name__ == '__main__':
    unittest.main()
