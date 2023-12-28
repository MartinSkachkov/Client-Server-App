import socket
import threading
import time

def selection_sort(arr, start, end):
    for i in range(start, end):
        min_index = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]

def multi_threaded_selection_sort(arr, num_threads=2):
    segment_size = len(arr) // num_threads
    threads = []

    start_time = time.time()

    for i in range(num_threads): #0,1
        start = i * segment_size
        end = (i + 1) * segment_size if i != num_threads - 1 else len(arr)
        thread = threading.Thread(target=selection_sort, args=(arr, start, end))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Multi-threaded selection sort took {elapsed_time:.6f} seconds.")

def handle_client(client_socket): #,last_interaction_time
    try:
        data = client_socket.recv(1024)  # assuming data is sent in chunks of 1024 bytes

        numbers = [int(num) for num in data.decode().split(',')]
        numbersCpy = numbers.copy()
        print(f"Received unsorted list: {numbers}")

        # Single-threaded selection sort
        start_time_single = time.time()
        selection_sort(numbers, 0, len(numbers))
        end_time_single = time.time()
        elapsed_time_single = end_time_single - start_time_single
        print(f"Single-threaded selection sort took {elapsed_time_single:.6f} seconds.")

        # Reset the array for the multi-threaded version
        numbers = numbersCpy.copy()
        print(f"Reset the list to original: {numbers}")
        
        # Multi-threaded selection sort with 2 threads
        multi_threaded_selection_sort(numbers)

        sorted_data = ','.join(map(str, numbers))
        client_socket.send(sorted_data.encode())
        
        #last_interaction_time[0] = time.time()
        client_socket.close()

    except Exception as e:
        print(f"Error handling client: {e}")

def start_server():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888))
    server.listen()

    print("Server listening on port 8888...")

    #last_interaction_time = [time.time()] # Initialize the last interaction time

    while True:
        # Проверка за активност в основния цикъл
        #if time.time() - last_interaction_time[0] > 30:
        #    print("No activity for 2 minutes. Closing the server.")
        #    break
        try:
            client, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
        
            #1 thread for each client to run parallel
            client_handler = threading.Thread(target=handle_client, args=(client,)) #last_interaction_time
            client_handler.start()
        except socket.error as e:
            print(f"Socket error: {e}")
            break

    server.close()

if __name__ == "__main__":
    start_server()
