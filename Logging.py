# Logging functionality
def log(code, message, line_num = None, line = None):
    print(code + "_ERROR: ", message)
    if (line_num != None):
        print("Location line: " + str(line_num + 1) + "] " + line)