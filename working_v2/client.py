import socket
import threading

def send_data(data):
    #open a socket for the client choosing IPv4 with TCP 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))

    data_str = ','.join(map(str, data))
    client.send(data_str.encode())

    sorted_data = client.recv(1024).decode()
    sorted_numbers = [int(num) for num in sorted_data.split(',')]

    print(f"Received sorted list from server: {sorted_numbers}")

    client.close()

def handle_user():
    unsorted_list = []
    n = int(input("Enter number of elements you want to sort: "))
    for i in range (0, n):
        elem = int(input())
        unsorted_list.append(elem)

    print(f"Sending unsorted list to server: {unsorted_list}")
    send_data(unsorted_list)

if __name__ == "__main__":
    user_input = ""
    while user_input.lower() != "stop":
        user_input = input("Enter 'stop' to stop the client execution, 'no' to continue: ")
        if user_input.lower() != "stop":
            handle_user()

    print("Exiting!")
