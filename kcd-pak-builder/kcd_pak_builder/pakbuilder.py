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

    def __init__(self, gui, pak_path, target_dir):
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
        self._files_processed = []
        super(PakBuilder, self).__init__()

    def start_pak(self):
        self.start()

    def stop_pak(self):
        self._stop_event.set()

    def run(self):

        with zipfile.ZipFile(self._pak_path, 'w', zipfile.ZIP_DEFLATED) as pak_file:
            for file in self._file_list:
                if self._stop_event.is_set():
                    break

                pak_file.write(file, os.path.relpath(file, self._target_dir))
                self._files_processed.append(file)
                self._gui.on_file_processed(file)

        self._gui.on_completion()

    def build_filelist(self):
        '''
        Builds the list of files to process in the target directory
        '''
        for root, dirs, files in os.walk(self._target_dir):
            for file in files:
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