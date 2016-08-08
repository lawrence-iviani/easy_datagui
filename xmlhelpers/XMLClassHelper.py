__author__ = 'law'

import xmlhelpers.XMLHelpersException

class XMLClassHelper(object):
    '''
    This class is a uniform wrapper for manage ElementTree and XML representation of several class.
     The functions determine the instance of the object and build the relative representation or build the object
     from the relative representation (XML, elementtree)
    '''

    def __init__(self):
        super().__init__()

    def getElementsRepresentation(self):
        ''' An element representation of this class in a string form is returned
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable(self.__class__.__name__)

    def getXMLStringRepresentation(self):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable(self.__class__.__name__)

    def saveToXMLFile(self, filename):
        ''' An XML representation of this class in a string form is returned
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable(self.__class__.__name__)

    @staticmethod
    def loadXMLFileToData( filename):
        '''
        From an XML file, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param filename:
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable('')


    @staticmethod
    def fromXMLStringRepresentationToData(xmlstring):
        '''
        From an XML string representation, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param xmlstring:
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable('')

    @staticmethod
    def fromElementsRepresentationToData(rootelement):
        '''
        From an ElementTree, given an instance (e.g. dataclass.DataClass) the relative object is reconstructed
        :param rootelement:
        :return:
        '''
        raise xmlhelpers.XMLHelpersException.XMLRepresentationNotAvailable('')
