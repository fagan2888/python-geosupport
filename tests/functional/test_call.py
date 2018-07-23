#import unittest

from geosupport import Geosupport, GeosupportError

from ..testcase import TestCase

class TestCall(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.geosupport = Geosupport()

    def test_invalid_function(self):
        with self.assertRaises(GeosupportError):
            self.geosupport.call({'function': 99})

    def test_1(self):
        result = self.geosupport.call({
            'function': 1,
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
        })

        self.assertDictSubsetEqual({
            'ZIP Code': '10013',
            'First Borough Name': 'MANHATTAN',
            'First Street Name Normalized': 'WORTH STREET'
        }, result)

        self.assertTrue('Physical ID' not in result)

    def test_1_extended(self):
        result = self.geosupport.call({
            'function': 1,
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
            'mode_switch': 'X'
        })

        self.assertDictSubsetEqual({
            'Physical ID': '0079828'
        }, result)

    def test_1E(self):
        result = self.geosupport.call({
            'function': '1e',
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
        })

        self.assertDictSubsetEqual({
            'City Council District': '01',
            'State Senatorial District': '26'
        }, result)

        self.assertTrue('Physical ID' not in result)

    def test_1A(self):
        result = self.geosupport.call({
            'function': '1a',
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
        })

        self.assertEqual(
            result['BOROUGH BLOCK LOT (BBL)']['BOROUGH BLOCK LOT (BBL)'],
            '1001680032'
        )

        self.assertEqual(
            result['Number of Entries in List of Geographic Identifiers'],
            '0004'
        )

        self.assertTrue(
            'Street Name' not in result['LIST OF GEOGRAPHIC IDENTIFIERS'][0]
        )

    def test_1A_extended(self):
        result = self.geosupport.call({
            'function': '1a',
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
            'mode_switch': 'X'
        })

        self.assertTrue(
            'Street Name' in result['LIST OF GEOGRAPHIC IDENTIFIERS'][0]
        )

    def test_1A_long(self):
        result = self.geosupport.call({
            'function': '1a',
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
            'long_work_area_2': 'Y',
        })

        self.assertEqual(
            result['Number of Buildings on Tax Lot'], '0001'
        )

        self.assertTrue(
            'TPAD BIN Status' not in result['LIST OF BUILDINGS ON TAX LOT'][0]
        )

    def test_1A_long_tpad(self):
        result = self.geosupport.call({
            'function': '1a',
            'house_number': '125',
            'street_name': 'Worth St',
            'borough_code': 'Mn',
            'long_work_area_2': 'Y',
            'tpad': 'Y'
        })

        self.assertTrue(
            'TPAD BIN Status' in result['LIST OF BUILDINGS ON TAX LOT'][0]
        )

    def test_bl_long(self):
        result = self.geosupport.call({
            'function': 'bl',
            'bbl': '1001680032',
            'long_work_area_2': 'Y'
        })

        self.assertEqual(
            result['LIST OF BUILDINGS ON TAX LOT'][0]['Building Identification Number (BIN)'],
            '1001831'
        )

    def test_bn(self):
        result = self.geosupport.call({
            'function': 'bn',
            'bin': '1001831'
        })

        self.assertEqual(
            result['BOROUGH BLOCK LOT (BBL)']['BOROUGH BLOCK LOT (BBL)'],
            '1001680032'
        )
