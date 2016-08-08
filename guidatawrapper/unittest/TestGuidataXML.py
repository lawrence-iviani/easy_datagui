

import unittest
import view.XMLViewHelper
import guidatawrapper.unittest.TestGuidataUtility
import xmlhelpers
import view.unittest.TestViewSupportFunctions
from guidata.qt.QtGui import (QApplication)
import guidatawrapper
import widget.XMLWidgetHelper

__author__ = 'law'

class TestGuidataXML(unittest.TestCase):
    '''
    Test class for XML Helpers related to DataClass
    '''
    _path = './guidatawrapper/unittest/xmlfiles/'
    #_path = './xmlfiles/'

    def test_xmlhelper_vidget_functions(self):
        import dataclass

        ## Test single data
        # Create a single data and test it.
        data1 = []
        data1.append(dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1,   initvalue=2, description='My first data'))
        data1.append(dataclass.DataClassNumber(        'Paperino', limits = [-10 , 10],               value = 2.1, initvalue = -1))
        widgettype1 = ['ComboBoxWidget' , 'FloatWidget']
        widget1 = []

        for index,d in enumerate(data1):
            widget1.append(guidatawrapper.GuidataWidget(d.name, widgettype1[index], d))

        filename1 = self._path + 'guidatawidget_test_creation1.xml'
        XML1 = widget.XMLWidgetHelper.widgetToXML(widgetelem=widget1,  widgettag='widget', filename=filename1)

        widget1_1 = widget.XMLWidgetHelper.XMLFileToWidget(filename=filename1,  widgettag='widget')
        XML1_1 = widget.XMLWidgetHelper.widgetToXML(widgetelem=widget1_1,  widgettag='widget')
        # Reopen filename1 and verify it
        self.assertEqual(XML1,XML1_1)
        self.assertEqual(widget1,widget1_1)

        ## Compare with reference xml
        filenameref = self._path + 'guidatawidget_test_creation_ref.xml'
        widgetref   = widget.XMLWidgetHelper.XMLFileToWidget(filenameref)
        XMLref = widget.XMLWidgetHelper.widgetToXML(widgetelem=widgetref,  widgettag='widget')
        self.assertEqual(XML1,XMLref)

        # Open an inexistent file
        filenamewrong = self._path + 'guidatawidget_wrongfile.ml'
        with self.assertRaises(OSError): widget.XMLWidgetHelper.XMLFileToWidget(filenamewrong)


        # Test a single widget not in a list
        data2 = dataclass.DataClassDiscreteNumber('Pippo',    limits = [1,2 ,4 ,1,complex(1,1)], value = 1,   initvalue=2, description='My first data')
        widget2= guidatawrapper.GuidataWidget('Pippo', 'ComboBoxWidget', data2)

        filename2 = self._path + 'guidatawidget_test_creation2.xml'
        XML2 = widget.XMLWidgetHelper.widgetToXML(widgetelem=widget2,  widgettag='widget', filename=filename2)

        widget2_1 = widget.XMLWidgetHelper.XMLFileToWidget(filename=filename2, widgettag='widget')
        XML2_1 = widget.XMLWidgetHelper.widgetToXML(widgetelem=widget2_1,  widgettag='widget')
        # Reopen filename1 and verify it
        self.assertEqual(XML2,XML2_1)
        self.assertEqual(widget2,widget2_1)

    def test_xmlhelper_view_functions(self):
        ## Test single data
        # Create a single data and test it.

        app = QApplication([])

        view1 = guidatawrapper.unittest.TestGuidataUtility.create_view1(app)
        filename1 = self._path + 'guidataview_testhelper_creation1.xml'
        XML1 = view.XMLViewHelper.viewToXML(view1, viewtag='view',  filename=filename1)

        view2, data1, data2 = guidatawrapper.unittest.TestGuidataUtility.create_complex_view(app)
        filename2 = self._path + 'guidatasubview_testhelper_creation2.xml'
        XML2 = view.XMLViewHelper.viewToXML(view2, viewtag='view',  filename=filename2)

        ## Reopen filename1 and verify it
        view1_1  = view.XMLViewHelper.XMLFileToView(filename1)
        XML1_1 = view.XMLViewHelper.viewToXML(view1_1)
        self.assertEqual(XML1,  XML1_1)
        self.assertEqual(view1, view1_1)

        ## Reopen filename1 and verify it
        view2_1  = view.XMLViewHelper.XMLFileToView(filename2)
        XML2_1 = view.XMLViewHelper.viewToXML(view2_1)
        self.assertEqual(XML2,  XML2_1)
        self.assertEqual(view2, view2_1)


        # Test empty view
        view_3 = guidatawrapper.GuidataView()
        emptyxml = view.XMLViewHelper.viewToXML(view_3)

        filenameempty   = self._path + 'guidataview_emptyref.xml'
        empty_view       = view.XMLViewHelper.XMLFileToView(filenameempty)
        emptyxmlref     = view.XMLViewHelper.viewToXML(empty_view)

        self.assertEqual(view_3, empty_view)
        self.assertEqual(emptyxml, emptyxmlref)

    def test_xml_version(self):
        # Version test
        # Different version -> Exception
        # no version in XML -> Exception
        # Correct version   -> OK

        filename1 = self._path + 'guidataview_no_version.xml'
        with self.assertRaises(xmlhelpers.XMLHelpersException.WrongVersionError): view.XMLViewHelper.XMLFileToView(filename1)

        filename2 = self._path + 'guidataview_wrong_version.xml'
        with self.assertRaises(xmlhelpers.XMLHelpersException.WrongVersionError): view.XMLViewHelper.XMLFileToView(filename2)

        filename3 = self._path + 'guidataview_ok_version.xml'
        view.XMLViewHelper.XMLFileToView(filename3)



    def test_XML_View_Class_Functions(self):
        '''
        Test the implementation of XMLClassHelper by DataClass
        :return:
        '''

        app = QApplication([])

        # Define dataset and widget
        filename1 = self._path + 'guidataview_test_creation1.xml'
        view1 = guidatawrapper.unittest.TestGuidataUtility.create_view1(app)
        element_view1 = view1.getElementsRepresentation()
        XML_view1 = view1.getXMLStringRepresentation()
        view1.saveToXMLFile(filename1)

        # Try to reload
        view1_1 = view.GenericView.loadXMLFileToData(filename1)
        element_view1_1 = view1_1.getElementsRepresentation()
        XML_view1_1 = view1_1.getXMLStringRepresentation()
        self.assertEqual(XML_view1, XML_view1_1)
        self.assertEqual(view1, view1_1)

        # Load reference and compare it
        filename_ref = self._path + 'guidataview_test_creation_ref.xml'
        view1_ref = view.GenericView.loadXMLFileToData(filename_ref)
        element_view1_ref = view1_ref.getElementsRepresentation()
        XML_view1_ref = view1_ref.getXMLStringRepresentation()
        self.assertEqual(XML_view1_ref, XML_view1_1)
        self.assertEqual(view1_ref, view1_1)

        # Redo the same with view with several subviews
        filename2 = self._path + 'guidatasubview_test_creation1.xml'
        view2, data1, data2 = guidatawrapper.unittest.TestGuidataUtility.create_complex_view(app)
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
        filename_ref = self._path + 'guidatasubview_test_creation_ref.xml'
        view2_ref = view.GenericView.loadXMLFileToData(filename_ref)
        element_view2_ref = view2_ref.getElementsRepresentation()
        XML_view2_ref = view2_ref.getXMLStringRepresentation()
        self.assertEqual(XML_view2_ref, XML_view2_1)
        self.assertEqual(view2_ref, view2_1)

if __name__ == '__main__':
    unittest.main()
