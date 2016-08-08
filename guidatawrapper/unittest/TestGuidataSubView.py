import unittest
import guidatawrapper
import view
from dataclass import (DataClass, DataClassNumber, DataClassDiscreteNumber, DataClassNotSupported)
from guidata.qt.QtGui import (QMainWindow, QSplitter, QApplication, QAction)
from pydispatch import dispatcher
from utilities.misc import FunctionThread
import logging
import guidatawrapper.unittest.TestGuidataUtility
import guidatawrapper.unittest.TestGuidataView


class TestGuidataSubView(unittest.TestCase):

    def test_addsubview_1(self):
        '''
        Test adding subview, verify MANUALLY the values are set properly
        :return:
        '''
        # QT Stuff
        newValue = -2

        app = QApplication([])
        main_view = guidatawrapper.GuidataView(viewname='Check ' + str(newValue) + " is applied in all subviews",  qtapp=app)
        (data1, widgettype1, widget1) = guidatawrapper.unittest.TestGuidataUtility .create_widget1(value=10)
        main_view.addWidgets(widget1)

        # Generate sub view1 and other two further subviews
        sub_view1 = guidatawrapper.GuidataView(viewname='Subview1', qtapp=app, viewtype='Splitter')
        sub_view1.addWidgets(widget1)

        sub_view2 = guidatawrapper.GuidataView(viewname='Subview2',  qtapp=app)
        sub_view2.addWidgets(widget1)

        main_view.addSubView(sub_view1)
        main_view.addSubView(sub_view2)

        main_view.show()
        th1 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=main_view.getViewContainer(), wait=2)
        th1.start()
        th2 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.setDataValue, datalist=data1, value=newValue, wait=1)
        th2.start()
        main_view.getQTApp().exec_()
        for d in data1:
            for wname in main_view.getSubViewNamesList():
                subv = main_view.getSubView(wname)
                subw = subv.getWidget(d.name)
                self.assertEquals(str(subw.getWidgetValue()), str(newValue))
            mainw = main_view.getWidget(d.name)
            self.assertEquals(str(mainw.getWidgetValue()), str(newValue))

    def test_addsubview_2(self):
        '''
        Test adding subview, verify MANUALLY the values are set properly
        :return:
        '''
        # QT Stuff
        newValue1 = -2.1
        newValue2 = -2.1

        app = QApplication([])
        main_view, data1, data2 = guidatawrapper.unittest.TestGuidataUtility.create_complex_view(app)

        main_view.show()
        th1 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=main_view.getViewContainer(), wait=3.5)
        th1.start()
        th2 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.setDataValue, datalist=data1, value=newValue1, wait=1)
        th3 = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.setDataValue, datalist=data2, value=newValue1, wait=2)
        th2.start()
        th3.start()
        main_view.getQTApp().exec_()

        all_sub_view = self._getAllSubView(main_view)
        for d in data1:
            for sw in all_sub_view:
                subw = sw.getWidget(d.name)
                if subw is not None:
                    self.assertEquals(str(subw.getWidgetValue()), str(newValue1))

    def _getAllSubView(self, view_instance):
        '''
        Creates a list with all the possible sub view, removing the storing hierarchy
        An utility for test all the subview
        :param view_instance:
        :return:
        '''
        sub_view_list = []
        if isinstance(view_instance, view.GenericView):
            for sw_name in view_instance.getSubViewNamesList():
                sw = view_instance.getSubView(sw_name)
                sub_view_list.append(sw)
                ssw = self._getAllSubView(sw)
                if len(ssw):
                    sub_view_list.extend(ssw)
                else:
                    sub_view_list.append(view_instance)

        return sub_view_list

    def test_set_any_string(self):
        app = QApplication([])

        view1, data1 = guidatawrapper.unittest.TestGuidataUtility.create_complexview_strings_only1(app, viewname='Change at least one value and apply')

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

        _someValueChanged = 0
        for pvk in _prevValues.keys():
            for sv in view1.getSubViewList():
                for d in data1:
                    if d.name == pvk:
                        w = sv.getWidget(d.name)
                        v = w.getWidgetValue()
                        print('Subview:'+sv.viewname+' prop:' +d.name + ' d.value=' + str(v) +' _prevValues[pvk]='+ str(_prevValues[pvk]))
                        if v != _prevValues[pvk]:
                            _someValueChanged += 1

        self.assertTrue(_someValueChanged > 0)
if __name__ == '__main__':
    unittest.main()
