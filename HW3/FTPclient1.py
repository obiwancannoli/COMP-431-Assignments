import sys
import socket

legalCommands = ["connect", "get", "quit"]
validConnect = 0  # global variable for valid CONNECT request; 1 = valid CONNECT request
portNum = 8000
file = sys.stdin.read().splitlines(keepends=True)

for line in file:

    sys.stdout.write(line)
    splitLine = line.split()

    try:
        legalCommands.index(splitLine[0].casefold())  # checks if the command is in the list of legal commands
    except ValueError:
        print("ERROR -- request")
        continue

    if splitLine[0].casefold() == "connect":  # checks for server host validity
        try:
            extraInput = splitLine[3]  # checks for additional inputs outside of accepted number of parameters

            print("ERROR -- server-port")
            continue
        except IndexError:  # additional input not found, command is OK to pass
            pass

        try:
            secondCharTest = splitLine[1][1]  # domain should at least be two characters
        except IndexError:
            print("ERROR -- server-host")  # domain only had one character
            continue

        try:
            if splitLine[1][0] == ".":
                print("ERROR -- server-host")  # host name starts with a period, not valid
                continue
            splitHostName = splitLine[1].split(".")  # split all words of domain by period character
            hostNamesChars = "".join(splitHostName)  # joined all the chars together to check if in range
            if not (all(65 <= ord(c) <= 90 for c in hostNamesChars) | all(
                    97 <= ord(c) <= 122 for c in hostNamesChars) | all(48 <= ord(c) <= 57 for c in hostNamesChars)):
                print("ERROR -- server-host")  # host name was not A to Z or a to z or 0 to 9
                continue

        except IndexError:

            print("ERROR -- server-host")  # no server host provided
            continue

    if splitLine[0].casefold() == "connect":  # checks for server port validity
        try:
            int(splitLine[2])
        except ValueError:
            print("ERROR -- server-port")  # server-port was not decimal integer
            continue
        try:
            if not (0 <= int(splitLine[2]) <= 65535):
                print("ERROR -- server-port")  # server port number was not within range
                continue
            if int(splitLine[2][0]) == 0:  # server port number started with zero
                print("ERROR -- server-port")
                continue
        except IndexError:
            print("ERROR -- server-host")  # no server port provided
            continue
        print("CONNECT accepted for FTP server at host " + splitLine[1] + " and port " + splitLine[2])
        validConnect = 1  # valid CONNECT request
        portNum = 8000  # resets port number
        sys.stdout.write("USER anonymous\r\n")
        sys.stdout.write("PASS guest@\r\n")
        sys.stdout.write("SYST\r\n")
        sys.stdout.write("TYPE I\r\n")
        continue

    if splitLine[0].casefold() == "get":
        try:
            extraInput = splitLine[2]  # checks for additional inputs outside of accepted number of parameters
            print("ERROR -- pathname")
            continue
        except IndexError:  # additional input not found, command is OK to pass
            pass
        try:
            if not all(ord(c) < 128 for c in splitLine[1]):
                print("ERROR -- pathname")
                continue
        except IndexError:
            print("ERROR -- pathname")  # no pathname provided
            continue
        if validConnect != 1:
            print("ERROR -- expecting CONNECT")  # if no valid connect request no more commands can be made
            continue
        my_ip = socket.gethostbyname(socket.gethostname())
        ipSplit = my_ip.split(".")  # splits the host IP address into list
        firstNum = round(portNum // 256, 0)
        secondNum = portNum % 256
        ipSplit.append(str(firstNum))  # adds first number of port address to list
        ipSplit.append(str(secondNum))  # adds second number of port address to list
        hostName = ",".join(ipSplit)
        print("GET accepted for " + splitLine[1])
        sys.stdout.write("PORT " + hostName + "\r\n")
        sys.stdout.write("RETR " + splitLine[1] + "\r\n")
        portNum += 1
        continue

    if splitLine[0].casefold() == "quit":
        try:
            extraInput = splitLine[1]
            print("ERROR -- request")
            continue
        except IndexError:
            if validConnect != 1:
                print("ERROR -- expecting CONNECT")  # if no valid connect request no more commands can be made
                continue
            print("QUIT accepted, terminating FTP client")
            sys.stdout.write("QUIT\r\n")
            break
