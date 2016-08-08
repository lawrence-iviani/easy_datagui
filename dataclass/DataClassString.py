__author__ = 'law'

from dataclass.DataClass import DataClass
from dataclass.DataClassException import DataMaxLengthError
from numbers import Number


class DataClassString(DataClass):
    """A Data class object. Implement a string"""

    def __init__(self, name, value, description='Numeric Data',  initvalue='', unit='', maxlength=-1):
        '''
        Instantiate a Data Class implemented to manage any type of string
        :param name: the name of the class (see DataClass)
        :param description: (see DataClass)
        :param value: a numeric value of any type  (int, float, bool etc). Cannot be empty
        :param limits: can be empty or a list of two values sorted (e.g. [1,2] is valid but not [2,1]
        if it is complex the abs value is used to compare limits
        :param initvalue: the init value used when a reset is called.
        NOTE: This is not set when the class is instantiated, call with value=initvalue
        :return: the instance or raise an exception
        '''

        descmaxlen  = self._checkMaxlength(maxlength)
        if not descmaxlen[0]:
            raise DataMaxLengthError(self.__class__.__name__,description,descmaxlen[1])

        self._maxlength = maxlength
        super().__init__(name=name, description=description, value=value, limits=None, initvalue=initvalue, unit=unit)

    def _checkMaxlength(self, maxlength):
        if not isinstance(maxlength, int):
            return (False, "Max length is not an integer, found {0}".format(maxlength.__class__.__name__))
        if maxlength < -1:
            return (False, "Max length doesn\'t represents a valid length, found {0}".format(maxlength))
        return (True,'')
    def _checkInitValue(self, initvalue):
        '''
        Verify if initvalue is a number and it is valid (consistent with limits)
        It can be empty
        :param initvalue:
        :return:
        '''
        _checkedInitValue = super()._checkInitValue(initvalue)
        if not _checkedInitValue[0]:
            return (False, _checkedInitValue[1])

        # Check if it is a number and length
        if not isinstance(initvalue, str):
            if initvalue == None:
                return (True,'')
            else:
                return (False, 'InitValue is not a string. Format is {}'.format(initvalue.__class__.__name__))

        # Validate if it is a valid value
        _checkedInitValue = self._checkValue(initvalue)
        if not _checkedInitValue[0]:
            return (False, _checkedInitValue[1])
        else:
            return (True,'')


    def _checkValue(self, value):
        '''
        Reimplementation to check if this a number
        :param value: the number to check
        :return: true if it is a number otherwise false
        '''

        # Check if the super class has something to say
        _checkedValue = super()._checkValue(value)
        if not _checkedValue[0]:
            return (False, _checkedValue[1])

        # Check if it is None
        if value == None:
            return (False, "None as value is not admitted")

        # Check if it is a number
        if not isinstance(value, str):
            return (False, 'Cannot set a value which is not a string. Format is {}'.format(value.__class__.__name__))

        if not(self._maxlength==-1) and (len(value) > self._maxlength):
            return (False, 'Length of string is {0}, max allowed is {1}'.format(len(value),  self._maxlength))
        return (True,'')


    def get_maxlength(self):
        return self._maxlength

    maxlength = property(get_maxlength,             doc='The max length allowed, -1 allows any length.  Readonly ')
