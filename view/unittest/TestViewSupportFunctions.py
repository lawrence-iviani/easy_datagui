
import dataclass.DataClassDiscreteNumber
import dataclass.DataClassNumber
import view.GenericView
import widget.GenericWidget

def createData1():
    data1 = []
    widgettype1 = []
    widgetname1 = []

    widgetname1.append('name1')
    data1.append(dataclass.DataClassNumber(name=widgetname1[-1], value=2))
    widgettype1.append('FloatWidget')
    widgetname1.append('name2')
    data1.append(dataclass.DataClassDiscreteNumber(name=widgetname1[-1], value=2, limits=[0,2]))
    widgettype1.append('ComboBoxWidget')
    widgetname1.append('a_strange_name')
    data1.append(dataclass.DataClassNumber(name=widgetname1[-1], value=2))
    widgettype1.append('FloatWidget')
    widgetname1.append('funny_11_name')
    data1.append(dataclass.DataClassDiscreteNumber(name=widgetname1[-1], value=2, limits=[0,2]))
    widgettype1.append('ComboBoxWidget')

    return data1, widgettype1, widgetname1

def createData2():
    # Define dataset and widget
    data2 = []
    widgettype2 = []
    widgetname2 = []

    widgetname2.append('name2_1')
    data2.append(dataclass.DataClassNumber(name=widgetname2[-1], value=2))
    widgettype2.append('FloatWidget')
    widgetname2.append('name2_2')
    data2.append(dataclass.DataClassDiscreteNumber(name=widgetname2[-1], value=2, limits=[0,2]))
    widgettype2.append('ComboBoxWidget')
    widgetname2.append('a_strange_name_2')
    data2.append(dataclass.DataClassNumber(name=widgetname2[-1], value=2))
    widgettype2.append('FloatWidget')
    widgetname2.append('funny_22_name')
    data2.append(dataclass.DataClassDiscreteNumber(name=widgetname2[-1], value=2, limits=[0,2]))
    widgettype2.append('ComboBoxWidget')

    return data2, widgettype2, widgetname2

def createView1():
    # Define dataset and widget
    widget1 = []
    data1, widgettype1, widgetname1 = createData1()

    # generate widget list and add to view 1
    view1 = view.GenericView('My View1')
    for idx, d in enumerate(data1):
        widget1.append(widget.GenericWidget(d.name, widgettype1[idx], d))
        view1.addWidget(widget1[-1])

    return view1, widget1, widgettype1,widgetname1, data1

def createView2():
    # Define dataset and widget

    widget2 = []

    data2, widgettype2, widgetname2 = createData2()

    # generate widget list and add to view 1
    view2 = view.GenericView('My View2')
    for idx, d in enumerate(data2):
        widget2.append(widget.GenericWidget(d.name, widgettype2[idx], d))
        view2.addWidget(widget2[-1])

    return view2, widget2, widgettype2,widgetname2, data2



def createSubView1():
    view1   = createView1()
    view1_1 = createView1()
    view2_1 = createView2()
    view1_1_1 = createView1()
    view1_1_2 = createView2()


    view1_1[0].addSubView(view1_1_1[0])
    view1_1[0].addSubView(view1_1_2[0])
    view1[0].addSubView(view1_1[0])
    view1[0].addSubView(view2_1[0])


    return view1[0]


