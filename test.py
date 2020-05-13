import unittest, os, shutil, time, functools
from contextlib import contextmanager
import server

class TestProcessManager(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TEMP_FOLDER = 'temp-process'
        self.TEMP_BINARY = 'temp-dat-unittest'
        self.TEMP_PROCESS_NAME = 'testcase-test-1'
        self.TEMP_PROCESS_FILENAME = 'process-test-1.py'
        
        self.pm = server.ProcessManager(persistence_filename=self.TEMP_BINARY)

    def test_createProcess(self):
        print('Creando proceso nuevo')
        self.pm.createProcess(
            self.TEMP_PROCESS_NAME, 
            self.TEMP_PROCESS_FILENAME, 
            'Testcase process 1', 
            self.TEMP_FOLDER
        )
        process = self.pm.getProcessByName(self.TEMP_PROCESS_NAME)
        self.assertEqual(self.TEMP_PROCESS_NAME, process.process_name)
    
    def test_getNotExistingProcess(self):
        print('Intentar devolver un proceso que no existe')
        self.assertIsNone(self.pm.getProcessByName('testcase-process-90'))
       
    def test_runExistentProcess(self):
        print('Ejecucion del proceso creado')
        self.pm.runProcess(self.TEMP_PROCESS_NAME)
        process = self.pm.getProcessByName(self.TEMP_PROCESS_NAME)
        time.sleep(1)
        self.assertIsNotNone(process.pid)

    def test_runNotExistentProcess(self):
        print('Intentando ejecutar un proceso inexistente')
        self.assertFalse(self.pm.runProcess('not-exists-901924'))

    def test_stopRunningProcess(self):
        print('Terminar ejecucion de proceso')
        process = self.pm.getProcessByName(self.TEMP_PROCESS_NAME)
        self.assertIsNotNone(process.pid)
        self.pm.stopProcess(self.TEMP_PROCESS_NAME)
        process = self.pm.getProcessByName(self.TEMP_PROCESS_NAME)
        self.assertIsNone(process.pid)


if __name__ == '__main__':
    try:
        os.remove(os.path.join('.','bin','temp-dat-unittest'))
        os.remove(os.path.join('.','temp-process', 'process-test-1.py'))
    except:
        pass
    finally:
        os.mkdir('temp-process')
        unittest.main()
        shutil.rmtree('temp-process')
