import sys
from lxml import etree
import xmlhelpers.XMLHelpersException
from utilities.misc import UTIL_listProperties

__author__ = 'law'

XMLUTIL_attribute_version = 'version'
XMLUTIL_attribute_module = 'module'


def UTIL_prepareXMLString(rootelement, filename=None, xml_declaration=True, pretty_print=True):
    tree = etree.ElementTree(rootelement)
    if not filename == None:
        tree.write(filename, pretty_print=pretty_print, xml_declaration=xml_declaration)
    xmlstring = etree.tostring(tree, pretty_print=pretty_print, xml_declaration=xml_declaration)

    return xmlstring


def UTIL_propertiesToElements(datalist, tag):
    '''
    Converts the properties from a list of object containing some attributes defined as property
    :param datalist: a single or a list of object
    :param tag: the tag which has to be used to indicate the start and the end of the block
    :return: the root element tree (etree from lxml) representing the list of object
    '''
    rootelement = etree.Element(tag)

    # if the instancetype is passed as a string then it is converted to a proper viewname type

    # Assign a single datalist value  to a list, to be called in a for loop
    datalist = (datalist if type(datalist) is list else  [datalist])
    for d in datalist:
        if d is None:
            raise xmlhelpers.XMLHelpersException.ClassNotSupportedError(None, '')
        try:
            propList = UTIL_listProperties(d)
        except Exception as e:
            raise xmlhelpers.XMLHelpersException.ClassNotSupportedError(d.__class__, 'Get error: ' + str(e))

        rootdataelement = etree.SubElement(rootelement, d.__class__.__name__,
                                           attrib={XMLUTIL_attribute_version: str(d.get_version()),
                                                   XMLUTIL_attribute_module: d.__module__})
        for p in propList:
            # extract the property with viewname in p from datalist
            value = eval('d.' + p)
            # skip if property is none,
            if not value == None:
                valuetype = value.__class__.__name__
                tElement = etree.SubElement(rootdataelement, p, attrib={'type': valuetype})
                tElement.text = ('\'' + value + '\'' if isinstance(value, str) else str(value))
    return rootelement


def UTIL_extract_class_module(class_module):
    # Load the module
    if class_module is None:
        raise xmlhelpers.XMLHelpersException.AttributeNotFound(XMLUTIL_attribute_module)

    __import__(class_module)
    module = sys.modules[class_module]
    return module


def UTIL_extract_version(elem):
    # Retrieve the version, later check
    version = elem.attrib.get(XMLUTIL_attribute_version)
    version = ("" if version == None else version)
    return version


def UTIL_compose_parameters_string(elem):
    params_string = ""
    for p in elem:
        if p.tag is etree.Comment:
            continue
        tyepAttrib = p.attrib.get('type')
        params_string = params_string + ("," if len(params_string) else "")

        if tyepAttrib == None or len(tyepAttrib) == 0:
            raise xmlhelpers.XMLHelpersException.EmptyPrimitiveTypeError()
        if p.text == None:
            raise xmlhelpers.XMLHelpersException.InvalidTextError('None')
        params_string = params_string + p.tag + "=" + tyepAttrib + "(" + p.text + ")"
    return params_string


def UTIL_elementsToProperties(rootelement, tag):
    '''
    From a root element create a list of data
    :param rootelement: the reference to the root element
    :param tag: the tag which contains the data elements
    :param preprendix_argument:
    :return: the instance of the object
    '''

    if not rootelement.tag == tag:
        raise xmlhelpers.XMLHelpersException.InvalidTagError(rootelement.tag, tag)

    # Extract the data
    data = [];
    for e in rootelement:

        # Load the module
        class_module = e.attrib.get("module")

        module = UTIL_extract_class_module(class_module)
        if module is None:
            raise xmlhelpers.XMLHelpersException.InvalidModule(e.tag, class_module)
        # prepare the string to instantiate this item
        class_name = 'module.' + e.tag

        # extract the version
        version = UTIL_extract_version(e)

        params_string = UTIL_compose_parameters_string(e)
        constructorstring = class_name + "(" + params_string + ")"
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


def UTIL_interrogate(self, item):
    """Print useful information about item."""
    if hasattr(item, '__name__'):
        print("NAME:    " + item.__name__)
    if hasattr(item, '__class__'):
        print("CLASS:   " + item.__class__.__name__)
    print("ID:      " + str(id(item)))
    print("TYPE:    " + str(type(item)))
    print("VALUE:   " + str(repr(item)))
    if callable(item):
        iscallable = 'Yes'
    else:
        iscallable = "No"
    print("CALLABLE:" + iscallable)
