from dataclass.DataClassNumber import DataClassNumber
from numbers import Number

__author__ = 'law'


class DataClassIntNumber(DataClassNumber):
    """
        An extension for data class number
    """

    def __init__(self, name, value, description='Integer numeric Data', limits=None, initvalue=None, unit=''):
        """
        See DataClass number constructor
        """
        super().__init__(name=name, description=description, value=value, limits=limits, initvalue=initvalue, unit=unit)

    def _checkLimits(self, limits):
        '''
        Reimplemented to check if the limits are integer,  call super method
        '''

        if (not limits == None) and len(limits):
            for l in limits:
                if not isinstance(l,int):
                    return False, 'One or more limits is not integer, find ' + str(l) + ' is an instance of: ' + l.__class__.__name__

        return super()._checkLimits(limits)

    def _checkInitValue(self, initvalue):
        '''
        Reimplemented to check if the init value is integer,  call super method
        '''
        if not isinstance(initvalue, int):
            if initvalue == None:
                return (True, '')
            else:
                return (False, 'init value is not an integer, instead is a ' + initvalue.__class__.__name__)
        return super()._checkInitValue(initvalue)



    def _checkValue(self, value):
        '''
        Reimplemented to check if the  value is integer,  call super method
        '''

        # Check if the super class has something to say
        if not isinstance(value, int):
            return (False, 'value is not an integer, instead is a ' + value.__class__.__name__)
        return super()._checkValue(value)