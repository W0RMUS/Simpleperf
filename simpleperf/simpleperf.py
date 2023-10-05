import argparse
import multiprocessing
import socket
import time
import sys

# The default time format
TIME_FORMAT = '%.2f'
# The default format for data size (megabytes)
DEFAULT_FORMAT = 'MB'
# The default server ip address
DEFAULT_IP = '10.0.0.2'
# The default server port
DEFAULT_PORT = 8088
# The default duration of the data transfer process
DEFAULT_DURATION = 25
# The default chunk size of 1000 bytes
BUFFER_SIZE = 1000
# The default table format, used for printing results
TABLE_FORMAT = "{:^15} {:^15} {:^15} {:^15}"


def format_size(size, unit):
    """
    Description:
        This function takes a size value in bytes and converts it to the specified unit (B, KB, or MB).
        It returns the converted size as a float

    Arguments:
        size (int or float): The size to be converted, represented in bytes.
        unit (str): The unit to convert the size into. Supported units are 'B', 'KB', and 'MB'.

    Returns:
        float: The size value after being converted to the specified unit.
               (Because the script needs functionality to support the specified units.)

    Raises:
        ValueError: If the specified unit is not one of the supported units ('B', 'KB', or 'MB').
    """
    # Dictionary to store the unit values
    units = {'B': 1, 'KB': 1000, 'MB': 1000000}

    if unit not in units:
        raise ValueError("Invalid unit specified. Supported units are 'B', 'KB', and 'MB'.")

    return size / units[unit]


def calculate_rate(data, elapsed_time):
    """
    Description:
        This function calculates the data transfer rate in megabits per second (Mbps), given the amount
        of data transferred and the elapsed time. It converts the data to megabits and divides it by the
        elapsed time to get the rate in Mbps.

    Arguments:
        data (int or float): The amount of data transferred, represented in bytes.
        elapsed_time (int or float): The time taken for the data transfer, represented in seconds.

    Returns:
        float: The data transfer rate in megabits per second (Mbps).
               (Because megabits per second is the desired output.)
    """
    # Convert from bytes to megabits
    megabits = (data * 8) / 1000000
    # Calculate rate as megabits per second (Mbps)
    rate = megabits / elapsed_time

    return rate


def print_interval(total_sent, last_interval_sent, interval_start, interval_stop, args):
    """
    Description:
        This function prints the data transfer information for a given time interval in a table format.
        It calculates the data sent during the interval, formats the data sent to the desired unit,
        calculates the data transfer rate, and prints the information in a formatted table.

    Arguments:
        total_sent (int): The total amount of data sent up to the current interval, in bytes.
        last_interval_sent (int): The total amount of data sent up to the previous interval, in bytes.
        interval_start (float): The start time of the current interval, in seconds.
        interval_stop (float): The end time of the current interval, in seconds.
        args (Namespace): A namespace object containing the following attributes:
            - serverip (str): The server IP address.
            - port (int): The server port number.
            - format (str): The desired unit for displaying the data sent ('B', 'KB', or 'MB').
            - interval (int or float): The time interval for which the data transfer information is printed, in seconds.

    Returns:
        None (because the purpose of this function is to print out the statistics of an interval.)
    """
    # Calculate the amount data sent during this interval
    interval_sent = total_sent - last_interval_sent
    # Format the data to the format specified by the user
    sent_data = format_size(interval_sent, args.format)
    # Calculate the rate
    rate = calculate_rate(interval_sent, args.interval)

    print(TABLE_FORMAT.format(f"{args.serverip}:{args.port}",
                              f"{interval_start:.2f} - {interval_stop:.2f}",
                              f"{sent_data} {args.format}",
                              f"{rate:.2f} Mbps"))


def parse_num_bytes(num_string):
    """
    Description:
        This function takes a string representation of a size value with a unit (B, KB, or MB) and converts
        it to the corresponding value in bytes. If the input string is empty or None, the function returns None.

    Arguments:
        num_string (str): A string representing the size value with a unit (e.g., '1 KB', '500 MB').

    Returns:
        int or None: The size value in bytes if a valid input is provided, or None if the input is empty or None.
                     (Because script can only calculate numbers, not strings.)

    Raises:
        ValueError: If the specified unit in the input string is not one of the supported units ('B', 'KB', or 'MB').
    """
    if not num_string:
        return None

    # Dictionary to stores the supported units
    units = {'B': 1, 'KB': 1000, 'MB': 1000000}
    # The number and unit variables of the string input to store the values
    num, unit = num_string.strip().split()
    # Cast the string number value to an integer value.
    num = int(num)

    if unit not in units:
        raise ValueError("Invalid unit specified for --num. Supported units are 'B', 'KB', and 'MB'.")

    return num * units[unit]


def print_header(args):
    """
    Description:
        This function prints the header for the data transfer table based on the mode specified in the
        'args' namespace. If the 'server' attribute is set to True, it prints the header for the server mode,
        otherwise, it prints the header for the client mode.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
            - server (bool): A flag indicating the mode. If True, the server mode is used; otherwise, the client mode is used.

    Returns:
        None (because the purpose of this function is to print information to the user.)
    """
    if args.server:
        print(TABLE_FORMAT.format(f"ID", f"Interval", f"Received", f"Rate" "\n"))
    else:
        print(TABLE_FORMAT.format(f"ID", f"Interval", f"Transfer", f"Bandwidth" "\n"))


def print_final_result(ip, port, elapsed_time, data, rate, args):
    """
    Description:
        This function prints the final data transfer results in a table format. It includes the IP and port,
        the total elapsed time, the total data transferred in the desired unit, and the average transfer rate in Mbps.

    Arguments:
        ip (str): The IP address of the server.
        port (int): The server port number.
        elapsed_time (float): The total elapsed time of the data transfer, in seconds.
        data (float): The total amount of data transferred, in the desired unit (B, KB, or MB).
        rate (float): The average data transfer rate, in Mbps.
        args (Namespace): A namespace object containing the following attributes:
            - format (str): The desired unit for displaying the data sent ('B', 'KB', or 'MB').

    Returns:
        None (because the purpose of the function is to print information to the user.)
    """
    print(TABLE_FORMAT.format(f"{ip}:{port}", f"0.0 - {elapsed_time:.2f}", f"{data} {args.format}", f"{rate:.2f} Mbps"))


def print_server_info(args):
    """
    Description:
        This function prints the server information, including the port number on which the server is listening,
        in a formatted manner. It displays a header and footer with dashes to separate the information from other outputs.

    Arguments:
    args (Namespace): A namespace object containing the following attributes:
        - port (int): The server port number.

    Returns:
        None (because the purpose of the function is to print information to the user.)
    """
    print("------------------------------------------------------------")
    print(f"       A simpleperf server is listening on port {args.port}")
    print("------------------------------------------------------------\n")


def handle_client(address, connection, args, print_lock):
    """
    Description:
        This function handles the data transfer from a connected client. It prints server and client
        information, receives the data sent by the client, and calculates the total data received,
        elapsed time, and data transfer rate. It then prints the final result in a table format.

    Arguments:
        address (tuple): A tuple containing the client's IP address and port number.
        connection (socket): A socket object representing the connection to the client.
        args (Namespace): A namespace object containing the following attributes:
            - bind (str): The server's bind address.
            - port (int): The server port number.
            - format (str): The desired unit for displaying the received data ('B', 'KB', or 'MB').
        print_lock (Lock): A threading.Lock object used to synchronize the print statements among threads.

    Returns:
        None (because this function is called from the server mode to handle incoming clients.)
    """
    # Print server information
    print_server_info(args)
    # Print client connection information
    print(f"A simpleperf client with {address[0]}:{address[1]} is connected with {args.bind}:{args.port}\n")

    # Initialize start time for data transfer
    start_time = time.time()
    # Initialize total_received variable to store the total amount of data received
    total_received = 0
    # Receive data from the client
    data = connection.recv(BUFFER_SIZE)

    # Process the received data
    while data:
        # Check if the received data is the 'BYE' message
        if b'BYE' in data:
            # Send an acknowledgement and terminate the connection
            connection.sendall(b'ACK: BYE')
            total_received += len(data) - len(b'BYE')
            break
        # Increment the total_received variable by the length of the received data
        total_received += len(data)
        # Receive more data from the client
        data = connection.recv(BUFFER_SIZE)

    # Close the connection to the client
    connection.close()

    # Calculate the elapsed time for the data transfer
    elapsed_time = time.time() - start_time
    # Format the total_received data using the specified unit
    received_data = format_size(total_received, args.format)
    # Calculate the data transfer rate
    rate = calculate_rate(total_received, elapsed_time)

    # Print the final result within the context of the print_lock
    with print_lock:
        print_header(args)
        print_final_result(args.bind, args.port, elapsed_time, received_data, rate, args)
        print("\n")


def server_mode(args):
    """
    Description:
        This function sets up and runs a server in server mode. It creates a server socket, binds it to
        the specified address and port, and listens for incoming client connections. For each client connection,
        it spawns a new process using multiprocessing to handle the client's data transfer. The server continues
        running until a KeyboardInterrupt occurs, at which point the server socket is closed.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
            - bind (str): The server's bind address.
            - port (int): The server port number.
            - format (str): The desired unit for displaying the received data ('B', 'KB', or 'MB').

    Returns:
        None (because this is a function that runs a loop, waiting for incoming clients.)
    """
    # Create a server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind the server socket to the specified address and port
    server_socket.bind((args.bind, args.port))
    # Set the server socket to listen for incoming connections
    server_socket.listen(5)

    # Print server information
    print_server_info(args)
    # Create a print_lock to synchronize print statements among processes
    print_lock = multiprocessing.Lock()

    try:
        # Continuously accept incoming client connections
        while True:
            # Accept a client connection
            connection, address = server_socket.accept()
            # Create a new process to handle the client's data transfer
            client_process = multiprocessing.Process(target=handle_client, args=(address, connection, args, print_lock))
            # Start the client_process
            client_process.start()
    except KeyboardInterrupt:
        # Handle the KeyboardInterrupt to stop the server
        print("Keyboard interrupt: Stopping server.")
    finally:
        # Close the server socket
        server_socket.close()


def print_client(args):
    """
    Description:
        This function prints the client information, including the server IP address and port number
        it is connecting to, in a formatted manner. It displays a header and footer with dashes to
        separate the information from other outputs.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
            - serverip (str): The server's IP address.
            - port (int): The server port number.

    Returns:
        None (because the purpose of this function is to print information to the user.)
    """
    print("------------------------------------------------------------")
    print(f"A simpleperf client connecting to server {args.serverip}, port {args.port}")
    print("------------------------------------------------------------\n")


def print_client_connection(args, client_ip, client_port):
    """
    Description:
        This function prints the client connection information in a formatted manner. It displays
        the client's IP address and port number if multiple clients are running in parallel, otherwise,
        it only prints the server IP address and port number the client is connecting to.

    Arguments:
    args (Namespace): A namespace object containing the following attributes:
        - serverip (str): The server's IP address.
        - port (int): The server port number.
        - parallel (int): The number of parallel clients.
    client_ip (str): The client's IP address.
    client_port (int): The client's port number.

    Returns:
        None (because the purpose of this function is to print information to the user.)
    """
    if args.parallel > 1:
        print(f"Client {client_ip}:{client_port} connected with {args.serverip} port {args.port}")
    else:
        print(f"Client connected with {args.serverip} port {args.port}\n")


def create_parallel_connections(args):
    """
    Description:
        This function creates multiple parallel connections to the server using multiprocessing.
        For each parallel connection, it creates a new process and runs the client_connection function.
        Once all processes are completed, it prints the header and final results for each connection.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
        - serverip (str): The server's IP address.
        - port (int): The server port number.
        - parallel (int): The number of parallel clients.
        - format (str): The desired unit for displaying the received data ('B', 'KB', or 'MB').

    Returns:
        None (because this function is called from client mode to create connections.)
    """
    # Create a Manager object to manage shared resources across processes
    manager = multiprocessing.Manager()
    # Create a shared list to store the results from each process
    results_list = manager.list()

    # Initialize an empty list to store the created processes
    processes = []

    # Create a process for each parallel connection
    for conn in range(args.parallel):
        process = multiprocessing.Process(target=client_connection, args=(args, results_list))
        process.start()
        processes.append(process)

    # Wait for all processes to complete
    for process in processes:
        process.join()

    if args.parallel > 1:
        print("\n")

    # Print the header and the results after all processes have completed
    print_header(args)
    for result in results_list:
        print_final_result(*result, args)


def client_connection(args, results_list):
    """
    Description:
        This function establishes a connection to the server and sends data for a specified amount of time,
        or until a specified number of bytes have been sent. It also prints the client connection information,
        sends data in intervals, and appends the final results to the shared results_list.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
            - serverip (str): The server's IP address.
            - port (int): The server port number.
            - interval (float): Time interval (in seconds) between printing status updates.
            - time (float): The total duration (in seconds) for sending data.
            - num (str): The total amount of data to send, specified with a unit ('B', 'KB', or 'MB').
            - format (str): The desired unit for displaying the received data ('B', 'KB', or 'MB').
            - parallel (int): The number of parallel clients.
        results_list (List): A shared list managed by the Manager object to store the results from each process.

    Returns:
        None (because this functions establishes a connection to a server.)

    Raises:
        socket.timeout: Raised if there is a timeout while waiting for an acknowledgement from the server.
    """
    # Create a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the client socket to server specified by user
    client_socket.connect((args.serverip, args.port))
    # Set a timeout for the client socket
    client_socket.settimeout(5)

    # Initialize the current time as start time
    start_time = time.time()
    # Initialize total data sent in number of bytes
    total_sent = 0
    # Initialize the data sent during the last interval
    last_interval_sent = 0
    # Creating a bytes object to store data sent from the client
    data_to_send = b'0' * BUFFER_SIZE
    # Initialize the interval start variable
    interval_start = 0
    # Initialize the interval stop variable
    interval_stop = args.interval
    # Initialize the remaining bytes to send
    remaining_bytes = 0
    # The minimum duration, helps the script make time to calculate if the amount of data is very low
    min_duration = 0.1

    # Get the client's IP address and port number
    client_ip, client_port = client_socket.getsockname()

    # Print the client connection information
    print_client_connection(args, client_ip, client_port)

    # Parse the total number of bytes to send, if specified
    if args.num:
        remaining_bytes = parse_num_bytes(args.num)

    # Send data to the server, while tracking intervals and remaining bytes
    while True:
        elapsed_time = time.time() - start_time

        if (args.interval > 0) & (elapsed_time >= interval_stop):
            print_interval(total_sent, last_interval_sent, interval_start, interval_stop, args)
            last_interval_sent = total_sent
            interval_start = interval_stop
            interval_stop += args.interval

        if elapsed_time >= args.time:
            break

        if args.num:
            if remaining_bytes <= 0:
                break
            data_to_send = data_to_send[:remaining_bytes]
            remaining_bytes -= len(data_to_send)

        client_socket.sendall(data_to_send)
        total_sent += len(data_to_send)

    # Initialize the remaining duration
    remaining_duration = min_duration - elapsed_time

    # Wait for the remaining duration, if any
    if remaining_duration > 0:
        time.sleep(remaining_duration)

    # Send a BYE message to the server
    client_socket.sendall(b'BYE')

    # Receive the acknowledgement from the server
    try:
        acknowledgement = client_socket.recv(1024)
    except socket.timeout:
        print("Error: Timeout while waiting for acknowledgement from server.")
        client_socket.close()
        return

    if args.interval > 0:
        print("\n------------------------------------------------------------\n")

    # Process the final results
    if acknowledgement == b'ACK: BYE':
        elapsed_time = time.time() - start_time
        sent_data = format_size(total_sent, args.format)
        rate = calculate_rate(total_sent, elapsed_time)

        results_list.append((args.serverip, args.port, elapsed_time, sent_data, rate))
    else:
        print("Error: Invalid acknowledgement message received from server.")

    client_socket.close()


def client_mode(args):
    """
    Description:
        This function runs the client mode, which first prints the client information, then
        creates parallel connections to the server by calling the create_parallel_connections function.

    Arguments:
        args (Namespace): A namespace object containing the following attributes:
            - serverip (str): The server's IP address.
            - port (int): The server port number.
            - interval (float): Time interval (in seconds) between printing status updates.
            - time (float): The total duration (in seconds) for sending data.
            - num (str): The total amount of data to send, specified with a unit ('B', 'KB', or 'MB').
            - format (str): The desired unit for displaying the received data ('B', 'KB', or 'MB').
            - parallel (int): The number of parallel clients.

    Returns:
        None (because this function runs the client mode option.)
    """
    # Print the client information
    print_client(args)

    # Create parallel connections to the server
    create_parallel_connections(args)


def main():
    """
    Description:
        This function serves as the main entry point for the Simpleperf network performance tool. It parses the
        command-line arguments, checks if the server is started in server or client mode, and then calls the
        appropriate functions.

    Returns:
        None (because its primary purpose is to serve as the entry point for the program)
    """
    parser = argparse.ArgumentParser(description='Simpleperf network performance tool')
    parser.add_argument('-s', '--server', action='store_true',
                        help='enable server mode')
    parser.add_argument('-b', '--bind', type=str, default=DEFAULT_IP,
                        help='select the ip address of the server’s interface where the client should connect')
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT,
                        help='select port number on which the server should listen; the port must be an integer and in the range [1024, 65535]')
    parser.add_argument('-f', '--format', type=str, default=DEFAULT_FORMAT, choices=['B', 'KB', 'MB'],
                        help='choose the format of the summary of results - it should be either in B, KB or MB')
    parser.add_argument('-c', '--client', action='store_true',
                        help='enable client mode')
    parser.add_argument('-I', '--serverip', type=str, default='',
                        help='specify the IP address of the server in client mode')
    parser.add_argument('-t', '--time', type=int, default=DEFAULT_DURATION,
                        help='the total duration in seconds for which data should be generated, also sent to the server (if it is set with -t flag at the client side) and must be > 0. NOTE If you do not use -t flag, your experiment should run for 25 seconds')
    parser.add_argument('-i', '--interval', type=int, default=0,
                        help='print statistics per z seconds')
    parser.add_argument('-P', '--parallel', type=int, default=1, choices=range(1, 6),
                        help='creates parallel connections to connect to the server and send data - it must be 1 and the max value should be 5 - default:1')
    parser.add_argument('-n', '--num', type=str, default='',
                        help='transfer number of bytes specified by -n flag, it should be either in B, KB or MB. e.g "20000 B", "3000 KB", "200 MB"')

    args = parser.parse_args()

    # Checking if the server is started in either server or client mode, if not, exit.
    if not args.server and not args.client:
        print('Error: you must run either in server or client mode')
        sys.exit(1)

    # Running server or client mode depending on the arguments
    if args.server:
        server_mode(args)
    else:
        # Checking if the time option value is greater than 0
        if args.time > 0:
            client_mode(args)
        else:
            print("Error: the -t (time) operation must be greater that 0.")


if __name__ == "__main__":
    main()
