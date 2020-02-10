import sys
import socket
import subprocess
import time
import datetime
import getopt
import threading

def port_scanner(ip, ports):

    # Add a percentage to signify how far the scanner is
    # Write results to a text file

    current_one = time.time()

    count = 0

    for port in range(1, ports):

        try:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(100)
            s.connect((ip, port))
            print("")
            print('#################################')
            print("")
            print("Port %d:OPEN" % (port))
            print("")
            print('#################################')
            print("")
            s.close()
            count += 1
            percent = count / ports
            print("The scanner is", percent, "% finished.")

        except:
            count += 1
            percent = count / ports
            print("The scanner is", percent, "% finished.")
            continue

        current_two = time.time()

        finished_time = current_two - current_one

        print("")
        print("The scanner has finished in %f seconds" % (finished_time))

print('')
print('#################################')
print('')
print('______  _____   ___ ______ _____ ')
print('| ___ \/  __ \ / _ \|  _  \  ___|')
print('| |_/ /| /  \// /_\ \ | | | |__  ')
print('| |_/ /| /  \// /_\ \ | | | |__  ')
print('| |\ \ | \__/\| | | | |/ /| |___ ')
print('\_| \_| \____/\_| |_/___/ \____/ ')
print('')
print('RCADE framework')
print('')
print('Version 1.0')
print('')
print('#################################')
print('')
print('Options: ')
print('1: Port scanner')
print('2: Ping sweep')
print('3: Network multitool')
print('4: Password-list generator')
print('5: FTP password cracker')
print('6: SSH password cracker')
print('7: Banner grabber')
print('')
print('#################################')
print('')

attack = int(input('Please choose an option: '))

if attack == 1:

    print("")
    ip = str(input("Please enter an IP-adress: "))
    print("")
    ports = int(input("Please enter the port you would like to scan up to: "))
    print("")
    ports += 1
    port_scanner(ip, ports)
