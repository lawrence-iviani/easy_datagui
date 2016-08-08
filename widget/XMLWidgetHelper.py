from lxml import etree

from xmlhelpers import XMLHelpersUtility

'''
A Collection of functions to manage a generic widget as ElementTree, XML import/export
'''

widgetTag = 'widget'


def elementToWdiget(rootelement, widgettag=widgetTag):
    '''
    From a root element create a list of data
    :param widgettag:   the tag which contains the widget elements
    :param prependix_widget: the prependix (for example parent widget) which must be added in the underneath constructor
    Introduced becasue some widget need to be initated with the root widget (window, frame etc. ).
    In TKinter you have always the first argument as parent
    :param rootelement: the reference to the root element
    :return:
    '''
    return XMLHelpersUtility.UTIL_elementsToProperties(rootelement,  widgettag)



def widgetToElement(widgetElem,  widgettag=widgetTag):
    '''
    Converts the properties from a list of widget (classes which inherits from DataClass)
    :param widgetElem: a single or a list of widget
    :param classtype: the class type of the widget, the type must inherit from GenericWidget
    :param widgettag: the tag which has to be used with these widget (default is widget)
    :return: the root element tree (etree from lxml) representing these widget
    '''

    return XMLHelpersUtility.UTIL_propertiesToElements(widgetElem, widgettag)


# Convert data from XML string or file to DataClass Properties
def XMLStringToWidget(xmlstring,  widgettag=widgetTag):
    '''
    Convert an xml string rapresentation  to a properties list
    :param xmlstring:
    :param classtype: the class type of the widget, the type must inherit from GenericWidget
    :param widgettag:
    :return:
    '''
    rootelement = etree.fromstring(xmlstring)
    return elementToWdiget(rootelement,  widgettag)


def XMLFileToWidget(filename,  widgettag=widgetTag):
    '''
    Convert a xml file to a properties list
    :param filename:
    :param classtype: the class type of the widget, the type must inherit from GenericWidget
    :param widgettag:
    :return:
    '''

    tree = etree.parse(filename)
    rootelement = tree.getroot()
    return elementToWdiget(rootelement,  widgettag)


# Convert DataClass Properties to XML
def widgetToXML(widgetelem,   widgettag=widgetTag,  filename=None , xml_declaration = True):
    '''
    an utility to create a  an xml string represantation of a properties list. if filename is specified a file is saved
    at the path and file specified. No test on overwrite, existency etc is performed on filename
    If the XML declaration is needed set xml_declaration = True (default) otherwise set to False
    :param widgetelem: the xml tag which contains the widgetelem list
    :param classtype: the class type of the widget, the type must inherit from GenericWidget
    :param widgettag:
    :param xml_declaration:
    :param filename:
    :return:
    '''
    rootelement = widgetToElement(widgetelem,   widgettag)
    return XMLHelpersUtility.UTIL_prepareXMLString(rootelement, filename=filename, xml_declaration=xml_declaration)

