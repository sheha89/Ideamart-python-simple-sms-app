import BaseHTTPServer
import ConfigParser
import logging
import mt_request_handler

LOG = logging.getLogger("alert.service.mo.request.handler")

config = ConfigParser.ConfigParser()
config.read('properties.ini')


class MoRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == config.get('urlPattern', 'sendAlert'):
            if self.headers.has_key('content-length'):
                self.handle_mo_request()

    def generate_mo_response(self, gettype):
        self.send_response(config.getint('responseCode', 'success'))
        self.send_header("Content-type", gettype)
        self.end_headers()

    def extract_mo_request(self):
        length = int(self.headers['content-length'])
        mo_request = self.rfile.read(length)
        LOG.debug("MO Request received [ %s ] : " % mo_request)
        return mo_request

    def handle_mo_request(self):
        self.generate_mo_response("application/json")
        send_alert_response(self.extract_mo_request())


def send_alert_response(mo_request):
    mt_request = mt_request_handler.MtRequest(mo_request)
    LOG.debug("MT Request [ %s ] : " % mt_request)
    mt_request_handler_object = mt_request_handler.MtRequestHandler()
    mt_request_handler_object.send_mt_request(mt_request)