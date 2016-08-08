
import unittest
import widget
import tkwrapper
import tkinter as tk
import tkinter.ttk as ttk
from dataclass import (DataClass, DataClassNumber, DataClassDiscreteNumber, DataClassNotSupported,
                       DataClassDiscreteString, DataClassString, DataClassIntNumber, DataClassDiscreteIntNumber)
from pydispatch import dispatcher
import widget.XMLWidgetHelper
#import tkwrapper.XML_TKWidgetHelper
import tkwrapper.TkWidget
from   utilities.misc import util_get_valid_path
import sys
__author__ = 'law'


class TestTkWidget(unittest.TestCase):
    _path = util_get_valid_path(['./xmlfiles/', './tkwrapper/unittest/xmlfiles/'])

    def test_constructor(self):
        # TKinter Stuff
        root = tk.Tk()

        # Init list
        data1 = []  # a list of sever data class
        widget1 = []

        """ ------------------------ """
        """ TEST WIDGET NAME VALIDITY"""
        # WidgetNameError
        with self.assertRaises(widget.WidgetNameError):   tkwrapper.TkWidget(root, object(), 'IntWidget')
        with self.assertRaises(widget.WidgetNameError):   tkwrapper.TkWidget(root,
                                                                             ' not a valid viewname',
                                                                             'FloatWidget')
        with self.assertRaises(widget.WidgetNameError):   tkwrapper.TkWidget(root, '', 'ComboBoxWidget')

        # Test an invalid combination of widget
        # WidgetNotExisting
        with self.assertRaises(widget.WidgetNotExisting):   tkwrapper.TkWidget(root, 'somename', 'NotExistingWidget')

        """ ---------------------- """
        """ TEST INVALID DATACLASS """
        # Test an invalid data type
        # WrongDataClass
        data1.append(['FloatWidget', DataClassNotSupported(name='somename', value=1)])
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0]))
        with self.assertRaises(widget.WrongDataClass): widget1[-1].associateData(data1[-1])

        """ ----------------------------------- """
        """ TEST INVALID WIDGET-DATACLASS MATCH """
        # Test if the dataclass is supported
        # NotExistentWidgetMatchingDataClass
        data1.append(['FloatWidget', DataClassNotSupported(name='somename', value=1)])
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0]))
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass): widget1[-1].associateData(data1[-1][1])

        """ ------------------------------------------------------------- """
        """ TEST DATACLASS NUMBER GENERIC AND ALSO FOR INT NUMBER WIDGETS """
        # Test constructor and association for DataClassNumber and DataClassDiscreteNumber
        data1.append(['IntWidget', DataClassIntNumber(name='name3', value=2)])  # Without limits
        data1.append(['FloatWidget', DataClassNumber(name='name3', value=2, limits=[-10, 10])])  # With Limits

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-2][0], data1[-2][1])
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-1][0], data1[-1][1])

        # Create not associated widget and try to associate to wrong dataclass first amd then associate correct dataclass
        widget1.append(tkwrapper.TkWidget(root, data1[-2][1].name, data1[-2][0]))
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0]))

        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass):  widget1[-2].associateData(data1[-1][1])
        with self.assertRaises(widget.NotExistentWidgetMatchingDataClass):  widget1[-1].associateData(data1[-2][1])
        widget1[-2].associateData(data1[-2][1])
        widget1[-1].associateData(data1[-1][1])

        # Re-associated to the same data and another data
        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-2].associateData(data1[-2][1])
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-1].associateData(data1[-1][1])

        """ --------------------------------------------------------------------- """
        """ TEST DISCRETE DATACLASS NUMBER GENERIC AND ALSO FOR INT NUMBER WIDGETS"""
        # Test constructor and association for DataClassNumber and DataClassDiscreteNumber
        data1.append(['ComboBoxWidget', DataClassDiscreteIntNumber(name='name4', value=2, limits=[-1 , 2 , 0, 3] )])
        data1.append(['ComboBoxWidget', DataClassDiscreteNumber(name='name4', value=2.1, limits=[-10, 2.1 , 10])])

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-2][0], data1[-2][1])
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-1][0], data1[-1][1])

        # Create not associated widget and try to associate to wrong dataclass first amd then associate correct dataclass
        widget1.append(tkwrapper.TkWidget(root, data1[-2][1].name, data1[-2][0]))
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0]))
        widget1[-2].associateData(data1[-2][1])
        widget1[-1].associateData(data1[-1][1])

        # Re-associated to the same data and another data
        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-2].associateData(data1[-2][1])
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-1].associateData(data1[-1][1])

        """ -------------------------------------- """
        """ TEST DISCRETE DATACLASS STRING WIDGETS """
        data1.append(['ComboBoxWidget', DataClassDiscreteString(name='name8', value='a', limits=['0', 'a', 'bbb'])])

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-1][0], data1[-1][1])

        # Widget and associate
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0]))
        widget1[-1].associateData(data1[-1][1])

        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-1].associateData(data1[-1][1])

        """ --------------------- """
        """ TEST DATACLASS STRING """
        data1.append(['EditLineWidget', DataClassString(name='name5', value='abaara', maxlength=10)])
        data1.append(['LabelWidget', DataClassString(name='name6', value='Valpolicella ripasso')])
        data1.append(['TextWidget', DataClassString(name='name7', value='Sangiovese')])
        data1.append(['OpenFileWidget', DataClassString(name='name8', value='non \'e pottibile')])

# TODO: enable OpenFileWidget for test

        # Test  the viewname assigned to widget is not compatible with the data type
        # WrongDataAssociation
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-4][0], data1[-4][1])
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-3][0], data1[-3][1])
        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-2][0], data1[-2][1])
#        with self.assertRaises(widget.WrongDataAssociation): tkwrapper.TkWidget(root, 'differentname', data1[-1][0], data1[-1][1])

        # Widget and associate
        widget1.append(tkwrapper.TkWidget(root, data1[-4][1].name, data1[-4][0], data1[-4][1]))
        widget1.append(tkwrapper.TkWidget(root, data1[-3][1].name, data1[-3][0], data1[-3][1]))
        widget1.append(tkwrapper.TkWidget(root, data1[-2][1].name, data1[-2][0], data1[-2][1]))
#        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0], data1[-1][1]))

        # WidgetAlreadyAssociated
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-4].associateData(data1[-4][1])
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-3].associateData(data1[-3][1])
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-2].associateData(data1[-2][1])
#        with self.assertRaises(widget.WidgetAlreadyAssociated): widget1[-1].associateData(data1[-1][1])

        # Final remove the TK stuff
        root.destroy()

    def test_association_widget(self):
        # TKinter Stuff
        root = tk.Tk()

        # Init list
        data1       = []  # a list of sever data class
        widget1     = []

        # Without limits
        data1.append(['FloatWidget', DataClassNumber(name='name3', value=2.1)])

        # With Limits
        data1.append(['IntWidget',  DataClassIntNumber(name='name4', value=2, limits=[-10, 10])])

        # Combo box widget
        data1.append(['ComboBoxWidget', DataClassDiscreteNumber(name='name5', value=2, limits=[0, 2, 3])])
        data1.append(['ComboBoxWidget', DataClassDiscreteString(name='name8', value='a', limits=['0', 'a', 'bbb'])])

        # Edit line widget
        data1.append(['EditLineWidget', DataClassString(name='name6', value='abaara', maxlength=10)])

        # Label widget
        data1.append(['LabelWidget', DataClassString(name='name9', value='Valpolicella ripasso')])

        # Text widget
        data1.append(['TextWidget', DataClassString(name='name10', value='Sangiovese')])

        # add widgets
        for index, d in enumerate(data1):
            widget1.append(tkwrapper.TkWidget(root, d[1].name, d[0], d[1]))


        # Test create and associate later
        data2       = DataClassNumber(name='Data2', value=2)
        data2_1     = DataClassNumber(name='Data2', value=2)
        widget2     = tkwrapper.TkWidget(root, 'Data2', 'FloatWidget')
        widget2.associateData(data2)
        with self.assertRaises(widget.WidgetAlreadyAssociated): widget2.associateData(data2_1)
        root.destroy()

    def test_valueassignment(self):
        '''
        Test if setting a value the widget value is changed after a set, in several conditions
        :return:
        '''
        # TKinter Stuff
        root = tk.Tk()

        ''' TEST 1.1 '''
        prevValue = 9.0
        newValue  = 10.1
        # Init float the widget
        data1 = DataClassNumber(name='name1', value=prevValue, limits=[prevValue-1.0, newValue+1])
        widgettype1 = 'FloatWidget'
        widget1 = tkwrapper.TkWidget(root, data1.name, widgettype1)
        widget1.associateData(data1)

        # A signal is sent, but not implemented in GenericWidget
        self.assertEquals(widget1.get_widget_value(), prevValue)
        data1.value = newValue
        self.assertEquals(widget1.get_widget_value(), newValue)
        self.assertEquals(widget1.get_widget_value().__class__, newValue.__class__)
        self._print_widget_value(widget1, prevValue, newValue)

        ''' NOTE: a signal is emitted but because there's no connection (no  model!!) with the test the follow code
                  it WORKS
        widget1.set_widget_value(newValue*2.1)
        self._print_widget_value(widget1, prevValue, newValue)
        '''

        ''' TEST 1.2 '''
        prevValue = 9
        newValue = 10
        # Init float the widget
        data1_1 = DataClassIntNumber(name='intname1', value=prevValue, limits=[prevValue - 1, newValue + 1])
        widgettype1_1 = 'IntWidget'
        widget1_1 = tkwrapper.TkWidget(root, data1_1.name, widgettype1_1)
        widget1_1.associateData(data1_1)

        # A signal is sent, but not implemented in GenericWidget
        self.assertEquals(widget1_1.get_widget_value(), prevValue)
        data1_1.value = newValue
        self.assertEquals(widget1_1.get_widget_value(), newValue)
        self.assertEquals(widget1_1.get_widget_value().__class__, newValue.__class__)
        self._print_widget_value(widget1_1, prevValue, newValue)

        ''' TEST 2 '''
        # Init a discrete number  widget
        prevValue = 9
        newValue = 10
        data2 = DataClassDiscreteNumber(name='name2', value=prevValue, limits=[10, -2, 30, 20, 9, -1])
        widgettype2 = 'ComboBoxWidget'
        widget2 = tkwrapper.TkWidget(root, data2.name, widgettype2)
        widget2.associateData(data2)
        # A signal is sent, but not implemented in GenericWidget

        self.assertEquals(widget2.get_widget_value(), prevValue)
        data2.value = newValue

        self.assertEquals(widget2.get_widget_value(), newValue)
        self.assertEquals(widget2.get_widget_value().__class__, newValue.__class__)
        self._print_widget_value(widget2, prevValue, newValue)

        ''' TEST 3.1 '''
        # Go with the strings, edit line
        prevValue = 'puppa'
        newValue  = 'melo'

        data6 = DataClassString(name='name6', value=prevValue, maxlength=10)
        widgettype6 = 'EditLineWidget'
        widget6 = tkwrapper.TkWidget(root,data6.name, widgettype6, data6)
        self.assertEquals(widget6.get_widget_value(), prevValue)
        data6.value = newValue
         # VERIFY
        self.assertEquals(widget6.get_widget_value(), newValue)
        self._print_widget_value(widget6, prevValue, newValue)

        ''' TEST 3.2 '''
        # Go with the strings, combobox
        data8 = DataClassDiscreteString(name='name8', value=prevValue, limits=[prevValue,  'some other value', newValue])
        widgettype8 = 'ComboBoxWidget'
        widget8 = tkwrapper.TkWidget(root,data8.name, widgettype8, data8)
        self.assertEquals(widget8.get_widget_value(), prevValue)
        data8.value = newValue
        # print(widget2.get_widget_value())
        self.assertEquals(widget8.get_widget_value(), newValue)
        self._print_widget_value(widget8, prevValue, newValue)

        ''' TEST 3.3 '''
        # Go with the strings, Label
        data9 = DataClassString(name='name8', value=prevValue)
        widgettype9 = 'LabelWidget'
        widget9 = tkwrapper.TkWidget(root, data9.name, widgettype9, data9)
        self.assertEquals(widget9.get_widget_value(), prevValue)
        data9.value = newValue
        # print(widget2.get_widget_value())
        self.assertEquals(widget9.get_widget_value(), newValue)
        self._print_widget_value(widget9, prevValue, newValue)

        ''' TEST 3.4 '''
        # Go with the strings, Label
        data10 = DataClassString(name='name8', value=prevValue)
        widgettype10 = 'TextWidget'
        widget10 = tkwrapper.TkWidget(root, data10.name, widgettype10, data10)
        self.assertEquals(widget10.get_widget_value(), prevValue)
        data10.value = newValue
        # print(widget2.get_widget_value())
        self.assertEquals(widget10.get_widget_value(), newValue)
        self._print_widget_value(widget10, prevValue, newValue)

        root.destroy()

    def test_xml_functions(self):
        # TKinter Stuff
        root = tk.Tk()
        root.title('Main root')
        root_reconstructed = tk.Tk()
        root_reconstructed.title('Reconstructed root')

        data1 = []  # a list of sever data class
        widget1 = []
        filename_xml1 = []

        """ ------------------------- """
        """ TEST 1 - ALL SINGLE WIDGETS """
        data1.append(['FloatWidget', DataClassNumber(name='name1', value=2, initvalue=1.11214)])
        filename_xml1.append(self._path + 'tkwidget_test_creation_float_1.xml')
        data1.append(['IntWidget', DataClassIntNumber(name='name2', value=2, limits=[-2,2])])
        filename_xml1.append(self._path + 'tkwidget_test_creation_int_1.xml')
        data1.append(['ComboBoxWidget', DataClassDiscreteNumber(name='name3', value=2, limits=[-2.1,2.2, 0.1, 1.1, -2,2], initvalue=0.1)])
        filename_xml1.append(self._path + 'tkwidget_test_creation_discretefloat_1.xml')
        data1.append(['ComboBoxWidget', DataClassDiscreteIntNumber(name='name4', value=2, limits=[-2, 0, 2])])
        filename_xml1.append(self._path + 'tkwidget_test_creation_discreteint_1.xml')

        for idx, d in enumerate(data1):
            widget1.append(tkwrapper.TkWidget(root, d[1].name, d[0], d[1]))
            #temp_XML = widget.XMLWidgetHelper.widgetToXML( widget1[idx], filename=filename_xml1[idx])
            temp_XML = widget1[idx].saveToXMLFile(filename=filename_xml1[idx])
            # Reopen filename1 and verify it
            self._verify_and_assert_xml_file(root_reconstructed, widget1[idx], temp_XML, filename_xml1[idx])

        # just for test
        # root.mainloop()
        # root_reconstructed.mainloop()

        # try to save the whole list and check it out
        root_list_reconstructed = tk.Tk()
        root_list_reconstructed.title('Reconstructed List root')
        filename_xml_list = (self._path + 'tkwidget_test_creation_list_1.xml')
        XML_list = widget.XMLWidgetHelper.widgetToXML(widget1, filename=filename_xml_list)
        self._verify_and_assert_xml_file(root_list_reconstructed, widget1, XML_list, filename_xml_list)

        # TEST ONLY!! Remove and uncomment root.destroy
#        root_list_reconstructed.mainloop()

        # Final remove the TK stuff
        root.destroy()
        root_list_reconstructed.destroy()
        root_reconstructed.destroy()

    def test_display_widget_and_modify(self):
        # TKinter Stuff
        root = tk.Tk()

        # Create a frame local class
        class LocalFrame():
            def __init__(self, master=None):
                self.frame = tk.Frame(master, relief=tk.SUNKEN, bd=3)
                self.frame.pack(padx=2, pady=2)

        app = LocalFrame(master=root)
        root.title('Simple widget test')

        # TODO: develop for every widget type
        # TODO: add a set value with proper test

        # Init int  widget
        label1 = []
        newValue = []
        data1 = []
        widget1 = []
        widgettype1 = []

        # Prepare Test FLOAT WIDGET
        newValue.append(9.0)
        widgettype1.append('FloatWidget')
        data1.append(DataClassNumber(name=widgettype1[-1], value=8.0))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        # Prepare Test INT WIDGET
        newValue.append(2)
        widgettype1.append('IntWidget')
        data1.append(DataClassIntNumber(name=widgettype1[-1], value=8))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        # Prepare Test FLOAT WIDGET DISCRETE
        newValue.append(-2.1)
        widgettype1.append('ComboBoxWidget')
        data1.append(DataClassDiscreteNumber(name=widgettype1[-1], value=2, limits=[-2.1, 2.2, 0.1, 1.1, -2, 2]))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        # Prepare Test INT WIDGET DISCRETE
        newValue.append(-3)
        widgettype1.append('ComboBoxWidget')
        data1.append(DataClassDiscreteIntNumber(name=widgettype1[-1], value=2, limits=[-2, 2, 0, 1, -3, 4]))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        # Prepare Test STRING WIDGET DISCRETE
        newValue.append('Ciao')
        widgettype1.append('ComboBoxWidget')
        data1.append(DataClassDiscreteString(name=widgettype1[-1], value='Hi', limits=['Hi', 'Hallo', 'Ciao', 'Tschuss'])) #, 1, -3, 4]))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        # Prepare Test STRING WIDGET DISCRETE
        newValue.append('Hallo')
        widgettype1.append('EditLineWidget')
        data1.append(DataClassString(name=widgettype1[-1], value='Hi man!'))
        widget1.append(tkwrapper.TkWidget(app.frame, data1[-1].name, widgettype1[-1], data1[-1]))

        for idx, w in enumerate(widget1):
            label1.append(ttk.Label(app.frame, text=widgettype1[idx] + ", change value to " + str(newValue[idx])))
            label1[idx].grid(row=idx, column=0)
            widget1[idx].grid(row=idx, column=1)



        def _checkValues():
            for idx, w in enumerate(widget1):
                #print (w.get_widget_value(), file=sys.stderr)
                self.assertEqual(w.get_widget_value(), newValue[idx])
            root.destroy()


        btn = ttk.Button(app.frame, text='Submit change!', command=_checkValues)
        btn.grid(row=idx+2, column=0, columnspan=2)

        #.grid(row=0)

        # data2 = DataClassNumber(name='intValue', value=intValue, limits=[intValue - 1, intValue + 1])
        # widgettype2 = 'FloatWidget'
        # widget2 = tkwrapper.TkWidget(app.frame, data2.name, widgettype2)
        # widget2.associateData(data2)
        # data2.set_value(9.1)
        # widget2.pack(ipady=10,padx=10)
        # self.widget3 = ttk.Label(app.frame, text="Hello", )
        # self.widget3.pack()

        root.mainloop()

    def test_signal(self):
        '''
        Test if setting a value the widget value is changed by sending the appropriate signal
        :return:
        '''
        # TKinter Stuff
        root = tk.Tk()

        # prepare signal callback
        _widgetChanged = [0]

        def on_widgetUpdated():
            _widgetChanged[0] = 1

        # data list for test
        data1 = []
        widget1 = []
        newValue1  = []
        newValue2 = []

        # test 1
        data1.append(['FloatWidget', DataClassNumber(name='floattest', value=1.1)])
        widget1.append(tkwrapper.TkWidget(root, data1[-1][1].name, data1[-1][0], data1[-1][1]))
        newValue1.append(2.5)
        newValue2.append(1.414)

        # TODO: develop for every widget type
        for idx, d in enumerate(data1):
            dispatcher.connect(on_widgetUpdated, signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=widget1[idx])
            _widgetChanged[0] = 0
            #d[1].value = newValue1[idx]
            widget1[idx].set_widget_value(newValue1[idx])
            self.assertEqual(_widgetChanged[0], 1)
            _widgetChanged[0] = 0
            d[1].value = newValue2[idx]
            self.assertEqual(_widgetChanged[0], 1)


        # # Init the widget
        # data1 = DataClassNumber(name='name1', value=prevValue)
        # widgettype1 = 'FloatWidget'
        # widget1 = guidatawrapper.GuidataWidget(data1.name, widgettype1, data1)
        #
        #
        #
        # # Connect the signal and test
        # dispatcher.connect(on_widgetUpdated, signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=widget1)
        #
        # # test by setting directly the value in the dataclass associated to widget
        # data1.value = newValue1
        # self.assertEqual(_widgetChanged[0], 1)
        #
        # # test the set widget
        # _widgetChanged[0] = 0
        # widget1.setWidgetValue(prevValue)
        # self.assertEqual(_widgetChanged[0], 1)
        #
        # # Test string based
        # prevValue = '2'
        # newValue1 = '3'
        # # Init the widget
        # data2 = DataClassDiscreteString(name='name2', value=prevValue, limits=[newValue1, prevValue])
        # widgettype2 = 'ComboBoxWidget'
        # widget2 = guidatawrapper.GuidataWidget(data2.name, widgettype2, data2)
        #
        # # prepare signal calls
        # # Connect the signal and reset flag
        # dispatcher.connect(on_widgetUpdated, signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE, sender=widget2)
        # _widgetChanged[0] = 0
        # # test by setting directly the value in the dataclass associated to widget
        # data2.value = newValue1
        # self.assertEqual(_widgetChanged[0], 1)
        #
        # # test the set widget
        # _widgetChanged[0] = 0
        # widget1.setWidgetValue(prevValue)
        # self.assertEqual(_widgetChanged[0], 1)

    def _print_widget_value(self, widget, prevalue, newvalue):
        wval = widget.get_widget_value()
        print(widget.name + ': ' + widget.__class__.__name__ + ' prevalue=' + str(prevalue) + ' newvalue= ' + str(newvalue) + ' get value=' + str(wval), file=sys.stderr)
        print('       instance new value >' + newvalue.__class__.__name__ + '< instance get value >' + wval.__class__.__name__  + '<', file=sys.stderr)

    def _verify_and_assert_xml_file(self, rootwidget, widgetdata, xmldata, filename):
        # Reopen filename and verify the xml content an regenerate the widget
        widget1_1 = tkwrapper.TkWidget.loadXMLFileToData(filename, rootwidget)
        XML1_1 = widget.XMLWidgetHelper.widgetToXML(widget1_1)
        self.assertEqual(xmldata, XML1_1)
        self.assertEqual(widgetdata, widget1_1)

if __name__ == '__main__':
    unittest.main()