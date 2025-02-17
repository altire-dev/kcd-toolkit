import time
import os
import zipfile
from threading import Thread
from threading import Event
# from .gui import KCDPakerGui

class PakBuilder(Thread):
    '''
    Paker Thread
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self, gui, pak_path, target_dir, max_size_mb):
        '''
        constructor

        :param gui: The parent GUI
        :type gui: KCDPakerGui
        '''
        self._gui = gui
        self._stop_event = Event()
        self._pak_path = pak_path
        self._target_dir = target_dir
        self._file_list = []
        self._max_size_bytes = int(int(max_size_mb) * 1024 * 1024)
        self._files_processed = []
        self._ignore_nested_paks = False
        super(PakBuilder, self).__init__()

    def start_pak(self):
        self.start()

    def stop_pak(self):
        self._stop_event.set()

    def run(self):
        '''
        PAK Builder Thread Runner
        :return:
        '''
        file_idx = 0
        pak_part_no = 0
        total_files = len(self._file_list)

        # ===================================================================================================
        # Main PAK Builder Loop
        # ===================================================================================================
        while file_idx < total_files and not self._stop_event.is_set():
            # Build PAK Path
            pak_path = self._pak_path
            if pak_part_no > 0:
                pak_path = self._pak_path.replace(".pak", "-part%s.pak" % pak_part_no)

            # Write to PAK
            with zipfile.ZipFile(pak_path, 'w', zipfile.ZIP_DEFLATED) as pak_file:
                pak_size = 0

                for file in self._file_list[file_idx:]:
                    pak_size += os.path.getsize(file)
                    if self._stop_event.is_set():
                        break

                    pak_file.write(file, os.path.relpath(file, self._target_dir))
                    self._files_processed.append(file)
                    self._gui.on_file_processed(file)
                    file_idx += 1

                    # Check if size limit reached
                    if pak_size > self._max_size_bytes:
                        break

            # If breaking because of size, move file and start pak counter
            if pak_size > self._max_size_bytes:
                if pak_part_no == 0:
                    os.replace(pak_path, pak_path.replace(".pak", "-part%s.pak" % pak_part_no))
                pak_part_no += 1

        self._gui.on_completion()

    # ===================================================================================================
    # Alternate Run: Checks file size Constantly. More accurate, but slower to run by a fair amount
    # ===================================================================================================
    # def run(self):
    #     '''
    #     PAK Builder Thread Runner
    #     :return:
    #     '''
    #     file_idx = 0
    #     pak_part_no = 0
    #     total_files = len(self._file_list)
    #     print("Max size: %s" % self._max_size_bytes)
    #
    #     # ===================================================================================================
    #     # Main PAK Builder Loop
    #     # ===================================================================================================
    #     while file_idx < total_files and not self._stop_event.is_set():
    #         # Build PAK Path
    #         pak_path = self._pak_path
    #         if pak_part_no > 0:
    #             pak_path = self._pak_path.replace(".pak", "-part%s.pak" % pak_part_no)
    #
    #         for file in self._file_list[file_idx:]:
    #             if self._stop_event.is_set():
    #                 break
    #
    #             if os.path.isfile(pak_path):
    #                 if os.path.getsize(pak_path) + os.path.getsize(file) >= self._max_size_bytes:
    #                     pak_part_no += 1
    #
    #             with zipfile.ZipFile(pak_path, 'a', zipfile.ZIP_DEFLATED) as pak_file:
    #                 pak_file.write(file, os.path.relpath(file, self._target_dir))
    #                 self._files_processed.append(file)
    #                 self._gui.on_file_processed(file)
    #                 file_idx += 1
    #
    #     self._gui.on_completion()

    def build_filelist(self):
        '''
        Builds the list of files to process in the target directory
        '''
        for root, dirs, files in os.walk(self._target_dir):
            for file in files:
                if self._ignore_nested_paks and file.lower().endswith(".pak"):
                    continue
                file_path = os.path.join(root, file)
                self._file_list.append(file_path)

    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def was_stopped(self):
        '''
        Checks if the PAK builder was cancelled/stopped by the user

        :return: True if build was cancelled, otherwise False
        :rtype: bool
        '''
        return self._stop_event.is_set()

    def get_total_file_count(self):
        '''
        Gets the total count of files found in the target directory

        :return: Total file count in target directory
        :rtype: int
        '''
        return len(self._file_list)

    def get_processed_file_count(self):
        '''
        Gets the count of files that have been processed and written to the PAK

        :return: Count of processed files
        :rtype: int
        '''
        return len(self._files_processed)

    def set_skip_pak_files(self, ignore):
        '''
        Sets whether the Packer should ignore/skip nested PAK files

        :param ignore: Whether to ignore/skip nested .pak files or not
        :type ignore: bool
        '''
        self._ignore_nested_paks = ignore