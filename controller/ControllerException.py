

def FormatErrorString(instance='', model='', view='', reason=''):
    errorstring =  'Error in Controller \n' \
                   '\tInstance  : {0}\n' \
                   '\tModel     : {1}\n' \
                   '\tview      : {2}\n' \
                   '\tReason    : {3}'.format(str(instance), str(model), str(view), str(reason))
    return errorstring


class InvalidModule(Exception):
    def __init__(self, controller,  module, instance):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'A problem loading module {0}, for instance: {1}'.format(module, instance)))

class ErrorAddingProperty(Exception):
    def __init__(self, controller, reason):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'An error occurs trying to add a property: ' + reason))

class ErrorAssociatingDatToWidget(Exception):
    def __init__(self, controller, property_name, widget_instance,reason):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'An error occurs trying to associate data property {0} to widget {1}: {2}'.format(property_name, widget_instance,reason) ))


class ErrorRetrievingProperty(Exception):
    def __init__(self, controller, property_name,reason):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'Property {0} not  retrieved: {1}'.format(property_name, reason)))


class ErrorAddingWidgetToView(Exception):
    def __init__(self, controller, property_name, widget_instance, view, reason):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'Property {0} not  retrieved: {1}'.format(property_name, reason)))


class ViewNotFound(Exception):
    def __init__(self, controller, property_name, widget_instance, view_name):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           controller.getView(),
                                           'View {0} is not present in the controller view list'.format(view_name)))


class ModelNotCompatible(Exception):
    def __init__(self, controller, model_instance, model_expected):
        super().__init__(FormatErrorString(controller,
                                           None,
                                           None,
                                           'Model instance {0} is not supported (should inherit from {1} '.
                                           format(model_instance, model_expected)))


class ViewNotCompatible(Exception):
    def __init__(self, controller, view_instance, view_expected):
        super().__init__(FormatErrorString(controller,
                                           controller.getModel(),
                                           None,
                                           'View  instance {0} is not supported (should inherit from {1} '.
                                           format(view_instance, view_expected)))