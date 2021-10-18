import app.core.protocol as protocol
import app.server.packages.keyboard_manip as keyboard_manip
import app.server.packages.machine_manip as machine_manip
import app.server.packages.process_manip as process_manip
import app.server.packages.reg_manip as reg_manip
import app.server.packages.screen_manip as screen_manip

import socket

class Service:
    """A wrapper for server class, can listen to client connection, and serve the
    requests
    """
    def __init__(self):
        # self.addr = socket.gethostbyname(socket.gethostname())
        self.addr = '127.0.0.1'
        self.port = protocol.SERVER_PORT

        self.listen_socket = None
        self.client_socket = None
        self.close_signal = False

        self.request_functions_dict = {
            'screenshot': self._request_screenshot,
            'process': self._request_process,
            'app': self._request_app,
            'keylogging': self._request_keylogging,
            'reg': self._request_registry,
            'shutdown': self._request_machine,
        }

    def start(self):
        """Starts listening for connection
        
        The method will enter an infinite loop to serve the client after
        the connection has been established. This will serve one client at
        a time, i.e. no more connection can be made until the current
        connection is closed, either by the client or by the service itself.
        """

        # self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.addr, self.port))
        self.listen_socket.listen()
        print('Service created listening socket', self.listen_socket.getsockname())

        while not self.close_signal:
            self.client_socket, add = self.listen_socket.accept()
            print('Service connected to client at', add, 'using socket', self.client_socket.getsockname())
            self.serve()
        self.close_signal = False

    def stop(self):
        """Stops the client connection, and stops the service
        """
        self.stop_client_connection()

        if self.listen_socket is not None:
            self.listen_socket.close()
        self.close_signal = True

    def stop_client_connection(self):
        """Stops the current client connection only, does not stop the service
        """
        if self.client_socket is not None:
            self.client_socket.close()
            self.client_socket = None

    def serve(self):
        """Receives requests from `self.client_socket`, does the request
        and then responses back

        The method will not return until the connection is closed, either
        by the client or by the server.
        """
        while True:
            r = protocol.receive(self.client_socket)
            if not r:
                self.stop_client_connection()
                break

            request = protocol.Request.from_bytes(r)
            response = self.do_request(request)
            # response = protocol.Response(0, '')
            protocol.send(self.client_socket, response)

    def do_request(self, request: protocol.Request) -> protocol.Response:
        if request.command() not in self.request_functions_dict:
            return protocol.Response(protocol.SC_UNRECOGNIZED_COMMAND, '')
        return self.request_functions_dict[request.command()](request.option(), request.content())

    def _request_screenshot(self, option, content) -> protocol.Response:
        return protocol.Response(protocol.SC_OK, screen_manip.take_screenshot())

    def _request_process(self, option, content):
        status_code = protocol.SC_OK
        data = ''

        if option == 'list':
            data = process_manip.get_running_process()
        elif option == 'start':
            if not process_manip.start(content): status_code = protocol.SC_PROCESS_NOT_FOUND
        elif option == 'kill':
            q = process_manip.kill(content)
            status_code = protocol.SC_OK if q == 0 \
                          else protocol.SC_PROCESS_NOT_RUNNING if q == 1 \
                          else protocol.SC_PROCESS_KILL_REQUEST_IS_DENIED if q == 2 \
                          else protocol.SC_PROCESS_CANNOT_KILL

        return protocol.Response(status_code, data)

    def _request_app(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == 'list':
            data = process_manip.get_running_applications()
        elif option == 'start':
            if not process_manip.start(content): status_code = protocol.SC_APP_NOT_FOUND
        elif option == 'kill':
            q = process_manip.kill(content)
            status_code = protocol.SC_OK if q == 0 \
                          else protocol.SC_APP_NOT_RUNNING if q == 1 \
                          else protocol.SC_APP_KILL_REQUEST_IS_DENIED if q == 2 \
                          else protocol.SC_APP_CANNOT_KILL

        return protocol.Response(status_code, data)

    def _request_keylogging(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == 'hook':
            keyboard_manip.keylogger.hook()
        elif option == 'unhook':
            data = keyboard_manip.keylogger.unhook()
        
        return protocol.Response(status_code, data)

    def _request_registry(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == 'send':
            if not reg_manip.import_file(content):
                status_code = protocol.SC_ERROR
        else:
            key, value, type, d = tuple(content.split(',', 3))
            if option == 'get':
                result = reg_manip.get(key, value)
                if not result:
                    status_code = protocol.SC_ERROR
                else:
                    data = result
            elif option == 'set':
                if not reg_manip.set(key, value, type, d):
                    status_code = protocol.SC_ERROR
            elif option == 'delete':
                if not reg_manip.delete(key, value):
                    status_code = protocol.SC_ERROR
            elif option == 'create-key':
                if not reg_manip.create_key(key):
                    status_code = protocol.SC_ERROR
            elif option == 'delete-key':
                if not reg_manip.delete_key(key):
                    status_code = protocol.SC_ERROR

        return protocol.Response(status_code, data)

    def _request_machine(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == '':
            if not machine_manip.shutdown():
                status_code = protocol.SC_MACHINE_CANNOT_SHUTDOWN
        
        return protocol.Response(status_code, data)

if __name__ == '__main__':
    # Create a service object
    service = Service()

    # The service will start listening and accepting connections
    # Call this function in a different thread than the GUI thread 
    # because this function will go into an infinite loop to serve the client.
    service.start()

    # Stop the service
    service.stop()

    # Stop the client connection only
    service.stop_client_connection()
