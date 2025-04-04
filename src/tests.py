import utils
bytes = bytearray(b'Hola como estamos')
bytes2 = bytearray(b' con los cabros')
for i in range(256):
    bytes[-1] = i
    print(bytes)
bytes.reverse()
print(bytes)
