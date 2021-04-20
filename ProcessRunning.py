import io
import os

"""Test file"""

def header_indices(header):
    """Helper function, returns the starting indices of the column names"""

    for i in range(0, len(header)):
        if header[i] == 'P':
            p = i
        if header[i] == 'T':
            t = i
            break
    return (0, p, t)

def get_running_process() -> str:
    # Query the processes
    output = io.StringIO(os.popen('wmic process get processid, threadcount, description').read())
    
    header = output.readline()
    (d, p, t) = header_indices(header)
    L = ''
    for line in output.readlines():
        line = line[0:len(line) - 1]
        if line == '':
            continue
        else:
            L += line[d:p].rstrip() + ',' + line[p:t].rstrip() + ',' + line[t:len(line)].rstrip() + '\n'

    return L
