import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import time

from librouteros import *

arr = []
api = connect(username='dexter', password='1011200107', host='10.1.1.7')


class findDuplicate(tornado.web.RequestHandler):
	def get(self):
		duplicate = []
		name = self.get_query_argument('name', True)
		arr.append(name)

		duplicate = list(set(x for x in arr if arr.count(x) > 1))

		if len(duplicate) > 0:
			arr.pop()
			response = {
				'names': arr,
				'msg': 'Name ' +name+ 'Already Exists'
			}
			self.write(response)

		else:
			response = {
				'names': arr,
			}
			self.write(response) 

class mikrotikIdentity(tornado.web.RequestHandler):
	def get(self):
		params = {'.id': 'wlan1', 'rounds': '1'}
		identity = api(cmd='/interface/wireless/scan', **params)
		response = json.dumps(identity)
		arr = []

		for i in range(len(identity)):
			arr.append(identity[i])
		
		print(arr)
		self.write(identity[0])

class changeName(tornado.web.RequestHandler):
	def get(self):
		newName = self.get_query_argument('name', True)
		params = {'name': newName}
		change = api(cmd='/system/identity/set', **params)
		getName = api(cmd='/system/identity/print')

		print(getName)
		self.write(getName[0])

class Index(tornado.web.RequestHandler):
	def get(self):
		self.render('static/index.html')



#WebSocket Implementation
class SocketHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print('WebSocket Connected')

	def on_message(self, message):
		arr = []
		getName = api(cmd='/system/identity/print')
		arr.append(getName[0])

		def comparator():
			newName = api(cmd='/system/identity/print')
			arr.append(newName[0])

			if arr[0] != arr[1]:
				print('Name has been changed to' + json.dumps(arr[1]))
				self.write_message('Name has been changed to '+ json.dumps(arr[1]))
				self.on_message(message)
			else:
				self.on_message(message)
		
		tornado.ioloop.IOLoop.instance().add_timeout(time.time()+3, comparator)

	def on_close(self):
		print('Connection Closed')

	def check_origin(self, origin):
		return True	




def make_app():
    return tornado.web.Application([
        (r"/addName", findDuplicate),
        (r"/identity", mikrotikIdentity),
        (r"/changeName", changeName),
        (r"/index", Index),
        (r"/ws", SocketHandler),

        #Static File option
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ])

#dummy function    
def ddd():
	print('ddd')



if __name__ == "__main__":
    app = make_app()
    ddd = ddd()
    app.listen(4000)
    tornado.ioloop.IOLoop.current().start()

