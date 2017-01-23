#  coding: utf-8
import SocketServer, os, mimetypes

# Copyright 2017 Larin Chen, Vinson Lai
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    status = "HTTP/1.1 200 OK \r\n"
    content = ""
    text = ""

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.array = self.data.split()
	method_type = self.array[0]
        print ("Got a request of: %s\n" % self.data)

    	if method_type != 'GET':
            self.status = "HTTP/1.1 405 Method not allowed\r\n"
	    self.request.sendall(self.status + self.content + self.text)
	    return
	    

    
	if self.array[1][-1] == '/':
	    path = os.getcwd() + "/www" + self.array[1] + "index.html"
	else:
	    path = os.getcwd() + "/www" + self.array[1]
    
	path = os.path.realpath(path)
    
	if os.path.isfile(path) and path.startswith(os.getcwd() + "/www"):
	    self.text = open(path).read()
	    mime = mimetypes.guess_type(path)[0]
	    self.content = "Content-Type: " + mime + "\r\n\r\n"
	    
	else:
	    self.status = "HTTP/1.1 404 Not Found\r\n"
	    
	self.request.sendall(self.status + self.content + self.text)

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
