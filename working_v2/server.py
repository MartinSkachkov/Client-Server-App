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

    for i in range(num_threads):
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

def handle_client(client_socket):
    #get the array
    data = client_socket.recv(1024)  # assuming data is sent in chunks of 1024 bytes
    
    #decode() - transform bytes received into string
    #split the string into substrings by the delim ,
    #convert each substring into an int
    numbers = [int(num) for num in data.decode().split(',')]
    
    print(f"Received unsorted list: {numbers}")

    # Perform parallel selection sort
    multi_threaded_selection_sort(numbers)

    #map(func, iterable object) -> convert each number into string
    #join all strings into one with delim ','
    sorted_data = ','.join(map(str, numbers))
    client_socket.send(sorted_data.encode()) #encode() so that we can send bytes not string
    
    client_socket.close()

def start_server():
    #open a connection socket for the server choosing IPv4 with TCP
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #telling this will be the server(a.k.a hosting)
    server.bind(('127.0.0.1', 8888)) #(should be private or loopback addr.)
    server.listen(5) #limit the possible connections waithing for acception to 5

    print("Server listening on port 8888...")

    while True:
        client, addr = server.accept() #client is the communitacion socket
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        
        #1 thread for each client to run paralel
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

if __name__ == "__main__":
    start_server()
