import model

import dataclass
import xmlhelpers.XMLClassHelper
from pydispatch import dispatcher
from collections import OrderedDict

__author__ = 'law'


class GenericModel(xmlhelpers.XMLClassHelper):
    _version = '20151014'

     # A signal emitted when one or more property in the models are changed
    SIGNAL_PROPERTYCHANGED  = 'PropertyChanged'
    # The signal is emitted whenever the internal structure is changed (e.g. add or remove property
    SIGNAL_MODELCHANGED     = 'ModelChanged'

    def __init__(self, propertydict = {}):
        super().__init__()
        self._propertyDictionary = OrderedDict()
        if isinstance(propertydict,dict) and len(propertydict):
            self.addProperties(propertydict)
        self._connectEventHandlers()

    def _connectEventHandlers(self):
        '''
        Override this method for any event must be received
        :return:
        '''

        pass

    def addProperties(self, propertydict):
        '''
        Add properties from a dictionary
        :param propertydict: add as properties as dictionary in the form key, class
        :return:
        '''

        for p in propertydict:
            self.addProperty(p,propertydict.get(p))

    def addProperty(self, propertyname, prop):
        '''
        Add a single propertyname in the internal dictionary, and check for duplicate values
        :param propertyname:
        :param prop:
        :return:
        '''
        if not self.isPropertyPresent(propertyname):
            self._propertyDictionary[propertyname] = prop
            dispatcher.connect(self.onValueChangedHandler, signal=dataclass.DataClass.SIGNAL_VALUECHANGED, sender=prop)
            dispatcher.send( signal=GenericModel.SIGNAL_MODELCHANGED, sender=self )
        else:
            raise model.PropertyAlreadyPresentError(propertyname)

    def isPropertyPresent(self, propertyname):
        if self._propertyDictionary.get(propertyname) == None:
            return False
        else:
            return True

    def removeProperty(self, propertyname):
        '''
        Remove one property in the model
        :param propertyname:
        :return:
        '''
        prop = self._propertyDictionary.get(propertyname)
        if not prop == None:
            self._propertyDictionary.pop(propertyname)
            dispatcher.disconnect(self.onValueChangedHandler, signal=dataclass.DataClass.SIGNAL_VALUECHANGED, sender=prop)
            dispatcher.send( signal=GenericModel.SIGNAL_MODELCHANGED, sender=self )
        else:
            raise model.PropertyNotPresentError('Property {} it isn\'t present in the model already present'.format(propertyname))

    def removeProperties(self, keyslist):
        '''
        From a list of keys remove the property. Remove duplicate from list
        :param keyslist:
        :return:
        '''
        for k in keyslist:
            self.removeProperty(k)

    def getPropertiesName(self):
        return list(self._propertyDictionary.keys())

    def getProperty(self, propertyname):
        return self._propertyDictionary.get(propertyname)

    def getAllProperties(self):
        return list(self._propertyDictionary.values())

    def onValueChangedHandler(self, sender):
        '''
        A listener which send a notification if one or more properties are changed
        <b>The property is connected to this method, but must emit a signal dataclass.DataClass.SIGNAL_VALUECHANGED,
        otherwise the model won't be updated and this method is not called</b>
        :param sender: it is an object which contains at least a string representing its <b><viewname/b> and the
        <b>value</b>
        :return:
        '''
        _name = sender.name
        _value = sender.value
        _sender = sender

        # Create a class to transport the change in the underlay property
        class propertyChanged():
            name   = _name
            value  = _value
            sender = _sender
        # print('onValueChangedHandler: \n\t'
        #       'Name     : {0}\n\t'
        #       'Value    : {1}\n\t'
        #       'instance : {2}'.format(propertyChanged.viewname, propertyChanged.value, propertyChanged.sender))
        dispatcher.send(signal=GenericModel.SIGNAL_PROPERTYCHANGED, sender=self, propertyChanged=propertyChanged )

    def __eq__(self, other):
        # Check Instance
        if not isinstance(other,self.__class__):
            return False
        # Check version
        if not self._version == other._version:
            return False
        # Check internal dictionary
        if not self._propertyDictionary == other._propertyDictionary:
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_version(self):
        return self._version

    def resetModel(self):
        '''
        Send a reset to all the properties stored in this model
        This method should be reimplemented
        :return:
        '''
        raise NotImplementedError()

    def setPropertiesValue(self, dict_properties_value):
        for p in dict_properties_value:
            self.setPropertyValue(p, dict_properties_value.get(p))

    def setPropertyValue(self, propertyname, value):
        '''
        Abstract method which has to be reimplemented by the inherit class.
        Set a the value of underlay property in the model named propertyname
        :param propertyname:
        :param value:
        :return:
        '''
        raise NotImplementedError()

    def getPropertyValue(self, name):
        raise NotImplementedError()

    def getPropertiesValue(self, name_list):
        retval = OrderedDict()
        for n in name_list:
            retval[n] = self.getPropertyValue(n)
        return retval

    def getElementsRepresentation(self):
        ''' An element representation of this class in a string form is returned
        :return:
        '''
        return model.XMLModelHelper.modelToElements(self)

    def getXMLStringRepresentation(self):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return model.XMLModelHelper.modelToXML(self,xml_declaration=False)

    def saveToXMLFile(self, filename):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return model.XMLModelHelper.modelToXML(self,xml_declaration=True, filename=filename)

    @staticmethod
    def loadXMLFileToData(instanceName, filename):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param filename:
        :return:
        '''
        return model.XMLModelHelper.XMLFileToDataModel(filename)

    @staticmethod
    def fromXMLStringRepresentationToData(instanceName, xmlstring):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param xmlstring:
        :return:
        '''
        return model.XMLModelHelper.XMLStringToModel(xmlstring)

    @staticmethod
    def fromElementsRepresentationToData(instanceName, rootelement):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param rootelement:
        :return:
        '''
        return model.XMLModelHelper.elementsToModel(rootelement)

