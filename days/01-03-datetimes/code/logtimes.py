from datetime import datetime
import os
import urllib.request

SHUTDOWN_EVENT = 'Shutdown initiated'

# prep: read in the logfile
tmp = os.getenv("TMP", "/tmp")
logfile = os.path.join(tmp, 'log')
urllib.request.urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/messages.log',
    logfile
)

with open(logfile) as f:
    loglines = f.readlines()


def convert_to_datetime(line):
    try:
        return datetime.strptime(line.split(' ')[1], '%Y-%m-%dT%X')
    except ValueError:
        print(f'Invalid timestamp found for {line}')


def time_between_shutdowns(loglines):
    shutdowns = [line for line in loglines if SHUTDOWN_EVENT in line]
    return convert_to_datetime(shutdowns[-1]) - convert_to_datetime(shutdowns[0])

