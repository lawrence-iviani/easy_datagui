__author__ = 'law'

import unittest
from model import GenericModel
from model import DataClassModel
from model import ModelException
import dataclass
from pydispatch import dispatcher

class TestDataClassModel(unittest.TestCase):

    def test_constructor(self):
        # Test empty model
        model = DataClassModel()
        self.assertEqual(model._propertyDictionary,{})

        # Test model constructor with dictonary
        data = []
        name = 'testname'
        limits = [0 , 5]
        limitsDisc = [1 , 5 ,9 , 3 ,3 ,2, 1, 3.2, complex(1,1)]
        value  = 3
        initvalue = 1
        data.append(dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue))
        model1 = DataClassModel(data)
        self.assertEqual(data , model1.getAllProperties())

        data.append(dataclass.DataClassNumber(name = name + str(2), limits = limits, value = value, initvalue = initvalue))
        data.append(dataclass.DataClassDiscreteNumber(name = name + str(3) , limits = limitsDisc,  value = value, initvalue = initvalue))
        model2 = DataClassModel(data)
        self.assertEqual(data, model2.getAllProperties())

    def test_addProperty(self):
        # Test model constructor with dictonary
        name = 'testname'
        limits = [0 , 5]
        limitsDisc = [1 , 5 ,9 , 3 ,3 ,2, 1, 3.2, complex(1,1)]
        value  = 3
        initvalue = 1


        # Test add single value
        model1 = DataClassModel()
        data1 = dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue)
        propertiesDict1 = {data1.name : data1}
        model1.addProperties(propertiesDict1)
        self.assertEqual(data1 , model1.getAllProperties())

        ##### Test add again same property leads to an exception
        with self.assertRaises(ModelException.PropertyAlreadyPresentError): model1.addProperties(propertiesDict1)
        # Test add a non dataclass property
        propertiesDict1_2 = {'PropB' , 2}
        with self.assertRaises(ModelException.PropertyIsNotCompatible): model1.addProperties(propertiesDict1_2)

        #### Test multiple  values in
        data2 = []
        model2 = DataClassModel()
        data2.append( dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue))
        data2.append(dataclass.DataClassNumber(name = name + str(2), limits = limits, value = value, initvalue = initvalue))
        data2.append(dataclass.DataClassDiscreteNumber(name = name + str(3) , limits = limitsDisc,  value = value, initvalue = initvalue))
        propertiesDict2 = {}
        for d in data2:
            propertiesDict2[d.name] = d
        model2.addProperties(propertiesDict2)

        # Test add again same property leads to an exception
        with self.assertRaises(ModelException.PropertyAlreadyPresentError): model1.addProperties(propertiesDict2)
        # Test add a non dataclass property
        propertiesDict1_2 = {'PropB' , 2}
        with self.assertRaises(ModelException.PropertyIsNotCompatible): model1.addProperties(propertiesDict1_2)

    def test_signals(self):
         # Test model constructor with dictonary
        name = 'testname'
        limits = [0 , 5]
        limitsDisc = [1 , 5 ,9 , 3 ,3 ,2, 1, 3.2, complex(1,1)]
        value  = 3
        initvalue = 1
        # Test add single value
        model1 = DataClassModel()
        data1 = dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue)

        # Verify if the model notify a model changed when a property is added
         # Create a function which change a variable inside
        _modelChanged = [0]
        def on_modelChanged():
            _modelChanged[0] = 1
        # Connect the signal
        dispatcher.connect(on_modelChanged, signal=GenericModel.SIGNAL_MODELCHANGED, sender=model1)
        propertiesDict1 = {data1.name : data1}
        model1.addProperties(propertiesDict1)
        self.assertEqual(_modelChanged[0], 1)

        _propChanged = [0]
        def on_propertyChanged():
            _propChanged[0] = 1
        # Connect the signal
        dispatcher.connect(on_propertyChanged, signal=GenericModel.SIGNAL_PROPERTYCHANGED, sender=model1)
        data1.value = 2
        self.assertEqual(_propChanged[0], 1)

    def test_setProperties(self):
        ## Test setPropertyValue and setPropertiesValue
        #
        name = 'testname'
        wrongname = 'xxx'
        limits = [-1 , 10]
        limitsDisc = [1 , 1.5 , 3.2, complex(1,1)]
        value  = 3.2
        initvalue = 1
        newvalue  = 1.1

        # Test set property of one values
        data1 = []
        model1 = DataClassModel()
        data1.append( dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue))
        data1.append(dataclass.DataClassNumber(name = name + str(2), limits = limits, value = value, initvalue = initvalue))
        data1.append(dataclass.DataClassDiscreteNumber(name = name + str(3) , limits = limitsDisc,  value = value, initvalue = initvalue))
        propertiesDict1 = {}
        for d in data1:
            propertiesDict1[d.name] = d
        model1.addProperties(propertiesDict1)

        # set and check values
        model1.setPropertyValue(name + str(1), newvalue)
        self.assertEqual(newvalue, model1.getPropertyValue(name + str(1)))

        # Test name is wrong
        with self.assertRaises(ModelException.PropertyNotPresentError):  model1.setPropertyValue(name, newvalue)


        ## Set a properties dict and check it
        propertiesDict1_2 = {}
        testNamesPropDict1_2 = []
        for p in data1:
            propertiesDict1_2[p.name] = 1.5
            testNamesPropDict1_2.append(p.name)
        model1.setPropertiesValue(propertiesDict1_2)
        dictvalues1_2 = model1.getPropertiesValue(testNamesPropDict1_2)
        for n in testNamesPropDict1_2:
            self.assertEqual(1.5, dictvalues1_2[n])

        ## Add a fake propr
        propertiesDict1_2[wrongname] = 1.5
        with self.assertRaises(ModelException.PropertyNotPresentError) : model1.setPropertiesValue(propertiesDict1_2)

    def test_reset(self):
        # Test model constructor with dictonary
        data = []
        name = 'testname'
        limits = [0 , 5]
        limitsDisc = [1 , 5 ,9 , 3 ,3 ,2, 1, 3.2, complex(1,1)]
        value  = 3
        initvalue = 1
        data.append(dataclass.DataClassNumber(name = name + str(1), limits = limits, value = value, initvalue = initvalue))
        data.append(dataclass.DataClassNumber(name = name + str(2), limits = limits, value = value, initvalue = initvalue))
        data.append(dataclass.DataClassDiscreteNumber(name = name + str(3) , limits = limitsDisc,  value = value, initvalue = initvalue))
        model1 = DataClassModel(data)
        model1.resetModel()

        for p in model1.getAllProperties():
            self.assertEqual(p.value, initvalue)

if __name__ == '__main__':
    unittest.main()
