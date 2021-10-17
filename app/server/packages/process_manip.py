import io
import os
import subprocess

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
        if line != '':
            L += line[d:p].rstrip() + ',' + line[p:t].rstrip() + ',' + line[t:len(line)].rstrip() + '\n'

    return L

def get_running_applications():
    # Get a set of PID of running applications
    r = subprocess.run(
        ['powershell',
        '-Command',
        'Get-Process | Where-Object {$_.mainWindowTitle} | Format-Table Id -HideTableHeaders'],
        capture_output=True
    )
    if r.returncode != 0:
        return None
    r = r.stdout.decode('ascii')
    s = set()
    for pid in r.splitlines():
        if pid != '':
            s.add(pid.strip())

    # Get processes information
    output = io.StringIO(os.popen('wmic process get processid, threadcount, description').read())
    header = output.readline()
    (d, p, t) = header_indices(header)
    L = ''
    for line in output.readlines():
        line = line[0:len(line) - 1]
        if line != '':
            pid = line[p:t].rstrip()
            # Join with s
            if pid in s:
                L += line[d:p].rstrip() + ',' + pid + ',' + line[t:].rstrip() + '\n'
    return L

def start(name):
    name = name[0:len(name) - 1] # Remove new line
    r = subprocess.run(
        ['powershell', '-Command', f'Start-Process -FilePath "{name}"'],
        capture_output=True
    )
    print(r.returncode)
    return r.returncode == 0

def kill(pid):
    r = subprocess.run(
        ['powershell', '-Command', f'Stop-Process -ID {pid}'],
        capture_output=True
    )
    
    if r.returncode == 0:
        return 0
    else:
        s = r.stderr.decode('ascii')
        s, _ = tuple(s.split('\n', 1))
        _, s = tuple(s.split(':', 1))
        s = s.strip()
        if s.startswith('Cannot find'):
            return 1
        elif s.endswith('Access is denied'):
            return 2
        else:
            return 3
