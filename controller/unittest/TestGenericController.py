import unittest
import controller
import dataclass
import view
import view.unittest.TestViewSupportFunctions
from utilities.misc import FunctionThread, start_logger_unittest


class TestGenericController(unittest.TestCase):
    def test_add_widget(self):

        # Fulfil a empty controller with properties and widget separtely
        model1 = controller.GenericController.modelFactory('model.DataClassModel')
        view1  =  controller.GenericController.viewFactory('guidatawrapper.GuidataView')
        _data, _widgettype, _widgetname = view.unittest.TestViewSupportFunctions.createData1()
        _controller1 = controller.GenericController(model1, view1)

        for d in _data:
            _controller1.addPropertyToModel(d)
        # Test re-add a property
        with self.assertRaises(controller.ControllerException.ErrorAddingProperty) :_controller1.addPropertyToModel(d)

        # Test adding a non valid property
        with self.assertRaises(controller.ControllerException.ErrorAddingProperty): _controller1.addPropertyToModel(1)

        for idx, wt in enumerate(_widgettype):
            _w = guidatawrapper.GuidataWidget(_data[idx].name, wt)
            _controller1.addWidgetToView(_data[idx].name, _w)
        # Test readd the last widget
        with self.assertRaises(controller.ControllerException.ErrorAssociatingDatToWidget): _controller1.addWidgetToView(_data[idx].name, _w)

        # Test to add a widget to not existing property
        with self.assertRaises(controller.ControllerException.ErrorRetrievingProperty):  _controller1.addWidgetToView('nodata',guidatawrapper.GuidataWidget('nodata', wt))

        view1.show()
        th = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=view1.getViewContainer())
        th.start()
        view1.getQTApp().exec_()

    def test_add_widget_to_subview(self):

        start_logger_unittest()
        # TODO: test the follow
        # Fulfil a empty controller with properties and widget separtely
        model1 = controller.GenericController.modelFactory('model.DataClassModel')
        main_view  =  controller.GenericController.viewFactory('guidatawrapper.GuidataView')
        _app = main_view.getQTApp()

        _data1, _widgettype1, _widgetname1 = view.unittest.TestViewSupportFunctions.createData1()
        _data2, _widgettype2, _widgetname2 = view.unittest.TestViewSupportFunctions.createData2()

        viewname1='Subview 1'
        viewname2='Subview 1 of 2'
        viewname3='Subview 2 of 2'
        sub_view1 = guidatawrapper.GuidataView(viewname=viewname1, qtapp=_app, viewtype='Tabs',)
        sub_view2 = guidatawrapper.GuidataView(viewname=viewname2, qtapp=_app)
        sub_view3 = guidatawrapper.GuidataView(viewname=viewname3, qtapp=_app)


        main_view.addSubView(sub_view1)
        sub_view1.addSubView(sub_view2)
        sub_view1.addSubView(sub_view3)

        _controller1 = controller.GenericController(model1, main_view)

        # Add widget to subview1
        for idx, d in enumerate(_data1):
            _controller1.addPropertyToModel(d)
            _w = guidatawrapper.GuidataWidget(_data1[idx].name, _widgettype1[idx])
            _controller1.addWidgetToView(_data1[idx].name, _w, view_name=viewname1)

        # Test re-add a sub view
        with self.assertRaises(controller.ControllerException.ErrorAssociatingDatToWidget):
            _controller1.addWidgetToView(_data1[idx].name, _w, view_name=viewname1)

        # Add widget to subview2
        for idx, d in enumerate(_data2):
            _controller1.addPropertyToModel(d)
            _w = guidatawrapper.GuidataWidget(_data2[idx].name, _widgettype2[idx])
            _controller1.addWidgetToView(_data2[idx].name, _w, view_name=viewname2)

        # Add widget to subview3
        for idx, d in enumerate(_data2):
            # _controller1.addPropertyToModel(d) # already added!!
            _w = guidatawrapper.GuidataWidget(_data1[idx].name, _widgettype1[idx])
            _controller1.addWidgetToView(_data1[idx].name, _w, view_name=viewname3)

        # Test add a widget to a wrong view
        _w = guidatawrapper.GuidataWidget(_data1[idx].name, _widgettype1[idx])
        with self.assertRaises(controller.ControllerException.ErrorAddingWidgetToView):
            _controller1.addWidgetToView(_data1[idx].name, _w, view_name='some wrong name')

        main_view.show()
        th = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=main_view.getViewContainer())
        #th.start()
        main_view.getQTApp().exec_()


    def test_add_property(self):
        model1 = controller.GenericController.modelFactory('model.DataClassModel')
        view1  =  controller.GenericController.viewFactory('guidatawrapper.GuidataView')

        _controller1 = controller.GenericController(model1, view1)

        data1 = dataclass.DataClassNumber('name1',1)
        _controller1.addPropertyToModelAndView(data1, 'guidatawrapper.GuidataWidget', 'FloatWidget')

        # TODO: test add to not existent subview


        view1.show()
        th = FunctionThread(guidatawrapper.unittest.TestGuidataUtility.closeWindow, win=view1.getViewContainer())
        th.start()
        view1.getQTApp().exec_()

if __name__ == '__main__':
    unittest.main()
