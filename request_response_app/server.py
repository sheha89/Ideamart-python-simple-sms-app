import BaseHTTPServer
import ConfigParser
import mo_request_handler
import logging

LOG = logging.getLogger("alert.service.server")
config = ConfigParser.ConfigParser()
config.read('properties.ini')


def httpd(handler_class=mo_request_handler.MoRequestHandler, server_address=(config.get('senderAddress', 'host'),
                                                                             config.getint('senderAddress', 'port')), ):
    try:
        alert_service_server = BaseHTTPServer.HTTPServer(server_address, handler_class)
        LOG.debug("Starting the server on host %s and port %s " % server_address)
        alert_service_server.serve_forever()

    except KeyboardInterrupt:
        LOG.debug('^C Received, shutting down the web server')


def init_logger():
    logging.basicConfig(filename='trace.log', level=logging.DEBUG)


if __name__ == "__main__":
    init_logger()
    httpd()