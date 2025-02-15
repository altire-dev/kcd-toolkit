# ===================================================================================================
# Imports: KCD Mod Generator
# ===================================================================================================
from kcd_mod_generator import KCDModGenerator

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "1.0.1"
AUTHOR = "Altire"

# ===================================================================================================
# Launch!
# ===================================================================================================
if __name__ == "__main__":
    mi = KCDModGenerator(VERSION, AUTHOR)
    mi.launch()


