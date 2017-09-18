#!/usr/bin/python3.5
from logger_init import *

# starting logger
log = ColoredLogger().root_logger

using_db = False
db_test = True
DATATABLE_PATH = 'db/'
DATATABLE_FILENAME = "race_db.db"

online_sync = False
port = 7777
race_laps = 1
race_rules = 'some rules'
# TODO: need to add good logger here -- complt
