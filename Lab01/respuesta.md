Lab 1 Seguridad Computacional: Padding Oracle Attack
Intergrantes: Edgar Morales, Jean Paul Duchens

a) Estudio de ambos servicios

Tenemos que el servicio 1 cifra y el 2 descifra.
Probando diferentes largos de inputs para el servicio 1:
-"H" (texto plano de largo 1) -> clave de largo 112 bytes
-"Ho" (texto plano de largo 2) -> clave de largo 112 bytes
.
.
.
-texto plano de largo 9 -> clave de largo 128 bytes

Concluyendo que los bloques son de largo de 16 bytes por la manera en la que opera PKCS7 rellenando un nuevo bloque con padding.

Además pudimos observar que tenemos un largo límite del texto plano que se puede ingresar y por ende un largo límite del texto plano que nos da al descifrar, pues dando como texto plano la secuencia "aaaaa....." (256 bytes) logramos que el descifrador se desfazara y, que para nuevas peticiones se entregaran respuestas pasadas de bloques que no se lograron procesar a tiempo.

b) Código adjunto

c) Según lo analizado en la parte a), podemos inferir el tamaño del bloque del cifrador enviando mensajes de longitud creciente, agregando un byte a la vez, y observando los largos del texto cifrado. Cuando se detecte un incremento repentino en la longitud del texto cifrado, ese salto indica el tamaño del bloque utilizado.

d) Código adjunto.

e) Código adjunto.

f) Código adjunto.
