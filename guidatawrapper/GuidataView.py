
import view
import widget
from guidatawrapper.GuidataWidget import GuidataWidget
from guidata.dataset.qtwidgets import DataSetShowGroupBox, DataSetEditGroupBox
from guidata.qt.QtGui import (QApplication,QMainWindow, QSplitter, QFrame, QVBoxLayout, QHBoxLayout, QTabWidget)
from guidata.dataset.datatypes import (DataSet)
from collections import OrderedDict
import logging

__author__ = 'law'


class GuidataView(view.GenericView):
    _CONST_Views = ['Splitter', 'Tabs', 'Standard']

    def __init__(self, viewname = '', viewtype ='Standard', qtapp=None):
        super().__init__(viewname)
        self._app = qtapp
        self._frame = None
        self._parentFrame = None
        self._viewtype = viewtype
        self._groupbox = None
        self._previousValues = OrderedDict()

    def getViewType(self):
        return self._viewtype

    viewtype = property(getViewType, doc='The view type, see _CONST_Views for available views. Readonly')

    def setParentView(self, parentview):
        '''
        Set the parent widget associated to this view (GenericView)
        :param parentview:
        :return:
        '''
        if self._parentFrame is not None:
            raise view.ViewInternalError(self, self._viewname, 'Parent was already set')
        # self._parentFrame = parentview.getViewContainer()
        self._parentFrame = parentview

    def show(self):
        # QT Stuff
        if self._app is None:
            self._app = QApplication([])
        if self._parentFrame is None:
            self._parentFrame = QMainWindow()

        # self._parentFrame.setWindowIcon(get_icon('python.png'))
        self._parentFrame.setWindowTitle(self.viewname)

         # Add the frame to this frame
        self._parentFrame.setCentralWidget(self.getFrame())
        self._parentFrame.setContentsMargins(10, 5, 10, 5)

        self._parentFrame.show()
        self._forceRefreshFromWidgets()
        self._previousValues = self._dumpValues()

    def close(self, closeapp=False):
        '''
        Implement the close view in the GerericView class, furthermore  close the QT application which this view belongs
        :param closeapp:
        :return:
        '''
        if self._parentFrame is not None:
            self._parentFrame.close()
            del self._parentFrame
        if self._app is not None and closeapp:
            del self._app

    def getFrame(self):
        '''
        Return the frame containing the presentation, check if the frame was created, otherwise it is created
        :return:
        '''
        if self._frame is None:
            self._generateFrame()
        return self._frame

    def _generateFrame(self):
        '''
        Return the frame containing the presentation, check if the frame was created, otherwise it is created
        :return:
        '''
        # generate the frame if necessary
        if self._frame is None:
            # Generate frame and define the layout based on the frame
            self._frame = QFrame(self._parentFrame)
            _layout = QVBoxLayout()
            self._frame.setLayout(_layout)

            # Add the "Main" group box for this view, if present. It is rendered in foreground
            if self._generateGroupBox() is not None:
                _layout.addWidget(self._groupbox)
            else:
                self._frame.setFrameStyle(QFrame.Panel|QFrame.Raised)
                self._frame.setLineWidth(1)

            # Add to layout eventually the other subview
            if self._viewtype == 'Tabs':
                _tabs = QTabWidget()
                _layout.addWidget(_tabs)
            elif self._viewtype == 'Splitter':
                _splitter =QSplitter()
                _layout.addWidget(_splitter)
            else:
                _sub_frame = QFrame()
                _sub_frame_layout = QHBoxLayout()
                _sub_frame.setLayout(_sub_frame_layout)
                _layout.addWidget(_sub_frame)

            # Add all the sub view as sub frames in the layout
            for sw in self._subViewDictionary.values():
                sw.setParentView(self._frame)
                if self._viewtype == 'Tabs':
                    _tabs.addTab(sw.getFrame(), sw.viewname)
                elif self._viewtype == 'Splitter':
                    _splitter.addWidget(sw.getFrame())
                else:
                    _sub_frame_layout.addWidget(sw.getFrame())

        return self._frame

    def _generateGroupBox(self):
        '''
        Generate if necessary the group box for this
        :return:
        '''
        if self._groupbox is None:
            # from  widgets create the view containing the datasets
            _dataSetView = self._generateGuidataDataset()
            if len(_dataSetView._items) > 0:
                if self._viewtype == 'Tabs':
                    self._groupbox = DataSetEditGroupBox(self.viewname, _dataSetView, comment='')
                else:
                    self._groupbox = DataSetEditGroupBox(self.viewname, _dataSetView, comment='')
                self._groupbox.SIG_APPLY_BUTTON_CLICKED.connect(self._updatedView)

        return self._groupbox

    def getViewContainer(self):
        '''
        This method must be reimplemented returning the proper window/frame etc.. It is based on the GUI implementation
        :return: a reference to the window container
        '''
        return self._parentFrame

    def getQTApp(self):
        '''
        Return the associated QT application, which is mandatory for guidata framework
        :return:
        '''
        return self._app

    def addWidget(self, widgetinstance):
        if not isinstance(widgetinstance, GuidataWidget):
            raise view.WrongWidgetClass(self, self._viewname, widgetinstance, GuidataWidget)
        super().addWidget(widgetinstance)

    def _dumpValues(self):
        widgetvalue = OrderedDict()

        for n, w in self._widgetDictionary.items():
            # I need to store the widget value and NOT the value returned (for example in a combo box I need to store
            # the index, not the value
            # widgetvalue[n] = w.getWidgetValue()
            widgetvalue[n] = GuidataWidget.convertValueToWidgetValue(w, w.getWidgetValue())

        return widgetvalue

    def _updatedViewHook(self):
        # En Widget ' + str(wtry point for a change...

        differences = {}
        differencesConverted = {}
        self._groupbox.get()
        dataset = self._groupbox.dataset

        for n, w in self._widgetDictionary.items():
            # if nameProp in  vars(dataset):
            # TODO: workaround,  the mechanism in the guidata framework is not very well documented.
            # TODO: then in order to get the proper value this is collected through the groupbox insteadm the value.
            # So i check in dataset every nameprop
            nameProp = w.name
            actualValue = getattr(dataset, nameProp) #, w.getWidgetValue())
            prevValue   = self._previousValues.get(n)
            logging.debug('--widgetname=' + w.name)

            if not (prevValue == actualValue):
                differences[n] = actualValue
                differencesConverted[n] = GuidataWidget.convertWidgetValueToValue(w, actualValue)
                #w._setWidgetValueHook(actualValue)
                logging.debug('  DIFFERENCE viewname={0}  prevvalue={1} - newvalue={2}'.format(n, prevValue, actualValue))
                logging.debug('  DIFFERENCE CONVERTED viewname={0}  prevvalue={1} - newvalue={2}'.format
                              (n, GuidataWidget.convertWidgetValueToValue(w, prevValue), differencesConverted[n]))
            else:
                logging.debug('  NO DIFFERENCE viewname={0}  prevvalue={1} - newvalue={2}'.format(n, prevValue, actualValue))

        if len(differences):
            self._forceRefreshToWidgets(differences)
            self._previousValues = self._dumpValues()
        return differencesConverted

    def _forceRefreshToWidgets(self, widget_to_set):
        '''
        A refresh to update the widget with the values stored in the groupbox associated
        This is a workaround relative to the guidata framework. (should be improved)
        :return:
        '''
        if self._groupbox == None:
            return

        #for key, w in self._widgetDictionary.items():
        for wname, valuetoconvert in widget_to_set.items():
            w = self.getWidget(wname)
            if w is None:
                raise RuntimeError('Widget cannot\'t be None')

            # TODO: this is horrible, but need a workaround for guidata to get the value from data set and force it in the GUI
            #valuetoconvert = getattr(self._groupbox.dataset, wname)
            converteddataset = GuidataWidget.convertWidgetValueToValue(w, valuetoconvert)
            logging.debug('For widget['+wname+'] Converted value from '+str(valuetoconvert)+' to ' + str(converteddataset))

            w.setWidgetValue(converteddataset) # Convertire from index to value
            logging.debug('\tValue set is '+str(w.getWidgetValue()))

    def _forceRefreshFromWidgets(self):
        '''
        A refresh to update the whole groupbox with the proper value associated in the widget
        A workaround in the bad documented guidata in order to  force the refresh from the data stored in the widget
        :return:
        '''
        if self._groupbox == None:
            return

        for key, w in self._widgetDictionary.items():
            value = w.getWidgetValue()
            valueconverted = w._getGuidataWidgetValue()
            logging.debug('For widget ['+key+'] Converted value from '+str(value)+' to ' + str(valueconverted))
            setattr(self._groupbox.dataset, key, valueconverted)
            logging.debug('\tRead back value  '+str(getattr(self._groupbox.dataset, key)))

        #PROBLEM IN GET!!! se faccio la get nelle combo box setto il valore del ITEM id e non del valore vero
        # in prarice il setattr dovrebbe settare l'ITEM ID per le combo box
        self._groupbox.get()

    def _userWidgetUpdatedHandler(self, sender):
        # WORKAROUND: the guidata need to be forced to update  the UI if the underlay widget is changed
        if not isinstance(sender, widget.GenericWidget):
            raise view.WrongWidgetClass(self,self.viewname, sender, widget.GenericWidget)
        self._forceRefreshFromWidgets()

        super()._userWidgetUpdatedHandler(sender)

    def _generateGuidataDataset(self):
        class DataSetView(DataSet):
            key = None
            value = None
            for key, value in self._widgetDictionary.items():
                locals()[key] = value.getDataSet()
            del key, value
        return DataSetView
