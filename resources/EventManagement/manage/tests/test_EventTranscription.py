# -*- coding: utf-8 -*-
# test_EventTranscription.py
#

# import pytests
from pathlib import Path
import pandas as pd

from manage import (EventMeta as Meta,
                    EventTranscription as TRX,
                    Utils as UTL)

# time_repl() is inside TRX.clean_text fn.
def time_repl(mo):
    """Fix spoken time; mo=match obj"""
    fmt = "{}{}:{}{} "
    o = fmt.format(mo.group(1),mo.group(2),mo.group(3),
                   mo.group(4).upper().replace('.','')) 
    return o

        
def test_time_repl():
    s1 = "it's 10 30 p.m your time "
    s2 = "   10 30 a.m your time "
    s3 = "	yeah I think yeah 10 15. "
    o1 = "it's 10:30 PM your time "
    o2 = "   10:30 AM your time "
    o3 = "	yeah I think yeah 10 15. "
    samples = [s1, s2, s3]
    outputs = [o1, o2, o3]
    n_samples = len(samples)
    
    p_time = re.compile(r"(\s*)(\d{1,2}) (\d{1,2}) ([pa].m)(.?)")

    for i, (s,o) in enumerate(zip(samples, outputs)):
        print("Search str: {!r}".format(s))
        new_s = None
        failed = True
        new_s = p_time.sub(time_repl, s)
        if new_s is not None:
            failed = False
            failed = new_s != o
            print(F"{i}/{n_samples}\tNew str: {new_s}; Failed: {failed}, expected: {}")
        else:
            news_s = None
            #print("No pattern found.")