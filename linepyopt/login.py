from .wrapper.linewrapper import LineWrapper
from .linethrift import TalkService, AuthService
from .config import Config


def token_login(token, poll=False):
	headers = LineWrapper.init_headers()
	headers["X-Line-Access"] = token
	if poll:
		endpoint = Config.poll_endpoint
	else:
		endpoint = Config.normal_endpoint
	client = TalkService.Client(LineWrapper.get_protocol(endpoint, headers))
	client.authToken = token
	return client


def qr_login(systemName="linepyopt"):
	headers = LineWrapper.init_headers()

	# Login via LINE app
	register = TalkService.Client(LineWrapper.get_protocol(Config.register_endpoint, headers))
	qr = register.getAuthQrcode(True, systemName)
	print("line://au/q/" + qr.verifier)
	LineWrapper.wait_login(qr.verifier)

	# Login process
	headers["X-Line-Access"] = qr.verifier
	auth = AuthService.Client(LineWrapper.get_protocol(Config.login_endpoint, headers))
	req = LineWrapper.get_loginrequest(systemName, qr.verifier)
	res = auth.loginZ(req)

	# Finalize
	client = token_login(res.authToken)
	return client
