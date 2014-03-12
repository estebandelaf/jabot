Jabot
=====

Jabot corresponde a un bot para Jabber programado en Python 2. La idea original
era buscar un bot ya programado, por lo cual busqué y encontré:

*	jabberbot (Python):
	http://thp.io/2007/python-jabberbot

*	Net-Jabber-Bot-2.1.5 (Perl):
	http://search.cpan.org/~toddr/Net-Jabber-Bot-2.1.5/lib/Net/Jabber/Bot.pm

Sin embargo, y por alguna extraña razón que no quise investigar, no los pude
hacer funcionar. Así que tomando idea de ambos (por eso los menciono en este
README) programé Jabot.

Requerimientos
--------------

Módulo xmpp, en Debian GNU/Linux paquete python-xmpp:

	# apt-get install python-xmpp

Ejemplo
-------

Revisar el archivo example.py que contiene un ejemplo de la ejecución del bot.
Básicamente se debe heredar desde DefaultCommands una clase que contendrá los
comandos que el Bot puede ejecutar.
