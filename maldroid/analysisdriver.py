
from analyze import analyze # Wrapper for androguard scanning
from maldroid_conf import *

import os
import sys
import sqlite3
import json


"""
    This class is the primary malware analysis driver.
    It should take as it's only argument the full path
    to the Android Application. It returns either a detailed
    JSON report about the app, or an error in the instance
    where the app was not an Android APK, or if there were
    any parsing issues.


"""

class MAEngine():

    digest  = '' # digest of the sample, used to lookup the db entry
    apk     = '' # Place holder for the Androguard APK object
    rep     = '' # Place holder for the report generated.
    db_path = ''

    """ Init digest and APK variable """
    def __init__(self, app_name, s, db):
        self.digest = s
        self.apk = analyze(app_name)
        self.db_path = db

    """ This is the meat of the stew. All malware tests are launched here,
    and subsequently all report data should be fed back here. This function
    finishes executiong by calling the 'report' function, which simply updates
    the DB record with the 'report' which is really just a JSON blob """
    def run_tests(self):
        self.rep += json.dumps(self.apk.check_permissions())
        self.rep += json.dumps(self.apk.check_risk())

        # This is just for ease of use. Now we ensure that the report will
        # be inserted as soon as all tests have completed. Also now we only
        # need 2 threads :P
        self.report()

    """ This function simply updates the DB entry with the JSON report """
    def report(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute('UPDATE reports SET report=? WHERE digest=?', (self.rep, self.digest))
        conn.commit()
        conn.close()