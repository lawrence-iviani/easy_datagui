__author__ = 'law'

import unittest
from dataclass import (DataClass, DataClassNumber, DataClassDiscreteNumber, DataClassNotSupported)
import widget


class TestGenericWidget(unittest.TestCase):
    # TODO: Test the follow conditions
    # test all widget for all available data class number

    def test_constructor(self):
        # Constructor: Wrong instance of dataclass
        # Instance of data class
        # Correct dataclass number and wrong widget
        # test correct dataclassnumber and widget

        # Define test conditions
        data1 = object()
        widgettype1 = 'WrongWidget'

        data2 = DataClassNotSupported(name='somename', value=1)
        widgettype2 = 'FloatWidget'

        data3 = DataClassNumber(name='name3', value=2)
        widgettype3 = 'FloatWidget'

        data4 = DataClassDiscreteNumber(name='name4', value=2, limits=[0,2])
        widgettype4 = 'ComboBoxWidget'

        # Test viewname validity
        # WidgetNameError
        with self.assertRaises(widget.WidgetNameError):   widget.GenericWidget(object(),widgettype1)
        with self.assertRaises(widget.WidgetNameError):   widget.GenericWidget(' not a valid viewname',widgettype1)
        with self.assertRaises(widget.WidgetNameError):   widget.GenericWidget('',widgettype1)

        # Test an invalid combination of widget
        # WidgetNotExisting
        with self.assertRaises(widget.WidgetNotExisting):   widget.GenericWidget('somename',widgettype1)

        # Test an invalid data type
        # WrongDataClass
        widget1 = widget.GenericWidget('somename',widgettype2)
        with self.assertRaises(widget.WrongDataClass): widget1.associateData(data1)

        # Test if the dataclass is supported
        # NotExistentWidgetMatchingDataClass
        widget2 = widget.GenericWidget('somename',widgettype2)
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass): widget2.associateData(data2)

        # Test the widget_type cannot be associated
        with self.assertRaises(widget.WidgetNotExisting):  widget.GenericWidget(data3.name,widgettype1)

        # Test constructor and association
        widget3 =  widget.GenericWidget(data3.name,widgettype3)
        widget3.associateData(data3)

        # Test it the widget associated cannot be associate to the selected data
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass): widget.GenericWidget(data3.name, widgettype4, data3)

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): widget.GenericWidget(data4.name, widgettype3, data3)

        # Reassociated to the same data and another data
        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated ): widget3.associateData(data3)
        with self.assertRaises(widget.WidgetAlreadyAssociated ): widget3.associateData(data4)

        # In guidatawrapper try to get the widget before associates to a class
        # widget4 = guidatawrapper.GuidataWidget(data4.name, widgettype4)
        # with self.assertRaises(widget.WidgetNotYetAssociated): widget4.getDataSet()

        # Test the constructor with association
        widget5 = widget.GenericWidget(data4.name, widgettype4, data4)

    def test_datasignal(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''

        # Init the widget
        data1 = DataClassNumber(name='name1', value=2)
        widgettype1 = 'FloatWidget'
        widget1 =  widget.GenericWidget(data1.name,widgettype1)
        widget1.associateData(data1)

        # A signal is sent, but not implemented in GenericWidget
        with self.assertRaises(NotImplementedError): data1.value = 3

if __name__ == '__main__':
    unittest.main()
