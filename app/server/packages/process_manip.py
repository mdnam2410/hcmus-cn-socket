import os
import subprocess
import re

def _get_process():
    s = os.popen('wmic process get processid, threadcount, description').read()
    s = s.strip()
    L = []
    processes = s.split('\n\n')
    processes = processes[1:]
    for p in processes:
        m = re.match(r'^(.+?)\s+(\d+)\s+(\d+)\s*$', p)
        if m != None:
            L.append([m.group(i) for i in range(1, 4)])
    return L

def get_running_process() -> str:
    processes = _get_process()
    return '\n'.join([','.join(info) for info in processes])

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
    print(r.strip().split())
    pids = set(r.strip().split())

    result = []
    processes = _get_process()
    for process in processes:
        if process[1] in pids:
            result.append(process)
    return '\n'.join([','.join(info) for info in result])

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
