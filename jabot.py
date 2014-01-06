#-*- coding: utf-8 -*

# importar módulos necesarios
import xmpp
from threading import Thread
import os
import traceback
from general import *

"""
Clase que representa al Bot
"""
class Jabot (Thread):

	# configuración por defecto del bot
	config = {
		'jabber' : {
			'user' : '',
			'pass' : '',
			'host' : 'talk.google.com',
			'port' : 5223,
			'avatar' : ''
		},
		'debug' : 0
	}
	# objeto que representa la conexión del cliente con el servidor
	client = None
	# objeto que representa el estado del bot
	status = None
	# flag para determinar cuando se debe terminar la conexión del bot
	quit = False
	# objeto con los comándos que el bot puede ejecutar
	commands = None

	"""
	Constructor de la clase
	"""
	def __init__ (self, config) :
		dict_merge (self.config, config)
		Thread.__init__ (self)

	"""
	Inicializar Bot y conectar al servidor
	"""
	def run (self) :
		# crear id para jabber
		jid = xmpp.JID (self.config['jabber']['user'])
		# crear cliente y atributo para el estado
		if self.config['debug'] >= 2 :
			self.client = xmpp.Client (jid.getDomain())
		else :
			self.client = xmpp.Client (jid.getDomain(), debug=[])
		self.status = xmpp.Presence()
		# conectar al  servidor y autenticar
		self.client.connect ((
			self.config['jabber']['host'],
			self.config['jabber']['port']
		))
		result = self.client.auth (
			jid.getNode(), self.config['jabber']['pass'], 'Bot'
		)
		# hacer el bot visible
		self.client.sendInitPresence ()
		# colocar estado inicial del bot
		self.setStatus ('Conectado el '+now())
		# registrar manejadores para eventos de XMPP
		self.client.RegisterDisconnectHandler (self.handler_disconnect)
		self.client.RegisterHandler ('message', self.handler_message)
		self.client.RegisterHandler ('presence', self.handler_presence)
		# asignar avatar del bot
		if self.config['jabber']['avatar'] != '' :
			self.setAvatar (self.config['jabber']['avatar'])
		# procesar mensajes XMPP entrantes infinitamente
		while not self.quit :
			self.client.Process (2)

	"""
	Método para asignar la clase con los comandos que el bot puede ejecutar
	"""
	def setCommands (self, commands) :
		self.commands = commands
		self.commands.bot = self

	"""
	Método para enviar un mensaje a un usuario
	"""
	def send (self, user, data):
		self.client.send (xmpp.Message(user, data, 'chat'))

	"""
	Método que reconectará al bot en caso de desconexión
	"""
	def handler_disconnect (self) :
		self.client.reconnectAndReauth ()
		self.setStatus ('Reconectado el '+now())

	"""
	Método para procesar los mensajes que son recibidos
	"""
	def handler_message (self, client, event) :
		# obtener mensaje y verificar que no sea vacio
		msg = event.getBody()
		if msg == None :
			return
		# determinar que comando se debe ejecutar
		try :
			command, args = msg.split (' ', 1)
		except :
			command = msg
			args = None
		command = command[0].lower() + command[1:]
		# ejecutar comando
		try :
			if args == None :
				response = getattr (self.commands, command) ()
			else :
				response = getattr (
					self.commands, command
				) (args)
		except :
			response = 'No entiendo lo que me dices :-('
			if self.config['debug'] >= 1 :
				traceback.print_exc ()
		# en caso que el comando haya devuelto algo enviarlo al usuario
		if response != None :
			self.send (event.getFrom(), str(response))

	"""
	Método que suscribirá un usuario a otro y solicitará suscribirse
	"""
	def handler_presence (self, con, event) :
		if event.getType() :
			self.client.send (xmpp.Presence (
				to=event.getFrom(), typ='subscribed'
			))
			self.client.send (xmpp.Presence (
				to=event.getFrom(), typ='subscribe'
			))

	"""
	Método para asignar el estado del Bot
	"""
	def setStatus (self, data) :
		self.status.setStatus (data)
		self.client.send (self.status)

	"""
	Método para asignar un avatar al bot
	"""
	def setAvatar (self, file) :
		pass

"""
Clase con las funciones que ejecutará el bot (funciones por defecto)
"""
class DefaultCommands :

	# objeto con el Bot de Jabber
	bot = None

	"""
	Método que muestra los comandos disponibles
	"""
	def help (self) :
		from inspect import getmembers, ismethod
		buffer = 'Comandos disponibles: '
		for name, data in getmembers (self, predicate=ismethod) :
			buffer += name+' '
		return buffer

	"""
	Método que ejecuta "uptime" en el sistema operativo
	"""
	def uptime (self) :
		return system ('uptime')

	"""
	Método que ejecuta "date" en el sistema operativo
	"""
	def date (self) :
		return system ('date')

	"""
	Método para cambiar el estado del bot
	"""
	def status (self, status) :
		self.bot.setStatus (status)

	"""
	Método para detener el bot
	"""
	def shutdown (self) :
		self.bot.quit = True
