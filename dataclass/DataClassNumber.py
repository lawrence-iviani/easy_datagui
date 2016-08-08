from dataclass.DataClass import DataClass
from numbers import Number

__author__ = 'law'


class DataClassNumber(DataClass):
    """A Data class object. Implement a number of any type (int, long, float or complex))"""

    def __init__(self, name, value, description = 'Numeric Data',  limits = None, initvalue = None, unit = ''):
        """
        Instantiate a Data Class implemented to manage any type of single numeric value
        :param name: the name of the class (see DataClass)
        :param description: (see DataClass)
        :param value: a numeric value of any type  (int, float, bool etc). Cannot be empty
        :param limits: can be empty or a list of two values sorted (e.g. [1,2] is valid but not [2,1]
        if it is complex the abs value is used to compare limits
        :param initvalue: the init value used when a reset is called.
        NOTE: This is not set when the class is instantiated, call with value=initvalue
        :return: the instance or raise an exception
        """
        super().__init__(name=name, description=description, value=value, limits=limits , initvalue=initvalue, unit = unit)


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
            # no limits
            if limits == None or len(limits) == 0:
                return (True,'')

            # Check limits are numbers instance and are ordered
            if len(limits) == 2:
                if isinstance(limits[0], Number) and isinstance(limits[1], Number):
                    if limits[0] <= limits[1]:
                        return (True,'')
                    else:
                        return (False,'Limits order aren\'t correct {} > {} '.format(limits[0], limits[1]))
                else:
                    return (False,'Limits are not a number. Lower limit is {}, Higher limit is {}, '
                            .format(limits[0].__class__.__name__,limits[1].__class__.__name__))
            else:
                return (False,'Wrong number of limits, 0 or 2 are allowed, found {} value(s)'.format(len(limits)))

        except Exception as e:
            # the limits are not a list...
            return (False,'Error in limits format, exception {}: --- cause: {} '.format(e.__class__.__name__, e.__cause__))


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
        if not isinstance(value, Number):
            return (False, 'Cannot set a value which is not a number. Format is {}'.format(value.__class__.__name__))

        # Check for limits
        if self._limits == None or  len(self._limits) == 0:
            return (True,'')
        
        l_lo = self._limits[0]
        l_hi = self._limits[1]

        if isinstance(value, complex):
            absvalue = abs(value)
            if absvalue >= l_lo and absvalue <= l_hi:
                return (True,'')
            else:
                return (False, "Absolute value {} of {} is out of limits [{} - {}] ".format(absvalue, value, l_lo,l_hi))
        else:
            if value >= l_lo and value <= l_hi:
                return (True,'')
            else:
                return (False, "Value {} is out of limits [{} - {}] ".format(value, l_lo,l_hi))