from lxml import etree

import dataclass
from xmlhelpers import XMLHelpersException, XMLHelpersUtility
from widget import XMLWidgetHelper, GenericWidget
import view

import importlib.machinery

#from view.GenericView import GenericView

'''
A Collection of functions to manage Views as ElementTree, XML import/export
'''

viewTag = 'view'
subviewTag = 'subview'
viewPropetiesTag = 'viewproperties'

def elementsToView(rootelement, viewtag=viewTag, subviewtag=subviewTag, viewpropetiestag=viewPropetiesTag, widgettag = XMLWidgetHelper.widgetTag):
    '''
    From a root element create a view
    :param rootelement: the reference to the root element
    :param datatag: the tag which contains the data elements
    :return:
    '''

    # Check if root element is view
    if not rootelement.tag == viewtag:
        raise XMLHelpersException.InvalidTagError(rootelement.tag, viewtag)

    # Check for the viewproperties tag, in order to create a view
    view_instance = None
    widget_instance = None
    subview_elements = []
    for d in rootelement:
        if d.tag == viewpropetiestag:
            view_instance = XMLHelpersUtility.UTIL_elementsToProperties(d,  viewpropetiestag)
            if isinstance(view_instance, list):
                if len(view_instance) > 1:
                    raise XMLHelpersException.ErrorDuringInstantiation(d.__class__.__name__, 'Internal error', 'View Instance must be single')
                view_instance = view_instance[0]
        if d.tag == widgettag:
            widget_instance = d
        if d.tag == subviewtag:
            subview_elements.append(d)

    if view_instance is None and widget_instance is not None:
        raise XMLHelpersException.ErrorDuringInstantiation(d.__class__.__name__, 'Internal error', 'Widget instance without View Instance')
    if view_instance is None:
        return None
    # print(view_instance)
    if widget_instance is not None:
        widgets_instance = XMLWidgetHelper.elementToWdiget(widget_instance,  widgettag)
        view_instance.addWidgets(widgets_instance)

    for sv_e in subview_elements:
        sv = elementsToView(sv_e, viewtag= subviewtag)
        view_instance.addSubView(sv)

    return view_instance

def viewToElements(view_instance, viewtag=viewTag):
    '''
    Converts the View from a view_instance to an elements structure
    :param view_instance: a single view (list is not supported). TODO: this should make sense, think about it
    :param viewtag: the tag which has to be used with these data (default is data)
    :return: the root element tree (etree from lxml) representing these data
    '''
    if type(view_instance) is list:
        if not isinstance(view_instance[0], view.GenericView):
            raise XMLHelpersException.ClassNotSupportedError(view_instance[0].__class__.__name__, view.GenericView)
        if len(view_instance) > 1:
            raise XMLHelpersException.MultipleInstancesAreNotAllowed(view_instance.__class__.__name__, len(view_instance))
        else:
            view_instance = view_instance[0]

    if not isinstance(view_instance, view.GenericView):
        raise XMLHelpersException.ClassNotSupportedError(view_instance.__class__.__name__, view.GenericView)

    # Create the root element and
    root_element = etree.Element(viewtag)#, attrib={'version': view_instance.get_version(), 'module': view_instance.__module__})
    # root_element = etree.Element(viewtag, attrib={'module': view_instance.__module__})

    view_prop = XMLHelpersUtility.UTIL_propertiesToElements(view_instance,  viewPropetiesTag)
    root_element.append(view_prop)

    widget_element = XMLWidgetHelper.widgetToElement(view_instance.getWidgetsList())
    root_element.append(widget_element)

    for sv in view_instance.getSubViewList():
        if not isinstance(sv, view.GenericView):
            raise XMLHelpersException.ClassNotSupportedError(sv.__class__.__name__, view.GenericView)
        # Get the rootElementWidget, if any
        sub_view_element = viewToElements(sv, subviewTag)
        root_element.append(sub_view_element)

    return root_element

# Convert data from XML string or file to DataClass Properties
def XMLStringToView(xmlstring, viewtag = viewTag):
    '''
    Convert an xml string representation  to a view
    :param xmlstring:
    :param datatag:
    :return:
    '''
    rootelement = etree.fromstring(xmlstring)
    return elementsToView(rootelement, viewtag)

def XMLFileToView(filename, viewtag=viewTag):
    '''
    Convert a xml file to a view
    :param filename:
    :param datatag:
    :return:
    '''
    tree = etree.parse(filename)
    rootelement = tree.getroot()
    return elementsToView(rootelement, viewtag)

# Convert DataClass Properties to XML
def viewToXML(view_instance,  viewtag=viewTag,  filename=None , xml_declaration = True):
    '''
    an utility to create a  an xml string representation of a view. if filename is specified a file is saved
    at the path and file specified. No test on overwrite, existency etc is performed on filename
    If the XML declaration is needed set xml_declaration = True (default) otherwise set to False
    :param view: the xml tag which contains the data list
    :param viewtag:
    :param xml_declaration:
    :param filename:
    :return: the string containing the representation
    '''
    rootelement = viewToElements(view_instance, viewtag)
    return XMLHelpersUtility.UTIL_prepareXMLString(rootelement, filename=filename, xml_declaration=xml_declaration)
