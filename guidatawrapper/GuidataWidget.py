import guidatawrapper
from widget.GenericWidget import GenericWidget
import widget
from guidata.dataset.dataitems import (ChoiceItem, FloatItem, StringItem, NumericTypeItem,
                                       DirectoryItem, FileOpenItem, MultipleChoiceItem)
from pydispatch import dispatcher
import logging
__author__ = 'law'


class GuidataWidget(GenericWidget):
    def __init__(self, name, widgettype, datainstance = None):
        self._dataset = None
        self._datasettype = None
        super().__init__(name, widgettype, datainstance)

    def _setWidgetValueHook(self, value):
        if self._widgettype == 'ComboBoxWidget':
            choices = self._dataset.get_prop('data', 'choices')
            logging.debug(str(choices))
            index = -1
            for c in choices:
                if c[1] == str(value):
                    index = c[0]
                    break
            valuetoset = index
            #logging.debug('  widgetname=' + self.name + '  value=' + str(value) + '->' 'valuetoset='+ str(valuetoset))
        else:
            valuetoset = value

        self._dataset.bind(self._dataset).set(valuetoset)
        # self._dataset.parent.get() # TODO: probably a mechanism like this will update the values inside the groupbox
        return True

    def _getWidgetValueHook(self):
        '''
        Return the actual stored value in the UI
        :return:
        '''
        if self._widgettype == 'ComboBoxWidget':
            choices = self._dataset.get_prop('data', 'choices')
            #logging.debug(str(choices))
            indexselected = self._dataset.bind(self._dataset).get()
            valuetoreturn = None
            for c in choices:
                if c[0] == indexselected:
                    valuetoreturn = GuidataWidget._fromDatasettypeToValue(self._datasettype, c[1])
            #logging.debug('  widgetname=' + self.name +'  indexselected=' + str(indexselected) + '->' 'valuetoreturn=' + str(valuetoreturn))
        else:
            valuetoreturn = self._dataset.bind(self._dataset).get()
        return valuetoreturn

    @staticmethod
    def _fromDatasettypeToValue(datasettype, value):
        '''
        An utility to convert a value stored in the guidatawidget in the relative native object, defined by datasettype
        :param datasettype:
        :param value:
        :return:
        '''
        value_to_return = None
        if datasettype is not None:
            str_split       = str.split(str(datasettype), '\'')
            # Adding quotes for type string, otherwise remain unmodified
            if str_split[1] == 'str':
                str_eval = str_split[1] + '(\''+ value + '\')'
            else:
                str_eval = str_split[1] + '('+ value + ')'
            value_to_return = eval(str_eval)
        return value_to_return

    @staticmethod
    def convertValueToWidgetValue(widgetinstance, value):
        '''
        Given a value returns the equivalent value which will be stored in the widget.
        For example, in combo box returns the index
        :param widgetinstance:
        :param value:
        :return:
        '''
        if widgetinstance._widgettype == 'ComboBoxWidget':
            choices = widgetinstance._dataset.get_prop('data', 'choices')
            logging.debug(str(choices))
            valuetoreturn = -1
            for c in choices:
                typed_value = GuidataWidget._fromDatasettypeToValue(widgetinstance._datasettype, c[1])
                if typed_value == value:
                    valuetoreturn = c[0]
                    break
            #logging.debug('  widgetname=' + widgetinstance.name +' value=' + str(value) + '->' 'valuetoreturn=' + str(valuetoreturn))
        else:
            valuetoreturn = value
        return valuetoreturn

    @staticmethod
    def convertWidgetValueToValue(widgetinstance, widget_value):
        '''
        Convert a widget value value as it stored in the widget and returns the  value expected by the application
        For example from the index of a combo box returns the value represented by the combo box
        :param widgetinstance:
        :param widget_value:
        :return:
        '''
        if widgetinstance._widgettype == 'ComboBoxWidget':
            choices = widgetinstance._dataset.get_prop('data', 'choices')
            logging.debug(str(choices))
            valuetoreturn = -1
            for c in choices:
                if c[0] == widget_value:
                    valuetoreturn = GuidataWidget._fromDatasettypeToValue(widgetinstance._datasettype, c[1])
                    break
            #logging.debug('  widgetname=' + widgetinstance.name + '  widget_value=' + str(widget_value) + '->' 'valuetoreturn=' + str(valuetoreturn))
        else:
            valuetoreturn = widget_value
        return valuetoreturn

    def _getGuidataWidgetValue(self):
        '''
        This is a workaround for the guidata framework only and should be use only in the internal communication of
        widget data. It was introduced to return the proper value, for example for the combo box widget which needs/wants
        the index. For example in a combo box, given the value in the widget it returns the proper index. If the value
        is coincident it returns the unmodified value
        :return: the value converted for the widget
        '''
        widget_value = None
        if self.widgettype == 'ComboBoxWidget':
            # need to access to private members, consider this  function as kind of package private function
            widget_value = self._dataset.bind(self._dataset).get()
        else:
            widget_value = self._dataset.bind(self._dataset).get()
        return widget_value

    def _createWidget(self, datainstance):
        '''
        Manage the instantiation of the widget
        :param datainstance:
        :return: True in case of success, otherwise false and the reason for failing
        '''
        try:
            self._createdataset(datainstance)
        except Exception as e:
            return (False, e.__class__.__name__ + ', ' + str(e))
        return (True,'')

    def isDataAssociated(self):
        '''
        Extend the behavior for data association, it also check if the dataset is created
        :return:
        '''
        if not super().isDataAssociated():
            return False
        if self._dataset == None:
            return False
        else:
            return True

    def _createdataset(self, datainstance):
        '''
        This function create the dataset in the guidata framework and save it self._dataset
        :return:
        '''

        name = datainstance.name
        widgettype = self._widgettype
        value = datainstance.value
        valuetype = type(value)
        limits = datainstance.limits
        unit = datainstance.unit
        helpstr = datainstance.description

        if widgettype == 'EditLineWidget':
            dataset = 'StringItem(\''+ name + '\'' \
                      ', default=\''+ str(value)+  '\'' \
                      ', help=\''+ helpstr +'\' )'
        elif widgettype == 'TextWidget':
            dataset = 'TextItem(\''+ name + '\'' \
                      ', default=\''+ str(value)+  '\'' \
                      ', help=\''+ helpstr +'\' )'
        elif widgettype == 'FloatWidget':
            if limits is None:
                dataset =  ('FloatItem(label=\'' + name + '\', '
                            'default=' + str(value) +
                            ', help=\''+ helpstr +
                            '\', unit=\''+ unit + '\')')
            else:
                dataset =  ('FloatItem(label=\'' + name + '\', '
                            'default=' + str(value) +
                            ', min='+ str(limits[0]) +' , max='+ str(limits[1]) +
                            ', help=\''+ helpstr +
                            '\', unit=\''+ unit + '\')')
        elif widgettype == 'ComboBoxWidget':
            if value in limits: selectval = limits.index(value)
            else: selectval = -1
            dataset =  ('ChoiceItem(\'' + name + '\', '
                        'default=' + str(selectval) +
                        ', choices =' + str([str(v) for v in limits]) +
                        ', help=\'' + helpstr + '\')')
        elif widgettype == 'MultipleChoiceWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'OpenFileWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'OpenMultipleFilesWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'SelectDirectoryWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'SaveFileWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'LabelWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'IntItem':
            raise widget.WidgetNotExisting(self, name, widgettype)
        elif widgettype == 'RadioBoxWidget':
            raise widget.WidgetNotExisting(self, name, widgettype)
        else:
            dataset = 'None'
        self._dataset = eval(dataset)
        # need to assign the viewname manually... boh
        self._dataset.set_name(name)
        self._datasettype = valuetype

    def getDataSet(self):
        if not self.isDataAssociated():
            raise widget.WidgetNotYetAssociated(self, self.name, self.widgettype)
        return self._dataset
