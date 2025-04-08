import socket
import utils
ENCRYPT = ("cc5327.hackerlab.cl", 5312)
DECRYPT = ("cc5327.hackerlab.cl", 5313)
BLOCK_SIZE = 16 # obtenido en la experimentacion

def oracle(CONNECTION_ADDR, MESSAGE):
    sock_input, sock_output = utils.create_socket(CONNECTION_ADDR)
    try:
        response = MESSAGE
        resp = utils.send_message(sock_input, sock_output, response)
        return resp
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

# Parte F: función de descifrado de un byte del bloque intermedio
def decrypt_char2(blocks, num_block, j, known_plaintext):
    original_prev = blocks[num_block - 1]
    original_curr = blocks[num_block]

    # Guardamos el valor original para probarlo al final
    original_byte = original_prev[j]

    padding_val = BLOCK_SIZE - j

    # Probar todos los guesses, excepto el original
    for guess in list(range(256)):
        if guess == original_byte:
            continue

        # Copias profundas
        crafted_prev = bytearray(original_prev)
        crafted_curr = bytearray(original_curr)

        crafted_prev[j] = guess

        # Aplicar padding a los bytes ya descubiertos
        for k in range(j + 1, BLOCK_SIZE):
            crafted_prev[k] = known_plaintext[k] ^ padding_val

        crafted_blocks = [crafted_prev, crafted_curr]
        cipher = utils.join_blocks(crafted_blocks)
        res = oracle(DECRYPT, utils.bytes_to_hex(cipher))

        print(f"Bloque {num_block}, posición {j}, probando guess = {guess}")

        if "invalid" not in res and "json" not in res:
            print(f"[✓] Byte correcto encontrado: {guess}")
            return guess ^ padding_val

    # Si no funcionó ninguno, probar el original como último recurso
    crafted_prev = bytearray(original_prev)
    crafted_curr = bytearray(original_curr)
    crafted_prev[j] = original_byte

    for k in range(j + 1, BLOCK_SIZE):
        crafted_prev[k] = known_plaintext[k] ^ padding_val

    crafted_blocks = [crafted_prev, crafted_curr]
    cipher = utils.join_blocks(crafted_blocks)
    res = oracle(DECRYPT, utils.bytes_to_hex(cipher))

    if "invalid" not in res and "json" not in res:
        print(f"[✓] Byte original ({original_byte}) fue el correcto en última instancia")
        return original_byte ^ padding_val

    # Nada funcionó
    print(f"[✗] No se encontró padding válido en la posición {j} del bloque {num_block}")
    raise ValueError(f"No se encontró padding válido en el byte {j} del bloque {num_block}")

def decrypt_full_message(cipher_blocks):
    plaintext_blocks = []

    for i in range(len(cipher_blocks) - 1, 0, -1):
        c_prev = cipher_blocks[i - 1]
        c_curr = cipher_blocks[i]

        decrypted = bytearray(BLOCK_SIZE)

        # Vamos de derecha a izquierda
        for j in range(BLOCK_SIZE - 1, -1, -1):
            decrypted[j] = decrypt_char2(cipher_blocks, i, j, decrypted)

        # XOR entre el intermedio y c_{i-1} para obtener el texto plano
        plaintext_block = bytearray(
            [decrypted[b] ^ c_prev[b] for b in range(BLOCK_SIZE)]
        )
        plaintext_blocks.insert(0, plaintext_block)

    full_plaintext = utils.join_blocks(plaintext_blocks)

    # Eliminar padding PKCS#7
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
    #decrypt_last_block(cipher_blocks)
    # Parte F
    mensaje_plano = decrypt_full_message(cipher_blocks)
    print("Mensaje descifrado:", mensaje_plano.decode(errors="ignore"))



