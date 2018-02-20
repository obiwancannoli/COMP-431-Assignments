# Description: Valid sequence with some invalid commands in it
#  1. Out of Sequence commands after user
#  2. Duplicate retr
#  3. Commands after quit
#
# WARNING: You must create your own file in the same directory called still_relative

import sys


sys.stdout.write("220 COMP 431 FTP server ready.\r\n")
sys.stdout.write("User kevin!!??\r\n")
sys.stdout.write("331 Guest access OK, send password.\r\n")
sys.stdout.write("sYSt\r\n")
sys.stdout.write("503 Bad sequence of commands.\r\n")
sys.stdout.write("pass password12345\r\n")
sys.stdout.write("230 Guest login OK.\r\n")
sys.stdout.write("tyPe A\r\n")
sys.stdout.write("200 Type set to A.\r\n")
sys.stdout.write("sYSt\r\n")
sys.stdout.write("215 UNIX Type: L8.\r\n")
sys.stdout.write("PorT 152,25,124,131,31,144\r\n")
sys.stdout.write("200 Port command successful (152.25.124.131,8080).\r\n")
sys.stdout.write("rEtr still_relative\r\n")
sys.stdout.write("150 File status okay.\r\n")
sys.stdout.write("250 Requested file action completed.\r\n")
sys.stdout.write("rEtr still_relative\r\n")
sys.stdout.write("503 Bad sequence of commands.\r\n")
sys.stdout.write("QUIT\r\n")
sys.stdout.write("200 Command OK.\r\n")

# TODO:Put commands after in input