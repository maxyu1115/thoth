import urllib.parse as up
from urllib.parse import urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import util
import whooshWrapper


SEARCH_KEYWORD = "phrase"


def startServer(output_path: str, server_port: int, host_name="localhost"):
    searcher = whooshWrapper.WhooshWrapper(util.DirectoryLocator(output_path))

    class ThothSearchEngine(BaseHTTPRequestHandler):
        def do_GET(self):
            parse_result = urlparse(self.path)
            if parse_result.path == "/search":
                self.handle_search(parse_result)
            else:
                self.send_error(404, "path not found")

        def handle_search(self, parse_result: up.ParseResult):
            query = parse_result.query
            query_components = dict(qc.split("=") for qc in query.split("&"))
            phrase = query_components[SEARCH_KEYWORD]
            self.send_response(200)

            # Setting the header
            self.send_header("Content-type", "application/json")
            # Whenever using 'send_header', you also have to call 'end_headers'
            self.end_headers()

            self.wfile.write(json.dumps(searcher.searchWhoosh(phrase)).encode(encoding="utf-8"))

    webServer = HTTPServer((host_name, server_port), ThothSearchEngine)
    print("Server started http://%s:%s" % (host_name, server_port))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")



