# ===================================================================================================
# PAK Utilites and Helpers
# ===================================================================================================
# ===================================================================================================
# Imports: External
# ===================================================================================================
import zipfile
import os
from zipfile import ZipFile

# ===================================================================================================
# Imports: Internal
# ===================================================================================================

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
            paks[item] = {
                "abs_path": paks_abs_path
            }

    return paks

def get_pak_file_list(target_pak):
    '''
    Get a list of files in the PAK at the specified location

    :param target_pak: The absolute path to the target PAK
    :type target_pak: str
    :return: A full list of files in the target PAK
    :rtype list:
    '''
    pak = ZipFile(target_pak)
    return pak.namelist()
