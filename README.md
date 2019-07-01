# filecarving
Una herramienta filecarving con un archivo de configuración para poder agregar todos los tipos de archivos que se deseen

Es completamente necesario el archivo de configuración para su ejecución
 
 El archivo de configuracion cuenta con ccomentarios '#' y '*' al inicio
	de la linea
	Toda linea que no tenga comentarios debe de comenzar con un magic number
	en hexadecimal, seguido de algun espacio, despues la etiqueta 'size=' al
	tamanio del archivo	resultante en KB, MB o GB y el tipo de archivo.
	ej: 
	\x89\x50\x4e\x47\x0d\x0a\x1a\x0a	size=1MB PNG

