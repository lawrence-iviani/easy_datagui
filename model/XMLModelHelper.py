from lxml import etree

import dataclass
import utilities.misc
from model import DataClassModel
from xmlhelpers import XMLHelpersUtility, XMLHelpersException
import sys

'''
A Collection of functions to manage Models as ElementTree, XML import/export
'''

modelTag = 'model'

def elementsToModel(rootelement, modeltag=modelTag):
    '''
    From a root element create a list of data
    :param rootelement: the reference to the root element
    :param datatag: the tag which contains the data elements
    :return:
    '''

    # Check if root element is model
    if not rootelement.tag == modeltag:
        raise XMLHelpersException.InvalidTagError(rootelement.tag, modeltag)

    # Load the module
    class_module = rootelement.attrib.get(XMLHelpersUtility.XMLUTIL_attribute_module)
    if class_module is None:
            raise XMLHelpersException.InvalidModule('UNKNOWN', class_module)
    namespace, classname = utilities.misc.util_get_namespace(class_module)
    __import__(class_module)
    module = sys.modules[class_module]
    if module is None:
            raise XMLHelpersException.InvalidModule(classname, class_module)

    construction_string = classname + '()'
    try:
        model = eval(construction_string)
    except Exception as e:
        raise XMLHelpersException.ErrorDuringInstantiation(rootelement.tag, e.__class__.__name__, str(e))

    if len(rootelement) > 1:
        raise XMLHelpersException.MultipleInstancesAreNotAllowed(model.__class__.__name__, len(rootelement))
    if not rootelement.attrib.get(XMLHelpersUtility.XMLUTIL_attribute_version) == model.get_version():
        raise XMLHelpersException.WrongVersionError(model.get_version(), rootelement.attrib.get(XMLHelpersUtility.XMLUTIL_attribute_version))



    # Then check if there is only one children called data
    datalist = rootelement.getchildren()
    if len(datalist) > 1:
        raise XMLHelpersException.MultipleInstancesAreNotAllowed(dataclass.DataClass, len(datalist))

    # Convert the list in a signle object value
    data = datalist[0]
    if not data.tag == dataclass.XMLDataClassHelper.dataClassTag:
        raise XMLHelpersException.InvalidTagError(rootelement.tag, modeltag)

    datalist = dataclass.XMLDataClassHelper.elementToDataClassProperties(data)
    model.addProperties(datalist)

    return model

def modelToElements(model, modeltag=modelTag):
    '''
    Converts the DataClass from a model
    :param data: a single or a list of data
    :param datatag: the tag which has to be used with these data (default is data)
    :param version: if you want to add  version to data used
    :return: the root element tree (etree from lxml) representing these data
    '''

    if type(model) is list:
        if not isinstance(model[0], DataClassModel):
            raise XMLHelpersException.ClassNotSupportedError(model[0].__class__.__name__, DataClassModel)
        if len(model) > 1:
            raise XMLHelpersException.MultipleInstancesAreNotAllowed(model.__class__.__name__, len(model))
        else:
            model = model[0]

    if not isinstance(model, DataClassModel):
        raise XMLHelpersException.ClassNotSupportedError(model.__class__.__name__, DataClassModel)

    rootelement = etree.Element(modeltag, attrib={XMLHelpersUtility.XMLUTIL_attribute_version: str(model.get_version()),
                                                  XMLHelpersUtility.XMLUTIL_attribute_module  : model.__module__})
    dataList = []
    for p in model.getPropertiesName():
        dataList.append(model.getProperty(p))

    dataElement = dataclass.XMLDataClassHelper.dataClassPropertiesToElement(dataList)
    rootelement.append(dataElement)

    return rootelement

# Convert data from XML string or file to DataClass Properties
def XMLStringToModel(xmlstring, modeltag = modelTag):
    '''
    Convert an xml string representation  to a model
    :param xmlstring:
    :param datatag:
    :return:
    '''
    rootelement = etree.fromstring(xmlstring)
    return elementsToModel(rootelement, modeltag)

def XMLFileToDataModel(filename, modeltag=modelTag):
    '''
    Convert a xml file to a model
    :param filename:
    :param datatag:
    :return:
    '''
    tree = etree.parse(filename)
    rootelement = tree.getroot()
    return elementsToModel(rootelement, modeltag)

# Convert DataClass Properties to XML
def modelToXML(model,  modeltag=modelTag,  filename=None , xml_declaration = True):
    '''
    an utility to create a  an xml string representation of a model. if filename is specified a file is saved
    at the path and file specified. No test on overwrite, existency etc is performed on filename
    If the XML declaration is needed set xml_declaration = True (default) otherwise set to False
    :param model: the xml tag which contains the data list
    :param modeltag:
    :param xml_declaration:
    :param filename:
    :return: the string containing the representation
    '''

    rootelement = modelToElements(model,  modeltag)
    return XMLHelpersUtility.UTIL_prepareXMLString(rootelement, filename=filename, xml_declaration=xml_declaration)
