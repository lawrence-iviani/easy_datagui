__author__ = 'law'

import unittest
import dataclass
from xmlhelpers.XMLClassHelper import XMLClassHelper

class TestXMLClassHelper(unittest.TestCase):

    _path = './xmlhelpers/unittest/xmlfiles/'

    def test_XML_Class_Helper_DataClass(self):
        pass
    #     viewname = 'ValidName'
    #     limits = [0 ,  2]
    #     initvalue = 1
    #     value  = 1.5
    #     desc   = 'Some description'
    #     filename1 = self._path + 'dataclass_test_creation.xml'
    #
    #     # From a single data create a element tree, xml string and an xml
    #     data1 = dataclass.DataClassNumber(viewname = viewname, description=desc, value = value,  limits = limits, initvalue= initvalue)
    #     dataElement1 = data1.getElementsRepresentation()
    #     data1XML = data1.getXMLStringRepresentation()
    #     data1.saveToXMLFile(filename1)
    #
    #     # Test reload single data
    #     data2 = XMLClassHelper.loadXMLFileToData(dataclass.DataClass, filename1)
    #     self.assertEqual(data1,data2)
    #
    #     # Create from data1XML data3 and compare
    #     data3 = XMLClassHelper.fromXMLStringRepresentationToData(dataclass.DataClass,data1XML)
    #     self.assertEqual(data1,data3)
    #
    #     data4 = XMLClassHelper.fromElementsRepresentationToData(dataclass.DataClass,dataElement1)
    #     self.assertEqual(data1,data4)

if __name__ == '__main__':
    unittest.main()
