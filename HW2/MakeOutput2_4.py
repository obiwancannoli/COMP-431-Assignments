# Description: Valid sequence with some invalid commands in it
#  1. Early Quit

import sys


sys.stdout.write("220 COMP 431 FTP server ready.\r\n")
sys.stdout.write("QUIT\r\n")
sys.stdout.write("200 Command OK.\r\n")