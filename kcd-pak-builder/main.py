# ===================================================================================================
# Imports: KCD PAK Builder
# ===================================================================================================
from kcd_pak_builder import KCDPakBuilder

# ===================================================================================================
# Properties
# ===================================================================================================
VERSION = "1.0.0"
AUTHOR = "Altire"

# ===================================================================================================
# Launch!
# ===================================================================================================
if __name__ == "__main__":
    paker = KCDPakBuilder(VERSION, AUTHOR)
    paker.launch()