
import dataclass
import guidatawrapper
import time

path = './guidatawrapper/unittest/xmlfiles/'
#path = './xmlfiles/'


def create_widget1(value=-2, valuestring='pippo'):
    '''
    A standard test, not a real test
    :return:
    '''
    # Init list
    data1       = []
    widgettype1 = []
    widget1     = []

    # Without limits
    data1.append(dataclass.DataClassNumber(name='n_name1_1', value=value))
    widgettype1.append('FloatWidget')

    # With Limits
    data1.append(dataclass.DataClassNumber(name='n_name1_2', value=value, limits=[-10, 10]))
    widgettype1.append('FloatWidget')

    # Discrete
    data1.append(dataclass.DataClassDiscreteNumber(name='dn_name1_3', value=value, limits=[-2, 10, -2.1,-1.1, 2.3, 20, 39, 49]))
    widgettype1.append('ComboBoxWidget')

    # String
    data1.append(dataclass.DataClassString(name='s_name1_4', value=valuestring))
    widgettype1.append('EditLineWidget')


    data1.append(dataclass.DataClassDiscreteString(name='ds_name1_5', value=valuestring, limits=['-2', '10', '-2.1','-1.1', '2.3', '20', '39', '49', 'pippo', 'papeRino', '@#$&(*&#@$']))
    widgettype1.append('ComboBoxWidget')

    for index, d in enumerate(data1):
        widget1.append(guidatawrapper.GuidataWidget(data1[index].name, widgettype1[index], data1[index]))

    return data1, widgettype1, widget1


def create_widget2(value=-1.1, valuestring='pippo'):
        '''
        Define a v
        :return:
        '''
        # Init list
        data1       = []
        widgettype1 = []
        widget1 = []

        # Without limits
        data1.append(dataclass.DataClassNumber(name='n_name2_1', value=value))
        widgettype1.append('FloatWidget')

        # With Limits
        data1.append(dataclass.DataClassNumber(name='n_name2_2', value=value, limits=[-10, 10]))
        widgettype1.append('FloatWidget')

        # Discrete
        data1.append(dataclass.DataClassDiscreteNumber(name='dn_name2_3', value=value, limits=[-1.1, 0.1, -2.1, 2.3, 3.1, 4.11]))
        widgettype1.append('ComboBoxWidget')

        # Discrete
        data1.append(dataclass.DataClassDiscreteNumber(name='dn_name2_4', value=value, limits=[-2.1,-1.1, 2.3]))
        widgettype1.append('ComboBoxWidget')

        # String
        data1.append(dataclass.DataClassString(name='s_name1_4', value=valuestring))
        widgettype1.append('EditLineWidget')

        data1.append(dataclass.DataClassDiscreteString(name='ds_name1_5', value=valuestring, limits=['-2', '10', '-2.1','-1.1', '2.3', '20', '39', '49', 'pippo', 'papeRino', '@#$&(*&#@$']))
        widgettype1.append('ComboBoxWidget')

        for index, d in enumerate(data1):
            widget1.append(guidatawrapper.GuidataWidget(data1[index].name, widgettype1[index], data1[index]))

        return data1, widgettype1, widget1


def create_widgetStringsOnly1(valuestring = 'come fosse antani'):
        # Init list
    data1       = []
    widgettype1 = []
    widget1     = []

    # String
    data1.append(dataclass.DataClassString(name='s_name1_1', value=valuestring))
    widgettype1.append('EditLineWidget')

    data1.append(dataclass.DataClassDiscreteString(name='ds_name1_1', value=valuestring, limits=['melo', 'puppo','come fosse antani', 'pippo', 'papeRino', '@#$&(*&#@$']))
    widgettype1.append('ComboBoxWidget')

    for index, d in enumerate(data1):
        widget1.append(guidatawrapper.GuidataWidget(data1[index].name, widgettype1[index], data1[index]))

    return data1, widgettype1, widget1

def create_view1(app, viewname='Main view 1'):
    main_view = guidatawrapper.GuidataView(viewname=viewname,  qtapp=app)
    (data1, widgettype1, widget1) = create_widget1(value=10)
    (data2, widgettype2, widget2) = create_widget2(value=2.3)
    main_view.addWidgets(widget1)
    main_view.addWidgets(widget2)
    return  main_view

def create_complex_view(app, viewname='Complex view 1'):
    main_view = guidatawrapper.GuidataView(viewname=viewname,  qtapp=app)
    sub_view1, sub_view2, data1, data2 = create_subview1(app)

    data1, widgettype1, widget1 = create_widget2()
    main_view.addWidgets(widget1)

    main_view.addSubView(sub_view1)
    main_view.addSubView(sub_view2)

    return main_view, data1, data2

def create_subview1(app, viewname1='Subview1' ,viewname2='Subview2'):
    (data1, widgettype1, widget1) = create_widget1(value=10)
    (data2, widgettype2, widget2) = create_widget2(value=2.3)

    # Generate sub view1 with  two further subviews as splitter
    sub_view1 = guidatawrapper.GuidataView(viewname1, qtapp=app, viewtype='Splitter')
    sub_view1_1 = guidatawrapper.GuidataView(viewname=viewname1+'_1',  qtapp=app)
    sub_view1_1.addWidgets(widget2)
    sub_view1_2 = guidatawrapper.GuidataView(viewname=viewname1+'_2',  qtapp=app)
    sub_view1_2.addWidgets(widget2)
    # then add two sub-subviews to subview1
    sub_view1.addSubView(sub_view1_1)
    sub_view1.addSubView(sub_view1_2)

    # Generate sub_view2 with tabs
    sub_view2 = guidatawrapper.GuidataView(viewname=viewname2, viewtype='Tabs', qtapp=app)
    sub_view2_1 = guidatawrapper.GuidataView(viewname=viewname2+'_1',  qtapp=app)
    sub_view2_1.addWidgets(widget2)
    sub_view2_2 = guidatawrapper.GuidataView(viewname=viewname2+'_2',  qtapp=app)
    sub_view2_2.addWidgets(widget2)
     # then add two sub-subviews to subview1
    sub_view2.addSubView(sub_view2_1)
    sub_view2.addSubView(sub_view2_2)

    return sub_view1, sub_view2, data1, data2

def create_complexview_strings_only1(app, viewname='Complex view 1'):
    main_view = guidatawrapper.GuidataView(viewname=viewname,  qtapp=app)

    data1, widgettype1, widget1 = create_widgetStringsOnly1()


    # Generate sub view1 with  two further subviews as splitter
    sub_view1 = guidatawrapper.GuidataView(viewname='Subview1', qtapp=app, viewtype='Splitter')
    sub_view1.addWidgets(widget1)

    # Generate sub_view2 with tabs
    sub_view2 = guidatawrapper.GuidataView(viewname='Subview2', viewtype='Tabs', qtapp=app)
    sub_view2.addWidgets(widget1)


    main_view.addSubView(sub_view1)
    main_view.addSubView(sub_view2)

    return main_view, data1

def closeWindow(win, wait=1.5):
        time.sleep(wait)
        if win is not None:
            win.close()
            del win

def setDataValue(datalist, value, wait=1.5):
        '''
        set a value
        :param wait:
        :param value:
        :return:
        '''
        time.sleep(wait)
        for d in datalist:
            if isinstance(d.value, str):
                d.value = str(value)
            else:
                d.value = value
            # print('viewname='+d.viewname+' = ' +str(d.value))

