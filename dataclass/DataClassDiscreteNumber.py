from dataclass.DataClass import DataClass
from numbers import Number
from utilities.misc import remove_duplicates_from_list

__author__ = 'law'


class DataClassDiscreteNumber(DataClass):
    """A Dara class object. Implement a number with only allowed discrete values"""

    def __init__(self, name, limits, value, description = 'Discrete Numeric Data', initvalue = None, unit = ''):
        '''
        Instantiate a Data Class implemented to manage any type of single numeric value from a discrete range
        The range is contained in the limits variable, which is mandatory in this implementation
        :param name: the viewname of the class (see DataClass)
        :param description: (see DataClass)
        :param value: a numeric value of any type  (int, float, bool etc), cannot be empty
        :param limits: a list of numeric values in any order. Duplicated items will be removed but not ordered
        :param initvalue: the init value used when a reset is called.
        NOTE: This is not set when the class is instantiated, call with value=initvalue
        :return: the instance or raise an exception
        '''
        super().__init__(name=name, description=description, value=value, limits=limits , initvalue=initvalue,  unit = unit)
        self._limits = remove_duplicates_from_list(limits)
        # self._limits = list(set(limits)) # create a set to remove duplicate and then store in a list

    def _checkLimits(self, limits):
        '''
        Reimplemented to check if the limits are an empty list (no limits) or a list with two elements sorted
        and if the elements are numbers
        :param limits:
        :return:
        '''

        # Check if the super class has something to say
        _checkedLimits = super()._checkLimits(limits)
        if not _checkedLimits[0]:
            return (False, _checkedLimits[1])

        try:
            # check limits length, at least should be 1
            if len(limits) < 1:
                return (False,'The limits length should be at least 1')

            # Check the first element of a list is a number
            for l in limits:
                if not isinstance(l, Number) :
                    return (False,'Found elements which is not a number {}'.format(l.__class__.__name__))
        except Exception as e:
            # the limits are not a list...
            return (False,'Error in limits format, exception {}: --- cause: {} '.format(e.__class__.__name__, e.__cause__))

        return (True, '')

    def _checkInitValue(self, initvalue):
        '''
        Verify if initvalue is a number and it is valid, satisfy one of the limits
        It can be empty
        :param initvalue:
        :return:
        '''
        _checkedInitValue = super()._checkInitValue(initvalue)
        if not _checkedInitValue[0]:
            return (False, _checkedInitValue[1])

        # Check if it is a number and length
        if not isinstance(initvalue, Number):
            if initvalue == None:
                return (True,'')
            else:
                return (False, 'InitValue is not a number. Format is {}'.format(initvalue.__class__.__name__))

        # Validate if it is a valid value
        _checkedInitValue = self._checkValue(initvalue)
        if not _checkedInitValue[0]:
            return (False, _checkedInitValue[1])
        else:
            return (True,'')


    def _checkValue(self, value):
        '''
        Reimplementation to check if this a number belongs to  discrete values inside limits
        :param value: the number to check
        :return: true if it is a number otherwise false
        '''

        # Check if the super class has something to say
        _checkedValue = super()._checkValue(value)
        if not _checkedValue[0]:
            return (False, _checkedValue[1])

        # Check if it is a number
        if not isinstance(value, Number):
            return False, 'Cannot set a value which is not a number. Format is {}'.format(value.__class__.__name__)

        if self._limits.count(value):
            return (True,'')
        else:
            return (False, "Value {} is not present in set {} ".format(value, self._limits ))
