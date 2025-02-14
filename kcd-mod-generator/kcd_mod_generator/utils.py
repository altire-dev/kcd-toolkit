# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import psutil
import subprocess

# ===================================================================================================
# Imports: Internal
# ===================================================================================================

# ===================================================================================================
# Utility/Helper Functions
# ===================================================================================================
def find_kcd2_path():
    '''
    Searches the local system for the KCD2 installation path

    :return: The KCD2 installation path, if found, otherwise None
    :rtype: str
    '''
    path = None
    kcd2_rel_path = os.path.join("steamapps", "common", "KingdomComeDeliverance2")

    for disk in psutil.disk_partitions():
        kcd2_abs_path = None
        if disk.mountpoint == "C:\\":
            kcd2_abs_path = os.path.join(disk.mountpoint, "Program Files (x86)", "Steam", kcd2_rel_path)
        else:
            kcd2_abs_path = os.path.join(disk.mountpoint, "SteamLibrary", kcd2_rel_path)

        if os.path.isdir(kcd2_abs_path):
            path = kcd2_abs_path
            break

    return path

def open_explorer_path(path):
    '''
    Opens Windows Explorer at the specified path

    :param path: The target path
    :type path: str
    '''
    cmd = 'explorer "%s"' % path
    subprocess.Popen(cmd)
