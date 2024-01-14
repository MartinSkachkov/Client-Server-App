import socket
import threading
import sys

def send_data(data):
 try:
     #open a socket for the client choosing IPv4 with TCP 
     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
     client.connect(('127.0.0.1', 8888))
 
     data_str = ','.join(map(str, data))
     client.send(data_str.encode())
 
     sorted_data = client.recv(1024).decode()
     sorted_numbers = [int(num) for num in sorted_data.split(',')]
 
     print(f"Received sorted list from server: {sorted_numbers}")
 
     client.close()
 
 except Exception as e:
        print(f"Can't connect to the server. Error: {e}")
        sys.exit()

def handle_user():
    unsorted_list = []

    while True:
        try:
            n = int(input("Enter number of elements you want to sort: "))
            break  # Излизаме от цикъла, ако въвеждането е успешно
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    for i in range(n):
        while True:
            try:
                elem = int(input(f"Enter element {i+1}: "))
                unsorted_list.append(elem)
                break  # Излизаме от цикъла, ако въвеждането е успешно
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    print(f"Sending unsorted list to server: {unsorted_list}")

    send_data(unsorted_list)

if __name__ == "__main__":
    user_input = ""

    while user_input.lower() != "stop":
        user_input = input("Enter 'stop' to stop the client execution, 'no' to continue: ")
        if user_input.lower() != "stop":
            if user_input.lower() != "no":
                print("Invalid input. Please enter 'no' to continue.")
            else:
                handle_user()

    print("Exiting!")
