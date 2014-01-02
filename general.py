#-*- coding: utf-8 -*

# importar módulos necesarios
import os

"""
Función que hace un merge entre dos diccionarios
http://python.6.x6.nabble.com/Deep-merge-two-dicts-tp4859822p4861127.html
"""
def dict_merge (a, b) :
	for k, v in b.items():
		if isinstance(v, dict) and k in a:
			dict_merge(a[k], v)
		else:
			a[k] = v

"""
Función que ejecuta un comando en el sistema y retorna su salida
"""
def system (command) :
	import subprocess
	process = subprocess.Popen (
		command,
		shell = True,
		stdout = subprocess.PIPE,
		stderr = subprocess.PIPE
	)
	output = process.stdout.read ()
	if output == '' :
		output = process.stderr.read ()
	return output

"""
Función que entrega un timestamp con la fecha y hora actual
"""
def now () :
	import time
	return time.strftime ('%Y-%m-%d %H:%M:%S', time.gmtime())

"""
Función que retorna el contenido de un archivo
"""
def file_get_contents (file, mode = 'rb') :
	try:
		os.stat (file)[6]
		fh = open (file, mode)
		data = fh.read ()
		return data
	except Exception, e:
		print >>sys.stderr, e
		sys.exit (1) 
