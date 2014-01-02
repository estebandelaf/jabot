#!/usr/bin/env python
#-*- coding: utf-8 -*

# importar módulos necesarios
from jabot import Jabot, DefaultCommands
from general import *

"""
Clase con las funciones que ejecutará el bot (funciones extendidas por usuario),
permite extender los comandos prexistentes en la clase DefaultCommands.
"""
class Commands (DefaultCommands) :

	"""
	Método que permite ejecutar cualquier comando en el sistema operativo.
	Esta funcionalidad no se incluye por defecto en los comandos en la clase
	DefaultCommands ya que podría representar un riesgo de seguridad para el
	sistema operativo.
	"""
	def system (self, args) :
		return system (args)

# lanzar bot
bot = Jabot ({
	'jabber' : {
		'user' : 'USUARIO@gmail.com',
		'pass' : 'CONTRASEÑA'
	}
})
bot.setCommands (Commands())
bot.start ()
