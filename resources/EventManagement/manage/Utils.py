# -*- coding: utf-8 -*-
# Utils.py
# Programmer: Cat Chenal
#
from pathlib import Path
import json
from collections import OrderedDict
from enum import Enum
import re
from IPython.display import HTML, Markdown


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
    """
    Regex source: 
    https://stackoverflow.com/questions/42440678/
    regular-expression-for-youtube-video-id
    """
    vid = ''
    regex = "(?:youtube(?:-nocookie)?\.com|youtu\.be).*[=/]([-\\w]{11})(?:\\?|=|&|$)"
    rc = re.compile(regex)
    matches = rc.search(url)
    if matches:
        vid = matches.groups()[0]
    return vid


def split_url(url, is_meetup=False):
    """
    Return a tuple: host site, id.
    Possible video url formats:
      https://youtu.be/0L1uM_18TTA
      https://www.youtube.com/watch?v=0L1uM_18TTA
      https://www.youtube.com/watch?v=0L1uM_18TTA&feature=youtu.be
      http://www.youtube.com/watch?feature=player_embedded&v=0L1uM_18TTA
      https://youtu.be/0L1uM_18TTA?t=1
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
            outfile.unlink()
            
    if not outfile.exists():
        if to_json:
            with open(outfile, 'w') as f:
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


def get_file_lines(fullpath):
    msg = "Utils.get_file_lines:: "
    if fullpath.is_dir():
        msg += "filepath is a dir: filename also needed."
        raise ValueError(msg)

    with open(fullpath) as fh:
        text = fh.readlines()
    return text

# ..............................................................................
def show_md_file(md_file, kind='README'):
    """md_file is either a Path filepath or url."""
    if isinstance(md_file, Path):
        which = 'Local'
        txt = F'### {which} {kind} file: {md_file.name}\n---\n---\n'
        txt += Markdown(filename=md_file).data
    else:
        which = 'Live'
        txt = F'### {which} {kind} file: \n---\n---\n'
        txt += Markdown(md_file).data
    txt +='\n---\n---'
    display(Markdown(txt))
    

def show_du_logo_hdr(as_html=True):
    """
    Render a constructed div string in HTML
    if as_html=True (default), else return the html string.
    """
    logo_src = "https://raw.githubusercontent.com/data-umbrella/"
    logo_src += "event-transcripts/master/images/full_logo_transparent.png"
    logo_link = '<a href="https://www.dataumbrella.org" target="_blank"> '
    logo_link += F'<img src="{logo_src}" width="20%" /></a>'
    div = '<div style="text-align:center;padding:5px;width:98%">' 
    div += F'{logo_link}</div>'
    if as_html:
        return HTML(div)
    else:
        return div
    

# ..............................................................................
EXTRA_REFS_EXAMPLE = """
<div style="overflow:auto;">
<h3>The `extra_references` value is a Markdown str that should conform to the entries preceding it:</h3>
<div style="overflow:auto;margin-left: 5%;">
<pre style="width:900px;">
# For example, to add a separate section called 'Other References' (##, H2 header),
# you would type the lines within the double quotes below:
""
## Other References (this header is optional)
- Binder: each listed item should have a 'list header', e.g. '- Binder'  
- Twitter: Use this format: [full name 1](twitter url), etc.     
- Wiki: This is an excellent [wiki on transcription](http://en.wikipedia.org/wiki/Main_Page)  
""
</pre>
</div>  

### The rendered output under the templated header items would be:
## Other References\n- Binder: each listed item should have a 'list header', e.g. '- Binder'  \n- Twitter: Use this format: [full name 1](twitter url), etc.  \n
- Wiki: This is an excellent [wiki on transcription](http://en.wikipedia.org/wiki/Main_Page)  \n
---
</div>
"""


# ..............................................................................
info_div = '<div style="text-align:left;padding:5px;width:98%;"'

section_info_add = info_div + """
<h3>ADD</h3>
<p>Create a new event:  
<ul>
  <li>A new row in the main table of the README file, and </li>
  <li>A starter transcript Markdown file, which includes the initial transcript.</li>
</ul>
</p>
"""  + '</div>'
section_info_modify = info_div + """
<h3>MODIFY</h3>
<p>Select and modify an event: any change provided via the input form will be 
applied to the README table and/or the transcript Markdown file.</p>
"""  + '</div>'
section_info_edit = info_div + """
<h3>EDIT</h3>
<p>Edit an event's transcript. Only the transcript text will be extracted from, 
then replaced into the associated transcript file.<br>The Audio file will be 
downloaded if not found.</p>
<p><strong>Note: </strong>Before saving an editing session, remember to update 
the Status and/or the Editor/Reviewer's names.
"""  + '</div>'

EventInfo = OrderedDict([('ADD', section_info_add),
                         ('MODIFY', section_info_modify),
                         ('EDIT', section_info_edit),
                         ('INIT', '')]
                       )


class EventFunction(Enum):
    # order follows menu order in accordion wgt.
    ADD = 'Add a Data Umbrella Event'
    MODIFY = 'Modify a Data Umbrella Event'
    EDIT = 'Edit a Data Umbrella Event Transcript'
    INIT = 'Data Umbrella Event Management'


class DisplaySectionInfo:
    def __init__(self, EventFunction):
        self.function = EventFunction
        self.info = EventInfo[EventFunction.name]

    def show_section_hdr(self, as_html=True):
        """
        Return formated HTML(<div>) if as_html=True(default),
        else return the html string.
        """
        val = self.function.value
        style = "text-align:center;padding:5px;background:#c2d3ef;"
        style += "color:#ffffff;font-size:3em;"
        style += "width:100%,height=40%"
        div = F'<div style="{style}">{val}</div>'
        if as_html:
            return HTML(div)
        else:
            return div
        
    def show_section_info(self, as_html=True):
        """
        Return formated HTML(<div>) if as_html=True(default),
        else return the html string.
        """
        style = F"text-align:justify;font-size:1em;width:100%;"
        div = F'<div style="{style}">{self.info}</div>'
        if as_html:
            return HTML(div)
        else:
            return div
    
    def show_header_with_info(self, as_html=False):
        """Return both section header & info,"""
        div = self.show_section_hdr(as_html)
        div += self.show_section_info(as_html)
        if as_html:
            return HTML(div)
        else:
            return div
