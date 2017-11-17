#!/usr/bin/python3.5
from logger_init import *

# Logger init
log = ColoredLogger().root_logger
# END #

# DB options
test_mode = True
db_test = True
DATATABLE_PATH = 'db/'
DATATABLE_FILENAME = 'race_db.db'
# END #

# other options
online_sync = False
port = 7777
race_laps = 1
race_rules = 'best time'  # FIXME: only best time added
# END #
