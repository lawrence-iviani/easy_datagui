__author__ = 'law'

import dataclass
import xmlhelpers
from pydispatch import dispatcher
from utilities.misc import util_check_is_valid_name, UTIL_listProperties


class DataClass(xmlhelpers.XMLClassHelper):
    """A Data class object. A generic container implementation"""

    # The version of this class, to preserve compatibility
    _version = '20151006'

    # The label for a value changed, it is associated to the signal emitted when value is changed
    SIGNAL_VALUECHANGED = 'ValueChanged'

    def __init__(self, name, description = 'Generic Data', value=None, limits = None, initvalue = None, unit = ''):
        '''
        The super class for any type of data
        :param name: a string, representing the viewname without space in it (set only with constructor and it is mandatory)
        :param description: a string with printable characters
        :param value: the value associated to this instance, it is a get/set property.
        :param limits: the limits of the value. Depend on the implementation. Guide lines are that this should contain
        numeric interval or a discrete number of value
        :param initvalue: the initial value, dependent on the implementation
        :return: the instantiated object or raise an exception
        '''
        super().__init__()

        # Check viewname
        namecheck  = self._checkName(name)
        if not namecheck[0]:
            raise dataclass.DataNameError(self.__class__.__name__,name,namecheck[1])
        self._name          = name

        # Check description
        descrcheck  = self._checkDescription(description)
        if not descrcheck[0]:
            raise dataclass.DataDescriptionError(self.__class__.__name__,description,descrcheck[1])
        self._description   = description

        # Check if limits format is correct
        limitcheck = self._checkLimits(limits)
        if not limitcheck[0]:
            raise dataclass.DataLimitsError(self.__class__.__name__,limits,limitcheck[1])
        self._limits        = limits


        # check if the limit value is correct and compatible
        initvaluecheck = self._checkInitValue(initvalue)
        if not initvaluecheck[0]:
            raise dataclass.DataInitValueError(self.__class__.__name__,initvalue,initvaluecheck[1])
        self._initvalue     = initvalue

        # Check if the unit is valid
        unitcheck = self._checkUnit(unit)
        if not unitcheck[0]:
            raise dataclass.DataUnitError(self.__class__.__name__,unit, unitcheck[1])
        self._unit          = unit

        # Set the values but performs a reset before set
        self._value = None
        self.reset()
        self.value          = value

        self._connectEventHandlers()

    def _connectEventHandlers(self):
        '''
        Override this method for any event must be received and managed by the inheriting class
        :return:
        '''
        pass

    def _checkInitValue(self, initValue):
        '''
        Reimplement to verify if the init value is correct
        :param initValue:
        :return:
        '''
        return (True,'')

    def _checkDescription(self,description):
        '''
        Check if the description  is in a  correct format.
        Check if it is a string with printable values
        :param description:
        :return:
        '''
        if not isinstance(description,str):
            return (False, "Description is not a string")

        if not description.isprintable():
            return (False, "Description is not printable")

        return (True,'')

    def _checkName(self, name):
        return util_check_is_valid_name(name)

    def _checkValue(self, value):
        '''
        Reimplement this function to check the limits and errors in the value
        :param value:
        :return: true if the value is corrected, otherwise false and a description of why the value is not correct
        '''
        return True, ''

    def _checkLimits(self, limits):
        '''
        Reimplement this function to check if the limits are in the correct values
        :param limits:
        :return: true if the limits are in the correct format, otherwise false and a description of why the value is not correct
        '''
        return (True,'')

    def _checkUnit(self,unit):
        if not isinstance(unit,str):
            return (False, "Unit should be a string")
        return (True,'')

    def reset(self):
        '''
        :return:
        '''
        _checkedValue = self._checkValue(self._initvalue)
        if _checkedValue[0]:
            self.value = self._initvalue
        else:
            self._value = None

    def set_value(self, value):
        '''
        :param value:
        :return:
        '''
        _checkedValue = self._checkValue(value)
        if _checkedValue[0]:
            if not value == self.value:
                self._value = value
                dispatcher.send(signal=DataClass.SIGNAL_VALUECHANGED, sender=self)
        else:
            raise dataclass.DataValueError(self.__class__.__name__,value,_checkedValue[1])

    def valueListener(self, sender):
           pass# print('Received: {0}'.format(sender.value))

    def testValueBeforeSet(self, value):
        '''
        Check if the value is assignable, otherwise return a message with the reasne
        :param value: the value to be checked
        :return: a tuple with (True/False, Message).
            True if test is ok (value assignable) and no message,
            False if test fails with a message containing the reason
        '''
        return self._checkValue(value)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            areequals = True
            for p in UTIL_listProperties(self):
                areequals = areequals and (getattr(self, p) == getattr(other, p))
            return areequals
        # in this case other is a list of length 1
        elif isinstance(other, list) and len(other) == 1:
            areequals = True
            for p in UTIL_listProperties(self):
                areequals = areequals and (getattr(self, p) == getattr(other[0], p))
            return areequals
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_version(self):
        return self._version

    def get_value(self):
        return self._value

    def get_limits(self):
        return self._limits

    def get_name(self):
        return self._name

    def get_description(self):
        return  self._description

    def get_initValue(self):
        return self._initvalue

    def get_unit(self):
        return self._unit

    """Properties list"""
    name        = property(get_name,             doc='The viewname of this data. Readonly')
    description = property(get_description,      doc='Description of this property. Readonly')
    value       = property(get_value, set_value, doc='The value stored in this class, Read and write')
    limits      = property(get_limits,           doc='The Limits associated to this value. Readonly')
    initvalue   = property(get_initValue,        doc='The initial value associated to this class.  Readonly and assigned to value during a reset operation')
    unit        = property(get_unit,             doc='The unit associated to this data class.  Readonly ')

    def getElementsRepresentation(self):
        ''' An element representation of this class in a string form is returned
        :return:
        '''
        return dataclass.XMLDataClassHelper.dataClassPropertiesToElement(self)

    def getXMLStringRepresentation(self):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return dataclass.XMLDataClassHelper.dataClassPropertiesToXML(self,xml_declaration=False)

    def saveToXMLFile(self, filename):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return dataclass.XMLDataClassHelper.dataClassPropertiesToXML(self,xml_declaration=True, filename=filename)

    @staticmethod
    def loadXMLFileToData( filename):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param filename:
        :return:
        '''
        return dataclass.XMLDataClassHelper.XMLFileToDataClassProperties(filename)

    @staticmethod
    def fromXMLStringRepresentationToData(xmlstring):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instance_name:
        :param xmlstring:
        :return:
        '''
        return dataclass.XMLDataClassHelper.XMLStringToDataClassProperties(xmlstring)

    @staticmethod
    def fromElementsRepresentationToData(rootelement):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param rootelement:
        :return:
        '''
        return dataclass.XMLDataClassHelper.elementToDataClassProperties(rootelement)

class DataClassNotSupported(DataClass):
    '''
    This class is used only for testint
    '''
    pass