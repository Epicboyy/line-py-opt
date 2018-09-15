from thrift.transport.THttpClient import THttpClient
from thrift.protocol.TCompactProtocol import TCompactProtocol


class ThriftWrapper:
	@staticmethod
	def get_protocol(host, endpoint, headers={}):
		transport = THttpClient(host + endpoint)
		transport.setCustomHeaders(headers)
		protocol = TCompactProtocol(transport)
		return protocol