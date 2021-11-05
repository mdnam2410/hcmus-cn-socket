# Project details

## 1. Functions need to implement
### 1.1 Screenshot
Features:
1. Taking screenshot from the server
2. Save the screenshot

### 1.2 Running Processes
Features:
1. Get the list of running processes from the server (including process name, ID, and count thread)
2. Kill a process given the process ID
3. Start a process given the process name

### 1.3 Running Applications
Features (similar to running processes):
1. Get the list running applications from the server (including application name, ID, and count thread)
2. Kill an application given the app ID
3. Start a application given the app name

### 1.4 Keylogging
Features:
1. Hooking/unhooking
2. Print the hooked keystrokes

### 1.5 Modifying registries
Features:
1. Modifying registries by sending a .reg file to the server
2. Direct modifying registries by specifying paths and new values. The types of modification:
    * Get values
    * Set values
    * Delete values
    * Create new keys
    * Delete keys

## Shutdown
Feature: Shut the server down

## 2 Client and server message structure
Messages are encoded in ASCII format.
### 2.1 Client messages
All client messages will have the following structure:
```
<command> [<option>]
<data>
```
Where:
* `command` field: A command corresponds to each function, e.g. `process` for the Running Processes function (full list shown later.)
* `option` field: (may be empty) specifies what type of a command, e.g `process kill` to kill a running process.
* `data` field: the data going along with the `command`. For example: `process kill\n123`. This message tells the server to kill the process having ID 123. If the `data` field contains many units, each separated by a `\n`.

### 2.2 Server messages
All server messages will have the following structure:
```
<error code> <message>
<data>
```
Where:
* `error code` field: A three-digit number. `000` is default for no error. All error codes other than `000` indicate that errors have occured at the server (full list of error codes shown later.)
* `message` field: A string describing what the `error code` means. `OK` is the default message for error code `000`.
* `data`: The data returned by the server to the client requirements (e.g. bytes for sreenshot).

## 3 Commands
Scope | Command | Option | Data | Description
-------- | ------- | ------ | ---- | -----------
Screenshot | `screenshot` | `<none>` | `<none>` | Require a screenshot (in JPG (PNG?) format)
Screen live streaming | `stream` | `<none>` | `<none>` | Request for screen streaming
Screen live streaming | `stream` | `start` | `<none>` | Start streaming
Screen live streaming | `stream` | `restart` | `<none>` | Restart streaming
Screen live streaming | `stream` | `pause` | `<none>` | Pause streaming
Screen live streaming | `stream` | `stop` | `<none>` | Stop streaming
Running Processes | `process` | `list` | `<none>` | Require a list of processes
Running Processes | `process` | `kill` | `<PID>` | Kill processes
Running Processes | `process` | `start` | `<process name>` | Start processes
Running Applications | `app` | `list` | `<none>` | Require a list of processes
Running Applications | `app` | `kill` | `<PID>` | Kill applications
Running Applications | `app` | `start` | `<application name>` | Start applications
Keylogging | `keylogging` | `hook` | `<none>` | Start hooking
Keylogging | `keylogging` | `unhook` | `<none>` | Stop hooking. The server automatically returns the hooked keystrokes.
Keylogging | `keylogging` | `lock` | `<none>` | Lock keyboard
Keylogging | `keylogging` | `unlock` | `<none>` | Unlock keyboard
Modifying Registries | `reg` | `send` | `<.reg file>` | Send the registry file to the server
Modifying Registries | `reg` | `get` | `<path to registry>` | Get the registry value
Modifying Registries | `reg` | `set` | `<path to registry>,<new value>,<value type>` | Set the registry value
Modifying Registries | `reg` | `delete` | `<path to registry>` | Delete the registry
Modifying Registries | `reg` | `create-key` | `<new registry key>` | Create new registry key
Modifying Registries | `reg` | `delete-key` | `<path to registry>` | Delete registry key
File system | `file` | `TBD` | `TBD` | Work on file system
Machine | `machine` | `shutdown` | `<none>` | Shut the server down
Machine | `machine` | `log-out` | `<none>` | Log out
Machine | `machine` | `mac` | `<none>` | Get MAC address



## 4 Status codes
The following table shows the status codes used in this socket application.

Scope | Status code | Message | Description
-------- | ---------- | ------- | -----------
General error | `000` | `OK` | No error. All tasks done successfully.
General error | `001` | `Server not running` | Cannot contact the server because it is not running.
General error | `002` | `Server shut down` | The server shut down by any mean, e.g. task kill, computer shut down, keyboard interrupt (Ctrl + C)
General error | `003` | `Unrecognized command` | Unrecognized command
General error | `004` | `Unknown error` | Unknown error
Screenshot | `100` | `Cannot take screenshot` | Cannot take screenshot
Running Processes | `200` | `Process not running` | Client tries to kill a process that is not running
Running Processes | `201` | `Kill request is denied` | Denied for many reasons, e.g. trying to kill a system process, etc.
Running Processes | `202` | `Cannot kill process` | Cannot kill a running process (OS doesn't allow, for example)
Running Processes | `203` | `Process not found` | Cannot find the process specified
Running Applications | `300` | `Application not running` | Client tries to kill an application that is not running
Running Applications | `301` | `Kill request is denied` | Denied for many reasons, e.g. trying to kill a system process, etc.
Running Applications | `302` | `Cannot kill application` | Cannot kill a running application
Running Applications | `303` | `Application not found` | Cannot find the application specified
Machine | `500` | `Cannot shutdown` | Cannot shutdown the server
Machine | `501` | `Cannot log out` | Cannot log out
Machine | `502` | `Cannot get MAC address` | Cannot get MAC address
