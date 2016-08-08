import threading
import logging
import sys
import xmlhelpers.XMLHelpersUtility
import os

def util_get_valid_path(paths='./'):
    '''
    Check if the path/paths exist and return the string containing the path
    If paths is a list of string check for the first path existing and return a string
    :param paths: a string or a list of strings
    :return return the first instance of an existing path
    '''
    if isinstance(paths, list):
        for path_dir in paths:
            if isinstance(path_dir, str):
                if os.path.isdir(path_dir):
                    return path_dir
    if isinstance(paths, str):
            if os.path.isdir(paths):
                return paths

    return ''

def util_check_is_valid_name(name):
    '''
    Check if the viewname is correct.
    Check if it is a string, length and must not contains space
    :param name:
    :return: true if is a valid viewname, otherwise false and a string explaining the reason
    '''

    if not isinstance(name, str):
        return False, "Name is not a string"

    if len(name) < 1:
        return False, "Name is too short"

    if name.find(' ') > -1:
        return False, "Name contains space"

    if not name.isprintable():
        return False, "Name is not printable"

    return True, ''


def remove_duplicates_from_list(list_to_order):
    if isinstance(list_to_order, list):
        ret_val = []
        for items in list_to_order:
            if items not in ret_val:
                ret_val.append(items)
    else:
        ret_val = list_to_order
    return ret_val


def start_logger_unittest():
    logging.basicConfig(level=logging.DEBUG, \
                        format='%(msecs)d-%(levelname)s-%(module)s::%(funcName)s:%(lineno)s--> %(message)s')


def stop_logging_unittest():
    logging.basicConfig(level=logging.CRITICAL)


class FunctionThread(threading.Thread):
    def __init__(self, func, **kwargs):
        threading.Thread.__init__(self)
        self._func = func
        self._kwargs = kwargs

    def run(self):
        # for key, value in self._kwargs.items():
        #     print("{0} = {1}".format(key, value))
        self._func(**self._kwargs)


def UTIL_listProperties(classType):
    className = classType.__class__
    properties_name = [p for p in dir(className) if isinstance(getattr(className, p), property)]
    return properties_name


def util_get_namespace(instance):
    '''
    From an instance or a string representing the viewname space load and returns the extracted module.
    Furthermore, returns the namespace and the classname as module.
    :param instance:
    :return: The module loaded with a spec object. For convenience returns also a string containing the viewname and the module
    '''

    if isinstance(instance, str):
        instancename = instance
    elif (isinstance(instance,type)) or str(instance)==xmlhelpers.XMLHelpersUtility.XMLUTIL_attribute_module:
        # After
        tstr1 = str(instance).split('\'')
        # I got something like ['<class ', 'dataclass.DataClass.DataClass', '>']
        #print(tstr1)
        # Then I want to clean the last repetition from tstr1, in order to have only
        # something like 'dataclass.DataClass'
        tstr2 = str(tstr1[1]).split('.')
        instancename = '.'.join(tstr2[0:len(tstr2)-1])
        #print(tstr2)
    # elif :
    #     return (None,'','') # this should be implemented
    else:
        return '', ''

    namespacelist = instancename.split('.')
    namespace = ''
    # If the viewname space is not empty add in front
    for n in range(0, len(namespacelist)-1):
        namespace = (namespace + '.' + namespacelist[n] if len(namespace) > 0 else namespacelist[n])
    classname = namespacelist[-1]

    return namespace, classname

def UTIL_importModule(module_implementation):
    # Prepare the widget
    _namespace, _classname = util_get_namespace(module_implementation)
    __import__(_namespace)
    _module = sys.modules[_namespace]

    # module = None must be handled by the caller
    # if _module is None:
    #     raise ImportError( )#  xmlhelpers.XMLHelpersException.InvalidModule(d.tag, class_module)

    return _module,_namespace, _classname