
import view
import widget
from collections import OrderedDict
from pydispatch import dispatcher
from  xmlhelpers.XMLClassHelper import XMLClassHelper
import view.XMLViewHelper

__author__ = 'law'


class GenericView(XMLClassHelper):
    '''
    Note, this class doesn't manage

    '''
    # Signal emitted by this class
    SIGNAL_VIEWUPDATE = 'ViewUpdate'
    SIGNAL_SUBVIEWUPDATE = 'SubViewUpdate'

    # The version of this class, to preserve compatibility
    _version = '20151123'

    def __init__(self, viewname=''):
        super().__init__()
        self._widgetDictionary  = OrderedDict()
        self._subViewDictionary = OrderedDict()
        self._viewname          = viewname
        self._inhibitSendUpdateViewByWidget = False # a flag to inhibit  a widget to send an update view signal
        # it is useful when an entire view is updated and avoid that every widget send the signal. It is managed in _updatedView
        # and used by

    def show(self):
        '''
        The UI implementation should display, and eventually update,  by reimplementing this method in the proper GUI context
        :return:
        '''
        raise NotImplementedError('show must be implemented in the view implementation')

    def close(self):
        '''
        The UI implementation should close the view by reimplementing this method in the proper GUI context
        :return:
        '''
        raise NotImplementedError('close must be implemented in the view implementation')

    def _updatedView(self):
        '''
        A convenient method to be called when the UI is changed, for example because some parameters are applied
        This method should be considered private
        :return:
        '''

        # this avoid every time a widget is updated a relative update view is also sent
        _prevInhibitSendUpdateViewByWidget = self._inhibitSendUpdateViewByWidget
        self._inhibitSendUpdateViewByWidget = True

        try:
            changedPropertiesDict = self._updatedViewHook()
        except Exception as e:
            self._inhibitSendUpdateViewByWidget =  _prevInhibitSendUpdateViewByWidget
            raise view.ViewInternalError(self, self._viewname, 'Internal View Error: ' + str(e))

        if not isinstance(changedPropertiesDict, dict):
            self._inhibitSendUpdateViewByWidget =  _prevInhibitSendUpdateViewByWidget
            raise view.ViewInternalError(self, self._viewname, 'Changed properties must be a dict, instead found type ' + changedPropertiesDict.__class__.__name__)
        if changedPropertiesDict:
            dispatcher.send(signal=GenericView.SIGNAL_VIEWUPDATE, sender=self, changedPropertiesDict=changedPropertiesDict )#, widgetinstance = None)
        self._inhibitSendUpdateViewByWidget =  _prevInhibitSendUpdateViewByWidget

    def _userWidgetUpdatedHandler(self, sender):
        '''
        Send a signal to notify a widget  has been changed, send a new signal for view and widget has been changed
        :param sender:
        :return:
        '''

        if not isinstance(sender, widget.GenericWidget ):
            raise view.WrongWidgetClass(self, self._viewname, sender, widget.GenericWidget)

        if not self._inhibitSendUpdateViewByWidget:
            changedPropertiesDict = {}
            changedPropertiesDict[sender.name] = sender.get_widget_value()
            dispatcher.send(signal=GenericView.SIGNAL_VIEWUPDATE, sender=self, changedPropertiesDict=changedPropertiesDict)


    def _updatedViewHook(self):
        '''
        The _updatedViewHook function must be implemented in the underlay view implementation
        It must return a dict in the form {propertyName: newValue} which effectively are changer
        :return: A dictionary with the updated value in the form {propertyName: newValue}.
        An empty dictionary if nothing changed
        '''
        raise NotImplementedError('_updatedViewHook must be implemented in the view implementation')

    def isAddable(self, widget_instance):
        """
        Test if a widget is addable, but DOESN'T add the widget
        :param widget_instance:
        :return: true if the widget is compatible and addable otherwise return a tuple with false and an explanation
        """
        """
        :return:
        """
        if not isinstance(widget_instance, widget.GenericWidget):
            # raise view.WrongWidgetClass(iewname, widget_instance, widget.GenericWidget)
            return False, 'Trying to add a widget instance ' + str( widget_instance) + ' but expected was: ' + str(widget.GenericWidget)
        widgetName = widget_instance.name
        if self.isWidgetPresent(widgetName):
            return False, 'Trying to add widget name ' + str( widgetName) + ' which is already present'
        return True, ''

    def addWidget(self, widget_instance):
        '''
        Add a widget in this view.
        :param widget_instance: an object inheriting from GenericWidget
        :return:
        '''
        _isAddable, reason = self.isAddable(widget_instance)
        if not _isAddable:
            raise view.ErrorAddingWidget(self, self._viewname, reason)

        widget_name = widget_instance.name
        self._widgetDictionary[widget_name] = widget_instance
        dispatcher.connect(self._userWidgetUpdatedHandler,
                           signal=widget.GenericWidget.SIGNAL_WIDGETUPDATE,
                           sender=widget_instance)

    def getWidget(self, widgetname):
        return self._widgetDictionary.get(widgetname)

    def getWidgetsList(self):
        return list(self._widgetDictionary.values())

    def getSubView(self, viewname):
        return self._subViewDictionary.get(viewname)

    def getSubViewList(self):
        return self._subViewDictionary.values()

    def _userSubViewUpdateHandler(self, sender, changedPropertiesDict):
        dispatcher.send(GenericView.SIGNAL_VIEWUPDATE, sender=self, widgetinstance=sender, changedPropertiesDict=changedPropertiesDict )

    def addWidgets(self, widgetslist):
        # First test if widgets are addable
        for w in widgetslist:
            _isAddable, reason = self.isAddable(w)
            if not _isAddable:
                raise view.ErrorAddingWidget(self, self._viewname, reason)

        for w in widgetslist:
            self.addWidget(w)

    def isWidgetPresent(self, widgetname):
        return widgetname in self._widgetDictionary.keys()

    def isSubViewPresent(self, viewname):
        return viewname in self._subViewDictionary.keys()

    def getWidgetNamesList(self):
        return list(self._widgetDictionary.keys())

    def getSubViewNamesList(self):
        return list(self._subViewDictionary.keys())

    def getSubViewListByName(self, subview_name):
        sv_list = []
        if self.viewname == subview_name:
            sv_list.append(self)
        for sv in self.getSubViewList():
            _ssv = sv.getSubViewListByName(subview_name)
            if len(_ssv):
                sv_list.extend(_ssv)
        return sv_list

    def addSubView(self, viewinstance):
        if not isinstance(viewinstance, view.GenericView):
            raise view.WrongSubViewClass(self, self._viewname, viewinstance, view.GenericView)
        # avoid to add the same view

        if str(viewinstance) == str(self):
            raise view.SubViewAlreadyPresentError(self, self._viewname, ' cannot add self view as subview  ')
        viewname = viewinstance.viewname
        if not self.isSubViewPresent(viewname):
            self._subViewDictionary[viewname] = viewinstance
        else:
            raise view.SubViewAlreadyPresentError(self, self._viewname, 'SubView ' + viewname + ' is already stored')
        #TODO:  verify if makes sense, furthermore specify the widget, sender etc
        dispatcher.connect(self._userSubViewUpdateHandler, signal=GenericView.SIGNAL_VIEWUPDATE, sender=viewinstance)

    def getViewName(self):
        return self._viewname

    def updateView(self, updatedProprietiesDict):
        pass

    def display(self):
        pass
        # for v in self._subViewDictionary:
        #     v.display()

    def get_version(self):
        return  self._version

    viewname = property(getViewName, doc='The viewname of this view. Readonly')

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            areequals = (self.viewname == other.viewname and
                         self._widgetDictionary == other._widgetDictionary and
                         self._subViewDictionary == other._subViewDictionary
                         )
            return areequals
        # in this case other is a list of length 1
        elif isinstance(other, list) and len(other) == 1:
            areequals = (self.viewname == other[0].viewname and
                         self._widgetDictionary == other[0]._widgetDictionary and
                         self._subViewDictionary == other[0]._subViewDictionary
                        )
            return areequals
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def getElementsRepresentation(self):
        ''' An element representation of this class in a string form is returned
        :return:
        '''
        return view.XMLViewHelper.viewToElements(self)

    def getXMLStringRepresentation(self):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        # return model.XMLModelHelper.modelToXML(self, xml_declaration=False)
        return view.XMLViewHelper.viewToXML(self, xml_declaration=False)

    def saveToXMLFile(self, filename):
        ''' An XML representation of this class in a string form is saved in a file
        Return the string saved
        :return:
        '''
        return view.XMLViewHelper.viewToXML(self, xml_declaration=True, filename=filename)

    @staticmethod
    def loadXMLFileToData(filename):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param filename:
        :return:
        '''
        return view.XMLViewHelper.XMLFileToView(filename)

    @staticmethod
    def fromXMLStringRepresentationToData(xmlstring):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param xmlstring:
        :return:
        '''
        return view.XMLViewHelper.XMLStringToView(xmlstring)

    @staticmethod
    def fromElementsRepresentationToData(rootelement):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param instanceName:
        :param rootelement:
        :return:
        '''
        return view.XMLViewHelper.elementsToView(rootelement)


