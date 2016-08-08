__author__ = 'law'

import unittest

import model
import dataclass
from model import XMLModelHelper
from xmlhelpers import XMLHelpersException
from utilities.misc import util_get_valid_path


class TestModelXMLHelpers(unittest.TestCase):
    '''
    Test class for XML Helpers related to DataClass
    '''
    #_path = './model/unittest/xmlfiles/'
    _path = util_get_valid_path(['./xmlfiles/', './model/unittest/xmlfiles/'])

    # TODO: To be tested
    ## 1 - Special cases for exception in elementstomodel and viceversa
    ## Implement old test for wrong model data  etc
    ## COMPARE with dataclass

    def test_xml_files(self):
        ## Test single data
        # Create a single data and test it.
        data1 = dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data')
        model1 = model.DataClassModel(data1)
        filename1 = self._path + 'test_model_creation1.xml'
        XML1 = XMLModelHelper.modelToXML(model1, modeltag = 'model',  filename=filename1)

        data2 = []
        data2.append(dataclass.DataClassNumber('Pippo',  limits = [1,3], value = 1, initvalue=1, description='My  data'))
        model2 = model.DataClassModel(data2)
        filename2 = self._path + 'test_model_creation2.xml'
        XML2 = XMLModelHelper.modelToXML(model2, modeltag = 'model',  filename=filename2)

        data3 = []
        data3.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data3.append( dataclass.DataClassNumber('Pluto',    limits = [1, 2], value = 1, initvalue=2, description='My second data'))
        model3 = model.DataClassModel(data3)
        filename3 = self._path + 'test_model_creation3.xml'
        XML3 = XMLModelHelper.modelToXML(model3, modeltag = 'model',  filename=filename3)

        ## Reopen filename1 and verify it
        model1_1  = XMLModelHelper.XMLFileToDataModel(filename1)
        XML1_1 = XMLModelHelper.modelToXML(model1_1, modeltag = 'model')
        self.assertEqual(XML1,XML1_1)
        self.assertEqual(model1,model1_1)

        ## Reopen filename1 and verify it
        model2_1  = XMLModelHelper.XMLFileToDataModel(filename2)
        XML2_1 = XMLModelHelper.modelToXML(model2_1, modeltag = 'model')
        self.assertEqual(XML2,XML2_1)
        self.assertEqual(model2,model2_1)

        ## Reopen filename3 and verify it
        model3_1  = XMLModelHelper.XMLFileToDataModel(filename3)
        XML3_1 = XMLModelHelper.modelToXML(model3_1, modeltag = 'model')
        self.assertEqual(XML3,XML3_1)
        self.assertEqual(model3,model3_1)

        ## Open an inexistent file
        filenamewrong = self._path + 'wrongfile.ml'
        with self.assertRaises(OSError): XMLModelHelper.XMLFileToDataModel(filenamewrong)

        ## Compare with reference xml
        filenameref = self._path + 'test_model_reference.xml'
        modelref= XMLModelHelper.XMLFileToDataModel(filenameref)
        XMLref = XMLModelHelper.modelToXML(model3, modeltag = 'model')

        self.assertEqual(XML3,XMLref)
        self.assertEqual(model3,modelref)

    def test_xml_version(self):
        # Version test
        # Different version -> Exception
        # no version in XML -> Exception
        # Correct version   -> OK

        filename1 = self._path + 'model_no_version.xml'
        with self.assertRaises(XMLHelpersException.WrongVersionError): XMLModelHelper.XMLFileToDataModel(filename1)

        filename2 = self._path + 'model_wrong_version.xml'
        with self.assertRaises(XMLHelpersException.WrongVersionError): XMLModelHelper.XMLFileToDataModel(filename2)

        filename3 = self._path + 'model_ok_version.xml'
        XMLModelHelper.XMLFileToDataModel(filename3)

    def test_module(self):
        filename1 = self._path + 'model_test_error_module1.xml'
        with self.assertRaises(ImportError): XMLModelHelper.XMLFileToDataModel(filename1)

        filename2 = self._path + 'model_test_error_module2.xml'
        with self.assertRaises(XMLHelpersException.ErrorDuringInstantiation): XMLModelHelper.XMLFileToDataModel(filename2)

        filename3 = self._path + 'model_test_error_module3.xml'
        with self.assertRaises(ImportError): XMLModelHelper.XMLFileToDataModel(filename3)

        filename4 = self._path + 'model_test_error_module4.xml'
        with self.assertRaises(XMLHelpersException.ErrorDuringInstantiation): XMLModelHelper.XMLFileToDataModel(filename4)

    def test_empty(self):
        filename1 = self._path + 'test_model_empty.xml'
        XMLModelHelper.XMLFileToDataModel(filename1)


    def test_data(self):
        # Test, create a model with an alien object
        data1 = []
        data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data1.append( dataclass.DataClassNumber('Pluto',    limits = [1, 2], value = 1, initvalue=2, description='My second data'))

    # List with alien objects
        # List with several data and an empty object
        # List with several data and one object
        # Empty list


        # Test with an alien object
        # data1 = [];
        # data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        # data1.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
        # data1.append(object)
        # with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.widgetToXML(data1, datatag = 'data')
        #
        # # Test with empty object
        # data2 = [];
        # data2.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        # data2.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
        # data2.append(None)
        # with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.widgetToXML(data2, datatag = 'data')
        #
        # # Test empty list
        # data1 = [];
        # emptyxml = XMLDataClassHelper.widgetToXML(data1, datatag = 'data')
        #
        # filenameempty = self._path + 'emptyview.xml'
        # emptydata  = XMLDataClassHelper.XMLFileToWidget(filenameempty)
        # emptyxmlref = XMLDataClassHelper.widgetToXML(data1, datatag = 'data')
        #
        # self.assertEqual(emptyxml,emptyxmlref)
        # self.assertEqual(data1,emptydata)

    def test_wrong_xml(self):
        pass

        # Modified XML with errors
            # Different properties viewname (e.g. value -> valu)
            # wrong values (e.g. limits, viewname not compatible)
            # Remove required values from XML (e.g. value)
        # iderror = 10
        # expectedException = [XMLHelpersException.ErrorDuringInstantiation , # 1
        #                      XMLHelpersException.ErrorDuringInstantiation,  # 2
        #                      XMLHelpersException.ErrorDuringInstantiation,  # 3
        #                      XMLHelpersException.InvalidTextError,          # 4
        #                      XMLHelpersException.ErrorDuringInstantiation,  # 5
        #                      XMLHelpersException.ErrorDuringInstantiation,  # 6
        #                      XMLHelpersException.ErrorDuringInstantiation,  # 7
        #                      XMLHelpersException.InvalidTagError,           # 8
        #                      XMLHelpersException.InvalidTextError,          # 9
        #                      OSError]
        #
        # for i in range(1,iderror+1):
        #     filenameerror = self._path + 'error' + str(i) + '.xml'
        #    # print(filenameerror)
        #     with self.assertRaises(Exception):
        #         try:
        #             XMLDataClassHelper.XMLFileToWidget(filenameerror)
        #         except Exception as e:
        #             if isinstance(e,expectedException[i-1]):
        #                 #print (str(e))
        #                 raise  Exception(str(e))
        #             else:
        #                 print("Find {0}, expected {1}".format(str(e.__class__),str(expectedException[i-1])))
        #                 import traceback
        #                 traceback.print_exc()

    def test_XMLDataClass(self):
        '''
        Test the implementation of XMLClassHelper by DataClass
        :return:
        '''
        # Create boundary condition
        filename1 = self._path + 'model_test_creation.xml'

        # create test
        data1 = []
        data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
        data1.append( dataclass.DataClassNumber('Pluto',    limits = [1, 2], value = 1, initvalue=2, description='My second data'))
        model1 = model.DataClassModel(data1)

        # test get elements
        model1Element = model1.getElementsRepresentation()

        # Test save to xml file
        model1XML = model1.saveToXMLFile(filename1)

        # Reload and verify it
        model2 = model.GenericModel.loadXMLFileToData(model.GenericModel, filename1)
        self.assertEqual(model1, model2)

        # Reuse XML and generate the model, then verify it
        model3 =  model.GenericModel.fromXMLStringRepresentationToData(model.GenericModel, model1XML)
        self.assertEqual(model1, model3)

        # from the element regenerate the model and then compare it
        model4 = model.GenericModel.fromElementsRepresentationToData(model.GenericModel, model1Element)
        self.assertEqual(model1, model4)

if __name__ == '__main__':
    unittest.main()
