
import unittest
import dataclass
import widget
import view
import view.unittest.TestViewSupportFunctions

__author__ = 'law'


class TestGenericView(unittest.TestCase):
    def test_constructor(self):
        # Init test conditions
        data1 = dataclass.DataClassNumber(name='name1', value=2)
        widgettype1 = 'FloatWidget'
        widget1 = widget.GenericWidget(data1.name,widgettype1,data1)

        # test add a single widget
        view1 = view.GenericView('My View1')
        view1.addWidget(widget1)

        self.assertTrue(view1.isWidgetPresent('name1'))
        self.assertFalse(view1.isWidgetPresent('name2'))

        # test add an already existing widget -> exception
        with self.assertRaises(view.ErrorAddingWidget): view1.addWidget(widget1)

        # test add a non widget
        with self.assertRaises(view.ErrorAddingWidget): view1.addWidget(object())

        # test add a list of widgets and several check
        data2 = []
        data2.append(dataclass.DataClassNumber(name='name1', value=1))
        data2.append(dataclass.DataClassNumber(name='name2', value=2))
        view2 = view.GenericView('My View2')
        widgettype2 = 'FloatWidget'
        for  idx, d in enumerate(data2):
            w = widget.GenericWidget(d.name,widgettype2,d)
            view2.addWidget(w)
            self.assertTrue(view2.getWidget(d.name))
            self.assertEqual(w,view2.getWidget(d.name))

        with self.assertRaises(NotImplementedError): view2.show()

        # test a set operation which must fail
        with self.assertRaises(NotImplementedError): view1.getWidget('name1').set_widget_value(1)

    def test_widgets_in(self):
        view1, widget1, widgettype1, widgetname1, data1 = view.unittest.TestViewSupportFunctions.createView1()

        # test the get
        for idx, wname in enumerate(widgetname1):
            w = view1.getWidget(wname)
            self.assertEqual(w,widget1[idx])

        # test get all widget name
        all_widgets_name = view1.getWidgetNamesList()
        self.assertEqual(all_widgets_name, widgetname1)

        #test the get_all
        all_widgets = view1.getWidgetsList()
        self.assertEqual(all_widgets, widget1)

        # Test wrong widget
        with self.assertRaises(view.ErrorAddingWidget): view1.addWidget(object())

        # test list of widget
        _wListWrong = []
        _wListWrong.append(object())
        with self.assertRaises(view.ErrorAddingWidget): view1.addWidgets(_wListWrong)

    def test_addsubview(self):
        # Init test conditions
        data1 = []
        widget1 = []

        data1.append(dataclass.DataClassNumber(name='name1', value=1.1))
        data1.append(dataclass.DataClassNumber(name='name2', value=2.2))
        data1.append(dataclass.DataClassNumber(name='name3', value=3.3))
        widgettype = 'FloatWidget'
        for d in data1:
            widget1.append(widget.GenericWidget(d.name, widgettype, d))

        # test add a single widget
        view1 = view.GenericView('My View1')
        view1.addWidgets(widget1)

        widget2 = widget.GenericWidget(data1[0].name, widgettype, data1[0])
        # test add a single widget
        view2 = view.GenericView('My subView2')
        view2.addWidget(widget2)
        view1.addSubView(view2)

        # add self
        with self.assertRaises(view.SubViewAlreadyPresentError): view1.addSubView(view1)

        # readd subview 2
        with self.assertRaises(view.SubViewAlreadyPresentError): view1.addSubView(view2)

        # add a wrong object
        with self.assertRaises(view.WrongSubViewClass): view1.addSubView(object())

    def test_subviewlist(self):
        # Init test conditions
        data1 = []
        widget1 = []

        data1.append(dataclass.DataClassNumber(name='name1', value=1.1))
        data1.append(dataclass.DataClassNumber(name='name2', value=2.2))
        data1.append(dataclass.DataClassNumber(name='name3', value=3.3))
        widgettype = 'FloatWidget'
        for d in data1:
            widget1.append(widget.GenericWidget(d.name, widgettype, d))

        # test add a single widget
        view1 = view.GenericView('My View1')

        # add some widgets
        sub_view1_1 = view.GenericView('My subView1_1')
        sub_view1_1.addWidget(widget1[0])
        sub_view1_2 = view.GenericView('My subView1_2')
        sub_view1_1.addWidget(widget1[1])
        sub_view1_3 = view.GenericView('My subView1_3')
        sub_view1_3.addWidget(widget1[2])
        # different subview but same name
        sub_view2_1 = view.GenericView('My subView1_1')
        sub_view2_1.addWidgets(widget1)

        # test add a single widget
        view1.addSubView(sub_view1_1)
        view1.addSubView(sub_view1_2)
        view1.addSubView(sub_view1_3)

        sub_view1_1.addSubView(sub_view2_1)

        # Test view 1
        _listView1 = view1.getSubViewListByName('My View1')
        self.assertEqual(view1,_listView1)

        # Test subview1_2
        _listView1_2 = view1.getSubViewListByName('My subView1_2')
        self.assertEqual(sub_view1_2,_listView1_2)

        # My subView1_1
        _listView1_1 = view1.getSubViewListByName('My subView1_1')
        self.assertEqual([sub_view1_1, sub_view2_1 ],_listView1_1)

        # Empty subview
        _listView_empty = view1.getSubViewListByName('My ')
        self.assertEqual([ ],_listView_empty)


if __name__ == '__main__':
    unittest.main()
