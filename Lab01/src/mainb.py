import socket
import utils
ENCRYPT = ("cc5327.hackerlab.cl", 5312)
DECRYPT = ("cc5327.hackerlab.cl", 5313)

def connect_to_server(server_addr):
    sock_input, sock_output = utils.create_socket(server_addr)
    return sock_input, sock_output

if __name__ == "__main__":
    sock_input_A, sock_output_A = connect_to_server(ENCRYPT)

    while True:
        try:
            message = input("Send a message for ENCRYPT: ")
            resp_A = utils.send_message(sock_input_A, sock_output_A, message)
            print("Server ENCRYPT: ", resp_A)

            sock_input_B, sock_output_B = connect_to_server(DECRYPT)

            resp_B = utils.send_message(sock_input_B, sock_output_B, resp_A)
            print("Server DECRYPT: ", resp_B)
            sock_input_B.close()
            sock_output_B.close()

        except Exception as e:
            print("Error:", e)
            print("Closing.")
            sock_input_A.close()
            sock_output_A.close()
            break
