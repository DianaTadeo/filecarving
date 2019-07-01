#!/bin/python

import optparse
import sys
import re
from binascii import hexlify

def options():
	"""
	Permite verificar las opciones de entrada de la herramienta
	"""
	parser = optparse.OptionParser()
	parser.add_option('-f', '--file', dest='file_n',help='Archivo para busqueda')
	parser.add_option('-c', '--config_file', dest='conf', default='filecarving.cnf', help='Archivo de configuracion')
	parser.add_option('-d', '--directory', dest='directory', default='.', help='Directorio donde se guardaran los archivos encontrados')
	opts, args = parser.parse_args()
	return opts
    
def read_config(config_file):
	"""
	Lee el archivo de configuracion y almacena los tipos de archivo que se 
	planean buscar en el binario.
	config_file: archivo de configuracion
	
	El archivo de configuracion cuenta con ccomentarios '#' y '*' al inicio
	de la linea
	Toda linea que no tenga comentarios debe de comenzar con un magicnumber
	en hexadecimal, seguido de algun espacio, despues la etiqueta 'size=' al
	tamanio del archivo	resultante en KB, MB o GB y el tipo de archivo.
	ej: 
	\x89\x50\x4e\x47\x0d\x0a\x1a\x0a	size=1MB PNG
	"""
	files=[]
	with open(config_file, 'r') as cf:
		for line in cf:
			if line[0] !="#" and line[0] !="*" and line!= "\n": #Se omiten comentarios
				values= re.match(r'(.*)size=([0-9]+)([a-zA-Z]+) ([A-Z]+)', line)
				if values.group(2):# se obtiene el tamanio del archivo resultado
					sizes=values.group(2)
					if values.group(3)=='KB':
						size=int(sizes)*1020
					elif values.group(3)=='MB':
						size=int(sizes)*1048576
					elif values.group(3)=='GB':
						size=int(sizes)*1073741824
					#Se guarda en una tupla (magicnumber, tamanio, tipo)
					files.append((values.group(1).strip(), size, values.group(4)))
				else:
					print ("El archivo de configuracion contiene errores.")
					exit(1)
	return files
	
def carve_file(file_name,values, directory):
	"""
	Funcion que realizara la busqueda de los magic number en el
	archivo binario y de acuerdo al tamanio elegido y tipo, lo 
	guardara en un directorio.
	file_name: archivo binario (donde se buscan los demas archivos)
	values: tupla de tipos de archivos
	dorectory: directorio donde se guardan los archivos encontrados
	"""
	with open(file_name, 'rb') as binary_file:
		#Nos movemos hasta el final del archivo binario y encontramos el tamanio de este
		binary_file.seek(0, 2) 
		num_bytes = binary_file.tell() 
		count = 0
		#para recorrer todo el archivo binario
		for i in range(num_bytes):
			binary_file.seek(i)
			#para cada tipo de archivo
			for mnumber in values:
				num_bytes = binary_file.read(mnumber[0].count('x'))
				magic=bytes(mnumber[0].encode()).decode('unicode-escape').encode('ISO-8859-1')#necesario para formatear a cadena hexa en bytes
				if num_bytes == magic:#Si encuentra coincidencia
					count+=1
					print("Found "+ mnumber[2]+" Signature #" + str(count) + " at " + str(i))
					png_size_bytes = mnumber[1]
					binary_file.seek(i)
					file_data = binary_file.read(mnumber[1]+ 8)
					#Se guarda el archivo encoentrado
					with open(directory+"/" + str(i) + "."+mnumber[2].lower(), "wb") as outfile:
						outfile.write(file_data)
                
                
                

if __name__ == '__main__':
	opts = options()
	vals=read_config(opts.conf)
	carve_file(opts.file_n, vals, opts.directory)
