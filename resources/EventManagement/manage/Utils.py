# -*- coding: utf-8 -*-
# Utils.py
# Programmer: Cat Chenal
#
import os # pathlib has no remove()
from pathlib import Path
import json
from warnings import warn

# To create often-used subfolders:
def get_project_dirs(which=['data', 'images'],
                     use_parent=True):
    '''Create folder(s) named in `which` at the parent level.'''
    if use_parent:
        dir_fn = Path.cwd().parent.joinpath
    else:
        dir_fn = Path.cwd().joinpath
        
    dir_lst = []    
    for d in which:
        DIR = dir_fn(d)
        if not DIR.exists():
            Path.mkdir(DIR)
        dir_lst.append(DIR)
    return dir_lst


def get_subfolder(subfolder_name, parent_dir=None):
    if parent_dir is None:
        parent_dir = Path.cwd()
    p = parent_dir.joinpath(subfolder_name)
    if not p.exists():
        Path.mkdir(p)
    return p

def get_id_from_YT_url(url):
    start_idx = len('http://') + 1
    url = url[start_idx:]
    
    p1 = url.partition('?')
    if p1[0] == url:
        return p1[0].split('/')[-1]
    else:
        p2 = p1[2].partition('&')
        if p2[0] == url:
            return p2[0].split('=')[-1]
        else:
            if 'v=' in p2[0]:
                url = p2[0]
            else:
                url = p2[2]
            return url.split('=')[-1]
        
        
def split_url(url, is_meetup=False):
    """
    Return a tuple: host site, id.
    Possible video url formats:
      https://youtu.be/0L1uM_18TTA
      https://www.youtube.com/watch?v=0L1uM_18TTA
      https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be
      http://www.youtube.com/watch?feature=player_embedded&v=0L1uM_18TTA
    Meetup url format: 
      https://www.meetup.com/nyc-data-umbrella/events/271116695/
    # Example:
    link ='https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be&t=2m5s'
    vsite, vid = split_video_url(link)
    print('Site:', vsite, '; VID:', vid)
    >> Site: https://www.youtube.com/watch?v; VID: 0L1uM_18TTA
    """
    if url is None:
        return None
    
    if is_meetup:
        dom = 'https://www.meetup.com/nyc-data-umbrella/events/'
        id = url[len(dom):]
        if id.endswith('/'):
            id = id[:-1]
        return dom, id

    id = get_id_from_YT_url(url)
    dom = url[:url.index(id)]
    return dom, id


def save_file(filepath, s, ext=None, replace=True):
    """
    Usual write method of file handle used with
    json output if stream s is a dict.
    Note: s can be empty => touch.
    :param filepath (Path object): output file name (full).
    :param s (string): text (dict) to save.
    :param: ext (str, None): file extension.
            If given, extension of filepath will be changed
            to ext, i.e. filepath is used as a filename pattern;
            ext is set to '.json' if stream is dict.
    :param: replace default (True):: overwrite
    """
    msg = "Utils.save_file:: "
    # full path needed:
    if filepath.is_dir():
        msg += "filepath is a dir: filename also needed."
        raise ValueError(msg)
    
    fname, fext = filepath.name.split('.')
    fext = "." + fext
    
    to_json = isinstance(s, dict)
    
    if ext is None:
        ext = fext
    else:
        if not ext.startswith('.'): ext = "." + ext
    
    if to_json:
        if ext != '.json': ext = '.json'
            
    if ext == '.json' and not to_json:
        msg += "\nSaving a string to .json would yield improper "
        msg += "encoding & lead to json.load() failure."
        raise ValueError(msg)

    outfile = filepath.parents[0].joinpath(fname + ext)
    
    if replace:
        if outfile.exists():
            os.remove(outfile)
            
    if not outfile.exists():
        if to_json:
            with open(outfile, 'w') as f:
                #json.dumps(s, f)
                f.write(json.dumps(s))
        else:
            with open(outfile, 'w') as f:
                f.write(s)
    return


def load_file_contents(filepath):
    """
    Return a file entire contents or None.
    :param filepath (Path object): full file name.
    """
    msg = "Utils.load_file_contents:: "
    if not filepath.exists():
        msg += "File not found."
        raise ValueError(msg)
    if filepath.is_dir():
        msg = "File needed, dir given."
        raise ValueError(msg)
    # else use default err handler:
    fname, fext = filepath.name.split('.')
    fext = "." + fext
    if fext == '.json':
        with open(filepath) as f:
            content = json.load(f)
    else:  
        with open(filepath) as f:
            content = f.read()

    return content


def save_json(obj, fname):
    with open(fname, 'w') as fh:
        json.dump(obj, fh)

        
def load_json(fname):
    with open(fname) as fh:
        content = json.load(fh)
    return content


def get_file_lines(fullpath):
    with open(fullpath) as fh:
        text = fh.readlines()
    return text


def check_year(yr):
    ok = len(str(yr)) == 4
    if not ok:
        warn('Provide a four-digit year.')
    return ok

# ...............................................    
# tests (temp) 
# ...............................................
def test_save_file(fullpath):
    # TODO
    s_txt = ''
    s_dict = {}
    
    # dir:
    p = fullpath.parents[0]
    save_file(p, s, ext=None, replace=True)
    #assertRaises(ValueError, msg="Param filepath is a directory: file path needed.")
    
    # s_txt -> json
    # s_dict -> json
    return


def test_split_url():
    dom = r'https://www.meetup.com/nyc-data-umbrella/events/'
    url = 'https://www.meetup.com/nyc-data-umbrella/events/271116695/'
    meetup = True
    d, i = split_url(url, meetup)
    print(F'Test meetup:\n\t{d}\n\t{i}')
    assert (d, i) == (dom, '271116695')
    
    yt_frmts = [('https://youtu.be/0L1uM_18TTA','https://youtu.be/'),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA', 
                 'https://www.youtube.com/watch?v='),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be',
                 'https://www.youtube.com/watch?v='),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be&t=2m5s',
                 'https://www.youtube.com/watch?v='),
                ('http://www.youtube.com/watch?feature=player_embedded&v=0L1uM_18TTA',
                 'http://www.youtube.com/watch?feature=player_embedded&v='),
                ('https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be&t=1',
                 'https://www.youtube.com/watch?v=')
               ]
    meetup = False
    print('\nTest youtube:')
    for u in yt_frmts:
        d, i = split_url(u[0], meetup)
        print(F'\n\t{d}\n\t{i}')
        assert (d, i) == (u[1], '0L1uM_18TTA')


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
