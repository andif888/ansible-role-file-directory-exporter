#! /usr/bin/python3
# -*- coding: utf-8 -*-

# Python3 File and Directory Exporter for Prometheus
# directory exporter library

#     Dev: wh0ami
# Licence: Public Domain <https://unlicense.org>
# Project: https://codeberg.org/wh0ami/file_directory_exporter

from pathlib import Path
import os

# function for getting metrics
def getMetrics(directories):
  # function for checking whether a directory exists
  def getExist(directory):
    string = 'directory_exist{directory="' + directory + '"} '
    try:
      if Path(directory).is_dir():
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
    except:
      age = 0
    return age
  
  # function for getting the size of a file
  def getSize(file):
    try:
      size = os.path.getsize(file)
    except:
      size = 0
    return size

  # function for getting the amount of elements in the directory
  def getContent(directory):
    try:
      i = 0
      age_oldest = 2147483647
      age_newest = 0
      size_smallest = float("inf")
      size_bigest = 0
      for element in os.scandir(directory):
        i += 1
        if element.is_file(follow_symlinks=False):
          age = getAge(element.path)
          if age < age_oldest:
            age_oldest = age
          if age > age_newest:
            age_newest = age
          size = getSize(element.path)
          if size > size_bigest:
            size_bigest = size
          if size < size_smallest:
            size_smallest = size

      res = 'directory_contains_elements_number{directory="' + directory + '"} ' + str(i) + "\n"
      if age_oldest != 2147483647:
        res += 'directory_contains_files_oldest{directory="' + directory + '"} ' + str(int(round(age_oldest, 0))) + "\n"
      if age_newest != 0:
        res += 'directory_contains_files_newest{directory="' + directory + '"} ' + str(int(round(age_newest, 0))) + "\n"
      if size_smallest != 0:
        res += 'directory_contains_files_smallest{directory="' + directory + '"} ' + str(int(round(size_smallest, 0))) + "\n"
      if size_bigest != float("inf"):
        res += 'directory_contains_files_bigest{directory="' + directory + '"} ' + str(int(round(size_bigest, 0))) + "\n"
    except:
      res = ""
    return res


  # print the headline
  output = "# directory exporter for prometheus\n\n"

  # go directory by directory and execute checks
  for directory in directories:
    status = getExist(directory)
    output += "# directory checks for " + directory + "\n" + status["string"]
    if status["boolean"]:
      output += getContent(directory)
    output += "\n"

  output += "\n"
  return output
