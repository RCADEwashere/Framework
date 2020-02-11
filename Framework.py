import sys
import socket
import subprocess
import time
import datetime
import getopt
import threading

def port_scanner_write(ip, ports, path):

    fobj = open(path, 'w')

    current_one = time.time()

    count = 0

    open_ports = 0

    print("Starting port scan for %s." % (ip))
    print("")

    fobj.write("Starting port scan for %s.\n" % (ip))

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

            fobj.write("Port %d: OPEN\n" % (port))

            count += 1
            open_ports += 1
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
    print("The IP-adress %s has been scanned in %f seconds." % (ip, finished_time))
    print("")
    fobj.write("The IP-adress %s has been scanned in %f seconds.\n" % (ip,finished_time))

    if open_ports == 0:

        print("There are no open ports on %s." % (ip))

        fobj.write("There are no open ports on %s.\n" % (ip))

    elif open_ports == 1:

        print("There is 1 open port on %s." % (ip))

        fobj.write("There is 1 open port on %s.\n" % (ip))

    elif open_ports > 1:

        print("There are %d open ports on %s." % (open_ports, ip))

        fobj.write("There are %d open ports on %s.\n" % (open_ports, ip))

    print("")

    fobj.close()

def port_scanner(ip, ports):

    current_one = time.time()

    count = 0

    open_ports = 0

    print("Starting port scan for %s." % (ip))
    print("")

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
            open_ports += 1
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
    print("The IP-adress %s has been scanned in %f seconds." % (ip, finished_time))
    print("")

    if open_ports == 0:

        print("There are no open ports on %s." % (ip))

    elif open_ports == 1:

        print("There is 1 open port on %s." % (ip))

    elif open_ports > 1:

        print("There are %d open ports on %s." % (open_ports, ip))

    print("")

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
print('Version 0.1')
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
print('8: Password generator')
print('9: FTP server')
print('10: FTP client')
print('99: Exit')
print('')
print('#################################')
print('')

attack = int(input('Please choose an option: '))

if attack == 1:

    print("")
    ip = str(input("Please enter an IP-adress: "))

    if ip == "":

        print("")
        print("Invalid input! Exiting!")
        print("")
        sys.exit(0)

    print("")

    ports = int(input("Please enter the port you would like to scan up to: "))

    if ports == 0:  # Find out how to sys.exit(0) if no input for ports is given!

        print("")
        print("Invalid input! Exiting!")
        print("")
        sys.exit(0)

    print("")

    ports += 1

    write_user_input = str(input("Would you like to write the output of the scan to a file? "))

    if write_user_input == "Yes":

        print("")
        print("###########################################################")
        print("If the file already exists any content will be overwritten!")
        print("###########################################################")
        print("")

        path = str(input("Please specify an absolute path for the password file: "))

        print("")

        port_scanner_write(ip, ports, path)

    elif write_user_input == "No":

        print("")

        port_scanner(ip, ports)

    else:

        print("")
        print("Invalid input! Exiting!")
        print("")

        sys.exit(0)

if attack == 99:

    print("")
    print("Goodbye!")
    print("")

    sys.exit(0)
