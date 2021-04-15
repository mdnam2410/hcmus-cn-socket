# Functions need to implement

## Screenshot
Features:
1. Taking screenshot from the server
2. Save the screenshot

## Running Processes
Features:
1. Get the list of running processes from the server (including process name, ID, and count thread)
2. Kill a process given the process ID
3. Start a process given the process name

## Running Applications
Features (similar to running processes):
1. Get the list running applications from the server (including process name, ID, and count thread)
2. Kill an application given the app ID
3. Start a application given the app name

## Keylogging
Features:
1. Hooking/unhooking
2. Print the hooked keystrokes

## Modifying registries
Features:
1. Modifying registries by sending a .reg file to the server
2. Direct modifying registries by specifying paths and new values. The types of modification:
    * Get values
    * Set values
    * Delete values
    * Create new keys
    * Delete keys

## Shutdown
Feature: just fucking shut the server down

# Client and server message structure

## Client
All client messages will have the following structure:
```
<command> [<option>] CRLF
<data>
```
Where:
* `command` field: A command corresponds to each function, e.g. `process` for the Running Processes function (full list shown later.)
* `option` field: (may be empty) specifies what type of a command, e.g `process kill` to kill a running process.
* `CRLF`: Carriage return and line feed, equivalent to `\r\n` (most Internet protocols use these characters to specify new lines)
* `data` field: the data going along with the `command`. For example: `process kill CRLF 123`. This message tells the server to kill the process having ID 123. If the `data` field contains many units, each separated by a `CRLF`.

## Server
All server messages will have the following structure:
```
<error code> <message> CRLF
<data>
```
Where:
* `error code` field: A three-digit number. `000` is default for no error. All error codes other than `000` indicate that errors have occured at the server (full list of error codes shown later.)
* `message` field: A string describing what the `error code` means. `OK` is the default message for error code `000`.
* `data`: The data returned by the server to the client requirements (e.g. bytes for sreenshot).

# Commands
Function | Command | Option | Data | Description
-------- | ------- | ------ | ---- | -----------
Screenshot | `screenshot` | `<none>` | `<none>` | Require a screenshot (in JPG (PNG?) format)
Running Processes | `process` | `list` | `<none>` | Require a list of processes
Running Processes | `process` | `kill` | `<list of ID>` | Kill processes
Running Processes | `process` | `start` | `<list of ID>` | Start processes
Running Applications | `app` | `list` | `<none>` | Require a list of processes
Running Applications | `app` | `kill` | `<list of ID>` | Kill applications
Running Applications | `app` | `start` | `<list of ID>` | Start applications
Keylogging | `keylogging` | `hook` | `<none>` | Start hooking
Keylogging | `keylogging` | `unhook` | `<none>` | Stop hooking. The server automatically returns the hooked keystrokes
Modifying Registries | `reg` | `send` | `<.reg file>` | Send the registry file to the server
Modifying Registries | `reg` | `get` | `<path to registry>` | Get the registry value
Modifying Registries | `reg` | `set` | `<path to registry> CRLF <new value>` | Set the registry value
Modifying Registries | `reg` | `delete` | `<path to registry>` | Delete the registry
Modifying Registries | `reg` | `create` | `<new registry key>` | Create new registry key
Modifying Registries | `reg` | `delete-key` | `<path to registry>` | Create new registry key
Shutdown | `shutdown` | `<none>` | `<none>` | Shut the server down


# Error codes
The following table shows the error codes used in this socket application.

Function | Error code | Message | Description
-------- | ---------- | ------- | -----------
General error | `000` | `OK` | No error. All tasks done successfully.
General error | `001` | `Server not running` | Cannot contact the server because it is not running.
General error | `002` | `Server shut down` | The server shut down by any mean, e.g. task kill, computer shut down, keyboard interrupt (Ctrl + C)
General error | ... | ... | ...
Screenshot | `100` | `Cannot take screenshot` | For some fucking reason a screenshot cannot be taken
Screenshoht | ... | ... | ...
Running Processes | `200` | `Process not running` | Client tries to kill a process that is not running
Running Processes | `201` | `Cannot kill process` | Cannot kill a running process (OS doesn't allow, for example)
Running Processes | ... | ... | ...
