# ===================================================================================================
# Imports: External
# ===================================================================================================
import re

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .pak_asset_types import *

# ===================================================================================================
# PAK Asset Class
# ===================================================================================================
class PAKAsset:
    '''
    PAK Asset. Represents a file within a PAK archive
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, pak, path):
        '''
        Constructor

        :param pak: The PAK File that the Asset belongs to
        :type pak: PAKFile
        :param path: The asset's path within the PAK File
        :type path: str
        '''
        self._pak = pak
        self._path = path
        self._path_sections = []
        self._asset_type = None
        self._filename = None

    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def get_path(self):
        '''
        Gets the Asset's path relative to the PAK File

        :return: The asset's path
        :rtype: str
        '''
        return self._path

    def get_pak(self):
        '''
        Gets the PAKFile that this asset belongs to

        :return: The parent PAKFile, or None of this asset has no parent
        :rtype: PAKFile | None
        '''
        return self._pak

    def get_path_sections(self):
        '''
        Gets the PAK Asset's path split into sections, e.g. test/testing/123 -> ["test", "testing", "123]

        :return: The asset path in sections
        :rtype: list[str]
        '''
        if not self._path_sections:
            self._path_sections = self.get_path().split("/")
        return self._path_sections

    def get_filename(self):
        '''
        Gets the asset's filename

        :return: The asset's filename
        :rtype: str
        '''
        if not self._filename:
            self._filename = self.get_path().split("/")[-1]
        return self._filename

    def get_asset_type(self):
        '''
        Gets the asset's type

        :return: The asset's type
        :rtype: str
        '''

        if not self._asset_type:
            # ===================================================================================================
            # Asset - Material
            # ===================================================================================================
            if self.get_filename().endswith(".mtl"):
                self._asset_type = ASSET_MATERIAL
            # ===================================================================================================
            # Asset - Texture
            # ===================================================================================================
            if not re.match(".*\.dds(\d+)*$", self.get_filename()):
                self._asset_type = ASSET_TEXTURE

        return self._asset_type

    def is_of_type(self, _type):
        '''
        Checks if the asset is of a specific type

        :param _type: The type to check for
        :type _type: str
        :return: True if asset is of the specified type, otherwise false
        :rtype: bool
        '''
        if self.get_asset_type() == _type:
            return True
        return False

