# ===================================================================================================
# Imports: External
# ===================================================================================================
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom

# ===================================================================================================
# Imports: Internal
# ===================================================================================================

# ===================================================================================================
# Mod Manifest Class
# ===================================================================================================
class ModManifest:
    '''
    Mod Manifest
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, id, name, author, version, kcd_version, desc):
        '''
        Constructor
        '''
        self.id             = id
        self.name           = name
        self.author         = author
        self.version        = version
        self.kcd_version    = kcd_version
        self.desc           = desc

    def write_to(self, path):
        '''
        Writes the mod.manifest to the specified Path

        :param path: The path to write the mod.manifest file to
        :type path: str
        '''
        mod_root = ET.Element("kcd_mod")

        # Build Info Section
        section_info = ET.SubElement(mod_root, "info")
        ET.SubElement(section_info, "modid").text = self.id
        ET.SubElement(section_info, "name").text = self.name
        ET.SubElement(section_info, "description").text = self.desc
        ET.SubElement(section_info, "author").text = self.author
        ET.SubElement(section_info, "version").text = self.version
        ET.SubElement(section_info, "created_on").text = datetime.today().strftime("%Y-%m-%d")

        # Build Supports Section
        if self.kcd_version:
            section_supports = ET.SubElement(mod_root, "supports")
            ET.SubElement(section_supports, "kcd_version").text = self.kcd_version

        # Convert to String
        xml_string = ET.tostring(mod_root, encoding="utf-8").decode()
        dom = minidom.parseString(xml_string)
        xml_bytes = dom.toprettyxml(encoding="utf-8", indent="  ")
        xml_output = xml_bytes.decode("utf-8")

        # Write to file
        with open(path, "w") as mm_file:
            mm_file.write(xml_output)




