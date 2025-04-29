import socket
import threading
import os
import sys

def exit_handler():
    global active
    client.send("/exit".encode('ascii'))
    active = False
    client.close()
    print("EXITED")
    os._exit(0)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Listening to server and sending nickname
def receive():
    global client
    global first_message
    global active
    global password

    while active:
        try:
            # Recieve message from server
            # If 'NICK' send nickname
            message = client.recv(1024).decode('ascii')
            if message == 'AUTH':
                client.send(password.encode('ascii'))
            elif message == 'NICK':
                client.send(nickname.encode('ascii'))
            elif message == 'EXIT':
                exit_handler()
            else:
                print(message)
                print_prompt()
                if (first_message == True):
                    write_thread = threading.Thread(target=write)
                    write_thread.start()
                    first_message = False
                    
        except:
            # Close connection when error
            client.close()
            break  

# Sending messages to server
def write():
    global client
    global nickname
    global active

    while active:
        user_input = input()
        if user_input.strip() == "/exit":
            exit_handler()
            sys.exit(0)
        elif 
        elif user_input.strip() == "/list":
            client.send("/list".encode('ascii'))
        elif user_input.strip() == "/clear":
            clear()
        else:
            message = '[{}]: {}'.format(nickname, user_input)
            client.send(message.encode('ascii'))

def main():
    global client
    global nickname
    global first_message
    global active
    global password
    

    first_message = True
    active = True
    prompted = False
    
    nickname = input("Choose your nickname: ")

    password = input("Enter server password: ")

    host = '127.0.0.1'
    port = 55556

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Error: Unable to connect to server on {}:{}\nIs the server running?".format(host, port))
        os._exit(0)

    # Starting Threads For Listening And Writing
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    try:
        receive_thread.join()
    except KeyboardInterrupt:
        exit_handler()
    except Exception as e:
        print("An unexpected error occured!")

if __name__ == "__main__":
    main()

