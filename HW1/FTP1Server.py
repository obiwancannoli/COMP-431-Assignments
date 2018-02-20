import sys

legalCommands = ["USER", "PASS", "TYPE", "SYST", "NOOP", "QUIT", "PORT", "RETR"]
casefoldCommands = [command.casefold() for command in
                    legalCommands]  # casefold commands for case-insensitive comparison


def crlfcheck(x):
    binLine = x.encode('ascii')  # converts line to binary
    binList = list(binLine)  # creates a list of the characters in binary
    if not (binList[-1] == 10 and binList[-2] == 13):
        return 0
    return 1


print("220 COMP 431 FTP server ready.")  # lets the user know that the server is up and ready

file = sys.stdin.readlines()
for line in file:

    print(line.strip("\n"))
    splitLine = line.split()

    try:
        casefoldCommands.index(splitLine[0].casefold())  # checks for casefold command in list of accepted commands
    except ValueError:
        print("500 Syntax error, command unrecognized.")  # if command not legal command an error for command is printed
        continue  # and it moves onto the next input

    try:
        if not all(ord(c) < 128 for c in splitLine[1]):
            if splitLine[0].casefold() == "user":
                print("501 Syntax error in parameter.")  # prints an error if character in username
                continue  # is not in ascii character set
            elif splitLine[0].casefold() == "pass":
                print("501 Syntax error in parameter.")  # prints an error if character in password
                continue  # is not in ascii character set

        if crlfcheck(line) == 1:  # checks if input has valid CRLF termination at the end
            if splitLine[0].casefold() == "user":
                print("331 Guest access OK, send password.")
                validUser = 1  # if valid username was provided the valid Username field is set to 1
                continue
            if splitLine[0].casefold() == "pass" and validUser == 1:
                print("230 Guest Login OK.")
                validLogin = 1  # if valid username and password were provided they are validLogin is set to 1
                continue
    except IndexError:
        if splitLine[0].casefold() == "user":
            print("501 Syntax error in parameter.")  # prints an error if user command but no username
            continue
        elif splitLine[0].casefold() == "pass":
            print("501 Syntax error in parameter.")  # prints an error if pass command but no password
            continue

    if splitLine[0].casefold() == "type":
        try:
            if not (splitLine[1] == "A" or splitLine[1] == "I"):
                print("501 Syntax error in parameter.")  # if code is not A or I it will print an error
                continue
            if crlfcheck(line) == 1:  # checks for proper CRLF termination
                if splitLine[1] == "A":
                    print("200 Type set to A")
                    continue
                elif splitLine[1] == "I":
                    print("200 Type set to I")
                    continue
        except IndexError:
            print("501 Syntax error in parameter.")  # if there is nothing after type command it will print an error
            continue

    if splitLine[0].casefold() == "syst" or splitLine[0].casefold() == "noop" or splitLine[0].casefold() == "quit":
        bCommand = splitLine[0].encode('ascii')  # converts command to binary
        correctCommand = bCommand + b'\r\n'  # creates how command should be with no space in between
        if not correctCommand == line.encode('ascii'):  # if the input commands does not equal correct command
            print("501 Syntax error in parameter.")  # error is thrown
            continue
        if splitLine[0].casefold() == "syst":
            print("215 UNIX Type: L8.")
            continue
        print("200 Command OK.")  # prints Command OK if proper NOOP or QUIT command input
        continue

