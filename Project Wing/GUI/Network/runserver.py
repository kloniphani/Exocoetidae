"""
This script runs the Network application using a development server.
"""

from os import environ
from Network import app

import sys

if __name__ == '__main__':
	HOST = environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(environ.get('SERVER_PORT', '5555'))
	except ValueError:
		PORT = 5555

	if len(sys.argv) > 1:
		try:
			PORT = int(environ.get('SERVER_PORT', '{0}'.format(sys.argv[1])))
		except ValueError:
			PORT = sys.argv[1]
	app.run(HOST, PORT)
