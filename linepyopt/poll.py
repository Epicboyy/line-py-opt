from .login import token_login
from .linethrift.ttypes import OpType


class Poll:
	def __init__(self, client):
		self.client = client
		self.poll = token_login(client.authToken, True)
		self.receiver = {}

	def set_receiver(self, opType, receiver):
		self.receiver[opType] = receiver

	def start(self):
		revision = self.client.getLastOpRevision()
		while True:
			try:
				ops = self.poll.fetchOperations(revision, 100)
			except:
				revision = self.client.getLastOpRevision()
				continue
			for op in ops:
				if op.type == OpType.END_OF_OPERATION:
					continue
				elif op.type in self.receiver.keys():
					self.receiver[op.type](op)
				revision = max(revision, op.revision)