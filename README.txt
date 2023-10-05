---------------------------------------------------------
         Simpleperf Network Performance Tool
---------------------------------------------------------
Simpleperf is a network performance tool designed to measure the
bandwidth and transfer rate between a server and a client.
It can be used to analyze the performance of a network
connection by sending and receiving data in various formats and sizes.
The script can be run in server mode, client mode,
or both to perform the desired tests.

Features:
Server and client mode
Customizable IP address and port
Selectable data format (B, KB, MB)
Configurable total duration for data transfer
Optional interval-based statistics reporting
Support for parallel connections
Transfer a specific number of bytes

Requirements:
Python 3.x

How to use:
Run the script in server mode on the server machine by executing the following command:
python simpleperf.py --server

You can also set the IP address and port number for the server to listen on:
python simpleperf.py --server --bind <IP_ADDRESS> --port <PORT_NUMBER>

Run the script in client mode on the client machine by executing the following command:
python simpleperf.py --client --serverip <SERVER_IP> --port <SERVER_PORT>

You can also customize the data transfer duration,
format, interval-based statistics, parallel connections,
and number of bytes to transfer:
python simpleperf.py --client --serverip <SERVER_IP> --port <SERVER_PORT> --time
<DURATION> --format <FORMAT> --interval <INTERVAL> --parallel <PARALLEL_CONNECTIONS>
--num "<NUMBER_OF_BYTES>"

For example:
python simpleperf.py --client --serverip 10.0.0.2 --port 8088 --time 30 --format KB --interval 5 --parallel 2 --num "1000 KB"

Command-line arguments
-s, --server: Enable server mode
-b, --bind: Select the IP address of the server's interface where the client should connect (default: '10.0.0.2')
-p, --port: Select the port number on which the server should listen (default: 8088)
-f, --format: Choose the format of the summary of results - it should be either in B, KB, or MB (default: 'MB')
-c, --client: Enable client mode
-I, --serverip: Specify the IP address of the server in client mode
-t, --time: The total duration in seconds for which data should be generated and sent to the server (default: 25)
-i, --interval: Print statistics per z seconds (default: 0)
-P, --parallel: Create parallel connections to connect to the server and send data, with a maximum value of 5 (default: 1)
-n, --num: Transfer the number of bytes specified by the -n flag,
           it should be either in B, KB, or MB, e.g., "20000 B", "3000 KB", "200 MB" (default: '')

Example output:

Server side:
------------------------------------------------------------
       A simpleperf server is listening on port 8088
------------------------------------------------------------

A simpleperf client with 10.0.0.2:36038 is connected with 10.0.0.3:8088

      ID           Interval        Received          Rate
     
 10.0.0.3:8088    0.0 - 25.00     5011.712 MB    1603.96 Mbps 

Client side:
------------------------------------------------------------
A simpleperf client connecting to server 10.0.0.3, port 8088
------------------------------------------------------------

Client connected with 10.0.0.3 port 8088

      ID           Interval        Transfer       Bandwidth
   
 10.0.0.3:8088    0.0 - 25.00     5011.712 MB    1603.74 Mbps 
