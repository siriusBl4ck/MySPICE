# MySPICE v0.1 by Saurav Sachin Kale EE19B141
# EE2703 : Applied Programming Lab

from sys import argv

print("MySPICE v0.1")

from Keywords import *
from Component import *
from Logging import *

#circuit will be a list of components
ckt = []

# extract the filepath of netlist file from command line arguments
try:
    netlistFile = argv[1]
except IndexError:
    # index 0 is "Spice1.py", index 1 should be filename, but if that isnt given, it will trigger Index out of range error
    print("ERROR : Netlist filepath not specified!")
    exit()

print("Loading file : ", netlistFile)

# open the file specified by the path
try:
    f = open(netlistFile)
except FileNotFoundError:
    print("ERROR: The netlist filepath you supplied is either incorrect, or no such file exists!")
    exit()

# stores all the netlist as a list of strings, each string being each line of the netlist
lines = f.readlines()

# Printing contents of read file
print("=======FILE CONTENTS======")
for e in lines:
    print(e, end='')
print("========END OF FILE=======")

print ("Netlist loaded successfully. Parsing...")

# this function checks if the values in validWords (list of parsed tokens) at the given indices toBeChecked are alphanumeric or not
def checkAlpha(validWords, toBeChecked, line_num):
    for i in toBeChecked:
        if not validWords[i].isalnum():
            log("INVALID_VALUE", "arguments specified are not of alphanumeric type!!!", line_num)
            exit()

# parse each line between CKT_BEGIN and CKT_END:
foundBeginning = False
foundEnd = False

for i in range(len(lines)):
    words = lines[i].split()

    if words[0] == CKT_BEGIN:
        foundBeginning = True
        continue
    elif words[0] == CKT_END:
        foundEnd = True
        break

    # this is the valid part of circuit
    if foundBeginning and not foundEnd:
        # extract the valid keywords from the line
        validWords = []

        # get rid of comments if any on the same line
        for e in words:
            if e[0] == '#':
                break
            else:
                validWords.append(e)

        # if there are no commands in the line, skip it, it probably contains only comments
        if (len(validWords) == 0):
            continue

        #parse the valid keywords
        if validWords[0][0] in [COM_RESISTOR, COM_CAPACITOR, COM_INDUCTOR, SRC_V, SRC_C]:
            # NAME n1 n2 VALUE
            # verify this syntax and feed it into the component object
            if len(validWords) != 4:
                if (len(validWords) > 4):
                    log("PARSING", "too many arguments for component!", i, lines[i])
                else:
                    log("PARSING", "too few arguments for component!", i, lines[i])
                exit()
            else:
                checkAlpha(validWords, [1, 2], i)
                print(validWords)
                try:
                    name = validWords[0]
                    type = validWords[0][0]
                    ports = []
                    ports.append(validWords[1])
                    ports.append(validWords[2])
                    dependencies = []
                    value = float(validWords[3])
                    ckt.append(Component(name, type, ports, dependencies, value))
                except ValueError:
                    log("INVALID_VALUE", "the arguments specified to component are not convertible to float!", i, lines[i])
                    exit()
        elif validWords[0][0] in [DEP_SRC_VCCS, DEP_SRC_VCVS]:
            # NAME n1 n2 n3 n4 VALUE
            # verify this syntax and feed it into the component object
            if len(validWords) != 6:
                if (len(validWords) > 6):
                    log("PARSING", "too many arguments for component!", i, lines[i])
                else:
                    log("PARSING", "too few arguments for component!", i, lines[i])
                exit()
            else:
                checkAlpha(validWords, [1, 2, 3, 4], i)
                print(validWords)
                try:
                    name = validWords[0]
                    type = validWords[0][0]
                    ports = []
                    ports.append(validWords[1])
                    ports.append(validWords[2])
                    dependencies = []
                    dependencies.append(validWords[3])
                    dependencies.append(validWords[4])
                    value = float(validWords[5])
                    ckt.append(Component(name, type, ports, dependencies, value))
                except ValueError:
                    log("INVALID_VALUE", "the arguments specified to component are not convertible to float!", i, lines[i])
                    exit()
        elif validWords[0][0] in [DEP_SRC_CCCS, DEP_SRC_CCVS]:
            # NAME n1 n2 V... VALUE
            # verify this syntax and feed it into the component object
            if len(validWords) != 5:
                if (len(validWords) > 5):
                    log("PARSING", "too many arguments for component!", i, lines[i])
                else:
                    log("PARSING", "too few arguments for component!", i, lines[i])
                exit()
            else:
                checkAlpha(validWords, [1, 2], i)
                # print(validWords)
                try:
                    name = validWords[0]
                    type = validWords[0][0]
                    ports = []
                    ports.append(validWords[1])
                    ports.append(validWords[2])
                    dependencies = []
                    dependencies.append(validWords[3])
                    value = float(validWords[4])
                    ckt.append(Component(name, type, ports, dependencies, value))
                except ValueError:
                    log("INVALID_VALUE", "the arguments specified to component are not convertible to float!", i, lines[i])
                    exit()
        else:
            log("PARSING", "No such component exists!", i, lines)
            # we are continuing because this error might happen due to the user forgetting to put .end()
            # if we put exit, then the user might be confused why its not detecting any component
            # by putting continue, we ensure that both messages appear (no such component and missing .end()) in case user forgets .end()
            continue

# check if .circuit and .end were detected
if not foundBeginning:
    log("PARSING", ".circuit not encountered in the file!!!")
    exit()
elif foundBeginning and (not foundEnd):
    log("PARSING", ".end corresponding to .circuit not found!!")
    exit()

# we have now populated the circuit
print("Parsing successful")
# we can traverse it in reverse order
for i in range(len(ckt) - 1, -1, -1):
    ckt[i].printInfo()