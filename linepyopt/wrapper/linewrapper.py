from .thriftwrapper import ThriftWrapper
from ..linethrift.ttypes import LoginRequest, IdentityProvider
from ..config import Config
import requests


class LineWrapper:
	@staticmethod
	def init_headers():
		headers = {
			"User-Agent": Config.user_agent,
			"X-Line-Application": Config.line_app,
			"x-lal": "ja-JP_JP"
		}
		return headers

	@staticmethod
	def get_protocol(endpoint, headers):
		headers["x-lpqs"] = endpoint
		protocol = ThriftWrapper.get_protocol(Config.host, endpoint, headers)
		return protocol

	@staticmethod
	def wait_login(verifier):
		headers = init_headers()
		headers["X-Line-Access"] = verifier
		result = requests.get(Config.host + Config.wait_endpoint, headers)
		return result.json()

	@staticmethod
	def get_loginrequest(systemName, verifier):
		req = LoginRequest()
		req.type = 1
		req.identityProvider = IdentityProvider.LINE
		req.keepLoggedIn = True
		req.accessLocation = "127.0.0.1"
		req.systemName = systemName
		req.verifier = verifier
		req.e2eeVersion = 1
		return req
