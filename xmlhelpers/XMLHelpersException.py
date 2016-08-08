__author__ = 'law'

class XMLRepresentationNotAvailable(Exception):
    '''
    This exception is raised when a proper XML representation is not available in the XML helpers
    '''
    def __init__(self, unsupportedInstance):
        super().__init__('Instance of {0} is unsupported for XML transformation'.format(unsupportedInstance))


class InvalidTagError(Exception):
    '''
    An error in the XML tag is detected, typically some wrong tag or bad  formed tag
    '''
    def __init__(self,tagFound, tagExpected):
        super().__init__('Found tag  {0}, instead of  {1}'.format(tagFound, tagExpected))

class InvalidTextError(Exception):
    '''
    Raised when the text  inside a tag is not properly formed or an error in the representation
    '''
    def __init__(self,text):
        super().__init__('Text found {0} is invalid '.format(text))

class ClassNotSupportedError(Exception):
    '''
    Raised when a class is not supported by the XMLHelper. This happen when the helper function is used with the wrong or
    unsupported class:
    '''
    def __init__(self,instanceFound, instanceExpected):
        super().__init__('Found an instance of {0}, instead of expected instance {1}'.format(instanceFound, instanceExpected))

class WrongVersionError(Exception):
    '''
    The XML representation version is not compatible with the actual implementation
    '''
    def __init__(self,versionFound, versionExpected):
        super().__init__('Found a version  {0}, instead of expected version {1}'.format(versionFound, versionExpected))

class AttributeNotFound(Exception):
    '''
    The XML representation version is not compatible with the actual implementation
    '''
    def __init__(self, attriubuteExpected):
        super().__init__('Attribute  {0} was expected, not found'.format(attriubuteExpected))


class EmptyPrimitiveTypeError(Exception):
    '''
    The primitive type (tag = type) is empty or not valid and cannot be restored, reading an XML file/string
    '''
    def __init__(self):
        super().__init__('Primitive type empty or invalid')

class ErrorDuringInstantiation(Exception):
    '''
    The primitive type is empty and cannot be restored
    '''
    def __init__(self, classinstance, exceptionname, reason):
        super().__init__('Error during instantiation of {0}\n\t'
                         'Exception: {1}\n\t'
                         'Due to   : {2}'.format(classinstance, exceptionname, reason))

class MultipleInstancesAreNotAllowed(Exception):
    def __init__(self, classtype, instanceNumbers):
        super().__init__('{0} must be single, instead found several {1} instances'.format(classtype, instanceNumbers))


class InvalidModule(Exception):
    def __init__(self, module, tag):
        super().__init__('A problem loading module {0}, for tag: {1}'.format(module, tag))