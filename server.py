import os, json
import psutil

class Process():
	def __init__(self, process_name='', file_name='', description='', process_path=''):
		self.id = 0
		self.process_name = process_name
		self.file_name = file_name
		self.description = description
		self.process_path = process_path
		self.pid = None
	
	def run(self):
		relative_path = os.path.join(self.process_path, self.file_name)
		ps = psutil.Popen(['python', relative_path])
		self.pid = ps.pid

class ProcessManager():
	def __init__(self):
		self.PROCESS_PATH = None
		self.BIN_PATH = None
		self.__PERSISTENCE_FILENAME = 'dat'
		self.__PERSISTENCE_PATH = 'bin'
		self.__PERSISTENCE_FULLPATH = os.path.join('.',self.__PERSISTENCE_PATH, self.__PERSISTENCE_FILENAME)
		self.__process = []
		self.__running = {}
		self.setProcessPath()
		self.loadProcesses()

	def setProcessPath(self, path='process'):
		self.PROCESS_PATH = path
	def setBinPath(self, path='bin'):
		self.BIN_PATH = path


	def loadScripts(self):
		# Hay que redefinirlo para que levante de algun pickle. (Levantar solo procesos registrados)
		self.__process = [ps for ps in os.listdir(self.PROCESS_PATH) if ps.endswith('.py')]

	def loadProcesses(self):
		try:
			with open(self.__PERSISTENCE_FULLPATH, 'r') as json_file:
				data = json.loads(json_file.read())

			for obj in data:
				process = Process()
				process.__dict__ = obj
				self.__process.append(process)

		except FileNotFoundError:
			with open(self.__PERSISTENCE_FULLPATH, 'w') as json_file:
				json_file.write('[]')
	
	def createProcess(self, process_name, file_name, description, process_path):
		'''Mandar la informacion del obj a un json.'''
		def __checkProcessExists(process):
			for ps in self.__process:
				if ps.__dict__ == process.__dict__:
					return True
			return False

		process = Process(
			process_name,
			file_name,
			description,
			process_name
		)

		if not __checkProcessExists(process):
			self.__process.append(process)

		with open(self.__PERSISTENCE_FULLPATH, 'w') as json_file:
			json_file.write(
				json.dumps([data.__dict__ for data in self.__process])
			)
		
	
	def getProcesses(self):
		return self.__process
	
	def runProcess(self, process_name):
		process = next(process for process in self.__process if process.process_name == process_name)
		process.run()

	def executeAllProcess(self):
		if len(self.__running) == 0:
			for p in self.__process:
				self.__executeScript(p)
		else:
			print('Some process are running:', self.getRunningProcess())

	def refreshProcessStatus(self):
		keys = [key for key in self.__running.keys()]
		for p in keys:
			pid = self.__running[p]
			if not psutil.pid_exists(pid):
				del self.__running[p]

	def getRunningProcess(self):
		self.refreshProcessStatus()
		return self.__running

	def __getProcessByPID(self, pid):
		return psutil.Process(pid)

	def stopAllRunningProcess(self):
		self.refreshProcessStatus()
		if len(self.__running) > 0:
			for p in self.__running:
				pid = self.__running[p]
				try:
					self.__getProcessByPID(pid).kill()
				except:
					print('Process', pid, "isn't running.")
				else:
					print('Killed:',pid)
		else:
			print('No process running.')

	def __isRunning(self, process_name):
		if process_name in self.__running:
			return True
		else:
			return False

	def __processExists(self, process_name):
		if process_name in self.__process:
			return True
		else:
			return False

	def __executeScript(self, process_name):
		relative_path = os.path.join(self.PROCESS_PATH, process_name)
		ps = psutil.Popen(['python', relative_path])
		self.__running[process_name] = ps.pid

	def executeProcess(self, process_name):
		if not self.__isRunning(process_name) and self.__processExists(process_name):
			self.__executeScript(process_name)
		else:
			print("This process can't be executed because it's running or the process doesn't exists.")

	def stopProcess(self, process_name):
		if self.__isRunning(process_name) and self.__processExists(process_name):
			pid = self.__running.get(process_name)
			self.__getProcessByPID(pid).kill()
		else:
			print("This process can't be executed because it's running or the process doesn't exists.")

pm = ProcessManager()
# pm.createProcess('test-process-10', 'process-test-10.py', 'Testing process 10', 'process')
print(
	pm.getProcesses()
)
#ps_test = pm.getProcesses()[0]
#ps_test.run()
#print(ps_test.pid)

pm.runProcess('test-process-10')

# while True:
	# action = input('prompt: ')
	# if action == 'run':
	# 	process_name = input('Process name: ')
	# 	p.executeProcess(process_name)
	# 	print(p.getRunningProcess())
	# elif action == 'exit':
	# 	p.stopAllRunningProcess()
	# 	exit()
	# elif action == 'status':
	# 	print(p.getRunningProcess())
	# elif action == 'stop':
	# 	process_name = input('Process name: ')
	# 	p.stopProcess(process_name)
	# 	print(p.getRunningProcess())