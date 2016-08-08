from lxml import etree

import dataclass
from xmlhelpers import XMLHelpersException
from xmlhelpers import XMLHelpersUtility

'''
A Collection of functions to manage DataClass as ElementTree, XML import/export
'''

dataClassTag = 'data'

def elementToDataClassProperties(rootelement, datatag=dataClassTag):
    '''
    From a root element create a list of data
    :param rootelement: the reference to the root element
    :param datatag: the tag which contains the data elements
    :return:
    '''
    return XMLHelpersUtility.UTIL_elementsToProperties(rootelement,  datatag)


def dataClassPropertiesToElement(data, datatag=dataClassTag):
    '''
    Converts the properties from a list of data (classes which inherits from DataClass)
    :param data: a single or a list of data
    :param datatag: the tag which has to be used with these data (default is data)
    :return: the root element tree (etree from lxml) representing these data
    '''
    return XMLHelpersUtility.UTIL_propertiesToElements(data,  datatag)

# Convert data from XML string or file to DataClass Properties
def XMLStringToDataClassProperties(xmlstring, datatag=dataClassTag):
    '''
    Convert an xml string rapresentation  to a properties list
    :param xmlstring:
    :param datatag:
    :return:
    '''
    rootelement = etree.fromstring(xmlstring)
    return elementToDataClassProperties(rootelement, datatag)

def XMLFileToDataClassProperties(filename, datatag=dataClassTag):
    '''
    Convert a xml file to a properties list
    :param filename:
    :param datatag:
    :return:
    '''
    tree = etree.parse(filename)
    rootelement = tree.getroot()
    return elementToDataClassProperties(rootelement, datatag)

# Convert DataClass Properties to XML
def dataClassPropertiesToXML(data,  datatag=dataClassTag,  filename=None , xml_declaration = True):
    '''
    an utility to create a  an xml string represantation of a properties list. if filename is specified a file is saved
    at the path and file specified. No test on overwrite, existency etc is performed on filename
    If the XML declaration is needed set xml_declaration = True (default) otherwise set to False
    :param data: the xml tag which contains the data list
    :param datatag:
    :param xml_declaration:
    :param filename:
    :return:
    '''
    rootelement = dataClassPropertiesToElement(data,  datatag)
    return XMLHelpersUtility.UTIL_prepareXMLString(rootelement, filename=filename, xml_declaration=xml_declaration)

