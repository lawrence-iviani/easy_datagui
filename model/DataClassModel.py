__author__ = 'law'

import model
from  dataclass.DataClass import DataClass
from collections import OrderedDict


class DataClassModel(model.GenericModel):

    def __init__(self, data={}):
        dataDict = self._convertToDict(data)
        super().__init__(dataDict)


    def addProperties(self, data):
        '''
        Add properties from a list
        :param propertydict: add as properties as dictionary in the form key, class
        :return:
        '''
        dataDict = self._convertToDict(data)
        super().addProperties(dataDict)

    def resetModel(self):
        '''
        Send a reset to all the properties stored in this model
        :return:
        '''
        for p in self.getAllProperties():
            p.reset()

    def _convertToDict(self, data):

        dataDict = OrderedDict()
        if isinstance(data, list):
            for d in data:
                if not isinstance(d, DataClass):
                    raise model.ModelException.PropertyIsNotCompatible(d.__class__.__name__, DataClass)
                dataDict[d.name] = d
        elif isinstance(data, DataClass):
            dataDict[data.name] = data
        elif isinstance(data, dict):
            dataDict = data
            for d in data.values():
                if not isinstance(d, DataClass):
                    raise model.PropertyIsNotCompatible(d.__class__.__name__, DataClass)
        else:
            raise model.PropertyIsNotCompatible(data.__class__.__name__, DataClass)

        return dataDict

    def setPropertyValue(self, propertyname, value):
        '''
        Set a value to a property in the model, given the viewname.
        :param propertyname:
        :param value:
        :return:
        '''
        # Check if prop viewname exists
        if  self.isPropertyPresent(propertyname):
            prop = self._propertyDictionary[propertyname]
        else:
            raise model.PropertyNotPresentError(propertyname)
        # Check if the value is compatible
        if not prop.testValueBeforeSet(value):
            raise model.PropertyValueError(propertyname, value)
        # Set the value
        prop.value = value

    def getPropertyValue(self, propertyname):
        # Check if prop viewname exists
        if  self.isPropertyPresent(propertyname):
            prop = self._propertyDictionary[propertyname]
        else:
            raise model.PropertyNotPresentError(propertyname)
        # Check if the value is compatible
        return prop.value