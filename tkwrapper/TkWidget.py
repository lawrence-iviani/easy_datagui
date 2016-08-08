from widget.GenericWidget import GenericWidget
import tkinter as tk
import tkinter.ttk as ttk
import tkwrapper.XML_TKWidgetHelper
import sys

import logging


class TkWidget(GenericWidget):
    def __init__(self, parent, name, widget_type, datainstance=None):
        """

        :param parent: the tk window or frame which this widget is associated
        :param name:
        :param widget_type:
        :param datainstance:
        """
        self._parent = parent
        super().__init__(name, widget_type, datainstance)

    def pack(self, **kwargs):
        """
        Expose the method pack for layout management
        :param kwargs: see TK pack help
        :return:
        """
        self._tkwidget.pack(**kwargs)

    def grid(self, **kwargs):
        """
        Expose the method grid for layout management
        :param kwargs: see TK pack help
        :return:
        """
        self._tkwidget.grid(**kwargs)

    def _create_widget_hook(self, datainstance):
        """
        This method create the object associated to this widget, for example graphics etc.
        This method should be reimplemented by the inheriting class to shape the widget
        If the widget wrapper has nothing to do leaves unmodified
        :param datainstance:
        :return:
        """
        retval = False
        reason = 'Unknown reason'

        if self._widgettype == 'FloatWidget':
            self._tkwidget = ttk.Entry(self._parent)
            reason = self._widgettype + ' success'
            retval = True
        elif self._widgettype == 'IntWidget':
            self._tkwidget = ttk.Entry(self._parent)
            reason = self._widgettype + ' success'
            retval = True
        elif self._widgettype == 'BoolWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'ComboBoxWidget':
            self._tkwidget = ttk.Combobox(self._parent)
            self._tkwidget['values'] = tuple([str(v) for v in datainstance.limits])
            reason = self._widgettype + ' success'
            self._datatype = type(datainstance.limits[0])
            retval = True
        elif self._widgettype == 'RadioBoxWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'MultipleChoiceWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'LabelWidget':
            self._tkwidget = ttk.Label(self._parent)
            reason = self._widgettype + ' success'
            retval = True
        elif self._widgettype == 'EditLineWidget':
            self._tkwidget = ttk.Entry(self._parent)
            reason = self._widgettype + ' success'
            retval = True
        elif self._widgettype == 'OpenFileWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'SaveFileWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'SelectDirectoryWidget':
            reason = self._widgettype + ' not yet implemented'
        elif self._widgettype == 'TextWidget':
            self._tkwidget = tk.Text(self._parent, wrap='none')
            reason = self._widgettype + ' success'
            retval = True
        else:
            reason = self._widgettype + ' unknown/unsupported widget'

        # set the value
        if retval:
            self._set_widget_value_hook(datainstance.value)
            # self._tkwidget.pack()

        return (retval, reason)

    def _set_widget_value_hook(self, value):
        retval = False
        if isinstance(self._tkwidget, ttk.Label):
            self._tkwidget['text'] = value
            retval = True
        elif isinstance(self._tkwidget, ttk.Combobox):
            # TODO:  value should be set (cheching if exists??)
            self._tkwidget.set(value)
        elif isinstance(self._tkwidget, tk.Text):
            self._tkwidget.delete(1.0, tk.END)
            self._tkwidget.insert(1.0, value)
            retval = True
        elif isinstance(self._tkwidget, ttk.Entry):
            self._tkwidget.delete(0, tk.END)
            self._tkwidget.insert(0, value)
            retval = True
        return retval

    def _get_widget_value_hook(self):
        if isinstance(self._tkwidget, ttk.Label):
            return self._tkwidget['text']
        elif isinstance(self._tkwidget, tk.Text):
            retval = self._tkwidget.get(1.0, tk.END)
            if retval[-1] == '\n':
                retval = retval[:-1]
            return retval
        elif isinstance(self._tkwidget, ttk.Combobox):
            retval = self._tkwidget.get()
            if (self._datatype == float):
                retval = float(retval)
            elif (self._datatype == int):
                retval = int(retval)
            # if (self._datatype==ClassData)
            return retval
        elif isinstance(self._tkwidget, ttk.Entry):
            retval = self._tkwidget.get()
            # remove the end \n if present
            if retval[-1] =='\n':
                retval = retval[:-1]
            if self._widgettype == 'FloatWidget':
                retval = float(retval)
            elif self._widgettype == 'IntWidget':
                retval = int(retval)
            elif self._widgettype == 'BoolWidget':
                raise NotImplementedError('BoolWidget get value not implemented')
            return retval

    @staticmethod
    def loadXMLFileToData(filename, parent_widget=None):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param parent_widget:
        :param filename:
        :return:
        '''
        return tkwrapper.XML_TKWidgetHelper.XMLFileToTKWidget(filename, parent_widget=parent_widget)

    @staticmethod
    def fromXMLStringRepresentationToData(xmlstring, parent_widget=None):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param parent_widget:
        :param xmlstring:
        :return:
        '''
        return tkwrapper.XML_TKWidgetHelper.XMLStringToDataClassProperties(xmlstring, parent_widget=parent_widget)

    @staticmethod
    def fromElementsRepresentationToData(rootelement, parent_widget):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instancetype:
        :param rootelement:
        :return:
        '''
        return tkwrapper.XML_TKWidgetHelper.TKUTIL_elementsToProperties(rootelement, parent_widget=parent_widget)
        # return widget.XMLWidgetHelper.elementToWdiget(rootelement, parent_widget=parent_widget)
