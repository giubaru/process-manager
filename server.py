import os, json
import psutil
import time


class Process():
	def __init__(self, process_name='', file_name='', description='', process_path=''):
		self.id = 0
		self.process_name = process_name
		self.file_name = file_name
		self.description = description
		self.process_path = process_path
		self.pid = None
	
	def run(self):
		relative_path = os.path.join('.',self.process_path, self.file_name)
		ps = psutil.Popen(['python', relative_path])
		self.pid = ps.pid

	def stop(self):
		if self.pid:
			if psutil.pid_exists(self.pid):
				psutil.Process(self.pid).kill()
		self.pid = None

class ProcessManager():
	def __init__(self, process_path='process', persistence_path='bin', persistence_filename='dat'):
		self.PROCESS_PATH = process_path
		self.__PERSISTENCE_FILENAME = persistence_filename
		self.__PERSISTENCE_PATH = persistence_path
		self.__PERSISTENCE_FULLPATH = os.path.join('.', self.__PERSISTENCE_PATH, self.__PERSISTENCE_FILENAME)
		self.__process = []
		self.__running = {}
		self.loadProcesses()

	def save_state(self):
		with open(self.__PERSISTENCE_FULLPATH, 'w') as json_file:
			json_file.write(
					json.dumps([data.__dict__ for data in self.__process])
				)

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
	
	def createProcess(self, process_name, file_name, description, process_path='process'):
		'''Mandar la informacion del obj a un json.'''
		def __checkProcessExists(process):
			for ps in self.__process:
				if ps.__dict__ == process.__dict__:
					return True
			return False
		if process_path == '':
			process_path = self.PROCESS_PATH

		process = Process(
			process_name,
			file_name,
			description,
			process_path
		)

		if not __checkProcessExists(process):
			with open(os.path.join(process_path, file_name), 'w') as process_file:
				process_file.write(f'# Auto-generated process <{process_name}>\nprint("Hello from Auto-generated process!")')
			self.__process.append(process)
		
		self.save_state()

	def removeProcess(self, process_name):	
		process = self.getProcessByName(process_name)
		self.__process.remove(process)
		self.save_state()
		return process.__dict__

	def getProcesses(self):
		return self.__process
	
	def getProcessByName(self, process_name):
		return next((process for process in self.__process if process.process_name == process_name),None)
	
	def runProcess(self, process_name):
		process = self.getProcessByName(process_name)
		if not process:
			return False
		process.run()
		self.save_state()
	
	def stopProcess(self, process_name):
		process = self.getProcessByName(process_name)
		process.stop()
		self.save_state()

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

if __name__ == '__main__':
	print('WARNING: this project is under development and this is not a stable version.')
	print('''\
Commands
	create:		Creates a new process
	run:		Run an existing process
	stop:		Stop a running process		
''')
	pm = ProcessManager()

	try:
		while True:
			action = input('>>> ')
			if action == 'run':
				process_name = input('Process name: ')
				pm.runProcess(process_name)
				print([process.__dict__ for process in pm.getProcesses()]) # Just to test
			elif action == 'create':
				process_name = input('Process name: ')
				pm.createProcess(
					process_name,
					input('Process filename: '),
					input('Description: '),
					input('Process path (default: process/')
				)
				print('Created:',pm.getProcessByName(process_name).__dict__) # Just to test
			elif action == 'status':
				print([process.__dict__ for process in pm.getProcesses()]) # Just to test
			elif action == 'stop':
				process_name = input('Process name: ')
				pm.stopProcess(process_name)
				print([process.__dict__ for process in pm.getProcesses()]) # Just to test
	except KeyboardInterrupt:
		print('See you later!')
		exit()
	