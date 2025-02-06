'''
Converts All PNG files in the target directory to DDS

:author: Altire
'''

# ===================================================================================================
# Imports: External
# ===================================================================================================
import os
import sys
import shutil

if len(sys.argv) <= 1:
    raise RuntimeError("Target directory must be specified")

target_path = " ".join(sys.argv[1:])
if not os.path.isdir(target_path):
    raise NotADirectoryError("%s is not a valid directory" % target_path)

out_path = os.path.join(target_path, "dds")
if os.path.exists(out_path):
    print("Deleting %s" % out_path)
    shutil.rmtree(out_path)
os.mkdir(out_path)

for file in os.listdir(target_path):
    path = os.path.join(target_path, file)
    if os.path.isdir(path):
        continue

    file_comps = file.split(".")
    if len(file_comps) < 2 or file_comps[-1].lower() != "png":
        continue

    file_name = ".".join(file_comps[:-1])
    dds_out_path = os.path.join(out_path, file_name + ".dds")

    # Determine Format
    format = "bc3"
    file_name = file_name.lower()
    if file_name.endswith("_g") or file_name.endswith("_s"):    # Emission/Glow Map
        format = "bc1"
    elif file_name.endswith("_m"):  # Glossiness - Mask for Cubemap to mask out metallness
        format = "bc4"
    elif file_name.endswith("_n") or file_name.endswith("_normal"): # Normal
        format = "bc3"

    print("Converting %s to : %s" % (file, dds_out_path))

    command = "nvtt_export %s --format %s --output %s" % (path, format, dds_out_path)
    os.system(command)