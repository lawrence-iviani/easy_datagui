__author__='law'

import unittest
import  dataclass
from pydispatch import dispatcher


class TestDataClassString(unittest.TestCase):
    def test_constructor(self):
        data=[];
        # These should pass
        data.append( dataclass.DataClassString(name='Pippo' ,       value='1'))
        data.append( dataclass.DataClassString(name='DonaldDuck',   value='0', description='some description'))
        data.append( dataclass.DataClassString(name='MickeyMouse',  value='0', description='some description'))
        data.append( dataclass.DataClassString(name='Gastone',      description='some description', value='1.1'))
        data.append( dataclass.DataClassString(name='Paperoga',     description='some description', value='1.5'))
        data.append( dataclass.DataClassString(name='cipeciop',     description='some description', value='True', maxlength=4))

        # Check and read back
        name       ='QuiQuoQua'
        description='some description'
        value      ='1.5'
        initvalue  ='1.2'
        maxlength  =3
        data.append( dataclass.DataClassString(name=name,    description=description, value=value, maxlength=maxlength, initvalue=initvalue))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].description, description, 'description is not set or read back properly')
        self.assertEqual(data[-1].maxlength, maxlength, 'limits are not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')
        self.assertEqual(data[-1].initvalue, initvalue, 'initvalue is not set or read back properly')


    def test_constructorName(self):
        data=[];
        # Create valid Test case
        value='Ciao'
        name='ValidName'

        # Validate test case, with read back
        data.append( dataclass.DataClassString(name=name,    value=value ))
        self.assertEqual(data[-1].value, value, 'Value is not set or read back properly')
        self.assertEqual(data[-1].name, name, 'Name is not set or read back properly')

        # Test name
        with self.assertRaises(TypeError): dataclass.DataClassString()
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name='', value=value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name='  ', value=value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name=1, value=value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name=object, value=value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name='hi there', value=value)
        with self.assertRaises(dataclass.DataNameError): dataclass.DataClassString(name=' hi there' , value=value,)

        # Test value
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name=name, value=1)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name=name, value=object)
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name=name, value=['1' , '2'])

    def test_constructorMaxlen(self):
        data=[];
        data.append(dataclass.DataClassString(name='testname1', maxlength=3, value='tre'))
        data.append(dataclass.DataClassString(name='testname1', maxlength=3, value='tr'))
        data.append(dataclass.DataClassString(name='testname2', value='any length, very long, I don\'t care, i am very long string with some strange character è ç à°  '))


        # Test limits shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name='testname', maxlength=2, value='tre')
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name='testname', maxlength=2, value='tre')
        with self.assertRaises(dataclass.DataMaxLengthError): dataclass.DataClassString(name='testname', maxlength='a', value='1')

    def test_initValueAndReset(self):
        # Create a valid test case real number
        data       =[];
        value      =['1.5', 'complex(1,1)']
        initvalue  =['first', 'second']
        maxlength     =20
        name       ='aNYNA@ME111++'

        for v in value:
            # Validate test case
            iv=initvalue[value.index(v)]
            data.append(dataclass.DataClassString(name=name, value=v, initvalue=iv, maxlength=maxlength))
            self.assertEqual(data[-1].value,      v,     'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].maxlength,    maxlength,    'maxlength is not set or read back properly')

            # Validate reset
            data[-1].reset()
            self.assertEqual(data[-1].value,     iv, 'Value is not properly set or read back')
            self.assertEqual(data[-1].initvalue, iv, 'Init value is not properly set or read back')
            self.assertEqual(data[-1].name,      name,      'viewname is not properly set or read back')
            self.assertEqual(data[-1].maxlength,    maxlength,    'limits is not set or read back properly')

        # Test init value, shouldn't pass
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassString(name=name, value=value,  maxlength=maxlength, initvalue=-100)
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassString(name=name, value=value,  maxlength=maxlength, initvalue=['aaaa', 'bbb'])
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassString(name=name, value=value,  maxlength=maxlength, initvalue=['ciao'])
        with self.assertRaises(dataclass.DataInitValueError): dataclass.DataClassString(name=name, value=value,  maxlength=maxlength, initvalue=object)

    def test_equality(self):
        data        = [];
        name        = 'ValidName'
        maxlength   = 10
        initvalue   = '1'
        value       = '1.5'
        desc        = 'Some description'

        data.append(dataclass.DataClassString(name=name, description=desc, value=value, maxlength=maxlength, initvalue= initvalue))
        data.append(dataclass.DataClassString(name=name, description=desc, value=value, maxlength=maxlength, initvalue= initvalue))
        self.assertEqual(data[-1], data[-2])
        self.assertFalse(data[-1] != data[-2])

        # Test single value with list of a single value
        datalistsingle =[];
        name        = 'ValidName'
        maxlength   = 10
        initvalue   = '1'
        value       = '1.5'
        desc        ='Some description'
        singledata = dataclass.DataClassString(name=name, description=desc, value=value,   maxlength=maxlength, initvalue=initvalue)
        datalistsingle.append(singledata)

        self.assertEqual(singledata, datalistsingle)

    def test_set(self):
        # test set, should pass
        data =[];
        name ='testname'
        maxlength   = 10
        data.append(dataclass.DataClassString(name='testname1', maxlength=maxlength, value='Ciao'))
        self.assertEqual(data[-1].value, 'Ciao', 'Value is not properly set or read back')
        data.append(dataclass.DataClassString(name='testname2', maxlength=maxlength, value='0123456789'))
        self.assertEqual(data[-1].value,   '0123456789', 'Value is not properly set or read back')

        # test set, shouldn't pass
        with self.assertRaises(dataclass.DataValueError): dataclass.DataClassString(name=name, maxlength=maxlength, value='01234567891')

    def test_signals(self):
        '''
        Test if signals are connected
        '''
        # Test conditions
        data        = [];
        name        = 'testname'
        maxlength   = 10

        data.append(dataclass.DataClassString(name=name, maxlength=maxlength, value='2'))
        # Create verification condition and verify it
        _dataChanged=[0]
        def on_dataChanged():
            _dataChanged[0]=1
        # Connect the signal
        dispatcher.connect(on_dataChanged, signal=dataclass.DataClass.SIGNAL_VALUECHANGED, sender=data[0])
        # Change the value, this should call the function above
        data[0].value='1'
        self.assertEqual(data[0].value,'1')

if __name__ == '__main__':
    unittest.main()
