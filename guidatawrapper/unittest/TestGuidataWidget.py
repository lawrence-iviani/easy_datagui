__author__ = 'law'

import unittest
import guidatawrapper
import widget
from dataclass import (DataClass, DataClassNumber, DataClassDiscreteNumber, DataClassNotSupported, DataClassDiscreteString, DataClassString)
from guidata.dataset.qtwidgets import DataSetShowGroupBox, DataSetEditGroupBox
from guidata.qt.QtGui import (QApplication)
from guidata.dataset.datatypes import (DataSet)
from pydispatch import dispatcher
import widget.XMLWidgetHelper

class TestGuidataWidget(unittest.TestCase):
    _path = './guidatawrapper/unittest/xmlfiles/'
    #_path = './xmlfiles/'
    def test_constructor(self):
        data1 = object()
        widgettype1 = 'WrongWidget'

        data2 = DataClassNotSupported(name='somename', value=1)
        widgettype2 = 'FloatWidget'

        # Without limits
        data3 = DataClassNumber(name='name3', value=2)
        widgettype3 = 'FloatWidget'

        # With Limits
        data4 = DataClassNumber(name='name4', value=2, limits=[-10, 10])
        widgettype4 = 'FloatWidget'

        data5 = DataClassDiscreteNumber(name='name5', value=2, limits=[0,2,3])
        widgettype5 = 'ComboBoxWidget'

        data6 = DataClassString(name='name6', value='abaara', maxlength=10)
        widgettype6 = 'EditLineWidget'

        data7 = DataClassString(name='name7', value='non \'e pottibile')
        widgettype7 = 'OpenFileWidget'

        data8 = DataClassDiscreteString(name='name8', value='a', limits=['0','a','bbb'])
        widgettype8 = 'ComboBoxWidget'

        # Test viewname validity
        # WidgetNameError
        with self.assertRaises(widget.WidgetNameError):   guidatawrapper.GuidataWidget(object(),widgettype1)
        with self.assertRaises(widget.WidgetNameError):   guidatawrapper.GuidataWidget(' not a valid viewname',widgettype1)
        with self.assertRaises(widget.WidgetNameError):   guidatawrapper.GuidataWidget('',widgettype1)

        # Test an invalid combination of widget
        # WidgetNotExisting
        with self.assertRaises(widget.WidgetNotExisting):   guidatawrapper.GuidataWidget('somename',widgettype1)

        # Test an invalid data type
        # WrongDataClass
        widget1 = guidatawrapper.GuidataWidget('somename',widgettype2)
        with self.assertRaises(widget.WrongDataClass): widget1.associateData(data1)

        # Test if the dataclass is supported
        # NotExistentWidgetMatchingDataClass
        widget2 = guidatawrapper.GuidataWidget('somename',widgettype2)
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass): widget2.associateData(data2)

        # Test the widgettype cannot be associated
        with self.assertRaises(widget.WidgetNotExisting):  guidatawrapper.GuidataWidget(data3.name,widgettype1)

        # Test constructor and association for DataClassNumber and DataClassDiscreteNumber
        widget3 = guidatawrapper.GuidataWidget(data3.name,widgettype3)
        widget3.associateData(data3)
        widget4 = guidatawrapper.GuidataWidget(data4.name,widgettype4, data4)

        # Test it the widget associated cannot be associate to the selected data
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass): guidatawrapper.GuidataWidget(data3.name, widgettype5, data3)

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): guidatawrapper.GuidataWidget(data5.name, widgettype3, data3)

        # Re-associated to the same data and another data
        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated ): widget3.associateData(data3)
        with self.assertRaises(widget.WidgetAlreadyAssociated ): widget3.associateData(data4)
        with self.assertRaises(widget.WidgetAlreadyAssociated ): widget3.associateData(data5)

        # In guidatawrapper try to get the widget before associates to a class
        widget5 = guidatawrapper.GuidataWidget(data5.name, widgettype5)
        with self.assertRaises(widget.WidgetNotYetAssociated): widget5.getDataSet()

        # Test the constructor with association
        widget5_1 = guidatawrapper.GuidataWidget(data5.name, widgettype5, data5)

        widget6 = guidatawrapper.GuidataWidget(data6.name, widgettype6, data6)
        #widget7 = guidatawrapper.GuidataWidget(data7.name, widgettype7, data7)
        widget8 = guidatawrapper.GuidataWidget(data8.name, widgettype8, data8)

    def test_associationWidget(self):
        # QT Stuff
        app = QApplication([])

        # Init list
        data1       = []
        widgettype1 = []
        widget1     = []
        dataset1    = []

        # Without limits
        data1.append(DataClassNumber(name='name3', value=2))
        widgettype1.append('FloatWidget')

        # With Limits
        data1.append(DataClassNumber(name='name4', value=2, limits=[-10, 10]))
        widgettype1.append('FloatWidget')

        # Combo box widget
        data1.append(DataClassDiscreteNumber(name='name5', value=2, limits=[0,2,3]))
        widgettype1.append('ComboBoxWidget')

        data1.append(DataClassString(name='name6', value='abaara', maxlength=10))
        widgettype1.append('EditLineWidget')

        data1.append(DataClassDiscreteString(name='name8', value='a', limits=['0','a','bbb']))
        widgettype1.append('ComboBoxWidget')

        # add widgets and datasets
        for index,d in enumerate(data1):
            widget1.append(guidatawrapper.GuidataWidget(data1[index].name, widgettype1[index], data1[index]))
            dataset1.append(widget1[index].getDataSet())

        class DataSetView(DataSet):
            for index,ds in enumerate(dataset1):
                locals()[data1[index].name]  = ds

        groupbox1 = DataSetShowGroupBox("My First Data Set SHOW", DataSetView, comment='')
        groupbox2 = DataSetEditGroupBox("My First Data Set EDIT", DataSetView, comment='')

        del app

    def test_valueassignment(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''

        prevValue = 9
        newValue  = 10
        # Init the widget
        data1 = DataClassNumber(name='name1', value=prevValue)
        widgettype1 = 'FloatWidget'
        widget1 =  guidatawrapper.GuidataWidget(data1.name,widgettype1)
        widget1.associateData(data1)

        # A signal is sent, but not implemented in GenericWidget
        self.assertEquals(widget1.getWidgetValue(),prevValue)
        data1.value = newValue
        self.assertEquals(widget1.getWidgetValue(),newValue)

        # Init a discrete numnber  widget
        data2 = DataClassDiscreteNumber(name='name1', value=prevValue, limits=[10, -2, 30, 20, 9, -1])
        widgettype2 = 'ComboBoxWidget'
        widget2 =  guidatawrapper.GuidataWidget(data2.name, widgettype2)
        widget2.associateData(data2)
        # A signal is sent, but not implemented in GenericWidget
        # print(widget2.getWidgetValue())
        self.assertEquals(widget2.getWidgetValue(),prevValue)
        data2.value = newValue
        # print(widget2.getWidgetValue())
        self.assertEquals(widget2.getWidgetValue(),newValue)

        # Go with the strings
        prevValue = 'puppa'
        newValue  = 'melo'

        data6 = DataClassString(name='name6', value=prevValue, maxlength=10)
        widgettype6 = 'EditLineWidget'
        widget6 = guidatawrapper.GuidataWidget(data6.name, widgettype6, data6)
        self.assertEquals(widget6.getWidgetValue(),prevValue)
        data6.value = newValue
        # print(widget2.getWidgetValue())
        self.assertEquals(widget6.getWidgetValue(),newValue)

        data8 = DataClassDiscreteString(name='name8', value=prevValue, limits=[prevValue, newValue])
        widgettype8 = 'ComboBoxWidget'
        widget8 = guidatawrapper.GuidataWidget(data8.name, widgettype8, data8)
        self.assertEquals(widget8.getWidgetValue(),prevValue)
        data8.value = newValue
        # print(widget2.getWidgetValue())
        self.assertEquals(widget8.getWidgetValue(),newValue)

    def test_setwidgetvalue(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''

        # ---------------- Test numeric widgets
        prevValue = -2
        newValue  = -4
        wrongValue = 100
        # Init the widget
        data1 = DataClassNumber(name='name1', value=prevValue)
        widgettype1 = 'FloatWidget'
        widget1 = guidatawrapper.GuidataWidget(data1.name,widgettype1)
        widget1.associateData(data1)

        # A signal is sent, but not implemented in GenericWidget
        self.assertEquals(widget1.getWidgetValue(), prevValue)
        widget1.setWidgetValue(newValue)
        self.assertEquals(widget1.getWidgetValue(), newValue)

        # Init the widget
        data2 = DataClassDiscreteNumber(name='name1', value=prevValue, limits=[10, -2, 11, 12, 9, -4])
        widgettype2 = 'ComboBoxWidget'
        widget2 = guidatawrapper.GuidataWidget(data2.name, widgettype2)
        widget2.associateData(data2)
        self.assertEquals(widget2.getWidgetValue(), prevValue)
        widget2.setWidgetValue(newValue)
        self.assertEquals(widget2.getWidgetValue(), newValue)

        # Test a wrong value
        #widget2.setWidgetValue(wrongValue)
        # set a string
        # ---------------- Test string widgets
        prevValue = 'evviva'
        newValue  = 'me'
        wrongValue = 'very wrong'

        # Init the widget
        data3 = DataClassString(name='name3', value=prevValue)
        widgettype3 = 'EditLineWidget'
        widget3 = guidatawrapper.GuidataWidget(data3.name, widgettype3)
        widget3.associateData(data3)

        # A signal is sent, but not implemented in GenericWidget
        self.assertEquals(widget3.getWidgetValue(),prevValue)
        widget3.setWidgetValue(newValue)
        self.assertEquals(widget3.getWidgetValue(),newValue)

        # Init the widget
        data4 = DataClassDiscreteString(name='name4', value=prevValue, limits=[newValue,prevValue ])
        widgettype4 = 'ComboBoxWidget'
        widget4 = guidatawrapper.GuidataWidget(data4.name, widgettype4)
        widget4.associateData(data4)
        self.assertEquals(widget4.getWidgetValue(), prevValue)
        widget4.setWidgetValue(newValue)
        self.assertEquals(widget4.getWidgetValue(), newValue)

        # Test a wrong value, it doesn't fail
        #widget4.setWidgetValue(wrongValue)

    def test_signal(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''

        prevValue = 2
        newValue  = 3
        # Init the widget
        data1 = DataClassNumber(name='name1', value=prevValue)
        widgettype1 = 'FloatWidget'
        widget1 =  guidatawrapper.GuidataWidget(data1.name,widgettype1,data1)

        # prepare signal calls
        _widgetChanged = [0]
        def on_widgetUpdated():
            _widgetChanged[0] = 1
        # Connect the signal and test
        dispatcher.connect(on_widgetUpdated, signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=widget1)

        # test by setting directly the value in the dataclass associated to widget
        data1.value = newValue
        self.assertEqual(_widgetChanged[0], 1)

        # test the set widget
        _widgetChanged[0] = 0
        widget1.setWidgetValue(prevValue)
        self.assertEqual(_widgetChanged[0], 1)

        # Test string based
        prevValue = '2'
        newValue  = '3'
        # Init the widget
        data2 = DataClassDiscreteString(name='name2', value=prevValue , limits=[newValue,prevValue])
        widgettype2 = 'ComboBoxWidget'
        widget2 =  guidatawrapper.GuidataWidget(data2.name, widgettype2, data2)

        # prepare signal calls
        # Connect the signal and reset flag
        dispatcher.connect(on_widgetUpdated, signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=widget2)
        _widgetChanged[0] = 0
        # test by setting directly the value in the dataclass associated to widget
        data2.value = newValue
        self.assertEqual(_widgetChanged[0], 1)

        # test the set widget
        _widgetChanged[0] = 0
        widget1.setWidgetValue(prevValue)
        self.assertEqual(_widgetChanged[0], 1)

    def test_converter(self):

        # Init list
        data1       = []
        widgettype1 = []
        widget1     = []

        # Without limits

        values1_1 = 2
        data1.append(DataClassNumber(name='name3', value=values1_1))
        widgettype1.append('FloatWidget')


        values1_2 = [0.1, -1.1, 2.2 ,-3.3 ]
        data1.append(DataClassDiscreteNumber(name='name5', value=2.2, limits=values1_2))
        widgettype1.append('ComboBoxWidget')
        testindex = list(range(0, len(values1_2)))

        # create dateset
        for index, d in enumerate(data1):
            widget1.append(guidatawrapper.GuidataWidget(data1[index].name, widgettype1[index], data1[index]))

        self.assertEqual(guidatawrapper.GuidataWidget.convertWidgetValueToValue(widget1[0], values1_1), values1_1)
        self.assertEqual(guidatawrapper.GuidataWidget.convertValueToWidgetValue(widget1[0], values1_1), values1_1)

        for idx, v in enumerate(values1_2):
            self.assertEqual(guidatawrapper.GuidataWidget.convertWidgetValueToValue(widget1[1], testindex[idx]), v)
            self.assertEqual(guidatawrapper.GuidataWidget.convertValueToWidgetValue(widget1[1], v),testindex[idx])

        # ---------- Test Strings widgets

        # Init list
        data2       = []
        widgettype2 = []
        widget2     = []

        # Without limits

        values2_1 = 'abc'
        data2.append(DataClassString(name='name6', value=values2_1, maxlength=3))
        widgettype2.append('EditLineWidget')

        values2_2 = ['aaa', 'BAC', ' a__ 2.2' ,'-3.3@@#$%^  &*(!)*(?><:"{}{' ]
        data2.append(DataClassDiscreteString(name='name7', value='BAC', limits=values2_2))
        widgettype2.append('ComboBoxWidget')
        testindex = list(range(0, len(values2_2)))

        # create dateset
        for index, d in enumerate(data2):
            widget2.append(guidatawrapper.GuidataWidget(data2[index].name, widgettype2[index], data2[index]))

        self.assertEqual(guidatawrapper.GuidataWidget.convertWidgetValueToValue(widget2[0], values2_1), values2_1)
        self.assertEqual(guidatawrapper.GuidataWidget.convertValueToWidgetValue(widget2[0], values2_1), values2_1)

        for idx, v in enumerate(values2_2):
            self.assertEqual(guidatawrapper.GuidataWidget.convertWidgetValueToValue(widget2[1], testindex[idx]), v)
            self.assertEqual(guidatawrapper.GuidataWidget.convertValueToWidgetValue(widget2[1], v),testindex[idx])

    def test_xml_functions(self):
        # Without limits
        data1 = DataClassNumber(name='name3', value=2)
        widgettype1 = 'FloatWidget'
        widget1 = guidatawrapper.GuidataWidget(data1.name, widgettype1)
        filename1 = self._path + 'guidatawidget_test_creation1.xml'
        XML1 = widget.XMLWidgetHelper.widgetToXML(widget1,  filename=filename1)
        # Reopen filename1 and verify it
        widget1_1  =  widget.XMLWidgetHelper.XMLFileToWidget(filename1)
        XML1_1 = widget.XMLWidgetHelper.widgetToXML(widget1_1)
        self.assertEqual(XML1, XML1_1)
        self.assertEqual(widget1, widget1_1)

        # With Limits
        data2 = DataClassNumber(name='name4', value=2, limits=[-10, 10])
        widgettype2 = 'FloatWidget'
        widget2 = guidatawrapper.GuidataWidget(data2.name, widgettype2)
        filename2 = self._path + 'guidatawidget_test_creation2.xml'
        XML2 = widget.XMLWidgetHelper.widgetToXML(widget2,   filename=filename2)
        # Reopen filename2 and verify it
        widget2_1  =  widget.XMLWidgetHelper.XMLFileToWidget(filename2)
        XML2_1 = widget.XMLWidgetHelper.widgetToXML(widget2_1)
        self.assertEqual(XML2, XML2_1)
        self.assertEqual(widget2, widget2_1)

        # Test data 3
        data3 = DataClassDiscreteNumber(name='name5', value=2, limits=[0, 2, 3])
        widgettype3 = 'ComboBoxWidget'
        widget3 = guidatawrapper.GuidataWidget(data3.name, widgettype3)
        filename3 = self._path + 'guidatawidget_test_creation3.xml'
        XML3 = widget.XMLWidgetHelper.widgetToXML(widget3,   filename=filename3)
        # Reopen filename3 and verify it
        widget3_1  =  widget.XMLWidgetHelper.XMLFileToWidget(filename3)
        XML3_1 = widget.XMLWidgetHelper.widgetToXML(widget3_1)
        self.assertEqual(XML3, XML3_1)
        self.assertEqual(widget3, widget3_1)

        # -------------- Test string based calss
        # Test data 4
        data4 = DataClassString(name='name4', value='2', maxlength=1)
        widgettype4 = 'EditLineWidget'
        widget4 = guidatawrapper.GuidataWidget(data4.name, widgettype4)
        filename4 = self._path + 'guidatawidget_test_creation4.xml'
        XML4 = widget.XMLWidgetHelper.widgetToXML(widget4,  filename=filename4)
        # Reopen filename1 and verify it
        widget4_1  =  widget.XMLWidgetHelper.XMLFileToWidget(filename4)
        XML4_1 = widget.XMLWidgetHelper.widgetToXML(widget4_1)
        self.assertEqual(XML4, XML4_1)
        self.assertEqual(widget4, widget4_1)

        # Test Data 5
        data5 = DataClassDiscreteString(name='name5', value='2', limits=['0sda4$#%$^@#@%$:}{|', '2', '3 '])
        widgettype5 = 'ComboBoxWidget'
        widget5 = guidatawrapper.GuidataWidget(data5.name, widgettype5)
        filename3 = self._path + 'guidatawidget_test_creation5.xml'
        XML5 = widget.XMLWidgetHelper.widgetToXML(widget5,   filename=filename3)
        # Reopen filename3 and verify it
        widget5_1  =  widget.XMLWidgetHelper.XMLFileToWidget(filename3)
        XML5_1 = widget.XMLWidgetHelper.widgetToXML(widget5_1)
        self.assertEqual(XML5, XML5_1)
        self.assertEqual(widget5, widget5_1)

        # Test with a list of widgets
        widget_list = []
        widget_list.append(widget1)
        widget_list.append(widget2)
        widget_list.append(widget3)
        widget_list.append(widget4)
        widget_list.append(widget5)
        widget_list.append(widget5_1[0])
        widget_list.append(widget4_1[0])
        widget_list.append(widget3_1[0])
        widget_list.append(widget2_1[0])
        widget_list.append(widget1_1[0])
        filename6 = self._path + 'guidatawidget_test_creation6.xml'
        XML6 = widget.XMLWidgetHelper.widgetToXML(widget_list,   filename=filename6)

        widget_list_6  =  widget.XMLWidgetHelper.XMLFileToWidget(filename6)
        XML6_1 = widget.XMLWidgetHelper.widgetToXML(widget_list_6)
        self.assertEqual(XML6, XML6_1)
        self.assertEqual(widget_list, widget_list_6)

        filename_ref = self._path + 'guidatawidget_test_creation_ref.xml'
        widget_list_ref  =  widget.XMLWidgetHelper.XMLFileToWidget(filename_ref)
        XML_ref = widget.XMLWidgetHelper.widgetToXML(widget_list_ref)
        self.assertEqual(XML6, XML_ref)
        self.assertEqual(widget_list, widget_list_ref)

if __name__ == '__main__':
    unittest.main()
