import time
import os
import zipfile
from threading import Thread
from threading import Event
# from .gui import KCDPakerGui

class Paker(Thread):
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
        self._total_files = 0
        self._files_processed = []
        super(Paker, self).__init__()

    def start_pak(self):
        self.start()

    def stop_pak(self):
        self._stop_event.set()

    def run(self):
        # print("Paking to %s " % self._pak_path)
        # print("Target Dir: %s " % self._target_dir)
        self._build_filelist()
        self._gui.pak_pg_bar.SetRange((len(self._file_list)))

        with zipfile.ZipFile(self._pak_path, 'w', zipfile.ZIP_DEFLATED) as pak_file:
            for file in self._file_list:
                if self._stop_event.is_set():
                    break

                pak_file.write(file, os.path.relpath(file, self._target_dir))
                self.__log_processed_file(file)


    def __log_processed_file(self, file):
        self._files_processed.append(file)
        self._gui.pak_pg_bar.SetValue(len(self._files_processed))

        count_processed = len(self._files_processed)
        new_status = "%s of %s (%s%%)" % (
            count_processed,
            self._total_files,
            int((count_processed / self._total_files) * 100)
        )
        self._gui.label_status.SetLabel(new_status)

    def _build_filelist(self):
        for root, dirs, files in os.walk(self._target_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self._file_list.append(file_path)
        self._total_files = len(self._file_list)