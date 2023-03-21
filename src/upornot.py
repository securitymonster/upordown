#!/usr/bin/python3

# Seb - 21 March 2023

import csv
import time
import socket
import subprocess

# List of (IP address, port, description) tuples to check
ip_port_list = [("9.9.9.9", 53, "Quad9 DNS"), ("8.8.8.8", 53, "Google DNS"), ("195.130.130.2", 53, "Telenet DNS"),("www.telenet.be", 443, "Telenet website")]

# List of (IP address, description) tuples to check using ICMP test
ip_list = [("192.168.0.1", "Default Gateway LAN Telenet"), ("84.192.0.1", "Default Gateway WAN Telenet")]


# Time interval to check the IP addresses in seconds
check_interval = 60

# Output file name
output_file = "/var/log/upornot.csv"




# Open the output file in append mode
with open(output_file, 'a', newline='') as file:
    writer = csv.writer(file)

    # Write the header row if the file is empty
    if file.tell() == 0:
        writer.writerow(["Timestamp", "Host", "Port", "Description", "Status"])

    # Loop indefinitely
    while True:
        # Get the current time
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Loop through the list of (IP address, port, description) tuples
        for ip_port_desc in ip_port_list:
            ip, port, desc = ip_port_desc
            try:
                # Attempt to connect to the IP address and port
                socket.create_connection(ip_port_desc[:2], timeout=10)

                # If successful, write a row to the CSV file with the status "OK"
                writer.writerow([timestamp, ip, port, desc, "OK"])
                file.flush()
            except Exception as e:
                # If unsuccessful, write a row to the CSV file with the status "ERROR"
                writer.writerow([timestamp, ip, port, desc, "ERROR: " + str(e)])
                file.flush()

        # Loop through the list of (IP address, description) tuples to check using ICMP test
        for ip_desc in ip_list:
            ip, desc = ip_desc
            try:
                # Execute the ping command and discard output
                subprocess.check_output(['ping', '-c', '1', '-w', '1', ip], stderr=subprocess.STDOUT)

                # If successful, write a row to the CSV file with the status "OK"
                writer.writerow([timestamp, ip, "ICMP", desc, "OK"])
                file.flush()
            except subprocess.CalledProcessError as e:
                # If unsuccessful, write a row to the CSV file with the status "ERROR"
                writer.writerow([timestamp, ip, "ICMP", desc, "ERROR: " + str(e.output)])
                file.flush()

        # Wait for the specified time interval
        time.sleep(check_interval)
