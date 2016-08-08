__author__ = 'law'


def FormatErrorString(instance='', viewname='',  reason=''):
    errorstring =  'Error in View \n' \
                   '\tInstance  : {0}\n' \
                   '\tView Name : {1}\n' \
                   '\tReason    : {2}'.format(str(instance), str(viewname),str(reason))
    return errorstring


class WrongWidgetClass(Exception):
    def __init__(self, viewinstance, viewname, widgetFound, widgetExpected):
        super().__init__(FormatErrorString(viewinstance, viewname, 'Invalid widget  instance {0}, expected was {1}'.format(widgetFound,widgetExpected)))


class WidgetNotAddable(Exception):
    def __init__(self,  viewinstance, viewname, widgetinstance):
        super().__init__(FormatErrorString(viewinstance, viewname,'Widget {0}: {1} is not addable'.format(widgetinstance.name, widgetinstance)))


class ErrorAddingWidget(Exception):
    def __init__(self,  viewinstance, viewname, reason):
        super().__init__(FormatErrorString(viewinstance, viewname, 'Adding a widget fail, due to: {0}'.format(reason)))



class ViewInternalError(Exception):
    def __init__(self, viewinstance, viewname, reason):
        super().__init__(FormatErrorString( viewinstance, viewname, 'An internal error happened, reason: \n\t' + reason))


class SubViewAlreadyPresentError(Exception):
    def __init__(self, viewinstance, viewname,  reason):
        super().__init__(FormatErrorString( viewinstance, viewname, 'Tried to add a wrong view, reason: \n\t' + reason))


class WrongSubViewClass(Exception):
    def __init__(self, viewinstance, viewname, subviewfound, subviewexpected):
        super().__init__(FormatErrorString(viewinstance,viewname, 'Invalid subview instance {0}, expected was {1}'.format(subviewfound,subviewexpected)))
