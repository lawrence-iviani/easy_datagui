__author__ = 'law'

import unittest
import dataclass
from pydispatch import dispatcher
from utilities.misc import remove_duplicates_from_list

class TestDataClassDiscreteString(unittest.TestCase):
    def test_constructor(self):
        data = [];

        # These should pass
        limits = ['1','2']
        value = '1'
        data.append( dataclass.DataClassDiscreteString(name = 'DonaldDuck',   limits = limits, value = value))
        data.append( dataclass.DataClassDiscreteString(name = 'MickeyMouse',  limits = limits, value = value, description = 'some description'))
        data.append( dataclass.DataClassDiscreteString(name = 'Gastone',      limits = limits, value = value, description = 'some description', initvalue='2'))

        # Check and read back
        name        = 'QuiQuoQua'
        description = 'some description'
        value       = 'a'
        limits      = ['b' , 'c', 'a']
        initvalue   = 'b'
        data.append( dataclass.DataClassDiscreteString(name = name,    description = description, value=value, limits = limits, initvalue=initvalue ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].limits, limits, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')

    def test_constructorNameAndLimits(self):
        # Create proper test case
        data = [];
        name = 'ValidName'
        limits = ['b' , 'c', 'a', 'A', 'a','BB','3' ,'bravo', '3']
        value  = '3'
        limitsunique = remove_duplicates_from_list(limits)

        # Validate complex number test case
        data.append(dataclass.DataClassDiscreteString(name = name , limits = limits,  value = value))
        self.assertEqual( data[-1].limits, limitsunique)
        self.assertEqual( data[-1].name,   name)


        # Test viewname
        with self.assertRaises(TypeError): dataclass.DataClassDiscreteString()
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = '',           value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = '  ',         value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = 1,            value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = object,       value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = 'hi there',   value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteString(name = ' hi there',  value = value , limits = limits)

        # Test Limits
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteString(name = name, limits = [1 , 2,  3 ],  value = '1'))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteString(name = name, limits = [1 , 'bc', 'a' ,'1' ], value = '1'))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteString(name = name, limits = [object , '1', 'a' ], value ='1'  ))

        # Test value
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, value = 'abbb',  limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, value = object,  limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, value = ['b' , 'c'], limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, value = [1, 'b'],limits = limits)

    def test_constructorDescription(self):
        # Create test case with valid data
        data = [];
        name = 'ValidName'
        limits = ['b' , 'c', 'a', 'A', 'a','BB','3' ,'bravo', '3']
        value  = '3'
        description = 'Some valid description'
        limitsunique = remove_duplicates_from_list(limits)

        # Validate the test case and readback
        data.append(dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = description))
        self.assertEqual(data[-1].description, description,  'Description is not properly set or read back')
        self.assertEqual(data[-1].value,       value,        'value is not properly set or read back')
        self.assertEqual(data[-1].name,        name ,        'viewname is not properly set or read back')
        self.assertEqual(data[-1].limits,      limitsunique, 'limits is not properly set or read back')

        # Test description
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = [1 , 2])
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = ['is it ' , ' valid?'])
        with self.assertRaises(dataclass.DataDescriptionError): dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = object)

    def test_unit(self):
        # Create test case with valid data
        data = [];
        name = 'ValidName'
        limits = ['b' , 'c', 'a', 'A', 'a','BB','3' ,'bravo', '3']
        value  = '3'
        description = 'Some valid description'
        limitsunique = remove_duplicates_from_list(limits)
        unit        = 'SOme units'
        data.append(dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = description, unit = unit))
        with self.assertRaises(dataclass.DataUnitError): dataclass.DataClassDiscreteString(name = name, limits = limits,  value = value, description = description, unit = 1)


    def test_initValueAndReset(self):
        # Create a valid test case
        data        = [];
        value       = ['-10' , 'complex(1,1)' , 'True']
        initvalue   = ['2', 'complex(2,2)', 'False']
        limits      = ['-1.2' , '1', '-10' , '2','complex(2,2)' ,'2.0001' ,'complex(1,1)', '-33' , '1', 'complex(1,1)', '2', 'True', 'False' ]
        limitsunique = remove_duplicates_from_list(limits)
        name        = 'aN+;;~~~+'

        for v in value:
            # Validate test case
            iv = initvalue[value.index(v)]
            data.append(dataclass.DataClassDiscreteString(name = name, value = v, initvalue= iv, limits = limits))
            self.assertEqual(data[-1].value,      v,     'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limitsunique,    'limits is not set or read back properly')

            # Validate reset
            data[-1].reset()
            self.assertEqual(data[-1].value,      iv, 'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limitsunique,    'limits is not set or read back properly')


        # Test init value
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteString(name = name, value = value,  limits = limits, initvalue= '-100') # not in limits
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteString(name = name, value = value,  limits = limits, initvalue= '')
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteString(name = name, value = value,  limits = limits, initvalue= 1)
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteString(name = name, value = value,  limits = limits, initvalue= ['1' ,'2' ])
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteString(name = name, value = value,  limits = limits, initvalue= object)

    def test_equality(self):
        data = [];
        name = 'ValidName'
        limits = ['1' , '5' ,'9' , '3' ,'3' ,'2', '1', '3.2', 'complex(1,1)']
        initvalue = '1'
        value  = '3'
        desc   = 'Some description'

        data.append(dataclass.DataClassDiscreteString(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        data.append(dataclass.DataClassDiscreteString(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        self.assertEqual(data[-1], data[-2])
        self.assertFalse(data[-1] != data[-2])

        # Test single value with list of a single value
        datalistsingle = [];
        name = 'ValidName'
        limits = ['0' , '2']
        initvalue = '2'
        value  = '2'
        desc   = 'Some description'
        singledata = dataclass.DataClassDiscreteString(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue)
        datalistsingle.append(singledata)

        self.assertEqual(singledata, datalistsingle)

    def test_set(self):
        # Create a valid test case of real and complex
        data        = [];
        limits = ['b' , 'c', 'a', 'A', 'a','BB','3' ,'bravo', '3']
        limitsunique = remove_duplicates_from_list(limits)
        name        = 'aN+;;~~~+'

        # Validate test case and readback values
        idtest = 1
        for l in limits:
            idtest += 1
            tname = 'testname' + str(idtest)
            data.append(dataclass.DataClassDiscreteString(name = tname, limits = limits, value = l))
            self.assertEqual(data[-1].value,  l, 'Value is not properly set or read back')
            self.assertEqual(data[-1].name,      tname,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limitsunique,    'limits is not set or read back properly')

        # test set, shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, limits = limits, value = '-1')
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, limits = limits, value = 3)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, limits = limits, value = 1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteString(name = name, limits = limits, value = ['b','c'])

        # Test boolean
        value = 'True'
        limits = ['False' , 'True']
        data.append(dataclass.DataClassDiscreteString(name = name, limits = limits, value = value))
        self.assertEqual(data[-1].value,  value, 'Value is not properly set or read back')
        self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
        self.assertEqual(data[-1].limits,    limits,    'limits is not set or read back properly')

    def test_signals(self):
        '''
        Test if signals are connected
        '''
        # Test conditions
        data        = [];
        limits      = ['-1.2' , '1', '-10'  ,'complex(1,-2)' , '2' ,'complex(1,-2)', '2.0001' , '-33' , '1' ,'2' ,'complex(1,1)' ]
        limitsunique = remove_duplicates_from_list(limits)
        name        = 'aN+;;~~~+'

        data.append(dataclass.DataClassDiscreteString(name = name, limits = limits, value = '2'))
        # Create verification condition and verify it
        _dataChanged = [0]
        def on_dataChanged():
            _dataChanged[0] = 1
        # Connect the signal
        dispatcher.connect(on_dataChanged, signal=dataclass.DataClass.SIGNAL_VALUECHANGED, sender=data[0])
        # Change the value, this should call the function above
        data[0].value = 'complex(1,1)'
        self.assertEqual(data[0].value, 'complex(1,1)')

if __name__ == '__main__':
    unittest.main()
