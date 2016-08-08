
from lxml import etree
import xmlhelpers
from widget.XMLWidgetHelper import widgetTag
import sys

def elementToTKWdiget(rootelement, widgettag=widgetTag, parent_widget=None):
    '''
    From a root element create a list of data
    :param widgettag:   the tag which contains the widget elements
    :param prependix_widget: the prependix (for example parent widget) which must be added in the underneath constructor
    Introduced becasue some widget need to be initated with the root widget (window, frame etc. ).
    In TKinter you have always the first argument as parent
    :param rootelement: the reference to the root element
    :return:
    '''
    return TKUTIL_elementsToProperties(rootelement,  widgettag, parent_widget)


def XMLFileToTKWidget(filename,  widgettag=widgetTag, parent_widget=None):
    '''
    Convert a xml file to a properties list
    :param filename:
    :param classtype: the class type of the widget, the type must inherit from GenericWidget
    :param widgettag:
    :return:
    '''
    tree = etree.parse(filename)
    rootelement = tree.getroot()
    return elementToTKWdiget(rootelement,  widgettag, parent_widget)


def XMLStringToDataClassProperties(xmlstring, widgettag=widgetTag, parent_widget=None):
    '''
    Convert an xml string rapresentation  to a TK Widget
    :param xmlstring:
    :param widgettag:
    :return:
    '''
    rootelement = etree.fromstring(xmlstring)
    return TKUTIL_elementsToProperties(rootelement, widgettag, parent_widget)


def TKUTIL_elementsToProperties(rootelement, tag, parent_widget=None):
    '''
    From a root element create a list of data
    :param rootelement: the reference to the root element
    :param tag: the tag which contains the data elements
    :param parent_widget: the TK parent widget (frame, window etc.)
    :return: the instance of the object
    '''

    if not rootelement.tag == tag:
        raise xmlhelpers.XMLHelpersException.InvalidTagError(rootelement.tag, tag)

    # Extract the data
    data = []
    for e in rootelement:

        # Load the module
        class_module = e.attrib.get("module")

        module = xmlhelpers.XMLHelpersUtility.UTIL_extract_class_module(class_module)
        if module is None:
            raise xmlhelpers.XMLHelpersException.InvalidModule(e.tag, class_module)
        # prepare the string to instantiate this item
        class_name = 'module.' + e.tag

        # extract the version
        version = xmlhelpers.XMLHelpersUtility.UTIL_extract_version(e)

        params_string = xmlhelpers.XMLHelpersUtility.UTIL_compose_parameters_string(e)
        constructorstring = class_name + "(parent_widget, " + params_string + ")"
        try:
            # print(constructorstring, file=sys.stderr)
            tdata = eval(constructorstring)
        except Exception as e:
            raise xmlhelpers.XMLHelpersException.ErrorDuringInstantiation(class_name, e.__class__.__name__, str(e))

        # Check instance is correct
        if not isinstance(tdata, eval(class_name)):
            raise xmlhelpers.XMLHelpersException.ClassNotSupportedError(
                "Not supported data {}".format(tdata.__class__.__name__))

        # Check version
        if not tdata.get_version() == version:
            raise xmlhelpers.XMLHelpersException.WrongVersionError(tdata.get_version(), version)
        data.append(tdata)

    return data

