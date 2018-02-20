import sys

file = sys.stdin.read().splitlines(keepends=True)


def crlfcheck(x):
    binLine = x.encode('ascii')  # converts line to binary
    binList = list(binLine)  # creates a list of the characters in binary
    if not (binList[-1] == 10 and binList[-2] == 13):  # 10 = \r and 13 = \n
        return 0  # \r\n not found as last two parts of input
    return 1  # CRLF termination sequence found


for line in file:

    sys.stdout.write(line)
    splitLine = line.split()

    try:
        if not (100 <= int(splitLine[0]) <= 599):  # reply code out of range (100 - 599)
            print("ERROR -- reply-code")
            continue
    except ValueError:
        print("ERROR -- reply-code")  # input is not valid decimal integer reply code
        continue
    try:
        replyString = "".join(splitLine[1:])
    except IndexError:
        print("ERROR -- reply-text")  # no reply text added
        continue

    if not all(ord(c) < 128 for c in replyString):  # reply text not in ascii character set
        print("ERROR -- reply-text")
        continue

    if crlfcheck(line) == 0:
        print("ERROR -- <CRLF>")  # no CRLF ending found
        continue

    print("FTP reply " + splitLine[0] + " accepted.  Text is : " + " ".join(splitLine[1:]))
