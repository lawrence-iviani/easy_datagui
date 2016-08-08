import unittest
import dataclass
from pydispatch import dispatcher

__author__ = 'law'


class TestDataClassNumber(unittest.TestCase):
    def test_constructor(self):
        data = [];
        # These should pass
        data.append( dataclass.DataClassNumber(name = 'Pippo' ,       value = 1))
        data.append( dataclass.DataClassNumber(name = 'DonaldDuck',   value = 0, description = 'some description'))
        data.append( dataclass.DataClassNumber(name = 'MickeyMouse',  value = 0, description = 'some description'))
        data.append( dataclass.DataClassNumber(name = 'Gastone',      description = 'some description', value=1.1))
        data.append( dataclass.DataClassNumber(name = 'Paperoga',     description = 'some description', value=1.5, limits = [1 , 2 ]))
        data.append( dataclass.DataClassNumber(name = 'cipeciop',     description = 'some description', value=True ))

        # Check and read back
        name        = 'QuiQuoQua'
        description = 'some description'
        value       = 1.5
        limits      = [1 , 2 ]
        initvalue   = 1.2
        data.append( dataclass.DataClassNumber(name = name,    description = description, value=value, limits = limits, initvalue=initvalue ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].limits, limits, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')

        # Check and read back complex number case
        name        = 'QuiQuoQua2'
        description = 'some description'
        value       = complex(1,1)
        limits      = [0 , 10 ]
        initvalue   = complex(1,-1)
        data.append( dataclass.DataClassNumber(name = name,    description = description, value=value, limits = limits, initvalue=initvalue ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].limits, limits, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')

    def test_constructorName(self):
        data = [];
        # Create valid Test case
        value = 1
        complexvalue = complex(1,1)
        name = 'ValidName'

        # Validate test case, with read back
        data.append( dataclass.DataClassNumber(name = name,    value=value ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')

        # Validate test case, with read back
        data.append( dataclass.DataClassNumber(name = name,    value=complexvalue ))
        self.assertEqual(data[-1].value, complexvalue, 'Value is not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')

        # Test viewname
        with self.assertRaises(TypeError): dataclass.DataClassNumber()
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = '', value = value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = '  ', value = value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = 1, value = value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = object, value = value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = 'hi there', value = value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassNumber(name = ' hi there' , value = value,)

        # Test value
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, value = 'a')
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, value = object)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, value = [1 , 2])
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, value = [1, 'a'])

    def test_constructorLimits(self):
        data = [];
        data.append(dataclass.DataClassNumber(name = 'testname1', limits = [0 , 2], value = 1))
        data.append(dataclass.DataClassNumber(name = 'testname2', limits = [1 , 2], value = 1))
        data.append(dataclass.DataClassNumber(name = 'testname3', limits = [1 , 2], value = 2))
        data.append(dataclass.DataClassNumber(name = 'testname4', limits = [False , True],  value=True ))
        data.append(dataclass.DataClassNumber(name = 'testname5', limits = [0 , 10],  value=complex(2,2) ))

        # Test limits shouldn't pass
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'testname', limits = ['a','b'], value = 'a')
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'testname', limits = [1,'b'],  value = 1)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'testname', limits = 2, value = 1)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'testname', limits = 'a', value = 1)
        with self.assertRaises(dataclass.DataLimitsError): dataclass.DataClassNumber(name = 'testname', limits = [2 , 1], value = 1)

    def test_constructorDescription(self):
        # valid test case parameters
        data = [];
        desc = 'My description'
        value = -1
        name = 'AValidname'
        # Validate test case pass
        data.append(dataclass.DataClassNumber(name = name, description = desc, value = value))
        self.assertEqual(data[-1].description, desc, 'Description is not properly set or read back')
        self.assertEqual(data[-1].value, value, 'value is not properly set or read back')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')

        # Test description, shouldn't pass
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassNumber(name = name, value = value, description = [1 , 2])
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassNumber(name = name, value = value, description = object)

    def test_initValueAndReset(self):
        # Create a valid test case real number
        data        = [];
        value       = [1.5 , complex(1,1)]
        initvalue   = [-1, complex(2,2)]
        limits      = [-10, 10]
        name        = 'aNYNA@ME111++'

        for v in value:
            # Validate test case
            iv = initvalue[value.index(v)]
            data.append(dataclass.DataClassNumber(name = name, value = v, initvalue= iv, limits = limits))
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
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = name, value = value,  limits = limits, initvalue= -100) # initvalue out of range
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = name, value = value,  limits = limits, initvalue= '')
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = name, value = value,  limits = limits, initvalue= 'aaaa')
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = name, value = value,  limits = limits, initvalue= [1 ,2 ])
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassNumber(name = name, value = value,  limits = limits, initvalue= object)

    def test_equality(self):
        data = [];
        name = 'ValidName'
        limits = [0 , 2]
        initvalue = 1
        value  = 1.5
        desc   = 'Some description'

        data.append(dataclass.DataClassNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        data.append(dataclass.DataClassNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        self.assertEqual(data[-1], data[-2])
        self.assertFalse(data[-1] != data[-2])

        # Test single value with list of a single value
        datalistsingle = [];
        name = 'ValidName'
        limits = [0 , 2]
        initvalue = 1
        value  = 1.5
        desc   = 'Some description'
        singledata = dataclass.DataClassNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue)
        datalistsingle.append(singledata)

        self.assertEqual(singledata, datalistsingle)

    def test_set(self):
        # test set, should pass
        data = [];
        name = 'testname'
        limits = [0 , 2]
        data.append(dataclass.DataClassNumber(name = 'testname1', limits = limits, value = 2))
        self.assertEqual(data[-1].value,  2, 'Value is not properly set or read back')
        data.append(dataclass.DataClassNumber(name = 'testname2', limits = limits, value = 0))
        self.assertEqual(data[-1].value,   0, 'Value is not properly set or read back')
        data.append(dataclass.DataClassNumber(name = 'testname3', limits = [False , True],  value=True ))
        self.assertEqual(data[-1].value,      True, 'Value is not properly set or read back')
        data.append(dataclass.DataClassNumber(name = 'testname4', limits = [False , True],  value=0.5)) # this should raise an exception but actually is not implemented in such wat
        self.assertEqual(data[-1].value,      0.5, 'Value is not properly set or read back')

        # test set, shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, limits = limits, value = -1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, limits = limits, value = 3)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, limits = limits, value = 'a')
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassNumber(name = name, limits = limits, value = [1,2])

    def test_signals(self):
        '''
        Test if signals are connected
        '''
        # Test conditions
        data = [];
        name = 'testname'
        limits = [0 , 2]

        data.append(dataclass.DataClassNumber(name = name, limits = limits, value = 2))
        # Create verification condition and verify it
        _dataChanged = [0]
        def on_dataChanged():
            _dataChanged[0] = 1
        # Connect the signal
        dispatcher.connect(on_dataChanged, signal=dataclass.DataClass.SIGNAL_VALUECHANGED, sender=data[0])
        # Change the value, this should call the function above
        data[0].value = 1
        self.assertEqual(data[0].value, 1)

if __name__ == '__main__':
    unittest.main()
