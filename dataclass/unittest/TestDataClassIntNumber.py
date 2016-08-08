import unittest
import dataclass
from pydispatch import dispatcher

__author__ = 'law'


class TestDataClassNumber(unittest.TestCase):
    def test_constructor(self):
        data = [];
        # These should pass
        data.append( dataclass.DataClassIntNumber(name = 'Pippo' ,       value = 1))
        data.append( dataclass.DataClassIntNumber(name = 'DonaldDuck',   value = 0, description = 'some description'))
        data.append( dataclass.DataClassIntNumber(name = 'Gastone',      description = 'some description', value=1))
        data.append( dataclass.DataClassIntNumber(name = 'Paperoga',     description = 'some description', value=1, limits = [0 , 2 ]))

        # Check and read back
        name        = 'QuiQuoQua'
        description = 'some description'
        value       = 1
        limits      = [0 , 3 ]
        initvalue   = 2
        data.append(dataclass.DataClassNumber(name = name,    description = description, value=value, limits = limits, initvalue=initvalue ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].limits, limits, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')

    def test_constructorLimits(self):
        data = [];
        data.append(dataclass.DataClassNumber(name= 'testname1', limits=[0, 2], value=1))

        # Test limits shouldn't pass
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassIntNumber(name = 'testname', limits=[1.1, 2], value = 1)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassIntNumber(name = 'testname', limits=[1, 2.1],  value = 1)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassIntNumber(name = 'testname', limits=[0.11 , 3/2], value = 1)

    def test_initValueAndReset(self):
        # Create a valid test case real number
        data        = [];
        value       = [1 , -1]
        initvalue   = [-1, 1]
        limits      = [-10, 10]
        name        = 'inttest'

        for v in value:
            # Validate test case
            iv = initvalue[value.index(v)]
            data.append(dataclass.DataClassIntNumber(name = name, value = v, initvalue= iv, limits = limits))
            self.assertEqual(data[-1].value,      v,     'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limits,    'limits is not set or read back properly')

            # Validate reset
            data[-1].reset()
            self.assertEqual(data[-1].value,      iv, 'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limits,    'limits is not set or read back properly')

        # Test init value, shouldn't pass
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassIntNumber(name = name, value = value,  limits = limits, initvalue= -100) # initvalue out of range
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassIntNumber(name = name, value = value,  limits = limits, initvalue= 1.1)
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassIntNumber(name = name, value = value,  limits = limits, initvalue= [1 ,2.1 ])

    def test_equality(self):
        data = [];
        name = 'ValidName'
        limits = [0 , 3]
        initvalue = 1
        value  = 2
        desc   = 'Some description'

        data.append(dataclass.DataClassIntNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        data.append(dataclass.DataClassIntNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        self.assertEqual(data[-1], data[-2])
        self.assertFalse(data[-1] != data[-2])

    def test_set(self):
        # test set, should pass
        data = [];
        name = 'testname'
        limits = [-2 , 3]
        data.append(dataclass.DataClassIntNumber(name = 'testname1', limits = limits, value = 2))
        self.assertEqual(data[-1].value,  2, 'Value is not properly set or read back')
        data.append(dataclass.DataClassIntNumber(name = 'testname2', limits = limits, value = -2))
        self.assertEqual(data[-1].value,   -2, 'Value is not properly set or read back')
        data.append(dataclass.DataClassIntNumber(name = 'testname3', limits = [False , True],  value=True ))
        self.assertEqual(data[-1].value,      True, 'Value is not properly set or read back')

        # test set, shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassIntNumber(name = name, limits = limits, value = -10)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassIntNumber(name = name, limits = limits, value = 4)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassIntNumber(name = name, limits = limits, value = 1.1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassIntNumber(name = name, limits = limits, value = [1.1,2])

if __name__ == '__main__':
    unittest.main()
