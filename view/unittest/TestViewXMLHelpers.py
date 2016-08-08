import unittest
import view.XMLViewHelper
import view.unittest.TestViewSupportFunctions
import xmlhelpers
from utilities.misc import util_get_valid_path

__author__ = 'law'

class TestModelXMLHelpers(unittest.TestCase):
    '''
    Test class for XML Helpers related to DataClass
    '''
    _path = util_get_valid_path(['./xmlfiles/', './view/unittest/xmlfiles/'])

    def test_xml_helper_functions(self):
        ## Test single data
        # Create a single data and test it.

        view1, widget1, widgettype1, widgetname1, data1 = view.unittest.TestViewSupportFunctions.createView1()
        filename1 = self._path + 'test_view_creation1.xml'
        XML1 = view.XMLViewHelper.viewToXML(view1, viewtag='view',  filename=filename1)

        view2, widget2, widgettype2, widgetname2, data2 = view.unittest.TestViewSupportFunctions.createView2()
        filename2 = self._path + 'test_view_creation2.xml'
        XML2 = view.XMLViewHelper.viewToXML(view2, viewtag='view',  filename=filename2)

        view3 = view.unittest.TestViewSupportFunctions.createSubView1()
        filename3 = self._path + 'test_subview_creation3.xml'
        XML3 = view.XMLViewHelper.viewToXML(view3, viewtag='view',  filename=filename3)


        ## Reopen filename1 and verify it
        view1_1  = view.XMLViewHelper.XMLFileToView(filename1)
        XML1_1 = view.XMLViewHelper.viewToXML(view1_1, viewtag='view')
        self.assertEqual(XML1,XML1_1)
        self.assertEqual(view1,view1_1)

        ## Reopen filename1 and verify it
        view2_1  = view.XMLViewHelper.XMLFileToView(filename2)
        XML2_1 = view.XMLViewHelper.viewToXML(view2_1, viewtag='view')
        self.assertEqual(XML2,XML2_1)
        self.assertEqual(view2,view2_1)

        ## Reopen filename3 and verify it
        view3_1  = view.XMLViewHelper.XMLFileToView(filename3)
        XML3_1 = view.XMLViewHelper.viewToXML(view3_1, viewtag='view')
        self.assertEqual(XML3,XML3_1)
        self.assertEqual(view3,view3_1)

        ## Open an inexistent file
        filenamewrong = self._path + 'wrongfile.ml'
        with self.assertRaises(OSError): view.XMLViewHelper.XMLFileToView(filenamewrong)

        ## Compare subview  with reference xml
        filenameref = self._path + 'test_view_creation_ref.xml'
        viewref= view.XMLViewHelper.XMLFileToView(filenameref)
        XMLviewref = view.XMLViewHelper.viewToXML(viewref, viewtag='view')

        self.assertEqual(XML1,XMLviewref)
        self.assertEqual(view1,viewref)

        ## Compare subview  with reference xml
        filenameref = self._path + 'test_subview_creation_ref.xml'
        subviewref= view.XMLViewHelper.XMLFileToView(filenameref)
        XMLsubviewref = view.XMLViewHelper.viewToXML(subviewref, viewtag='view')

        self.assertEqual(XML3,XMLsubviewref)
        self.assertEqual(view3,subviewref)

    def test_xml_version(self):
        # Version test
        # Different version -> Exception
        # no version in XML -> Exception
        # Correct version   -> OK

        filename1 = self._path + 'view_no_version.xml'
        with self.assertRaises(xmlhelpers.XMLHelpersException.WrongVersionError): view.XMLViewHelper.XMLFileToView(filename1)

        filename2 = self._path + 'view_wrong_version.xml'
        with self.assertRaises(xmlhelpers.XMLHelpersException.WrongVersionError): view.XMLViewHelper.XMLFileToView(filename2)

        filename3 = self._path + 'view_ok_version.xml'
        view.XMLViewHelper.XMLFileToView(filename3)

    def test_data(self):
        # Test empty view
        view1 = view.GenericView()
        emptyxml = view.XMLViewHelper.viewToXML(view1)

        filenameempty   = self._path + 'emptyview.xml'
        empty_view       = view.XMLViewHelper.XMLFileToView(filenameempty)
        emptyxmlref     = view.XMLViewHelper.viewToXML(view1)

        self.assertEqual(view1, empty_view)
        self.assertEqual(emptyxml, emptyxmlref)

    def test_module(self):
        filename1 = self._path + 'test_view_module_error1.xml'
        with self.assertRaises(ImportError): view.XMLViewHelper.XMLFileToView(filename1)



        # filename1 = self._path + 'dataclass_test_error_module1.xml'
        # with self.assertRaises(ImportError): XMLDataClassHelper.XMLFileToDataClassProperties(filename1)
        #
        # filename2 = self._path + 'dataclass_test_error_module2.xml'
        # with self.assertRaises(ImportError): XMLDataClassHelper.XMLFileToDataClassProperties(filename2)
        #
        # filename3 = self._path + 'dataclass_test_error_module3.xml'
        # with self.assertRaises(XMLHelpersException.ErrorDuringInstantiation): XMLDataClassHelper.XMLFileToDataClassProperties(filename3)


    # def test_wrong_xml(self):
    #     pass
    #
    #     # Modified XML with errors
    #         # Different properties viewname (e.g. value -> valu)
    #         # wrong values (e.g. limits, viewname not compatible)
    #         # Remove required values from XML (e.g. value)
    #     # iderror = 10
    #     # expectedException = [XMLHelpersException.ErrorDuringInstantiation , # 1
    #     #                      XMLHelpersException.ErrorDuringInstantiation,  # 2
    #     #                      XMLHelpersException.ErrorDuringInstantiation,  # 3
    #     #                      XMLHelpersException.InvalidTextError,          # 4
    #     #                      XMLHelpersException.ErrorDuringInstantiation,  # 5
    #     #                      XMLHelpersException.ErrorDuringInstantiation,  # 6
    #     #                      XMLHelpersException.ErrorDuringInstantiation,  # 7
    #     #                      XMLHelpersException.InvalidTagError,           # 8
    #     #                      XMLHelpersException.InvalidTextError,          # 9
    #     #                      OSError]
    #     #
    #     # for i in range(1,iderror+1):
    #     #     filenameerror = self._path + 'error' + str(i) + '.xml'
    #     #    # print(filenameerror)
    #     #     with self.assertRaises(Exception):
    #     #         try:
    #     #             XMLDataClassHelper.XMLFileToWidget(filenameerror)
    #     #         except Exception as e:
    #     #             if isinstance(e,expectedException[i-1]):
    #     #                 #print (str(e))
    #     #                 raise  Exception(str(e))
    #     #             else:
    #     #                 print("Find {0}, expected {1}".format(str(e.__class__),str(expectedException[i-1])))
    #     #                 import traceback
    #     #                 traceback.print_exc()

    def test_XML_Class_Functions(self):
        '''
        Test the implementation of XMLClassHelper by DataClass
        :return:
        '''
        # Define dataset and widget
        filename1 = self._path + 'test_view_creation1.xml'
        view1, widget1, widgettype1, widgetname1, data1 = view.unittest.TestViewSupportFunctions.createView1()
        element_view1 = view1.getElementsRepresentation()
        XML_view1 = view1.getXMLStringRepresentation()
        view1.saveToXMLFile(filename1)

        # Try to reload
        view1_1 = view.GenericView.loadXMLFileToData( filename1)
        element_view1_1 = view1_1.getElementsRepresentation()
        XML_view1_1 = view1_1.getXMLStringRepresentation()
        self.assertEqual(XML_view1, XML_view1_1)
        self.assertEqual(view1, view1_1)

        # Load reference and compare it
        filename_ref = self._path + 'test_view_creation_ref.xml'
        view1_ref = view.GenericView.loadXMLFileToData(filename_ref)
        element_view1_ref = view1_ref.getElementsRepresentation()
        XML_view1_ref = view1_ref.getXMLStringRepresentation()
        self.assertEqual(XML_view1_ref, XML_view1_1)
        self.assertEqual(view1_ref, view1_1)

        # Redo the same with view with several subviews
        filename2 = self._path + 'test_subview_creation1.xml'
        view2 =  view.unittest.TestViewSupportFunctions.createSubView1()
        XML_view2 = view2.saveToXMLFile(filename2)
        element_view2 = view2.getElementsRepresentation()
        XML_view2 = view2.getXMLStringRepresentation()

        # Try to reload filename2
        view2_1 = view.GenericView.loadXMLFileToData( filename2)
        element_view2_1 = view2_1.getElementsRepresentation()
        XML_view2_1 = view2_1.getXMLStringRepresentation()
        self.assertEqual(XML_view2, XML_view2_1)
        self.assertEqual(view2, view2_1)

        # Load reference and compare it
        filename_ref = self._path + 'test_subview_creation_ref.xml'
        view2_ref = view.GenericView.loadXMLFileToData(filename_ref)
        element_view2_ref = view2_ref.getElementsRepresentation()
        XML_view2_ref = view2_ref.getXMLStringRepresentation()
        self.assertEqual(XML_view2_ref, XML_view2_1)
        self.assertEqual(view2_ref, view2_1)

if __name__ == '__main__':
    unittest.main()
