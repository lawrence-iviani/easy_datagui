import unittest
import dataclass
from pydispatch import dispatcher
from utilities.misc import remove_duplicates_from_list

__author__ = 'law'


class TestDataClassDiscreteIntNumber(unittest.TestCase):
    def test_constructor(self):
        data = [];

        # These should pass
        limits = [1,2]
        value = 1
        data.append( dataclass.DataClassDiscreteIntNumber(name = 'DonaldDuck',   limits = limits, value = value))
        data.append( dataclass.DataClassDiscreteIntNumber(name = 'MickeyMouse',  limits = limits, value = value, description = 'some description'))
        data.append( dataclass.DataClassDiscreteIntNumber(name = 'Gastone',      limits = limits, value = value, description = 'some description', initvalue=2))

        # Check and read back
        name        = 'QuiQuoQua'
        description = 'some description'
        value       = 2
        limits      = [1 , 2]
        initvalue   = 1
        data.append( dataclass.DataClassDiscreteIntNumber(name = name,    description = description, value=value, limits = limits, initvalue=initvalue ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].limits, limits, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')

    def test_constructorNameAndLimits(self):
        # Create proper test case
        data = [];
        name = 'ValidName'
        limits = [1 , 5 ,9 , 3 ,3 ,2, 1]
        value  = 3
        limitsunique = remove_duplicates_from_list(limits)

        # Validate real number test case
        data.append(dataclass.DataClassDiscreteIntNumber(name = name, limits = limits, value = value))
        self.assertEqual( data[-1].limits, limitsunique)
        self.assertEqual( data[-1].value,  value)
        self.assertEqual( data[-1].name,   name)

        # Test viewname
        with self.assertRaises(TypeError): dataclass.DataClassDiscreteIntNumber()
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = '',           value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = '  ',         value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = 1,            value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = object,       value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = 'hi there',   value = value,  limits = limits)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassDiscreteIntNumber(name = ' hi there',  value = value , limits = limits)

        # Test Limits
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteIntNumber(name = name, limits = ['1' , '2' ],  value = 1))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteIntNumber(name=name, limits=[1, 2.1], value=1))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteIntNumber(name=name, limits=[1.1, 2], value=2))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteIntNumber(name = name, limits = ['a' , 'bc' ], value = 1))
        with self.assertRaises(dataclass.DataLimitsError): data.append(dataclass.DataClassDiscreteIntNumber(name = name, limits = [object , 1, 'a' ], value = 1 ))

        # Test value
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name=name, value='a',     limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name=name, value=object,  limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name=name, value=[1 , 2], limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name=name, value=[1, 'a'],limits = limits)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name=name, value=1.1,limits=limits)

    def test_initValueAndReset(self):
        # Create a valid test case
        data        = [];
        value       = [-10 , 0 , 10]
        initvalue   = [2, -3, 0]
        limits      = [-10 , 0, 10 , 2, -3 , 1 ]
        limitsunique = remove_duplicates_from_list(limits)
        name        = 'discreteint'

        for v in value:
            # Validate test case
            iv = initvalue[value.index(v)]
            data.append(dataclass.DataClassDiscreteIntNumber(name = name, value = v, initvalue= iv, limits = limits))
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
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteIntNumber(name = name, value = value,  limits = limits, initvalue= -100) # not in limits
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassDiscreteIntNumber(name = name, value = value,  limits = limits, initvalue= 1.1)


    def test_equality(self):
        data = [];
        name = 'ValidName'
        limits = [1 , 5 ,9 , 3 ,3 ,2, 1, 4]
        initvalue = 1
        value  = 3
        desc   = 'Some description'

        data.append(dataclass.DataClassDiscreteIntNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        data.append(dataclass.DataClassDiscreteIntNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue))
        self.assertEqual(data[-1], data[-2])
        self.assertFalse(data[-1] != data[-2])

        # Test single value with list of a single value
        datalistsingle = [];
        name = 'ValidName'
        limits = [0 , 2]
        initvalue = 2
        value  = 2
        desc   = 'Some description'
        singledata = dataclass.DataClassDiscreteIntNumber(name = name, description=desc, value = value,  limits = limits, initvalue= initvalue)
        datalistsingle.append(singledata)

        self.assertEqual(singledata, datalistsingle)

    def test_set(self):
        # Create a valid test case of real and complex
        data        = [];
        limits      = [1, 5, 9, 3, 3, 2, 1, 4, 7 , -3 ,4]
        limitsunique = remove_duplicates_from_list(limits)
        name        = 'testsetdiscreteint'

        # Validate test case and readback values
        idtest = 1
        for l in limits:
            idtest += 1
            tname = 'testname' + str(idtest)
            data.append(dataclass.DataClassDiscreteIntNumber(name = tname, limits = limits, value = l))
            self.assertEqual(data[-1].value,  l, 'Value is not properly set or read back')
            self.assertEqual(data[-1].name,      tname,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].limits,    limitsunique,    'limits is not set or read back properly')

        # test set, shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name = name, limits = limits, value = -1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name = name, limits = limits, value = 3.1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name = name, limits = limits, value = 'a')
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassDiscreteIntNumber(name = name, limits = limits, value = [1,2])


if __name__ == '__main__':
    unittest.main()
