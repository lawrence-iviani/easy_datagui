from dataclass.DataClassDiscreteNumber import DataClassDiscreteNumber

__author__ = 'law'


class DataClassDiscreteIntNumber(DataClassDiscreteNumber):
    """A Data class object. Implement an INT  number with only allowed discrete values"""

    def __init__(self, name, limits, value, description = 'Discrete Numeric Data', initvalue = None, unit = ''):
        '''
        See DataClassDiscreteNumber, the same but with integer number
        :param name: the viewname of the class (see DataClass)
        :param description: (see DataClass)
        :param value: a numeric value of any type  (int, float, bool etc), cannot be empty
        :param limits: a list of numeric values in any order. Duplicated items will be removed but not ordered
        :param initvalue: the init value used when a reset is called.
        NOTE: This is not set when the class is instantiated, call with value=initvalue
        :return: the instance or raise an exception
        '''
        super().__init__(name=name, description=description, value=value, limits=limits , initvalue=initvalue,  unit = unit)

    def _checkLimits(self, limits):
        '''
        Add check for INT limits
        and if the elements are numbers
        :param limits:
        :return:
        '''

        for l in limits:
            if not isinstance(l, int):
                return (False, 'One or more limits is not integer, find ' + str(l) + ' is an instance of: ' + l.__class__.__name__)
        return super()._checkLimits(limits)


    def _checkInitValue(self, initvalue):
        '''
        Verify if initvalue is a number and it is valid, satisfy one of the limits
        It can be empty
        :param initvalue:
        :return:
        '''
        if not isinstance(initvalue, int):
            if not initvalue == None:
                return (False, 'InitValue is not an int. Format is {}'.format(initvalue.__class__.__name__))
        return super()._checkInitValue(initvalue)


    def _checkValue(self, value):
        '''
        Reimplementation to check if this a number belongs to  discrete values inside limits
        :param value: the number to check
        :return: true if it is a number otherwise false
        '''
        if not isinstance(value, int):
            return False, 'value is not an int. Format is {}'.format(value.__class__.__name__)

        # Check if the super class has something to say
        return super()._checkValue(value)
