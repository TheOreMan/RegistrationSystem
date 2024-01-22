from tacacs_plus.client import TACACSClient
server_host = '192.168.55.143'
server_port = 49
secret = 'secret1'

def authenticate(username, password):
    cli = TACACSClient(server_host, server_port, secret, timeout=10)
    authen = cli.authenticate(username, password)
    return authen.valid
