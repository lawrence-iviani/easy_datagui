__author__ = 'law'

import unittest
import dataclass

class TestDataClassException(unittest.TestCase):
    def test_DataNameError(self):
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = 'Pippo ' , value = 1)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteNumber(name = '',   limits = [1,2], value = 1)

    def test_DataDescriptionError(self):
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassNumber(name = 'Pippo' , value = 1, description=object)
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassDiscreteNumber(name = 'Pluto',   limits = [1,2], value = 1,description=['1','2'])

    def test_DataLimitsError(self):
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'Pippo' ,limits=[1,2,3] , value = 0)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassDiscreteNumber(name = 'Pluto',   limits = [1,'2'], value = 1)

    def test_DataValueError(self):
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = 'Pippo' , value = object)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteNumber(name = 'Pluto',   limits = [1,2], value = -1)

    def test_DataInitValueError(self):
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = 'Pippo' , value = 1, limits = [1,2], initvalue=0)
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteNumber(name = 'Pluto',   limits = [1,2], value = 1, initvalue=[1,2])

    def test_DataUnitError(self):
        with self.assertRaises(dataclass.DataUnitError): dataclass.DataClassNumber(name = 'Pippo' , value = 1, limits = [1,2], initvalue=1, unit=object())
        with self.assertRaises(dataclass.DataUnitError): dataclass.DataClassDiscreteNumber(name = 'Pluto',   limits = [1,2], value = 1, initvalue=1, unit=0)

    def test_MaxLengthError(self):
        with self.assertRaises(dataclass.DataMaxLengthError): dataclass.DataClassString(name = 'Pippo' , value = '1', maxlength=object(), initvalue='1')
        with self.assertRaises(dataclass.DataMaxLengthError): dataclass.DataClassString(name = 'Pippo' , value = '1', maxlength='aa', initvalue='1')

if __name__ == '__main__':
    unittest.main()
