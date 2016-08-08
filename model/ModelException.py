__author__ = 'law'


class PropertyAlreadyPresentError(Exception):
    def __init__(self, propertyname):
        super().__init__('Property >{}< it is already present in the model'.format(propertyname))

class PropertyNotPresentError(Exception):
    def __init__(self, propertyname):
        super().__init__('Property >{}< it isn\'t present in the model'.format(propertyname))

class PropertyIsNotCompatible(Exception):
    def __init__(self, datafound, dataexpceted):
        super().__init__('Data type >{}< it isn\'t compatible, it was expected type {}'.format(datafound, dataexpceted ))

class PropertyValueError(Exception):
    def __init__(self, propertyname, value):
        super().__init__('For property >{}< value >{}< it isn\'t admitted'.format(propertyname, value ))

