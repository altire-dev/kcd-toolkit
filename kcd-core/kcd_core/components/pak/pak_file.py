# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import shutil
from zipfile import ZipFile

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from .pak_asset import PAKAsset
from ...exceptions import *

# ===================================================================================================
# PAK File Class
# ===================================================================================================
class PAKFile:
    '''
    KCD2 PAK File Instance
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================
    PAK_EXTENSION = ".pak"

    # ===================================================================================================
    # Static Methods
    # ===================================================================================================
    @staticmethod
    def from_existing(path):
        '''
        Factory method to build a PAK instance from an existing PAK file

        :param path: Absolute path to the PAK file to load
        :type path: str
        :return: New PAKFile instance
        :rtype: PAKFile
        '''
        if not os.path.isfile(path):
            raise FileNotFoundError("No PAK file found at the specified path: %s" % path)
        if not path.lower().endswith(".pak"):
            raise InvalidPAKExtension()

        pak = PAKFile()
        pak.set_path(path)
        return pak

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self):
        '''
        Constructor
        '''
        self._path = None
        self._name = None
        self._assets = []

    def export_asset(self, asset, target_dir):
        '''
        Exports the specified PAK Asset to the target directory

        :param asset: The PAKAsset to export
        :type asset: PAKAsset
        :param target_dir: The target directory to export the PAKAsset to
        :type target_dir: str
        '''
        dest = os.path.join(target_dir, asset.get_filename())
        with ZipFile(self.get_path()) as pak_file:
            with pak_file.open(asset.get_path()) as asset_file, open(dest, 'wb') as out_file:
                shutil.copyfileobj(asset_file, out_file)



    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def get_path(self):
        '''
        Gets the PAK File's path

        :return: The PAK File's path
        :rtype: str
        '''
        return self. _path

    def get_name(self):
        '''
        Gets the PAK's name

        :return: The PAK name
        :rtype: str
        '''
        return self._name

    def get_assets(self):
        '''
        Gets all assets in the PAK File

        :return: List of all PAKFile Assets
        :rtype: list[PAKAsset]
        '''
        if not self._assets:
            pak = ZipFile(self.get_path())
            for asset_path in pak.namelist():
                self._assets.append(PAKAsset(self, asset_path))

        return self._assets

    def get_asset_by_path(self, path):
        '''
        Gets a PAKAsset from this PAKFile using a specified asset path

        :return: The corresponding PAKAsset if this PAKFile has an asset that matches the path, otherwise None
        :rtype: PAKAsset | None
        '''
        match = None
        for asset in self.get_assets():
            if asset.get_path() == path:
                match = asset
                break
        return match


    # ===================================================================================================
    # Setters
    # ===================================================================================================
    def set_path(self, path):
        '''
        Sets the PAK's file path

        :param path: The path to use
        :type path: str
        '''
        path_components = os.path.split(path)
        filename = path_components[-1]
        if not filename.lower().endswith(self.PAK_EXTENSION):
            raise InvalidPAKExtension()

        self._path = path
        self._name = filename