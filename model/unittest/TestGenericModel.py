__author__ = 'law'

import unittest
import model
from pydispatch import dispatcher


class TestGenericModel(unittest.TestCase):
    # TODO: TO be tested in  MODEL!!!
    # 1 - Reset, also to be implemented
    # 2 - Implement constructor test (single, empty, list)
    # 3 - Implement addproperty test (single, empty, list)


    def test_constructor(self):
        # Test empty _model
        _model = model.GenericModel()
        self.assertEqual(_model._propertyDictionary,{})

        # Test _model constructor with dict
        dataDict = {'PropA' : 1 , 'PropB': 2 , 'PropC': 3}
        _model = model.GenericModel(dataDict)
        self.assertEqual(_model._propertyDictionary,dataDict)

    def testPresence(self):
        model1 = model.GenericModel()
        propertiesDict1 = {'PropA' : 1}
        model1.addProperties(propertiesDict1)

        self.assertTrue(model1.isPropertyPresent('PropA'))
        self.assertFalse(model1.isPropertyPresent('PropB'))

    def test_addProperty(self):
        model1 = model.GenericModel()

        # Test add one
        propertiesDict1 = {'PropA' : 1}
        model1.addProperties(propertiesDict1)

        # Test add again same property leads to an exception
        with self.assertRaises(model.ModelException.PropertyAlreadyPresentError): model1.addProperties(propertiesDict1)

        # Test add multiple, should pass
        model2 = model.GenericModel()
        propertiesDict2 = {'PropA' : 1 , 'PropB': 2 , 'PropC': 3}
        model2.addProperties(propertiesDict2)

        # Test add multiple, raise an exception
        propertiesDict3 = {'PropA' : 1 , 'PropB': 2 }
        model3 = model.GenericModel()
        model3.addProperties(propertiesDict3)
        with self.assertRaises(model.ModelException.PropertyAlreadyPresentError): model3.addProperties({'PropB':3})

    def test_removeProperty(self):
        # Test add multiple, should pass
        model1 = model.GenericModel()
        keyslist = ['PropA' , 'PropB', 'PropC']
        propertiesDict1 = {keyslist[0] : 1 , keyslist[1]: 2 , keyslist[2]: 3}
        model1.addProperties(propertiesDict1)

        # Remove one key
        propertiesKeyRemove1 = keyslist[-1]
        model1.removeProperty(propertiesKeyRemove1)
        with self.assertRaises(model.ModelException.PropertyNotPresentError): model1.removeProperty(propertiesKeyRemove1)

        # Remove multiple keys
        propertiesKeyRemove2 = [keyslist[0] , keyslist[1]]
        model1.removeProperties(propertiesKeyRemove2)
        self.assertEqual(model1._propertyDictionary, {})

        # Remove already removed keys
        propertiesKeyRemove3 = keyslist

    def test_equailities(self):
        model1 = model.GenericModel()
        keyslist = ['PropA' , 'PropB', 'PropC']
        propertiesDict1 = {keyslist[0] : 1 , keyslist[1]: 2 , keyslist[2]: 3}
        model1.addProperties(propertiesDict1)

        # Test equal with another model
        model2 = model.GenericModel(propertiesDict1)
        self.assertEqual(model1,model2)

        # Test several not equal
        model3 = model.GenericModel()
        self.assertNotEqual(model1,model3)

        # Version not equal
        model4 = model.GenericModel(propertiesDict1)
        model4._version = ''
        self.assertNotEqual(model1,model4)

        # Another object
        self.assertNotEqual(model1,{})

    def test_getproperties(self):
        model1 = model.GenericModel()
        propertieslist1 = ['PropA' , 'PropB', 'PropC']
        propertiesValue = [1 ,2 ,3]
        propertiesDict1 = {propertieslist1[0] : propertiesValue[0] , propertieslist1[1]: propertiesValue[1] , propertieslist1[2]: propertiesValue[2]}
        model1.addProperties(propertiesDict1)

        # convert to set, because list could be in thw wrong order.
        # (the system assures the properties are unique
        self.assertEqual(set(propertieslist1),set(model1.getPropertiesName()))
        # Test getAllProperties
        self.assertEqual(set(propertiesValue),set(model1.getAllProperties()))

        # Test getProperty with list
        propertieslist2 = ['PropA']
        propertyValue2  = 1
        propertiesDict2 = {propertieslist2[0] : propertyValue2 }
        model2 = model.GenericModel(propertiesDict2)
        self.assertEqual(propertyValue2, model2.getProperty(propertieslist2[0]))

        # Test getProperty with single value
        propertiesName = 'PropA'
        propertyValue3  = 2
        propertiesDict3 = {propertiesName : propertyValue3 }
        model3 = model.GenericModel(propertiesDict3)
        self.assertEqual(propertyValue3, model3.getProperty(propertiesName))

    def test_signals(self):
        model1 = model.GenericModel()
        propertieslist1 = ['PropA' , 'PropB', 'PropC']
        propertiesValue = [1 ,2 ,3]
        propertiesDict1 = {propertieslist1[0] : propertiesValue[0] , propertieslist1[1]: propertiesValue[1] , propertieslist1[2]: propertiesValue[2]}

        # Verify if the model notify a model changed when a property is added
         # Create a function which change a variable inside
        _modelChanged = [0]
        def on_modelChanged():
            _modelChanged[0] = 1

        dispatcher.connect(on_modelChanged, signal=model.GenericModel.SIGNAL_MODELCHANGED, sender=model1)
        # Update the model and check it
        model1.addProperties(propertiesDict1)


if __name__ == '__main__':
    unittest.main()
