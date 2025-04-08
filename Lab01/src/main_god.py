import socket
import utils
ENCRYPT = ("cc5327.hackerlab.cl", 5312)
DECRYPT = ("cc5327.hackerlab.cl", 5313)
BLOCK_SIZE = 16 # obtenido en la experimentacion

def oracle(CONNECTION_ADDR, MESSAGE):
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    response = MESSAGE
    resp = utils.send_message(sock_input, sock_output, response)
    return resp

# Parte D
def decrypt_last_char(encrypt):
    encrypt = utils.hex_to_bytes(encrypt)
    encrypt = utils.split_blocks(encrypt, BLOCK_SIZE)
    curr = bytearray(encrypt[-1])
    prev = bytearray(encrypt[-2])
    prev_mod = bytearray(prev)
    for i in range(256):
        print("trying", i)
        prev_mod[-1] = i
        res = oracle(DECRYPT, utils.bytes_to_hex(utils.join_blocks([prev_mod,curr])))
        if res.startswith("pkcs7: invalid padding"):
            continue
        else:
            plain_byte = 0x01 ^ i ^ prev[-1]
            #caso borde
            print(plain_byte)
            return plain_byte

# Parte E

def decrypt_last_block(encrypt):
    encrypt = utils.hex_to_bytes(encrypt)
    encrypt = utils.split_blocks(encrypt, BLOCK_SIZE)
    decrypt = bytearray(BLOCK_SIZE)
    middle = bytearray(BLOCK_SIZE)
    curr = bytearray(encrypt[-1])
    prev = bytearray(encrypt[-2])
    prev_mod = bytearray(prev)
    two_blocks = [prev_mod, curr]
    for i in range(BLOCK_SIZE-1, -1, -1):
        for j in range(256):
            print("trying", j)
            prev_mod[i] = j
            res = oracle(DECRYPT, utils.bytes_to_hex(utils.join_blocks(two_blocks)))
            if res.startswith("pkcs7: invalid padding"):
                continue
            else:
                padding = BLOCK_SIZE - i

                middle[i] = prev_mod[i] ^ padding
                plain_byte = middle[i] ^ prev[i]
                decrypt[i] = plain_byte

                for k in range(i, BLOCK_SIZE):
                    prev_mod[k] = middle[k] ^ (padding + 1)
                
                break
        print(decrypt)
    return decrypt

# Parte F: función de descifrado de un byte del bloque intermedio
def decrypt_full_message(encrypt):
    encrypt = utils.hex_to_bytes(encrypt)
    encrypt = utils.split_blocks(encrypt, BLOCK_SIZE)
    decrypt = bytearray()
    print("Son",len(encrypt), "Bloques en total")
    for curr_i in range(len(encrypt) - 1, 0, -1):
        print("bloque", curr_i)

        curr = bytearray(encrypt[curr_i])
        prev = bytearray(encrypt[curr_i-1])
        prev_mod = bytearray(prev)
        two_blocks = [prev_mod, curr]

        decrypt_block = bytearray(BLOCK_SIZE)
        middle = bytearray(BLOCK_SIZE)
        for i in range(BLOCK_SIZE-1, -1, -1):
            for j in range(256):
                print("Probando", j)
                prev_mod[i] = j
                res = oracle(DECRYPT, utils.bytes_to_hex(utils.join_blocks(two_blocks)))
                if res.startswith("pkcs7: invalid padding"):
                    continue
                else:
                    padding = BLOCK_SIZE - i

                    middle[i] = prev_mod[i] ^ padding
                    plain_byte = middle[i] ^ prev[i]
                    decrypt_block[i] = plain_byte

                    for k in range(i, BLOCK_SIZE):
                        prev_mod[k] = middle[k] ^ (padding + 1)
                    
                    break
            print(decrypt_block)
        decrypt[:0] = decrypt_block
        print(decrypt)
    return decrypt

if __name__ == "__main__":
    ciphertext = oracle(ENCRYPT, MESSAGE = input("message:"))

    # # Parte D
    # print(ciphertext)
    # decrypt_last_char(ciphertext)
    # # Parte E
    # decrypt_last_block(ciphertext)
    # Parte F
    mesagge = decrypt_full_message(ciphertext)
    print("Mensaje descifrado:", mesagge)



