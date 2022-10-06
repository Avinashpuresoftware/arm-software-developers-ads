#/usr/bin/env python3

import argparse
import logging
import os
import subprocess
import csv
from datetime import datetime, timedelta


'''
List pages older than a period in days
'''
def report(period):
    global verbosity, level

    orig = os.path.abspath(os.getcwd())

    # chdir to the root folder
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")
    dname = ["content/install-tools", "content/learning-paths"]
    result = {}

    for d in dname:
        l = os.listdir(d)
        for i in l:
            date = subprocess.run(["git", "log", "-1" ,"--format=%cs", d +"/" + i], stdout=subprocess.PIPE)
            date = datetime.strptime(date.stdout.rstrip().decode("utf-8"), "%Y-%m-%d")
            # check if article is older than the period
            if date < datetime.now() - timedelta(days = period):
                # strip out '\n' and decode byte to string
                result[d + "/" + i] = date

    fn="outdated_files.csv"
    fields=["File", "Last updated"]
    os.chdir(orig)
    logging.info("Results written in " + orig + "/" + fn)

    with open(fn, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fields)
        writer.writeheader()
        for key in result.keys():
            csvfile.write("%s, %s\n" % (key, result[key]))

