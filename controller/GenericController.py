import model
import controller
import view
import dataclass
from xmlhelpers.XMLClassHelper import XMLClassHelper
import utilities.misc
import widget
from pydispatch import dispatcher
from collections import OrderedDict

__author__ = 'law'

class GenericController(XMLClassHelper):
    '''
    A class
    '''
    _version = '20151214'

    def __init__(self, model_instance, view_instance):
        super().__init__()

        if not issubclass(model_instance.__class__, model.GenericModel):
            raise controller.ModelNotCompatible(self, model_instance, model.GenericModel)
        self._model = model_instance

        if not issubclass(view_instance.__class__, view.GenericView):
            raise controller.ModelNotCompatible(self, view_instance, view.GenericView)
        self._view = view_instance

        dispatcher.connect(self._viewUpdateHandler, signal=view.GenericView.SIGNAL_VIEWUPDATE, sender=view_instance)


    def _viewUpdateHandler(self, signal, sender, changedPropertiesDict ):
        '''
        Catch any update from the view stored and manage the set model operation
        :return:
        '''
        print('signal' + str(signal) + ' sender=' + str(sender) + ' ' + str(changedPropertiesDict))

    def getModel(self):
        return self._model

    def getView(self):
        return self._view

    def addPropertyToModel(self, data_property):
        '''
        Add to the internal model a property defined in data_property (inherits from DataClass) and the relative widgets
        associated to the property. The widget must be already added to the view to be properly showed
        :param data_property:
        :param widget_list_property:
        :return:
        '''

        try:
            # Then add property to model and widget
            self._model.addProperty(data_property.name, data_property)
        except Exception as e:
            raise controller.ErrorAddingProperty(self, str(e))

    def addWidgetToView(self, name_property, widget_instance, view_name=''):
        '''
        Add a widget, which is not yet associated to the data, to the view name list.
        Associate the data
        :param name_property:
        :param widget_instance:
        :param view_name:
        :return:
        '''

        # The property exists?
        _prop = self._model.getProperty(name_property)
        if _prop is None:
            raise controller.ErrorRetrievingProperty(self, name_property , 'Property not found')

        try:
            widget_instance.associateData(_prop)
        except Exception as e:
            raise controller.ErrorAssociatingDatToWidget(self, name_property, widget_instance ,str(e))

        # view and widget_instance check
        _views = []
        try:
            if view_name == '':
                # if self._view.isWidgetPresent(widget_instance.name):
                #     raise view.WidgetAlreadyPresentError(self._view, self._view.viewname, widget_instance.name)
                _views.append(self._view)
            else:
                # Create a list before add, I want to check if the widget is present
                for sv in self._view.getSubViewListByName(view_name):
                    if not sv.isAddable(widget_instance):
                        raise view.WidgetNotAddable(sv, sv.viewname, widget_instance)
                    _views.append(sv)
            if len(_views) == 0:
                raise controller.ViewNotFound(self, name_property, widget_instance,view_name)
        except Exception as e:
            _viewError = (_views[-1] if len(_views) else None) # Retrieve the last added view which should be the one with the error
            raise controller.ErrorAddingWidgetToView(self, name_property, widget_instance,_viewError, str(e))

        # Finally, add the widget_instance in the several views
        # TODO: one widget_instance only or one widget_instance for every view????
        # TODO: Error shoudn't happen at this stage but a try ... catch should be used
        for v in _views:
            v.addWidget(widget_instance)

    def addPropertyToModelAndView(self, data_property, widget_implementation, widget_type, view_name=''):
        '''
        Add to the internal model a property (inerithing from DataClass), instantiate a widget defined by the string
        widget_implementation and add to all the views with the view_name.
        View_name can be a list of strings, in this way a new widget is instantiated and added to all the views and
        sub views with the given names
        If no view_name is given the widget is instantiated and added to the main view
        In case of error nothing is added, data_property either widget
        :param data_property:
        :param widget_implementation:
        :param widget_type:
        :param view_name:
        :return:
        '''

        try:
            self.addPropertyToModel(data_property)
        except Exception as e:
            raise e  # TODO: define an exception at this point

        try:
            _module,_namespace, _classname = utilities.misc.UTIL_importModule(widget_implementation)
            if _module is None:
                raise controller.InvalidModule(widget_implementation, _module)
            _widget = eval('_module.'+ _classname + "(\'" + data_property.name + "\',\'" +   widget_type + "\')")
            self.addWidgetToView( data_property.name, _widget, view_name)
        except Exception as e:
            # I want to remove the property in case of an error
            self._model.removeProperty(data_property.name)
            raise e  # TODO: define an exception at this point

    def setValues(self, dict_values):
        '''
        From a dictonary in the form {name, value} set the values of every
        :param dict_values:
        :return:
        '''
        self._model.setPropertiesValue(dict_values)

    def getValues(self, name_list):
        return self._model.getPropertiesValue(name_list)

    def setValue(self, prop_name, value):
        '''
        For the property called prop_name set the value. A simple wrapper, it is like to retrive the model and use the relative
        Set value
        :param prop_name:
        :param value:
        :return:
        '''
        self._model.setPropertyValue(prop_name, value)

    def getValue(self, name):
        '''
        Return the value of the  properties with attribute name. It is like to retrieve the value from the model
        :param name:
        :return: the value of the data class
        '''
        return self._model.getPropertyValue(name)

    # def _connectProperty(self):
    #     '''
    #     TODO: prameters to define,
    #     The purpose is to connect
    #     :return:
    #     '''
    #     # 1. Get the list of propert

    @staticmethod
    def modelFactory(model_implementation):
        '''
        Create an empty model  using the factory pattern
        :param model_implementation:
        :return:
        '''

        # _namespace, _classname = utilities.misc.util_get_namespace(model_implementation)
        # __import__(_namespace)
        # _module = sys.modules[_namespace]
        # if _module is None:
        #     raise ImportError()#  xmlhelpers.XMLHelpersException.InvalidModule(d.tag, class_module)

        _module,_namespace, _classname = utilities.misc.UTIL_importModule(model_implementation)
        if _module is None:
            raise controller.InvalidModule(model_implementation, _module)
        return eval('_module.' + _classname + "("")")

    @staticmethod
    def viewFactory(view_implementation):
        '''
        Create an empty view using the factory pattern
        :return:
        '''

        # _namespace, _classname = utilities.misc.util_get_namespace(view_implementation)
        # __import__(_namespace)
        # _module = sys.modules[_namespace]
        # if _module is None:
        #     raise ImportError()#  xmlhelpers.XMLHelpersException.InvalidModule(d.tag, class_module)

        _module,_namespace, _classname = utilities.misc.UTIL_importModule(view_implementation)
        if _module is None:
            raise controller.InvalidModule(view_implementation, _module)
        return eval('_module.' + _classname + "("")")

    # TODO: load/save XML