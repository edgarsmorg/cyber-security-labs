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

# Parte E
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
            return i
        
def decrypt_last_block(blocks):
    key = bytearray(BLOCK_SIZE)
    last_block = blocks[-1]
    for i in range(len(last_block)-1, -1, -1):
        key[int(i)] = decrypt_char(blocks, last_block, i)
        print(key)
    return key

# Parte F
def decrypt_char2(blocks, num_block, j):
    block = blocks[num_block]
    for i in range(256):
        block[j] = i
        blocks[num_block] = block
        cipher = utils.join_blocks(blocks)
        print("trying", i)

        res = oracle(DECRYPT, utils.bytes_to_hex(cipher))
        if "invalid" in res or "json" in res:
            continue
        else:
            return i
        
def decrypt_full_message(cipher_blocks):
    plaintext_blocks = []

    # Recorremos de derecha a izquierda, desde el último bloque al segundo
    for i in range(len(cipher_blocks) - 1, 0, -1):
        # Copiamos los bloques relevantes
        c_prev = cipher_blocks[i - 1]  # bloque anterior (IV o Ci-1)
        c_curr = cipher_blocks[i]      # bloque actual (Ci)

        # Armamos el mensaje a descifrar: [c_prev, c_curr]
        crafted_blocks = [bytearray(c_prev), bytearray(c_curr)]

        # Usamos la función que ya construye el bloque intermedio
        decrypted = bytearray(BLOCK_SIZE)
        for j in range(BLOCK_SIZE - 1, -1, -1):
            decrypted[j] = decrypt_char2(cipher_blocks, num_block = i, j = j)
            print(decrypted)
        # Calculamos el bloque de texto plano: p_i = decrypt(ci) ^ c_{i-1}
        plaintext_block = bytearray(
            [decrypted[b] ^ c_prev[b] for b in range(BLOCK_SIZE)]
        )
        print(plaintext_block)
        print(plaintext_blocks)
        plaintext_blocks.insert(0, plaintext_block)  # insertamos al inicio

    # Juntamos los bloques en un solo mensaje
    full_plaintext = utils.join_blocks(plaintext_blocks)

    # Eliminamos el padding PKCS#7
    padding_len = full_plaintext[-1]
    if padding_len > BLOCK_SIZE or padding_len == 0:
        raise ValueError("Padding inválido al final del mensaje")
    return full_plaintext[:-padding_len]

if __name__ == "__main__":
    ciphertext = oracle(ENCRYPT, MESSAGE = input("message:"))

    # # Parte D
    # print(ciphertext)
    # decrypt_last_char(ciphertext)
    # Parte E
    ciphertext = utils.hex_to_bytes(ciphertext)
    cipher_blocks = utils.split_blocks(ciphertext, 16)
    key_plaintext = decrypt_full_message(cipher_blocks)
    print("\n✅ Mensaje descifrado (sin padding):")
    print(key_plaintext.decode(errors="ignore"))





