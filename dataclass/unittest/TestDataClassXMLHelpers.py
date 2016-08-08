

import unittest
import dataclass
from dataclass import XMLDataClassHelper
from xmlhelpers import XMLHelpersException
from utilities.misc import util_get_valid_path

__author__ = 'law'


class TestXMLHelpers(unittest.TestCase):
    """
    Test class for XML Helpers related to DataClass
    """
    _path = util_get_valid_path(['./xmlfiles/', './dataclass/unittest/xmlfiles/'])

    def test_xml_files(self):
        ## Test single data
        # Create a single data and test it.
        data1 = dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data')
        filename1 = self._path + 'dataclass_test_creation1.xml'
        XML1 = XMLDataClassHelper.dataClassPropertiesToXML(data1, datatag = 'data',  filename=filename1)

        # Reopen filename1 and verify it
        data1_1  = XMLDataClassHelper.XMLFileToDataClassProperties(filename1)
        XML1_1 = XMLDataClassHelper.dataClassPropertiesToXML(data1_1, datatag = 'data')
        self.assertEqual(XML1,XML1_1)
        self.assertEqual(data1,data1_1)

        ## Test list of  data
        # Create data list. This is the same of reference.xml
        data2 = [];
        data2.append( dataclass.DataClassDiscreteNumber('Pippo',    limits=[1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data2.append( dataclass.DataClassDiscreteNumber('Pluto',    limits=[True, False], value = True, unit='mA'))
        data2.append( dataclass.DataClassNumber(        'Paperino', limits=[-10 , 10], value = 2.1, initvalue=-1))
        data2.append( dataclass.DataClassString(        'Paperoga', maxlength=5, value='2.1', initvalue='-1'))
        data2.append( dataclass.DataClassDiscreteString('QuiQuoQua', limits=['a', 'b', 'ciao'], value='a', initvalue='ciao'))

        # Create the XML and save it
        filename2 = self._path + 'dataclass_test_creation2.xml'
        XML2 = XMLDataClassHelper.dataClassPropertiesToXML(data2, datatag = 'data',  filename=filename2)

        # Open an inexistent file
        filenamewrong = self._path + 'wrongfile.ml'
        with self.assertRaises(OSError): XMLDataClassHelper.XMLFileToDataClassProperties(filenamewrong)

        # Reopen filename2
        data3 = XMLDataClassHelper.XMLFileToDataClassProperties(filename2)
        XML3 = XMLDataClassHelper.dataClassPropertiesToXML(data3, datatag = 'data')

        self.assertEqual(XML2,XML3)
        self.assertEqual(data2,data3)

        ## Compare with reference xml
        filenameref = self._path + 'dataclass_test_ref.xml'
        dataref= XMLDataClassHelper.XMLFileToDataClassProperties(filenameref)
        XMLref = XMLDataClassHelper.dataClassPropertiesToXML(dataref, datatag = 'data')

        self.assertEqual(XML2, XMLref)
        self.assertEqual(data2, dataref)

    def test_xml_version(self):
        # Version test
        # Different version -> Exception
        # no version in XML -> Exception
        # Correct version   -> OK

        filename1 = self._path + 'dataclass_no_version.xml'
        with self.assertRaises(XMLHelpersException.WrongVersionError): XMLDataClassHelper.XMLFileToDataClassProperties(filename1)

        filename2 = self._path + 'dataclass_wrong_version.xml'
        with self.assertRaises(XMLHelpersException.WrongVersionError): XMLDataClassHelper.XMLFileToDataClassProperties(filename2)

        filename3 = self._path + 'dataclass_ok_version.xml'
        XMLDataClassHelper.XMLFileToDataClassProperties(filename3)

    def test_module(self):
        filename1 = self._path + 'dataclass_test_error_module1.xml'
        with self.assertRaises(ImportError): XMLDataClassHelper.XMLFileToDataClassProperties(filename1)

        filename2 = self._path + 'dataclass_test_error_module2.xml'
        with self.assertRaises(ImportError): XMLDataClassHelper.XMLFileToDataClassProperties(filename2)

        filename3 = self._path + 'dataclass_test_error_module3.xml'
        with self.assertRaises(XMLHelpersException.ErrorDuringInstantiation): XMLDataClassHelper.XMLFileToDataClassProperties(filename3)



    def test_data(self):
    # List with alien objects
        # List with several data and an empty object
        # List with several data and one object
        # Empty list


        # Test with an alien object
        data1 = [];
        data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data1.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
        data1.append(object)
        with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.dataClassPropertiesToXML(data1, datatag = 'data')

        # Test with empty object
        data2 = [];
        data2.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data2.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
        data2.append(None)
        with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.dataClassPropertiesToXML(data2, datatag = 'data')

        # Test empty list
        data3 = [];
        emptyxml = XMLDataClassHelper.dataClassPropertiesToXML(data3, datatag = 'data')

        filenameempty = self._path + 'dataclass_emptydata.xml'
        emptydata  = XMLDataClassHelper.XMLFileToDataClassProperties(filenameempty)
        emptyxmlref = XMLDataClassHelper.dataClassPropertiesToXML(data3, datatag = 'data')

        self.assertEqual(emptyxml,emptyxmlref)
        self.assertEqual(data3,emptydata)

    def test_wrong_xml(self):
        # Modified XML with errors
            # Different properties viewname (e.g. value -> valu)
            # wrong values (e.g. limits, viewname not compatible)
            # Remove required values from XML (e.g. value)
        iderror = 11
        expectedException = [XMLHelpersException.ErrorDuringInstantiation , # 1
                             XMLHelpersException.ErrorDuringInstantiation,  # 2
                             XMLHelpersException.ErrorDuringInstantiation,  # 3
                             XMLHelpersException.InvalidTextError,          # 4
                             XMLHelpersException.ErrorDuringInstantiation,  # 5
                             XMLHelpersException.ErrorDuringInstantiation,  # 6
                             XMLHelpersException.ErrorDuringInstantiation,  # 7
                             XMLHelpersException.InvalidTagError,           # 8
                             XMLHelpersException.InvalidTextError,          # 9
                             ImportError,                                   # 10
                             OSError]

        for i in range(1,iderror+1):
            filenameerror = self._path + 'dataclass_error' + str(i) + '.xml'
            with self.assertRaises(Exception):
                try:
                    XMLDataClassHelper.XMLFileToDataClassProperties(filenameerror)
                except Exception as e:
                    if isinstance(e,expectedException[i-1]):
                        #print (str(e))
                        raise Exception(str(e))
                    else:
                        print("Find {0}, expected {1}".format(str(e.__class__),str(expectedException[i-1])))
                        import traceback
                        traceback.print_exc()

    def test_XMLDataClass(self):
        '''
        Test the implementation of XMLClassHelper by DataClass for any possible data class
        Add here your data class
        :return:
        '''

        # From a single data create a element tree, xml string and an xml
        data1 = []
        data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data1.append( dataclass.DataClassDiscreteNumber('Pluto',    limits = [True, False], value = True, unit='mA'))
        data1.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
        data1.append( dataclass.DataClassString(        'Paperoga', maxlength=5, value = '2.1', initvalue = '-1'))
        data1.append( dataclass.DataClassDiscreteString('QuiQuoQua', limits=['a', 'b', 'ciao'], value='a', initvalue='ciao'))
        data1.append( dataclass.DataClassIntNumber     ('ZioPaperone', limits=[-3, 4], value=1, initvalue=0))
        data1.append( dataclass.DataClassDiscreteIntNumber('Etabeta',  limits=[-3, 4, 7 ,1, -2 , 0], value=1, initvalue=0, description='Data class discrete int number'))

        for idx,d in enumerate(data1):
            filename1 = self._path + 'dataclass_test_xmlhelper_'+ d.__class__.__name__ +"_"+ str(idx)+'.xml'
            dataElement1 = d.getElementsRepresentation()
            data1XML = d.getXMLStringRepresentation()
            d.saveToXMLFile(filename1)

            # Test reload single data
            data2 = dataclass.DataClass.loadXMLFileToData(filename1)
            self.assertEqual(d, data2)

            # Create from data1XML data3 and compare
            data3 = dataclass.DataClass.fromXMLStringRepresentationToData(data1XML)
            self.assertEqual(d, data3)

            data4 = dataclass.DataClass.fromElementsRepresentationToData(dataElement1)
            self.assertEqual(d, data4)

if __name__ == '__main__':
    unittest.main()
