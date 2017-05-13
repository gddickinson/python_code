#!/usr/bin/env python
#
# Copyright 2011 Abdulrahman Alotaiba
# http://www.mawqey.com/
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socketserver
import serial
import time

HOST = ''
PORT = 9999
BAUD_RATE = 115200
SERIAL_PORT = 'COM3'

class ArduinoTCPHandler(socketserver.BaseRequestHandler):
	def handle(self):
		try:
			arduino = serial.Serial(SERIAL_PORT, BAUD_RATE)
			print ("Connected to Arduino successfully.\n")
			print ("%s" % (arduino.readline()))
		except:
			print ("Failed to connect Arduino on %s" % (SERIAL_PORT))
		
		self.request.send("\r\nType a number between 0 and 9 - 'Q' to quit!\n\r")
		
		print ("%s is connected" % self.client_address[0])
		try:
			while True:
				self.data = self.request.recv(1024).strip()
				print (self.data)
				try:
					char = int(self.data)
					if (0 <= char < 10):
						arduino.write(str(char))
					else:
						continue
				except ValueError:
					if self.data.upper() == 'Q':
						break
					else:
						pass
		except IOError:
			print ("Connection to peer has been lost.\r\n")

try:
	print ('Waiting for a connection...')
	server = socketserver.TCPServer((HOST, PORT), ArduinoTCPHandler, False)
	server.allow_reuse_address = True
	server.server_bind()
	server.server_activate()
	server.serve_forever()
except KeyboardInterrupt:
	print ('Terminating Server...')
	server.socket.close()
