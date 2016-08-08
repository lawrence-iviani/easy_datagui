import unittest
import dataclass
from widget import XMLWidgetHelper
from xmlhelpers import XMLHelpersException
from utilities.misc import util_get_valid_path

__author__ = 'law'


class TestWidgetXMLHelpers(unittest.TestCase):
    '''
    Test class for XML Helpers related to Widget
    '''
    _path = util_get_valid_path(['./xmlfiles/', './widget/unittest/xmlfiles/'])

    def test_xml_files(self):
        ## Test single data
        # Create a single data and test it.
        data1 = []
        data1.append(dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1,   initvalue=2, description='My first data'))
        data1.append(dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10],               value = 2.1, initvalue = -1))
        widgettype1 = ['ComboBoxWidget' , 'FloatWidget']
        widget1 = []

        # Open an inexistent file
        filenamewrong = self._path + 'wrongfile.ml'
        with self.assertRaises(OSError): XMLWidgetHelper.XMLFileToWidget(filenamewrong)

        # TODO:  Because to instantiate a file I need a real implementation this should be moved in a GUI implementation like TK

        # for index,d in enumerate(data1):
        #     widget1.append(guidatawrapper.GuidataWidget(d.name, widgettype1[index], d))
        #
        # filename1 = self._path + 'widget_test_creation1.xml'
        # XML1 = XMLWidgetHelper.widgetToXML(widgetelem=widget1,  widgettag='widget', filename=filename1)
        #
        # widget1_1 = XMLWidgetHelper.XMLFileToWidget(filename=filename1,  widgettag='widget')
        # XML1_1 = XMLWidgetHelper.widgetToXML(widgetelem=widget1_1,  widgettag='widget')
        # # Reopen filename1 and verify it
        # self.assertEqual(XML1,XML1_1)
        # self.assertEqual(widget1,widget1_1)
        #
        # ## Compare with reference xml
        # filenameref = self._path + 'widget_test_reference.xml'
        # widgetref   = XMLWidgetHelper.XMLFileToWidget(filenameref)
        # XMLref = XMLWidgetHelper.widgetToXML(widgetelem=widgetref,  widgettag='widget')
        # self.assertEqual(XML1, XMLref)

        # Test a single widget not in a list

        # data2   = dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1,   initvalue=2, description='My first data')
        # widget2 = guidatawrapper.GuidataWidget('Pippo', 'ComboBoxWidget', data2)
        #
        # filename2 = self._path + 'widget_test_creation2.xml'
        # XML2 = XMLWidgetHelper.widgetToXML(widgetelem=widget2,  widgettag='widget', filename=filename2)
        #
        # widget2_1 = XMLWidgetHelper.XMLFileToWidget(filename=filename2, widgettag='widget')
        # XML2_1 = XMLWidgetHelper.widgetToXML(widgetelem=widget2_1,  widgettag='widget')
        # # Reopen filename1 and verify it
        # self.assertEqual(XML2,XML2_1)
        # self.assertEqual(widget2,widget2_1)

    def test_module(self):
        filename1 = self._path + 'widget_test_error_module1.xml'
        with self.assertRaises(ImportError): XMLWidgetHelper.XMLFileToWidget(filename1)

        filename2 = self._path + 'widget_test_error_module2.xml'
        with self.assertRaises(ImportError): XMLWidgetHelper.XMLFileToWidget(filename2)

    def test_xml_version(self):
        # Version test
        # Different version -> Exception
        # no version in XML -> Exception
        # Correct version   -> OK

        pass

        # TODO: remove and put in a proper unit test with some implementation like TK etc.
        # filename1 = self._path + 'widget_no_version.xml'
        # with self.assertRaises(XMLHelpersException.WrongVersionError): XMLWidgetHelper.XMLFileToWidget(filename1)
        #
        # filename2 = self._path + 'widget_wrong_version.xml'
        # with self.assertRaises(XMLHelpersException.WrongVersionError): XMLWidgetHelper.XMLFileToWidget(filename2)
        #
        # filename3 = self._path + 'widget_ok_version.xml'
        # XMLWidgetHelper.XMLFileToWidget(filename3)

    # def test_data(self):
    # # List with alien objects
    #     # List with several data and an empty object
    #     # List with several data and one object
    #     # Empty list
    #
    #
    #     # Test with an alien object
    #     data1 = [];
    #     data1.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
    #     data1.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
    #     data1.append(object)
    #     with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.widgetToXML(data1, modelTag = 'data')
    #
    #     # Test with empty object
    #     data2 = [];
    #     data2.append( dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1, initvalue=2, description='My first data'))
    #     data2.append( dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10], value = 2.1, initvalue = -1))
    #     data2.append(None)
    #     with self.assertRaises(XMLHelpersException.ClassNotSupportedError): XMLDataClassHelper.widgetToXML(data2, modelTag = 'data')
    #
    #     # Test empty list
    #     data3 = [];
    #     emptyxml = XMLDataClassHelper.widgetToXML(data3, modelTag = 'data')
    #
    #     filenameempty = self._path + 'dataclass_emptydata.xml'
    #     emptydata  = XMLDataClassHelper.XMLFileToWidget(filenameempty)
    #     emptyxmlref = XMLDataClassHelper.widgetToXML(data3, modelTag = 'data')
    #
    #     self.assertEqual(emptyxml,emptyxmlref)
    #     self.assertEqual(data3,emptydata)
    #
    # def test_wrong_xml(self):
    #     # Modified XML with errors
    #         # Different properties viewname (e.g. value -> valu)
    #         # wrong values (e.g. limits, viewname not compatible)
    #         # Remove required values from XML (e.g. value)
    #     iderror = 10
    #     expectedException = [XMLHelpersException.ErrorDuringInstantiation , # 1
    #                          XMLHelpersException.ErrorDuringInstantiation,  # 2
    #                          XMLHelpersException.ErrorDuringInstantiation,  # 3
    #                          XMLHelpersException.InvalidTextError,          # 4
    #                          XMLHelpersException.ErrorDuringInstantiation,  # 5
    #                          XMLHelpersException.ErrorDuringInstantiation,  # 6
    #                          XMLHelpersException.ErrorDuringInstantiation,  # 7
    #                          XMLHelpersException.InvalidTagError,           # 8
    #                          XMLHelpersException.InvalidTextError,          # 9
    #                          OSError]
    #
    #     for i in range(1,iderror+1):
    #         filenameerror = self._path + 'dataclass_error' + str(i) + '.xml'
    #        # print(filenameerror)
    #         with self.assertRaises(Exception):
    #             try:
    #                 XMLDataClassHelper.XMLFileToWidget(filenameerror)
    #             except Exception as e:
    #                 if isinstance(e,expectedException[i-1]):
    #                     #print (str(e))
    #                     raise  Exception(str(e))
    #                 else:
    #                     print("Find {0}, expected {1}".format(str(e.__class__),str(expectedException[i-1])))
    #                     import traceback
    #                     traceback.print_exc()
    #
    def test_XMLWidget(self):
        '''
        Test the implementation of XMLClassHelper by DataClass
        :return:
        '''
        # TODO: remove and put in a proper unit test with some implementation like TK etc.

        name = 'ValidName'
        limits = [0 ,  2]
        initvalue = 1
        value  = 1.5
        desc   = 'Some description'
        filename1 = self._path + 'widget_test_creation.xml'
        # classtype = guidatawrapper.GuidataWidget
        #
        # # From a single data create a element tree, xml string and an xml
        # data1 = dataclass.DataClassNumber(name = name,  description=desc, value = value,  limits = limits, initvalue= initvalue)
        # widgettype1 =  'FloatWidget'
        # widget1 = guidatawrapper.GuidataWidget(data1.name, widgettype1, data1)
        #
        # widgetElement1 = widget1.getElementsRepresentation()
        # widget1XML = widget1.getXMLStringRepresentation()
        # widget1.saveToXMLFile(filename1)
        #
        # # Test reload single data
        # widget2 = guidatawrapper.GuidataWidget.loadXMLFileToData( filename=filename1)
        # self.assertEqual(widget1,widget2)
        #
        # # Create from data1XML data3 and compare
        # widget3 = guidatawrapper.GuidataWidget.fromXMLStringRepresentationToData(widget1XML)
        # self.assertEqual(widget1,widget3)
        #
        # widget4 = guidatawrapper.GuidataWidget.fromElementsRepresentationToData( widgetElement1)
        # self.assertEqual(widget1,widget4)

if __name__ == '__main__':
    unittest.main()
