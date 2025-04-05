import socket

# We connect to a (host,port) tuple
import utils
ENCRYPT = ("cc5327.hackerlab.cl", 5312)
DECRYPT = ("cc5327.hackerlab.cl", 5313)
BLOCK_SIZE = 16 # obtenido en la experimentacion

def oracle(CONNECTION_ADDR, MESSAGE):
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    try:
        response = MESSAGE
        # You need to use encode() method to send a string as bytes.
        resp = utils.send_message(sock_input, sock_output, response)
        return resp
        # Wait for a response and disconnect.
    except Exception as e:
        return e

def decrypt_char(blocks, last_block, j):
    for i in range(256):
        last_block[j] = i
        blocks[-1] = last_block
        cipher = utils.join_blocks(blocks)
        print("trying", i)

        res = oracle(DECRYPT, utils.bytes_to_hex(cipher))
        if "invalid" in res or "json" in res:
            continue
        else:
            print(i)
            return i
        
def decrypt_last_block(blocks):
    key = bytearray(BLOCK_SIZE)
    last_block = blocks[-1]
    for i in range(len(last_block)-1, -1, -1):
        key[int(i)] = decrypt_char(blocks, last_block, i)
        print(key)
    print(key)


# Parte D
def decrypt_last_char(encrypt):
    encrypt = utils.hex_to_bytes(encrypt)
    for i in range(256):
        encrypt[-1] = i
        print("trying", i)
        res = oracle(DECRYPT, utils.bytes_to_hex(encrypt))
        if "invalid" in res:
            continue
        else:
            print(i, res)
            return bytes(i)
        
if __name__ == "__main__":
    ciphertext = oracle(ENCRYPT, MESSAGE = input("message:"))

    # # Parte D
    # print(ciphertext)
    # decrypt_last_char(ciphertext)
    # Parte E
    ciphertext = utils.hex_to_bytes(ciphertext)
    cipher_blocks = utils.split_blocks(ciphertext, 16)
    decrypt_last_block(cipher_blocks)





