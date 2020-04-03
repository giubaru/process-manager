import os
import psutil

class Server():
	def __init__(self):
		self.PROCESS_PATH = 'process'
		self.__process = []
		self.__running = {}
		self.getProcessScripts()

	def getProcessScripts(self):
		self.__process = [ps for ps in os.listdir(self.PROCESS_PATH) if ps.endswith('.py')]

	def executeAllProcess(self):
		if len(self.__running) == 0:
			for p in self.__process:
				self.__executeScript(p)
		else:
			print('Some process are running:',self.getRunningProcess())

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

p = Server()

while True:
	action = input('prompt: ')
	if action == 'run':
		process_name = input('Process name: ')
		p.executeProcess(process_name)
		print(p.getRunningProcess())
	elif action == 'exit':
		p.stopAllRunningProcess()
		exit()
	elif action == 'status':
		print(p.getRunningProcess())
	elif action == 'stop':
		process_name = input('Process name: ')
		p.stopProcess(process_name)
		print(p.getRunningProcess())