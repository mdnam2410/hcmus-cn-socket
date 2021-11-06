from app.core.exceptions import ReceivingError, SendingError
import app.core.protocol as protocol
import app.server.packages.keyboard_manip as keyboard_manip
import app.server.packages.machine_manip as machine_manip
import app.server.packages.process_manip as process_manip
import app.server.packages.reg_manip as reg_manip
import app.server.packages.screen_manip as screen_manip
from app.server.packages.stream_manip import StreamService

import socket
import logging

logging.basicConfig(format='%(asctime)s: %(message)s', level=logging.DEBUG)

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
            'stream': self._request_stream,
            'process': self._request_process,
            'app': self._request_app,
            'keylogging': self._request_keylogging,
            'reg': self._request_registry,
            'machine': self._request_machine,
        }

        self.stream_service = StreamService()

    def start(self):
        """Starts listening for connection
        
        The method will enter an infinite loop to serve the client after
        the connection has been established. This will serve one client at
        a time, i.e. no more connection can be made until the current
        connection is closed, either by the client or by the service itself.
        """

        # self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        logging.debug(f'Creating listening socket')
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((self.addr, self.port))
        self.listen_socket.listen()

        while True:
            self.client_socket, _ = self.listen_socket.accept()
            if self.close_signal:
                break
            logging.debug(f'Connected to client {self.client_socket.getpeername()}, using socket {self.client_socket.getsockname()}')
            self.serve()
        
        self.listen_socket.close()
        self.listen_socket = None
        self.close_signal = False

    def stop(self):
        """Stops the client connection, and stops the service
        """
        self.close_signal = True
        if self.is_connected_to_client():
            self.stop_client_connection()
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.addr, self.port))
        # if self.listen_socket is not None:
        #     self.listen_socket.close()
        # self.listen_socket = None

    def clean_up(self):
        logging.debug('Clearing hook history')
        keyboard_manip.keylogger.clear_history()
        logging.debug('Unlocking keyboard')
        keyboard_manip.keylogger.unlock()
        if self.stream_service.is_running():
            logging.debug('Stopping streaming service')
            self.stream_service.stop()

    def stop_client_connection(self):
        """Stops the current client connection only, does not stop the service
        """
        logging.debug('Stopping client connection')
        if self.client_socket is not None:
            logging.debug('Closing client socket')
            self.client_socket.close()
        self.client_socket = None

    def is_alive(self):
        return self.listen_socket is not None

    def is_connected_to_client(self):
        return self.client_socket is not None

    def serve(self):
        """Receives requests from `self.client_socket`, does the request
        and then responses back

        The method will not return until the connection is closed, either
        by the client or by the server.
        """
        try:
            while True:
                r = protocol.receive(self.client_socket)

                request = protocol.Request.from_bytes(r)
                logging.debug(f'Doing request: {request.command()} {request.option()}')

                response = self.do_request(request)
                logging.debug(f'Sending response: {response.status_code()} {response.status_message()}')
                protocol.send(self.client_socket, response)
        except (SendingError, ReceivingError):
            logging.debug('Communicating error')
        finally:
            self.stop_client_connection()
            self.clean_up()

    def do_request(self, request: protocol.Request) -> protocol.Response:
        if request.command() not in self.request_functions_dict:
            return protocol.Response(protocol.SC_ERROR_UNRECOGNIZED_COMMAND, '')
        return self.request_functions_dict[request.command()](request.option(), request.content())

    def _request_screenshot(self, option, content) -> protocol.Response:
        data = screen_manip.take_screenshot()
        status_code = protocol.protocol.SC_SCREENSHOT_CANNOT_TAKE \
                      if data is None \
                      else protocol.SC_OK
        return protocol.Response(status_code, screen_manip.take_screenshot())

    def _request_stream(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == '':
            if not self.stream_service.is_running():
                logging.debug('Stream service is not running, initializing...')
                if not self.stream_service.connect_to_peer(self.client_socket.getpeername()[0]):
                    logging.debug('Unable to stream')
                    status_code = protocol.SC_STREAM_CANNOT_INITIALIZE
            else:
                status_code = protocol.SC_STREAM_SERVICE_ALREADY_INITIALIZED
        elif self.stream_service.is_running():
            if option == 'start':
                logging.debug('Starting streaming...')
                self.stream_service.start()
            elif option == 'restart':
                logging.debug('Restarting streaming...')
                self.stream_service.restart()
            elif option == 'pause':
                logging.debug('Pausing streaming...')
                self.stream_service.pause()
            elif option == 'stop':
                logging.debug('Stopping streaming...')
                self.stream_service.stop()
        else:
            logging.debug('Stream service is not running')
            status_code = protocol.SC_STREAM_IS_NOT_RUNNING

        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))

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

        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))

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

        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))

    def _request_keylogging(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == 'hook':
            keyboard_manip.keylogger.hook()
        elif option == 'unhook':
            data = keyboard_manip.keylogger.unhook()
        elif option == 'lock':
            keyboard_manip.keylogger.lock()
        elif option == 'unlock':
            keyboard_manip.keylogger.unlock()
        
        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))

    def _request_registry(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''
        content = content.decode(protocol.MESSAGE_ENCODING)
        if option == 'send':
            if not reg_manip.import_file(content):
                status_code = protocol.SC_REGISTRY_CANNOT_IMPORT_FILE
        else:
            # bug here, not all command have full 4 parameter
            key, value, type, d = tuple(content.split(',', 3))
            if option == 'get':
                result = reg_manip.get(key, value)
                if not result:
                    status_code = protocol.SC_REGISTRY_CANNOT_GET_VALUE
                else:
                    data = result
            elif option == 'set':
                if not reg_manip.set(key, value, type, d):
                    status_code = protocol.SC_REGISTRY_CANNOT_SET_VALUE
            elif option == 'delete':
                if not reg_manip.delete(key, value):
                    status_code = protocol.SC_REGISTRY_CANNOT_DELETE_VALUE
            elif option == 'create-key':
                if not reg_manip.create_key(key):
                    status_code = protocol.SC_REGISTRY_CANNOT_CREATE_KEY
            elif option == 'delete-key':
                if not reg_manip.delete_key(key):
                    status_code = protocol.SC_REGISTRY_CANNOT_DELETE_KEY

        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))

    def _request_machine(self, option, content) -> protocol.Response:
        status_code = protocol.SC_OK
        data = ''

        if option == 'shutdown':
            if not machine_manip.shutdown():
                status_code = protocol.SC_MACHINE_CANNOT_SHUTDOWN
        elif option == 'mac':
            m = machine_manip.get_mac()
            if m is None:
                status_code = protocol.SC_MACHINE_CANNOT_GET_MAC
            else:
                data = m
        elif option == 'log-out':
            if not machine_manip.logout():
                status_code = protocol.SC_MACHINE_CANNOT_LOGOUT
        elif option == "sleep":
            if not machine_manip.sleep():
                status_code = protocol.SC_MACHINE_CANNOT_SLEEP
        elif option == "restart":
            if not machine_manip.restart():
                status_code = protocol.SC_MACHINE_CANNOT_RESTART
        return protocol.Response(status_code, data.encode(protocol.MESSAGE_ENCODING))
