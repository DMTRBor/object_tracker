import builtins
import os, sys
import logging
from datetime import datetime


def exceptionHook(excType, excValue, excTraceback):
    logging.exception(
        "Unexpected exception",
        exc_info=(excType, excValue, excTraceback)
    )


def setUpLogger(logsPath=r'C:/Temp'):
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)

    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y_%H")
    filename = f'{logsPath}/epoch_time_alerts_log-{timestampStr}.log'
    logging.basicConfig(filename=filename)
    sys.excepthook = exceptionHook


def print(*args, **kwargs):
    if args.__len__() >= 1:
        builtins.print(*args)

    if kwargs.__len__() >= 1:
        if 'consoleObj' in kwargs.keys():
            kwargs['consoleObj'].append(args[0])
