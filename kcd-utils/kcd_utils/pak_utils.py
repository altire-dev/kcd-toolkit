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

def get_pak_assets(target_pak):
    '''
    Get a list of assets/files in the PAK at the specified location

    :param target_pak: The absolute path to the target PAK
    :type target_pak: str
    :return: A full list of assets in the target PAK
    :rtype list:
    '''
    pak = ZipFile(target_pak)
    return pak.namelist()

def export_pak_asset(export_path, pak_path, asset_path):
    '''
    Exports an asset from a PAK file

    :param pak_path: The path to the target PAK file
    :type pak_path: str
    :param asset_path: The path to the asset to export
    :type asset_path: str
    '''
    print("Export %s from pak %s" % (asset_path, pak_path))
    asset_filename = asset_path.split("/")[-1]
    out_file = os.path.join(export_path, asset_filename)
    print("Outputing to %s" % out_file)

    # ===================================================================================================
    # Read Asset from PAK
    # ===================================================================================================
    with zipfile.ZipFile(pak_path) as pak_file:
        with pak_file.open(asset_path) as asset_file, open(out_file, 'wb') as out_file:
            shutil.copyfileobj(asset_file, out_file)


