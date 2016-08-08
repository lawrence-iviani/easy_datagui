import unittest
import guidatawrapper
import view
from dataclass import (DataClass,DataClassString, DataClassNumber, DataClassDiscreteString, DataClassDiscreteNumber, DataClassNotSupported)
from guidata.qt.QtGui import (QMainWindow, QSplitter, QApplication, QAction)
from pydispatch import dispatcher
from utilities.misc import FunctionThread, start_logger_unittest
import widget
import guidatawrapper.unittest.TestGuidataUtility


__author__ = 'law'


class TestGuidataView(unittest.TestCase):

    def test_view(self):
        # QT Stuff
        app = QApplication([])
        view1 = guidatawrapper.GuidataView(viewname='test_view',  qtapp=app)
        # add widget
        (data1, widgettype1, widget1) = guidatawrapper.unittest.TestGuidataUtility.create_widget1()

        for w in widget1:
            view1.addWidget(w)

        # Try to add a not compatible widget
        _wrongWidget = widget.GenericWidget('somename', 'FloatWidget')
        with self.assertRaises(view.WrongWidgetClass): view1.addWidget(_wrongWidget)

        view1.show()
        th = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=view1._parentFrame )
        th.start()

        view1.getQTApp().exec_()

    def test_set_wrong_value(self):
        # QT Stuff
        app = QApplication([])
        view1 = guidatawrapper.GuidataView(viewname='Press apply when a wrong value appears and then the value of 1',  qtapp=app)
        initvalue = 1
        # With Limits
        data1=DataClassNumber(name='n_name1_2', value=initvalue, limits=[-10, 10])
        widget1=guidatawrapper.GuidataWidget(data1.name, 'FloatWidget', data1)
        view1.addWidget(widget1)

        # test if the value is update
        wrongValue = 100.1111
        def set_wrong_value(wait):
            import time
            time.sleep(wait)
            widget1.setWidgetValue(wrongValue)

        _viewChanged = [0]
        def on_viewUpdated():
            _viewChanged[0] = 1
            guidatawrapper.unittest.TestGuidataUtility.closeWindow(view1.getViewContainer(),0.01)

        dispatcher.connect(on_viewUpdated, signal=view.GenericView.SIGNAL_VIEWUPDATE, sender=view1)

        view1.show()
        th2 = FunctionThread(set_wrong_value, wait=1)
        th2.start()
        view1.getQTApp().exec_()

        import time
        time.sleep(1)
        view1.show()
        view1.getQTApp().exec_()

        self.assertEqual( _viewChanged[0], 1)
        self.assertEqual(initvalue, widget1.getWidgetValue())

    def test_viewupdate(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''
        # QT Stuff
        app = QApplication([])
        view1 = guidatawrapper.GuidataView(viewname='test_viewupdate ',  qtapp=app)

        (data1,widgettype1,widget1) = guidatawrapper.unittest.TestGuidataUtility.create_widget1(value=-2.1)

        for w in widget1:
            view1.addWidget(w)

        # Retrieve the widget and check it
        widget1_1 = view1.getWidget(data1[0].name)
        self.assertEquals(widget1[0], widget1_1)

        # Change the value in data before show it and verify if it reflected in the widget
        # Note, the user must check the widget displayed is correct
        prevValue = -2.1 # Check in create_widget1 it is correct
        newValue  = -2
        self.assertEquals(widget1_1.getWidgetValue(), prevValue)
        for d in data1:
            w = view1.getWidget(d.name)
            if isinstance(d.value, str):
                d.value = str(newValue)
                self.assertEquals(w.getWidgetValue(), str(newValue))
            else:
                d.value = newValue
                self.assertEquals(w.getWidgetValue(), newValue)

        view1.show()
        th = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=view1.getViewContainer())
        th.start()
        view1.getQTApp().exec_()

        # Test if the value change after display (not very useful, it is related to data class baehvior)
        prevValue = newValue
        newValue  = 10
        self.assertEquals(widget1_1.getWidgetValue() , prevValue)
        for d in data1:
            w = view1.getWidget(d.name)
            if isinstance(d.value, str):
                d.value = str(newValue)
                self.assertEquals(w.getWidgetValue(), str(newValue))
            else:
                d.value = newValue
                self.assertEquals(w.getWidgetValue(), newValue)

        # test if the value is update
        newValue = -2
        view1.show()
        th1 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=view1.getViewContainer(), wait =2)
        th1.start()
        th2 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.setDataValue, datalist=data1, value=newValue, wait=1)
        th2.start()
        view1.getQTApp().exec_()
        self.assertEquals(widget1_1.getWidgetValue(), newValue)

    def test_signal(self):
        '''
        Test if setting a value the widget value is changed
        :return:
        '''
        # QT Stuff
        app = QApplication([])
        view1 = guidatawrapper.GuidataView(viewname='test_signal: Change one value and apply',  qtapp=app)
        (data1, widgettype1, widget1) = guidatawrapper.unittest.TestGuidataUtility.create_widget1(value=-2)
        view1.addWidgets(widget1)

        # prepare signal calls
        _viewChanged = [0]
        def on_viewUpdated():
            _viewChanged[0] = 1
        # Connect the signal
        dispatcher.connect(on_viewUpdated, signal=view.GenericView.SIGNAL_VIEWUPDATE, sender=view1)

        # test by setting directly the value in the dataclass associated to widget
        data1[0].value = 2.1
        self.assertEqual(_viewChanged[0], 1)

        # test the set widget
        _viewChanged[0] = 0
        widget1[0].setWidgetValue(3)
        self.assertEqual(_viewChanged[0], 1)

    def test_apply_and_signal(self):
        '''
        Test for the user interaction. User must change at least one of the values inside the test
        :return:
        '''

        app = QApplication([])
        view1 = guidatawrapper.GuidataView(viewname='Apply test: change two or more values and apply',  qtapp=app)
        (data1, widgettype1, widget1) = guidatawrapper.unittest.TestGuidataUtility.create_widget1(value=-1.1)
        view1.addWidgets(widget1)

        # Backup values
        _prevValues = {}
        for d in data1:
            _prevValues[d.name] = d.value

        _viewChanged = [0]
        def on_viewUpdated():
            _viewChanged[0] = 1
            guidatawrapper.unittest.TestGuidataUtility.closeWindow(view1.getViewContainer(), 0.01)

        dispatcher.connect(on_viewUpdated, signal=view.GenericView.SIGNAL_VIEWUPDATE, sender=view1)

        view1.show()
        view1.getQTApp().exec_()

        # _someValueChanged = False
        # for pvk in _prevValues.keys():
        #     for d in data1:
        #         if d.name == pvk:
        #             v = d.value
        #             print(d.name + ' d.value=' + str(v) +' _prevValues[pvk]='+ str(_prevValues[pvk]))
        #             if v != _prevValues[pvk]:
        #                 _someValueChanged = True
        #                 break
        # self.assertTrue(_someValueChanged)

        _someValueChanged = 0
        for pvk in _prevValues.keys():
            for w in widget1:
                if w.name == pvk:
                    v = w.getWidgetValue()
                    print(w.name + ' w.value=' + str(v) +' _prevValues[pvk]='+ str(_prevValues[pvk]))
                    if v != _prevValues[pvk]:
                        _someValueChanged += 1


        self.assertEqual(_viewChanged[0], 1)
        self.assertTrue(_someValueChanged > 1)


    def test_apply_number(self):
        '''
        Test the combo box widget, that requires special attention  due to the guidata implementation which returns the
        index and not the value
        :return:
        '''

        initValue = 20.1
        endValue  = 1.414
        widget_type = 'ComboBoxWidget'
        data_inst = (DataClassDiscreteNumber(name='Set_value_' + str(endValue)+ '_and_apply', value=initValue, limits=[-10.4, 20.1, 10.44, -22.1, 333.1, 1.414]))
        self._apply_value( data_inst, widget_type, initValue, endValue)


    def test_apply_string(self):
        '''
        Test the combo box widget, that requires special attention  due to the guidata implementation which returns the
        index and not the value
        :return:
        '''

        initValue = 'pippo'
        endValue  = 'pluto'
        widget_type = 'ComboBoxWidget'
        data_inst = (DataClassDiscreteString(name='Set_value_' + str(endValue)+ '_and_apply',
                                             value=initValue,
                                             limits=[initValue,'puppami la fava', 'ein pils bitte', endValue]))
        self._apply_value( data_inst, widget_type, initValue, endValue)

    def _apply_value(self, data_inst, widget_type, initValue, endValue):

        app = QApplication([])
        view_inst = guidatawrapper.GuidataView(viewname='Apply test',  qtapp=app)

        # add a second widget...
        data1 = DataClassString(name='seconddata', value='This value doesnt affect the test')
        view_inst.addWidget(guidatawrapper.GuidataWidget(data1.name, 'EditLineWidget', data1))

        widget_inst = guidatawrapper.GuidataWidget(data_inst.name, widget_type, data_inst)
        view_inst.addWidget(widget_inst)

        _viewChanged = [0]
        def on_viewUpdated():
            _viewChanged[0] = 1
            guidatawrapper.unittest.TestGuidataUtility.closeWindow(view_inst.getViewContainer(), 0.01)

        dispatcher.connect(on_viewUpdated, signal=view.GenericView.SIGNAL_VIEWUPDATE, sender=view_inst)

        view_inst.show()
        self.assertEqual(widget_inst.getWidgetValue(), initValue)
        # self.assertEqual(data_inst.value, initValue)
        view_inst.getQTApp().exec_()
        self.assertEqual(widget_inst.getWidgetValue(), endValue)

    def test_view_with_no_data(self):
        app = QApplication([])

        view1 = guidatawrapper.GuidataView(viewname='Apply test',  qtapp=app)
        widget1 = guidatawrapper.GuidataWidget('test1', 'ComboBoxWidget')
        view1.addWidget(widget1)
        with self.assertRaises(widget.WidgetException.WidgetNotYetAssociated):
            view1.show()
            view1.getQTApp().exec_()


if __name__ == '__main__':
    unittest.main()
