__author__ = 'law'

def FormatErrorString(instance='', propertyname='', propertyvalue='', reason=''):
    errorstring =  'Error in Data property \n' \
                   '\tInstance : {0}\n' \
                   '\tProperty : {1}\n' \
                   '\tValue    : {2}\n' \
                   '\tReason   : {3}'.format(str(instance), str(propertyname), str(propertyvalue),str(reason))
    return errorstring

class DataNameError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'viewname',value,reason))

class DataDescriptionError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'description',value,reason))

class DataLimitsError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'limits',value,reason))

class DataValueError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'value',value,reason))

class DataInitValueError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'initvalue',value,reason))

class DataUnitError(Exception):
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'unit',value,reason))

class DataMaxLengthError(Exception):
    # This exception is used in DataClassString
    def __init__(self,instance,value,reason):
        super().__init__(FormatErrorString(instance,'maxlength',value,reason))