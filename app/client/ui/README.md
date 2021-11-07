# Computer Network Exam Year 2

## This is repo of UI: Server and cliet

### Server
- Server is a computer that is controlled
- The "trojan" part will run in background
> nircmd hide trojan.bat


### Client
- Client is the remote computer controoled
- GUI control with function to:
	+ Input ip and port to 
		* Connect
		* Disconnect
	+ Screenshot
		* Take
		* Save
	+ Share screen (new)
		* Take
		* Record
	+ App/Process
		* Features (similar to running processes):
            1. Get the list running applications from the server (including application name, ID, and count thread)
            2. Kill an application given the app ID
            3. Start a application given the app name
	+ Regedit
		* Modifying registries by sending a .reg file to the server
		* Direct modifying registries by specifying paths and new values. The types of modification:
			* Get values
		    * Set values
		    * Delete values
		    * Create new keys
		    * Delete keys
	+ Keylogger
		* Hooking/unhooking
		* Print the hooked keystrokes
		* Lock/Unlock keyboard (new)
	+ Power control (new)
		* Shuttdown
		* Logout
		* Restart
		* Sleep

Show preview ui file:
pyuic5 -p name_file.ui