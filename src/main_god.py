import socket

# We connect to a (host,port) tuple
import utils
ENCRYPT = ("cc5327.hackerlab.cl", 5312)
DECRYPT = ("cc5327.hackerlab.cl", 5313)

def fuc(CONNECTION_ADDR, MESSAGE):
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    try:
        response = MESSAGE
        # You need to use encode() method to send a string as bytes.
        resp = utils.send_message(sock_input, sock_output, response)
        return resp
        # Wait for a response and disconnect.
    except Exception as e:
        return e

def decrypt_char(crypt, j):
    for i in range(256):
        crypt[j] = i
        print("tryig", i)
        res = fuc(DECRYPT, utils.bytes_to_hex(crypt))
        print("tryig", i)
        if "invalid" in res:
            continue
        else:
            print(i, res)
            return bytes(i)
        
def decrypt_block(block):
    key = bytearray()
    for i in range(len(block)-1, 0, -1):
        key += decrypt_char(block, i)
    print(key.reverse())
             
if __name__ == "__main__":
    res = fuc(ENCRYPT, MESSAGE = input("message:"))
    res = utils.hex_to_bytes(res)
    blocks = utils.split_blocks(res, 16)
    print(blocks)

