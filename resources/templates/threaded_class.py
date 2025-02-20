# ===================================================================================================
# Imports: External
# ===================================================================================================
import time
import os
import zipfile
from threading import Thread
from threading import Event

# ===================================================================================================
# Imports: Internal
# ===================================================================================================

# ===================================================================================================
# Template Threaded Class
# ===================================================================================================
class ThreadTemplate(Thread):
    '''
    Template Thread Class. Use this as a basis for any threaded classes or components within applications
    '''

    # ===================================================================================================
    # Properties
    # ===================================================================================================

    # ===================================================================================================
    # Methods
    # ===================================================================================================
    def __init__(self):
        '''
        constructor
        '''
        self._stop_event = Event()
        super(ThreadTemplate, self).__init__()

    def start_action(self):
        '''
        Start object background action
        '''
        self.start()

    def stop_action(self):
        '''
        Stop object background action
        '''
        self._stop_event.set()

    def run(self):
        '''
        Object Code. Do your thing here.
        :return:
        '''
        while not self._stop_event.is_set():
            time.sleep(0.1)

    # ===================================================================================================
    # Getters
    # ===================================================================================================
    def was_stopped(self):
        '''
        Checks if the Thread was stopped/halted

        :return: True if build was cancelled, otherwise False
        :rtype: bool
        '''
        return self._stop_event.is_set()