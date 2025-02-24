# ===================================================================================================
# PAK Utilites and Helpers
# ===================================================================================================
# ===================================================================================================
# Imports: External
# ===================================================================================================
import zipfile
import os
import shutil
from zipfile import ZipFile

# ===================================================================================================
# Imports: Internal
# ===================================================================================================
from ..components.pak import PAKFile

# ===================================================================================================
# Pak Utility/Helper Methods
# ===================================================================================================
def find_paks(target_dir):
    '''
    Performs PAK discovery in the target directory

    :param target_dir: The Target directory to search (Absolute Path)
    :type target_dir: str
    :return: Dictionary of Discovered PAK files and their details
    :rtype: dict
    '''
    paks = {}

    for item in os.listdir(target_dir):
        paks_abs_path = os.path.join(target_dir, item)
        if item.lower().endswith(".pak") and zipfile.is_zipfile(paks_abs_path):
            paks[item] = PAKFile.from_existing(paks_abs_path)

    return paks