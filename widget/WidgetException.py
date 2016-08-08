__author__ = 'law'

def FormatErrorString(instance='', widgetname='', widgettype='', reason=''):
    errorstring =  'Error in Widget \n' \
                   '\tInstance    : {0}\n' \
                   '\tWidget Name : {1}\n' \
                   '\tWidget Type : {2}\n' \
                   '\tReason      : {3}'.format(str(instance), str(widgetname), str(widgettype),str(reason))
    return errorstring

class WidgetAlreadyAssociated(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype, dataname):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype,'The widget viewname of {0} is already assigned to {1}, impossible to (re)associate to data viewname {2}'.format(widgetinstance.__class__.__name__ ,widgetname,dataname)))

class WidgetNotYetAssociated(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype,'The widget {0} is not yet associated with a DataClass Property'.format(widgetinstance.__class__.__name__)))

class WrongDataAssociation(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype, dataname):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype, 'The widget is named {0} and cannot be associated with data property viewname {1}'.format(widgetname,dataname)))

class WrongDataClass(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype, dataClassFound, dataClassExpected):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype, 'Invalid data instance {0}, expected was {1}'.format(dataClassFound,dataClassExpected)))

class NotExistentWidgetMatchingDataClass(Exception):
    def __init__(self,widgetinstance, widgetname,  widgettype, dataClass,reason):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype, 'The DataClass {0} cannot be associated to widget {1} due to {2}'.format(dataClass.name, widgettype, reason)))

class WidgetNotExisting(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype, 'The widget  {1} has not (yet?) implemented for data class {2}'.format(widgetinstance.__class__.__name__,widgetname, widgettype)))

class WidgetNameError(Exception):
    def __init__(self, widgetinstance, widgetname, widgettype, reason):
        super().__init__( FormatErrorString(widgetinstance,widgetname, widgettype, reason) )

class ErrorDuringDataAssociation(Exception):
    def __init__(self, widgetinstance, widgetname,  widgettype,  reason):
        super().__init__(FormatErrorString(widgetinstance,widgetname, widgettype, 'An error occured during data association, due to: {0}'.format(reason)))
