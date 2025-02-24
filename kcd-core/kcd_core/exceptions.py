# ===================================================================================================
# KCD2 Core Exception Library
# ===================================================================================================

# ===================================================================================================
# Invalids PAK File Exception
# ===================================================================================================
class InvalidPAKFile(Exception):
    '''
    Raised when an invalid PAK file is encountered
    '''

    def __init__(self, path):
        '''
        Constructor

        :param path: The PAK file's Park
        :type path: str
        '''
        msg = "Invalid PAK file '%s'" % path
        super(InvalidPAKFile, self).__init__(msg)


# ===================================================================================================
# Invalids PAK Extension Exception
# ===================================================================================================
class InvalidPAKExtension(Exception):
    '''
    Raised when an invalid extension is encountered or specified for a PAK File
    '''

    def __init__(self):
        '''
        Constructor
        '''
        msg = "Invalid Extension for PAK File"
        super(InvalidPAKExtension, self).__init__(msg)