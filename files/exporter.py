#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Python3 File and Directory Exporter for Prometheus
# file and directory exporter webserver

#     Dev: wh0ami
# Licence: Public Domain <https://unlicense.org>
# Project: https://codeberg.org/wh0ami/file_directory_exporter

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
import sys
import fileexporter
import directoryexporter

# webserver config
ip = "0.0.0.0"
port = 9101

# check whether a config exists
try:
  configfile = sys.argv[1]
  if not Path(configfile).is_file():
    raise Excpetion()
except:
  raise Exception("[Error] Config not found! Usage: ./exporter.py <config>")
  sys.exit(1)

# try to load the config
try:
  with open(configfile, "r") as infile:
    data = json.load(infile)
    config = data["file_exporter_config"]
    files = data["files"]
    directories = data["directories"]
    ip = config["ipaddress"]
    port = config["port"]
except:
  raise Exception("Error while opening the config file!")
  sys.exit(1)

# create a custom class for the webserver
# standard functions (GET and POST request) are overwritten by our own procedures
class exporter(BaseHTTPRequestHandler):
  global files
  global directories
  global config

  def do_GET(self):
    if self.path == "/" or self.path == "/metrics":
      self.send_response(200)
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(bytes(fileexporter.getMetrics(files, config), "utf-8"))
      self.wfile.write(bytes(directoryexporter.getMetrics(directories), "utf-8"))
    else:
      self.send_response(404)

  def do_POST(self):
    if self.path == "/" or self.path == "/metrics":
      self.send_response(200)
      self.send_header("Content-type", "text/plain")
      self.end_headers()
      self.wfile.write(bytes(fileexporter.getMetrics(files, config), "utf-8"))
      self.wfile.write(bytes(directoryexporter.getMetrics(directories), "utf-8"))
    else:
      self.send_response(404)

if __name__ == "__main__":
    webServer = HTTPServer((ip, port), exporter)
    print("File and Directory Exporter for Prometheus started at http://%s:%s" % (ip, port))

    try:
      webServer.serve_forever()
    except KeyboardInterrupt:
      pass

    webServer.server_close()
    print("\nFile and Directory Exporter for Prometheus stopped")
