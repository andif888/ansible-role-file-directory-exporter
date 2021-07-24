#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Python3 File and Directory Exporter for Prometheus
# file exporter library

#     Dev: wh0ami
# Licence: Public Domain <https://unlicense.org>
# Project: https://codeberg.org/wh0ami/file_directory_exporter

from pathlib import Path
import os

# function for getting metrics
def getMetrics(files, config):
  # function for checking whether a file exists
  def getExist(file):
    string = 'file_exist{file="' + file + '"} '
    try:
      if Path(file).is_file():
        string += "1\n"
        boolean = True
      else:
        string += "0\n"
        boolean = False
    except:
      string += "0\n"
      boolean = False
    res = {}
    res["string"] = string
    res["boolean"] = boolean
    return res

  # function for getting the age of a file
  def getAge(file):
    try:
      age = os.path.getmtime(file)
      res = "file_age_seconds{file=" + '"' + file + '"} ' + str(int(round(age, 0))) + "\n"
    except:
      res = ""
    return res

  # function for getting the size of a file
  def getSize(file):
    try:
      size = os.path.getsize(file)
      res = "file_size_bytes{file=" + '"' + file + '"} ' + str(int(round(size, 0))) + "\n"
    except:
      res = ""
    return res



  # print the headline
  output = "# file exporter for prometheus\n\n"

  # go file by file and execute checks
  for file in files:
    status = getExist(file)
    output += "# file checks for " + file + "\n" + status["string"]
    if config["age"] and status["boolean"]:
      output += getAge(file)
    if config["size"] and status["boolean"]:
      output += getSize(file)
    output += "\n"

  output += "\n"
  return output
