__author__ = 'law'

import widget
import widget.XMLWidgetHelper
from dataclass import (DataClassNumber, DataClass)
import xmlhelpers
from pydispatch import dispatcher
from utilities.misc import util_check_is_valid_name, UTIL_listProperties


class GenericWidget(xmlhelpers.XMLClassHelper):
    '''
    This class is the basic class which all the widgets must inherits. It doesn't provide any GUI implementation
    but only the glue for the MVC system. The widget it is the graphic component associated to the data property
    which is displayed by the view. A single data property could have no widget, one widget or many widgets.
    '''
    # The version of this class, to preserve compatibility
    _version = '20151029'

    # The label for a value changed, it is associated to the signal emitted when value is changed
    SIGNAL_WIDGETUPDATE = 'WidgetUpdate'

    def __init__(self, name, widget_type, datainstance=None):
        super().__init__()

        # Check viewname
        (is_valid_name, reason) = self._checkName(name)
        if not is_valid_name:
            raise widget.WidgetNameError(self, name, widget_type, reason)
        self._name = name
        self._dataAssociated = False

        # Check if this widget is supported
        if not widget_type in GenericWidget.getSupportedWidgets():
            raise widget.WidgetNotExisting(self, name, widget_type)
        self._widgettype = widget_type

        if not datainstance is None:
            self.associateData(datainstance)

    def _checkName(self, name):
        """
        Check if the viewname is correct.
        Check if it is a string, length and must not contains space.
        :param name:
        :return:
        """
        return util_check_is_valid_name(name)

    def isDataAssociated(self):
        return self._dataAssociated

    def associateData(self, datainstance):
        """
        This function associated the instance of a DataClass to  this widget
        The widget viewname must be the same of the DataClass viewname and the widget type must be compatible
        (isValidWidget must be satisfied)
        The private method _create_widget_hook is called, inheriting class should re-implement this method in order to create
        the real widget implementation
        :param datainstance: an Instance of DataClass
        :return: in case of error raise an Exception
        """
        # Several checks
        # Is datainstance a valid data property?
        if not isinstance(datainstance, DataClass):
            raise widget.WrongDataClass(self, self.name, self.widget_type, datainstance, DataClass)
        # Is the data already associated?
        if self.isDataAssociated():
            raise widget.WidgetAlreadyAssociated(self, self.name, self.widget_type, datainstance.name)
        # Is the viewname assigned to this widget the same of the data property?
        if not (self.name == datainstance.name):
            raise widget.WrongDataAssociation(self, self.name, self.widget_type, datainstance.name)
        # Is it possible to associate this data property to this widget?
        (isvalid, reason) = GenericWidget.isValidWidget(datainstance, self.widget_type)
        if not isvalid:
            raise widget.NotExistentWidgetMatchingDataClass(self, self.name, self.widget_type, datainstance, reason)

        # Create the widget
        (widgetIstantiated, reason) = self._create_widget_hook(datainstance)
        if not widgetIstantiated:
            raise widget.ErrorDuringDataAssociation(self, self.name, self.widget_type, 'Due to exception: ' + reason)
        # Then Connect SIGNAL_VALUECHANGED in order to update the UI
        dispatcher.connect(self._update_widget_value_handler, signal=DataClass.SIGNAL_VALUECHANGED, sender=datainstance)

        # OK, then the data association is finished
        self._dataAssociated = True

    def _create_widget_hook(self, datainstance):
        '''
        This method create the object associated to this widget, for example graphics etc.
        This method should be reimplemented by the inheriting class to shape the widget
        If the widget wrapper has nothing to do leaves unmodified
        :param datainstance:
        :return:
        '''
        return (True, '')

    def get_name(self):
        return self._name

    def get_widget_type(self):
        return self._widgettype

    def set_widget_value(self, value):
        '''
        This method set the value  in the widget, in the same way of a user action.
        It is based on the implementation of the underlay widget mechanism and for this reason an hook is called

        :return: True if the value is updated correctly otherwise return false
        '''
        if not self.isDataAssociated():
            raise widget.WidgetNotYetAssociated(self, self.name, self.widget_type)
        value_set = self._set_widget_value_hook(value)
        if value_set:
            dispatcher.send(signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=self)
        return value_set

    def _set_widget_value_hook(self, value):
        '''
        Override this method  to change the value stored in the actual UI of this widget.
        This method must be implemented on the widget class mechanism and will be called by set_widget_value
        :return: True if the value is updated correctly otherwise return false
        '''
        raise NotImplementedError('_set_widget_value_hook must be implemented in the widget implementation')

    def get_widget_value(self):
        '''
        This method return the value stored in the widget. Because the value retrieval is based on the
        widget mechanism an hook is called
        :return: the value associated to this class, it should be the same of the dataclass associated
        '''
        if not self.isDataAssociated():
            raise widget.WidgetNotYetAssociated(self, self.name, self.widget_type)
        return self._get_widget_value_hook()

    def _get_widget_value_hook(self):
        '''
        Override this method  to return the value stored in the actual UI of this widget.
        This method must be based on the implementation of the widget class
        :return: the value associated to this class, it should be the same of the dataclass associated
        '''
        raise NotImplementedError('_get_widget_value_hook must be implemented in the widget implementation')

    def _update_widget_value_handler(self, sender):
        '''
        Recevice the signal of a DataClass.SIGNAL_VALUECHANGED and manage the update process
        :param sender: the reference to the data class which is changing the value
        :return:
        '''
        if not isinstance(sender, DataClass):
            raise widget.WrongDataClass(self, self.name, self.widget_type, sender, DataClass)

        new_value = sender.value
        actual_value = self.get_widget_value()
        if not new_value == actual_value:
            self.set_widget_value(new_value)

    def get_version(self):
        return self._version

    def get_instance(self):
        return self._dataAssociated

    """Properties list"""
    name = property(get_name, doc='The viewname of this widget. It is associated to a data property viewname. Readonly')
    widget_type = property(get_widget_type, doc='The widget type. Readonly')

    """ Static Attributes """
    _CONST_class_widget_relation = {
        'DataClassNumber': ['FloatWidget'],  # -> NumericTypeItem , FloatTypeItem (plus Slider option))
        'DataClassIntNumber': ['IntWidget'],  # IntTypeItem (plus Slider option))
        'DataClassBool': ['BoolWidget'],  # BoolItem
        'DataClassDiscreteNumber': ['ComboBoxWidget', 'RadioBoxWidget', 'MultipleChoiceWidget'],
        'DataClassDiscreteIntNumber': ['ComboBoxWidget', 'RadioBoxWidget', 'MultipleChoiceWidget'],
    # ChoiceItem, MultipleChoiceItem  (horizontal or vertical options)
        'DataClassString': ['TextWidget', 'LabelWidget', 'EditLineWidget', 'OpenFileWidget', 'SaveFileWidget',
                            'SelectDirectoryWidget'],  # StringItem, FileSaveItem, FileOpenItem, DirectoryItem
        'DataClassDiscreteString': ['ComboBoxWidget', 'RadioBoxWidget', 'MultipleChoiceWidget'],
        'DataClassMultipleString': ['TextWidget', 'ComboBoxWidget', 'RadioBoxWidget', 'MultipleChoiceWidget',
                                    'OpenMultipleFilesWidget'],
    # TextItem , ChoiceItem, MultipleChoiceItem (horizontal or vertical options), FilesOpenItem,
        'DataClassDate': [],  # DateItem
        'DataClassColor': [],  # ColorItem
        'DataClassDictionary': [],  # DictItem
        'DataClassArrayNumber': [],  # FloatArrayItem
    }

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            areequals = True
            for p in UTIL_listProperties(self):
                areequals = areequals and (getattr(self, p) == getattr(other, p))
            return areequals
        # in this case other is a list of length 1
        elif isinstance(other, list) and len(other) == 1:
            areequals = True
            for p in UTIL_listProperties(self):
                areequals = areequals and (getattr(self, p) == getattr(other[0], p))
            return areequals
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def getAvailableWidgetsForDataClass(dataclassobject):
        '''
        For the given DataClass object return a list of available widgets type
        This is just a link between the available class and the implementation which must be done in the inerithed class
        :param dataclasstype:
        :return: a list of available
        '''
        return GenericWidget._CONST_class_widget_relation.get(dataclassobject.__class__.__name__, [])

    @staticmethod
    def getSupportedWidgets():
        """
        Generate a list of unique widget supported by the generic widget and which should be implemented in the implementing
        class
        :return: a list containing the strings description of the supported widgets (  ['EditLineWidget', 'OpenMultipleFilesWidget', etc... ]
        """

        widgetlist = []
        values = GenericWidget._CONST_class_widget_relation.values()
        for v in values:
            widgetlist.extend(v)
        return list(set(widgetlist))

    @staticmethod
    def getSupportedDataClass():
        """
        Generate a list of unique DataClass supported covered by the generic widget mechanism and which should be implemented in the implementing
        class
        :return: a list containing the strings description of the supported widgets (  ['DataClassMultipleString', 'DataClassDictionary', etc... ]
        """
        return list(GenericWidget._CONST_class_widget_relation.keys())

    @staticmethod
    def isValidWidget(dataclassobject, widgettype):
        if not (dataclassobject.__class__.__name__ in GenericWidget.getSupportedDataClass()):
            return (False, dataclassobject.__class__.__name__ + ' is not supported by a widget representation')

        availableWidget = GenericWidget.getAvailableWidgetsForDataClass(dataclassobject)
        if (not len(availableWidget)) or (not widgettype in availableWidget):
            return (
            False, 'Widget ' + str(widgettype) + ' is not available for class ' + dataclassobject.__class__.__name__)

        return (True, '')

    def getElementsRepresentation(self):
        ''' An element representation of this class in a string form is returned
        :return:
        '''
        return widget.XMLWidgetHelper.widgetToElement(self)

    def getXMLStringRepresentation(self):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return widget.XMLWidgetHelper.widgetToXML(self, xml_declaration=False)

    def saveToXMLFile(self, filename):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        return widget.XMLWidgetHelper.widgetToXML(self, xml_declaration=True, filename=filename)

    @staticmethod
    def loadXMLFileToData(filename):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instancetype:
        :param filename:
        :return:
        '''
        return widget.XMLWidgetHelper.XMLFileToWidget(filename)

    @staticmethod
    def fromXMLStringRepresentationToData(xmlstring):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instancetype:
        :param xmlstring:
        :return:
        '''
        return widget.XMLWidgetHelper.XMLStringToWidget(xmlstring)

    @staticmethod
    def fromElementsRepresentationToData(rootelement):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instancetype:
        :param rootelement:
        :return:
        '''
        return widget.XMLWidgetHelper.elementToWdiget(rootelement)
