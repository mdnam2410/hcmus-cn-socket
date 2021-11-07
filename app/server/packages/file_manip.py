import os
import shutil
import win32api

#   DWORD    dwFileAttributes;
#   FILETIME ftCreationTime;
#   FILETIME ftLastAccessTime;
#   FILETIME ftLastWriteTime;
#   DWORD    nFileSizeHigh;
#   DWORD    nFileSizeLow;
#   DWORD    dwReserved0;
#   DWORD    dwReserved1;
#   CHAR     cFileName[MAX_PATH];
#   CHAR     cAlternateFileName[14];

def all_list(path: str):
    r = ''
    if path == "disk":
        drives = win32api.GetLogicalDriveStrings()
        drives = drives.split('\000')[:-1]
        r = ','.join(drives)
        return r
    else:
        res = []
        try:
            # path be like this: C:\\Folder
            path += "\\*"
            raw = win32api.FindFiles(path)
            if len(raw) != 0:
                for i in raw:
                    res.append(i[-2])
        except:
            raise Exception("Command cannot execute")
        finally:
            return ', '.join(res)

def rename_file(pathDestDir: str, old_name: str, new_name: str):
    print(pathDestDir, old_name, new_name)
    filePath = os.path.join(pathDestDir, old_name)
    newFilePath = os.path.join(pathDestDir, new_name)
    print(filePath)
    print(newFilePath)
    try:
        shutil.move(filePath, newFilePath)
    except:
        raise Exception("No such file or directory.")
    return 1

def remove_F(filePath: str):
    print(filePath)
    if os.path.isfile(filePath):
        os.remove(filePath)
    elif os.path.isdir(filePath):
        shutil.rmtree(filePath)
    else:
        raise Exception("Path not exists")
        return 0
    return 1

def receive_to_server(folderPath: str, fileName: str, content):
    filePath = os.path.join(folderPath, fileName)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    with open(filePath, 'w') as f:
        f.write(content)
    return 1

def send_to_client(folderPath: str, fileName: str):
    r = ''
    filePath = os.path.join(folderPath, fileName)
    if os.path.isdir(filePath):
        raise Exception("It not a file to download.")
    else:
        with open(filePath, 'r') as f:
            r = f.read()
        return r