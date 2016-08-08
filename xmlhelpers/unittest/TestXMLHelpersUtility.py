__author__ = 'law'

import unittest
import dataclass
from xmlhelpers.XMLHelpersUtility import (UTIL_elementsToProperties, UTIL_propertiesToElements)
import xmlhelpers.unittest.TestXMLClassHelper

class TestXMLHelpersUtility(unittest.TestCase):

    def test_elementsrepresentation(self):
        # Create a valid data test set
        name        = 'ValidName'
        limits      = [0, 2]
        initvalue   = 0
        value       = 2
        desc        = 'Some description'
        data1       = []
        data1.append(dataclass.DataClassDiscreteNumber(name = name+'1', description=desc, value = value,  limits = limits, initvalue= initvalue))
        data1.append( dataclass.DataClassNumber(name = name+'2', description=desc, value = value,  limits = limits, initvalue= initvalue))
        dataElement1_1 =  UTIL_propertiesToElements(data1,  dataclass.XMLDataClassHelper.dataClassTag)

        data1_1 = UTIL_elementsToProperties(dataElement1_1, dataclass.XMLDataClassHelper.dataClassTag)
        #self.assertEqual(data1,data1_1)
        #self.assertEqual(data1,data1_2)
        #self.assertEqual(data1,data1_3)
        self.assertEqual(data1, data1_1)


if __name__ == '__main__':
    unittest.main()
