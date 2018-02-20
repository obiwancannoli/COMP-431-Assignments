import sys
import shutil
import os

legalCommands = ["USER", "PASS", "TYPE", "SYST", "NOOP", "QUIT", "PORT", "RETR"]
casefoldCommands = [command.casefold() for command in
                    legalCommands]  # casefold commands for case-insensitive comparison
validUser = 0  # global variable for valid username; 1 = valid username provided
validLogin = 0  # global variable for valid login; 1 = valid login provided
validPort = 0  # global variable for valid ip address and port; 1 = valid port input provided
numOfRetrs = 0  # global variable for keeping count of successful RETR commands


def crlfcheck(x):
    binLine = x.encode('ascii')  # converts line to binary
    binList = list(binLine)  # creates a list of the characters in binary
    if not (binList[-1] == 10 and binList[-2] == 13):  # 10 = \r and 13 = \n
        return 0  # \r\n not found as last two parts of input
    return 1  # CRLF termination sequence found


def get_absolute_file_path(first_character_stripped_filepath):  # thank you Jisan for this <3
    current_working_directory = os.getcwd()
    absolute_file_path = current_working_directory + os.sep + first_character_stripped_filepath
    return absolute_file_path


sys.stdout.write("220 COMP 431 FTP server ready.\r\n")  # lets the user know that the server is up and ready

file = sys.stdin.read().splitlines(keepends=True)
for line in file:

    sys.stdout.write(line)
    splitLine = line.split()

    try:
        casefoldCommands.index(splitLine[0].casefold())  # checks for casefold command in list of accepted commands
    except ValueError:
        sys.stdout.write("500 Syntax error, command unrecognized.\r\n")  # error not legal command
        continue  # and it moves onto the next input

    try:
        if not all(ord(c) < 128 for c in splitLine[1]):
            if splitLine[0].casefold() == "user":
                sys.stdout.write("501 Syntax error in parameter.\r\n")  # prints an error if character in username
                continue  # is not in ascii character set
            elif splitLine[0].casefold() == "pass":
                sys.stdout.write("501 Syntax error in parameter.\r\n")  # prints an error if character in password
                continue  # is not in ascii character set

        if crlfcheck(line) == 1:  # checks if input has valid CRLF termination at the end
            if splitLine[0].casefold() == "user":
                sys.stdout.write("331 Guest access OK, send password.\r\n")
                validUser = 1  # if valid username was provided the valid Username field is set to 1
                validLogin = 0  # resets if valid username was put in again
                continue
            if splitLine[0].casefold() == "pass" and validUser == 1:
                sys.stdout.write("230 Guest login OK.\r\n")
                validLogin = 1  # if valid username and password were provided they are validLogin is set to 1
                continue
    except IndexError:
        if splitLine[0].casefold() == "user":
            sys.stdout.write("501 Syntax error in parameter.\r\n")  # prints an error if user command but no username
            continue
        elif splitLine[0].casefold() == "pass":
            sys.stdout.write("501 Syntax error in parameter.\r\n")  # prints an error if pass command but no password
            continue

    if splitLine[0].casefold() == "quit":
        bCommand = splitLine[0].encode('ascii')  # converts command to binary
        correctCommand = bCommand + b'\r\n'  # creates how command should be with no space in between
        if not correctCommand == line.encode('ascii'):  # if the input commands does not equal correct command
            sys.stdout.write("501 Syntax error in parameter.\r\n")  # error is thrown
            continue
        sys.stdout.write("200 Command OK.\r\n")
        break

    if not validLogin == 1:  # if the person is not logged in properly it will throw an error
        sys.stdout.write("530 Not logged in.\r\n")
        continue

    if splitLine[0].casefold() == "type":
        try:
            if not (splitLine[1] == "A" or splitLine[1] == "I"):
                sys.stdout.write(
                    "501 Syntax error in parameter.\r\n")  # if code is not A or I it will sys.stdout.write an error
                continue
            if crlfcheck(line) == 1:  # checks for proper CRLF termination
                if splitLine[1] == "A":
                    sys.stdout.write("200 Type set to A.\r\n")
                    continue
                elif splitLine[1] == "I":
                    sys.stdout.write("200 Type set to I.\r\n")
                    continue
        except IndexError:
            sys.stdout.write(
                "501 Syntax error in parameter.\r\n")  # if there is nothing after type command an error is printed
            continue

    if splitLine[0].casefold() == "syst" or splitLine[0].casefold() == "noop":
        bCommand = splitLine[0].encode('ascii')  # converts command to binary
        correctCommand = bCommand + b'\r\n'  # creates how command should be with no space in between
        if not correctCommand == line.encode('ascii'):  # if the input commands does not equal correct command
            sys.stdout.write("501 Syntax error in parameter.\r\n")  # error is thrown
            continue
        if splitLine[0].casefold() == "syst":
            sys.stdout.write("215 UNIX Type: L8.\r\n")
            continue
        sys.stdout.write("200 Command OK.\r\n")  # sys.stdout.writes Command OK if proper NOOP command input
        continue

    if splitLine[0].casefold() == "port":

        if crlfcheck(line) == 1:  # checks for CRLF termination sequence
            try:
                splitAddress = splitLine[1].split(",")  # splits the input at each comma
            except IndexError:
                sys.stdout.write(
                    "501 Syntax error in parameter.\r\n")  # error if there it is not properly formatted with commas
                continue
            if not len(splitAddress) == 6:
                sys.stdout.write(
                    "501 Syntax error in parameter.\r\n")  # input does not have 6 numbers needed for port command
                continue
            if not all(0 <= int(n) <= 255 for n in splitAddress):  # range of integers not between 0 and 255
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                continue
            try:
                for n in splitAddress:
                    int(n)  # tries to convert string to integer to see if it is input has integers
            except ValueError:
                sys.stdout.write("501 Syntax error in parameter.\r\n")  # input does not contain only integers
                continue
            portAddress = (int(splitAddress[-2]) * 256) + int(splitAddress[-1])  # calculates the port address
            del splitAddress[-1]  # removes the last number
            del splitAddress[-1]  # removes the second to last number
            ipAddress = ".".join(splitAddress)
            sys.stdout.write("200 Port command successful (%s,%s).\r\n" % (ipAddress, portAddress))
            validPort = 1  # a valid port number was provided
            continue
        sys.stdout.write("501 Syntax error in parameter.\r\n")  # no CRLF terminator found
        continue

    if splitLine[0].casefold() == "retr":
        if validPort == 0:  # no valid port has been established yet
            sys.stdout.write("503 Bad sequence of commands.\r\n")
            continue
        if crlfcheck(line) == 1:  # checks for CRLF termination sequence
            if splitLine[1][0] == "/":  # if beginning is '/' character cut it off the top
                retrCommand = splitLine[1][1:]
            if ord(splitLine[1][0]) == 92:  # if beginning is '\' character cut it off the top
                retrCommand = splitLine[1][1:]
            retrCommand = splitLine[1]  # otherwise assume there is a '/' or '\' by process of elimination
            if not all(
                    ord(c) < 128 for c in retrCommand):  # makes sure that the path token is within ascii character set
                sys.stdout.write("501 Syntax error in parameter.\r\n")
                continue
        stringCommand = get_absolute_file_path(retrCommand)  # converts path token into string
        try:
            shutil.copy(stringCommand, "retr_files")
            sys.stdout.write("150 File status okay.\r\n")
            numOfRetrs += 1  # adds 1 to number of successful
        except FileNotFoundError:
            sys.stdout.write("550 File not found or access denied.\r\n")  # file was not found
            continue
        newName = "file" + str(numOfRetrs)  # file + number of successful retr commands is the new filename
        newName = "retr_files/" + newName  # creates the new name for the file
        oldName = "retr_files/" + str(retrCommand)  # string for old name
        os.rename(oldName, newName)  # renames the file
        validPort = 0  # resets validPort variable for another pair of PORT and RETR commands
        sys.stdout.write("250 Requested file action completed.\r\n")
        continue
