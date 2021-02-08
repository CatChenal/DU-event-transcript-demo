# -*- coding: utf-8 -*-
# test_Utils.py
#

# import pytests
from pathlib import Path
import shutil
import json

from manage import Utils as UTL


def test_split_url():
    dom = 'https://www.meetup.com/nyc-data-umbrella/events/'
    url = 'https://www.meetup.com/nyc-data-umbrella/events/271116695/'
    is_meetup = True
    d, idx = UTL.split_url(url, is_meetup)
    print(F'Test meetup...')
    assert (d, idx) == (dom, '271116695')
    
    yt_frmts = [('https://youtu.be/0L1uM_18TTA','0L1uM_18TTA'),
                ('https://youtu.be/0L1uM_18TTA?t=1','0L1uM_18TTA'),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA',
                 '0L1uM_18TTA'),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be',
                 '0L1uM_18TTA'),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be&t=2m5s',
                 '0L1uM_18TTA'),
                ('http://www.youtube.com/watch?feature=player_embedded&v=0L1uM_18TTA',
                 '0L1uM_18TTA'),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be&t=1',
                 '0L1uM_18TTA'),
                ('youtube.com/watch?v=iwGFalTRHDA',
                 'iwGFalTRHDA'),
                ('http://www.youtube.com/watch?feature=player_embedded&v=Pkg-DKkObKs',
                 'Pkg-DKkObKs'),
                ('http://www.youtube.com/watch?feature=player_embedded&v=TVe-uT_So6c',
                 'TVe-uT_So6c'),
               ]
    n_urls = len(yt_frmts)
    is_meetup = False
    print('Test youtube...')
    for i, u in enumerate(yt_frmts):
        
        d, idx = UTL.split_url(u[0], is_meetup)
        try:
            assert idx == u[1]
        except AssertionError:
            #print(F'\n{i}:\t{d}; vid::\t{idx}')
            print(F'{i}:\tFailed on: {u[0]} with: {idx}')
            pass
    print('All done.')


def test_save_file(fullpath):
    # TODO
    s_txt = ''
    s_dict = {}
    
    # dir:
    p = fullpath.parents[0]
    UTL.save_file(p, s, ext=None, replace=True)
    #assertRaises(ValueError, msg="Param filepath is a directory: file path needed.")
    
    # s_txt -> json
    # s_dict -> json
    return

def p_time_test():
    s1 = "it's 10 30 p.m your time "
    s2 = "   10 30 p.m your time "
    s3 = "	yeah I think yeah 10 15. "
    p_time = re.compile('([\S\s]*)(\d{1,2}) (\d{1,2}) ([pa].m) ([\S\s]*)')

    for s in [s1, s2, s3]:
        print("Search str: {!r}".format(s))
        new_s = ''
        m = p_time.match(s)
        if m is not None:
            new_s = m.group(1) + m.group(2) + ":" + m.group(3) + " " + m.group(4) + " " + m.group(5)
            print("   New str: {!r}".format(new_s))
        else:
            print("No pattern found.")
                     