# -*- coding: utf-8 -*-
# EventMeta.py
#
from pathlib import Path
import shutil
from warnings import warn
from datetime import datetime as dt
import pandas as pd
from collections import OrderedDict
from enum import Enum
import json
from pprint import pprint as pp, pformat
from IPython.display import Markdown
import re
from bs4 import BeautifulSoup as soup
from jinja2 import Environment, FileSystemLoader
from jinja_markdown import MarkdownExtension
import pypandoc as pand

from manage.Utils import (save_file,
                          load_file_contents,
                          get_file_lines,
                          get_project_dirs,
                          split_url)

#..........................................................
# EventManagement project folders:
# DIR_DATA: to store audio tracks and audio text;
# DIR_IMG: to store pictures/figures, for documentation mostly.
DIR_DATA, DIR_IMG = get_project_dirs()

# Repo info, the parent folder of ./resources:
REPO_PATH = Path(__file__).parents[3]
REPO_NAME = REPO_PATH.name
#'event-transcripts-demo' 
# '-demo': for this proof of concept only, else will be 'event-transcripts'
DEMO = REPO_NAME.endswith('demo')
DEMO_README = 'README_new.md'

def main_readme_path():
    md_file = DEMO_README if DEMO else 'README.md'
    return REPO_PATH.joinpath(md_file)

MAIN_README = main_readme_path()

# Templating with jinja
DIR_MD_TPL = DIR_DATA.parent.joinpath('templates')
MD_TPL = 'transcript_header.md'

CURRENT_YEAR = dt.today().year
DEFAULT_HOST = "Reshama Shaikh"
NA = 'N.A.' # 'Not Applicable or Not Available; 'N/A' is 'N over A'.

# YouTube domains
YT_URL = "https://youtu.be/"
#  thumbnail:
YT_IMG_URL0 = "http://img.youtube.com/vi/" # <vid>/0.jpg"
YT_IMG_URL1 = "/0.jpg"
HREF_DOM = "http://www.youtube.com/watch?feature=player_embedded&v="

# reading of main readme table (in NEW readme):
TBL_COLS = 6
TBL0 = '<!-- main_tbl_start -->'
TBL1 = '<!-- main_tbl_end -->'
DEF_IMG_W = "25%"

#..................................................................
class TrStatus(Enum):
    COMPLETE = "Complete"
    PARTIAL_WIP = "Partial (w.i.p.)"
    PARTIAL_HELP = "Partial (new editor requested)"
    REVIEW = "Needs reviewer"
    TODO = "Not yet processed (editor needed)"
    NOREC = "Not recorded"


def get_meta_dir(year=CURRENT_YEAR):
    return REPO_PATH.joinpath(str(year), 'meta')


def check_year(yr):
    ok = len(str(yr)) == 4
    if not ok:
        warn('Provide a four-digit year.')
    return ok


def get_meta_jsonname(idn, year=CURRENT_YEAR, create_year_dir=True):
    """
    Return the meta json filepath, else None.
    Create the year folder if not found.
    """
    if not check_year(year):
        return None

    META = get_meta_dir(year)
    if not META.is_dir():
         Path.mkdir(META)
         return None

    fpath = META.joinpath(F'{int(idn):02d}.json')
    if fpath.is_file():
        return fpath
    return None


def split_tbl_line(txt):
    t = [w.strip() for w in txt.split('|')]
    return t[1:-1]

   
def get_tbl_from_readme(main_readme, is_text=False):
    """
    Extract the table portion of the readme text.
    Return info about the table, e.g:
    Example:
    tbl_info = get_tbl_from_readme(main_readme)
    with parts:
      tbl_info[0]: header -> df.columns
      tbl_info[1]: rows
      tbl_info[2]: start/end markers indices, [s,e]
      tbl_info[-1]: whether last row was empty
    """
    if is_text:
        readme_text = main_readme
    else:
        readme_text = get_file_lines(main_readme)

    idx0 = readme_text.index(TBL0+'\n')
    idx1 = readme_text.index(TBL1+'\n')
    tbl = readme_text[idx0+1:idx1]
    #| #| Speaker| Talk Transcript| Transcriber| Status| Notes|
    cols = split_tbl_line(tbl[0].replace('#', 'N'))
    
    # check: empty last row?
    empty = '|' * (TBL_COLS+1) + '\n'
    empty_last_row = tbl[-1].replace(' ', '') == empty
    # rows only, no headers
    tbl = tbl[2:]
        
    return cols, tbl, [idx0, idx1], empty_last_row


def df_from_readme_tbl(main_readme=MAIN_README, is_text=False):
    """
    Return the table in README as a pd.df.
    main_readme is either the md filepath or its lines.
    See `get_tbl_from_readme` docstring.
    """
    tbl_info = get_tbl_from_readme(main_readme, is_text=is_text)

    tbl_arr = []
    for e in tbl_info[1]:
        tbl_arr.append(split_tbl_line(e))
    df = pd.DataFrame(tbl_arr, columns=tbl_info[0])

    empty_last_row = tbl_info[-1]
    if empty_last_row:
        df.drop(df.index.argmax())
        
    # Split "Talk Transcript (md link)": 
    # title, readme= transcript md file.
    titles = []
    reads = []
    talk_link = [v.split('](') for v in df['Talk Transcript'].values]
    for i, v in enumerate(talk_link):
        titles.append(talk_link[i][0].strip('['))
        if len(talk_link[i]) > 1:
            reads.append(talk_link[i][1][5:-1])
        else:
            reads.append(NA)

    df['title'] = titles
    df['readme'] = reads
    
    return df, empty_last_row, tbl_info[2]

#............................................................
# List flds_internals: first 2 are autogenerated once relevant info exists
flds_internals = ['idn', # index of new row in main readme table
                  'video_url',
                  'video_href_src', # video thumbnail, defaults to 1st frame pic.
                  'video_href_alt', # alt text, defaults to title
                  'video_href_w', # img width, defaults to 25%
                  'title_kw', # topic, possibly extracted from title
                  'transcript_md', # filename for saving & linking
                  'meta_json',  # json filename (from transcript_md)
                  'audio_track', # ../data/<idn>_<video_id>.mp4
                  'audio_text',  # ../data/<idn>_<video_id>.txt
                  'has_transcript', # bool
                  'status', # to enable status update
                  'notes', # to enable notes update
                 ]

REPR_INFO = "< NOT SHOWN (can be VERY long).\n To view  it, you can "
REPR_INFO += "pretty-print TranscriptMeta.metadata['formatted_transcript']) >"
            
# class TranscriptMeta
# ....................................................................
class TranscriptMeta:
    
    def __init__(self, idn=None, year=CURRENT_YEAR):
        self.year = str(year)
        self.readme = MAIN_README
        self.readme_text = get_file_lines(self.readme).copy()
        
        tbl_info = df_from_readme_tbl(self.readme_text, is_text=True)
        self.df = tbl_info[0]
        self.empty_lastrow = tbl_info[1]
        self.tbl_delims = tbl_info[2]
        self.row_offset = 1 if self.empty_lastrow else 2
        # not used
        #self.df_unassigned = self.df[self.df.Transcriber == "?"]
        
        self.TPL = MarkdownTpl()
        self.fields_autogenerated = flds_internals

        # idn is a switch: if None => new event setup.
        if idn is None:  # initial setup
            self.metadata = self.make_meta(year)
        else:
            try:
                # Load json file
                self.metadata = self.load_meta(idn, year)
            except: # FileNotFoundError
                # Parse header of existing transcript.md file
                self.metadata = self.parse_md(idn, year)
                
            if self.metadata['transcript_md'] == NA:
                self.set_path_keys()
                
            self.set_audiov_keys()
            self.save_meta()
            

    def idn_frmt(self, i):
        return F"{int(i):02d}"

    
    def default_href(self, id=None):
        href = HREF_DOM
        if id is None:
            href += self.metadata['yt_video_id']
        else:
            href += id
        return href

    
    def default_href_src(self, id=None):
        href_src = YT_IMG_URL0
        if id is None:
            href += self.metadata['yt_video_id']
        else:
            href += id
        return href + YT_IMG_URL1

    
    def key_exists(self, k):
        return self.metadata.get(k,None) is not None

    
    def key_isna(self, k):
        return self.metadata[k] == NA

            
    def check_key(self, k):
        if self.key_isna(k):
            msg = F"check_key :: metadata['{k}']={NA}"
            raise ValueError(msg)


    def set_path_keys(self):
        """Set the value of keys: transcript_md & meta_json.
        File name pattern:
        <idn>-<presenter first>-<presenter last>-<title_kw>.[md]
        """
        self.check_key('idn')
        self.check_key('presenter')
        
        presenter = self.metadata['presenter'].lower()
        if ',' in presenter:
            # retrieve first names (up to 2):
            names = [n.split() for n in presenter.split(',')[:2]]
            # first names only if multi
            pres_first, pres_last = names[0][0], names[1][0]
        else:
            pres_first, pres_last = presenter.split()
            
        i = self.metadata['idn']
        self.metadata['meta_json'] = F'{i}.json'
        
        if not self.key_exists('title_kw'):
            self.metadata['title_kw'] = NA
            
        if self.key_isna('title_kw'):
            transx = F"{i}-{pres_first}-{pres_last}.md"
        else:
            tkw = self.metadata['title_kw'].replace(' ', '-').lower()
            transx = F"{i}-{pres_first}-{pres_last}-{tkw}.md"
        self.metadata['transcript_md'] = transx
        
        return


    def set_audiov_keys(self):
        """Set the value of 'audio & video' keys: 
           - audio_track, audio_text (filenames);
           - video_href, video_href_src, video_href_alt, video_href_w;
           The audio keys will be used by transcriber for 
           downloading into the ../data folder.
           File name pattern: <idn>_<video_id> + ['.mp4' | '.txt'].
        """
        self.check_key('idn')
        self.check_key('yt_video_id')
        
        pat = F"{self.metadata['idn']}_"
        pat += F"{self.metadata['yt_video_id']}"
        self.metadata['audio_track'] = pat + '.mp4'
        # file path of initial transcript (xml->str):
        # once text is finalized -> metadata['formatted_transcript']
        self.metadata['audio_text'] = pat + '.txt'
        
        if (self.metadata['video_href'] == NA
            or self.metadata['video_href'] is None):
           self.metadata['video_href'] = self.default_href()
        
        if (self.metadata['video_href_src'] == NA
            or self.metadata['video_href_src'] is None):
           self.metadata['video_href_src'] = self.default_href_src()
        
        if (self.metadata['video_href_alt'] == NA
            or self.metadata['video_href_alt'] is None):
           self.metadata['video_href_alt'] = self.metadata['title'].split('(https')[0]
        
        if (self.metadata['video_href_w'] == NA
            or self.metadata['video_href_w'] is None):
           self.metadata['video_href_w'] = DEF_IMG_W

        return 
    

    def make_meta(self, year):
        """
        Generic presentation meta file (data to be provided at setup 
        after video url is known). Its values will be presented by the
        Workflow Admin tab for interactive update.
        Refer to the md template: ../templates/transcript_header.md
        """
        md_header_d = OrderedDict()
        fields = self.TPL.tpl_keys + self.fields_autogenerated 
        
        for k in fields:
            md_header_d[k] = NA

        # Update dict with defaults:
        new = self.df.index.argmax() + self.row_offset
        md_header_d['idn'] = self.idn_frmt(new)
        md_header_d['year'] = str(year)
        md_header_d['transcriber'] = '?'
        md_header_d['extra_references'] = None
        md_header_d['has_transcript'] = False
        md_header_d['status'] = TrStatus.TODO.value
        md_header_d['notes'] = ''
        md_header_d['video_href_w'] = DEF_IMG_W #thumbnail
        
        return md_header_d


    def order_json(self, metajson):
        header_d = OrderedDict()
        fields = self.TPL.tpl_keys + self.fields_autogenerated
        for k in fields:
            header_d[k] = metajson[k]
        return header_d    
            
        
    def load_meta(self, idn, year):
        """Load the presentation meta data.
           Assume json file exists; init() traps error.
       :param: idn (int, None): presentation id
       :param: year (int): default to current day's year.
        """
        meta_name = get_meta_jsonname(idn, year)
        with open(meta_name) as fh:
            meta_json = json.load(fh)
        header_od = self.order_json(meta_json)
        return header_od 

    
    @staticmethod
    def parse_href(trx_md_top):
        v_header = "## Video"
        v0 = trx_md_top.find(v_header)
        v1 = trx_md_top.find("## Transcript")

        href_block = trx_md_top[v0:v1].replace(v_header,'')
        href_block = href_block.replace('\n\n','').replace('\n',' ')
        href_html = soup(href_block, 'html.parser')

        # meta keys needed: 
        # 'yt_video_id','video_href' & '~_src', '~_alt','~_w'
        video_hrefs = OrderedDict([('yt_video_id', None),
                                   ('href', None),
                                   ('src',None),
                                   ('alt',None),
                                   ('width', None)])
        
        for link in href_html.find_all('a', {'href': True}):
            video_hrefs['href'] = link.get('href')
            _, vid = split_url(video_hrefs['href'])
            
            norm_src = YT_IMG_URL0 + vid + YT_IMG_URL1
            for c in link.find_all('img'):
                if c.has_attr('src'):
                    s = c.get('src')
                    if s != norm_src:
                        video_hrefs['src'] = s
                    else:
                        video_hrefs['src'] = norm_src
                else:
                    video_hrefs['src'] = norm_src
                    
                if c.has_attr('alt'):
                    video_hrefs['alt'] = c.get('alt')
                    
                if c.has_attr('width'):
                    w = c.get('width')
                    if w != DEF_IMG_W:
                        video_hrefs['width'] = w
                    else:
                        video_hrefs['width'] = DEF_IMG_W
                else:
                    video_hrefs['width'] = DEF_IMG_W
                    
            video_hrefs['yt_video_id'] = vid
            return video_hrefs
        
        
    def parse_md(self, idn, year):
        """Parse exsisting transcript.md file and extract the metadata
           from the header.
           Case where no json file.
        """
        idn = self.idn_frmt(idn)
        # Use df to get path
        trx_md = self.df.loc[self.df.N==idn, 'readme'].values[0]
        if trx_md == NA:
            msg = "**This event may not have a transcript:** either it was not "
            msg += "recorded or the README table was not updated.<br>"
            # col idx -2: don't display cols of extracted data
            ro = self.df.loc[self.df.N==idn,self.df.columns[:-2]].style.render()
            msg += F"<div>{ro}</div>"
            return Markdown(msg)

        fname = REPO_PATH.joinpath(str(year), trx_md)
        # The unsplit `mdlines` is used by parse_href()
        mdlines = Markdown(filename=fname).data
        
        md_lines = mdlines.splitlines()
        n_lines = len(md_lines)
        has_transcript = n_lines > self.TPL.min_header_lines

        # get the key, values pairs
        HDR2 = '## '
        LST = '- '
        md_kvals = {}
        
        # Fill dict with available so far:
        md_kvals['year'] = str(year)
        md_kvals['idn'] = idn
        
        # Get 1st line => presenter, title
        pt = md_lines[0][1:].split(':')
        md_kvals['presenter'] = pt[0].strip()
        md_kvals['title'] = pt[1].strip()
        
        # Get the video link params
        vhrefs = self.parse_href(mdlines[:2500])

        md_kvals['video_href'] = vhrefs['href']
        md_kvals['video_href_src'] = vhrefs['src']
        md_kvals['video_href_alt'] = vhrefs['alt']
        md_kvals['video_href_w'] = vhrefs['width']
        
        # <h2> headers list from template:
        h2_hdrs = self.TPL.tpl_h2
        h2_subheaders = list(self.TPL.hdrs_to_keys.keys())
        
        trans_idx = () # to retrieve any existing Transcript text
        extra = ''
        add_key = False
        for i, s in enumerate(md_lines):
            if s.startswith(HDR2):
                hdr = s.split(HDR2)[1].strip()
                if hdr == 'Transcript':
                    trans_idx = (i, hdr)
                    # done: processing further would parse
                    # the transcript text following "## Transcript"
                    break
                add_key = hdr in h2_hdrs
                if not add_key:
                    # treat all 'custom' items as extra_references:
                    extra += HDR2 + hdr + '\n'
                continue
            elif s.startswith(LST):
                kval = s.split(LST)[1].split(':', maxsplit=1)
                k = kval[0].strip()
                if add_key and k in h2_subheaders:
                    if k == 'Video':
                        k = 'video_url'
                    #else:
                    #    k = self.TPL.hdrs_to_keys[k]

                    md_kvals[k] = kval[1].strip()
                else:
                    extra += LST + k + ':  ' + kval[1].strip() + ' \n'

        if extra:
            md_kvals['extra_references'] = extra
        else:
            md_kvals['extra_references'] = NA

        if has_transcript:
            i = 2 if len(md_lines[trans_idx[0]+1]) == 0 else 1
            text = "\n".join(md_lines[trans_idx[0]+i:])
            md_kvals['formatted_transcript'] = text
        else:
            md_kvals['formatted_transcript'] = NA
 
        # reconcile
        for k, v in self.TPL.hdrs_to_keys.items():
            # Get the value from the md dict:
            val = md_kvals.get(k, NA)

            if k == 'Video':
                _, vid = split_url(md_kvals['video_url'])
                md_kvals['yt_video_id'] = vid
                
                if md_kvals['video_href'] is None:
                   md_kvals['video_href'] = self.default_href(vid)
                
                if md_kvals['video_href_src'] is None:
                   md_kvals['video_href_src'] = self.default_href_src(vid)
                
                if md_kvals['video_href_alt'] is None:
                    # title w/o the link
                    md_kvals['video_href_alt'] = md_kvals['title'].split('(https')[0]

            elif k == 'Transcript': # markdown file link
                if val == NA:
                    msg = "No Transcript value (Markdown file): required"
                    raise ValueError(msg)

                md_kvals[v] = val.split('/')[-1]
                p = md_kvals['presenter'].lower().replace(' ', '-')
                t_kw = md_kvals[v].partition(p)[2][1:-3].replace('-',' ')
                md_kvals['title_kw'] = t_kw
                del md_kvals[k]
            else:
                md_kvals[v] = val
                del md_kvals[k]

       
        # Check which main fields are missing:
        msg = ''
        leftover = set(self.TPL.tpl_keys).difference(set(md_kvals.keys()))
        n_leftover = len(leftover)
        if n_leftover:
            msg = 'Warning: '
            if n_leftover > 1:
                msg += 'these keys are not set:\n'
                for n in leftover:
                    msg += F'\t{n}\n'
            else:
                msg += F'this key is not set:\n{leftover}'
            print(msg)
        
        # Finally, set the other internal fields:
        status = self.df.loc[self.df.N==idn, 'Status'].values[0]
        md_kvals['status'] = status
        notes = self.df.loc[self.df.N==idn, 'Notes'].values[0]
        md_kvals['notes'] = notes
        md_kvals['has_transcript'] = has_transcript
        md_kvals['meta_json'] = F'{idn}.json'
        
        return md_kvals
            
            
    def update_metadata(self, new_meta):
        """Update metadata dict with new_meta dict."""
        new_meta['presenter'] = new_meta['presenter'].title()
        new_meta['title'] = new_meta['title'].title()
        new_meta['title_kw'] = new_meta['title_kw'].replace(' ', '-').lower()
        self.metadata = new_meta
        self.set_path_keys()
        self.set_audiov_keys()

        
    def save_meta(self):
        """Save dict as json file."""
        self.check_key('transcript_md')
        META = get_meta_dir(self.metadata['year'])
        meta_json = META.joinpath(self.metadata['meta_json'])
        with open(meta_json, 'w') as fh:
            json.dump(self.metadata, fh)
        return


    def get_transcript_text(self):
        txt = self.metadata.get('formatted_transcript', NA)
        if txt == NA:
            out = ''
        else:
            out = '\n'.join([line for line in txt])
        return out


    def transcript_md_path(self):
        return REPO_PATH.joinpath(str(self.metadata['year']), 
                                  self.metadata['transcript_md'])
        
    def save_transcript_md(self):
        """
        Output the rendered template into the transcript_md file.
        """
        self.check_key('transcript_md')
        md_out = self.transcript_md_path().as_posix()
        
        self.TPL.render_to_md(self.metadata, md_out)
        self.metadata['by_pandoc'] = True
        return

    
    def update_readme(self):
        """
        Add (update) table row as per meta.
        :params main_readme (pathlib.Path): fullpath to repo readme.
        :params meta (dict): data dict
        """
        bkp = DIR_DATA.joinpath('backup', self.readme.name + '.bkp')
        # Backup the file to /notebooks fld
        shutil.copy(self.readme, bkp)
        
        # Get the text
        # rem: self.readme_text contains a copy
        #       => for recovery?
        try:
            readme_txt = get_file_lines(self.readme)
        except FileNotFoundError:
            # try reverting to previously backup copy
            shutil.copy(bkp, self.readme)
            readme_txt = get_file_lines(self.readme)

        # Backup the file to /notebooks fld
        #shutil.move(self.readme, bkp)

        # Get the table data:
        i, j = self.tbl_delims
        off1 = 3  # offset 1 = delim row + 2 header rows
        off2 = -1 if self.empty_lastrow else 0
        tbl = readme_txt[i+off1:j+off2]
        
        #| #| Speaker| Talk Transcript| Transcriber| Status| Notes|
        # Construct last row:
        pipestr = '| '
        # Talk Transcript = md link: [title](year/readme)
        talk = F"[{self.metadata['title']}]"
        talk += F"({self.metadata['year']}/{self.metadata['transcript_md']})"
        fields = [self.metadata['idn'],
                  self.metadata['presenter'],
                  talk, 
                  self.metadata['transcriber'],
                  self.metadata['status'],
                  self.metadata['notes']
                 ]
        ro = pipestr + pipestr.join(fields) + pipestr + '\n'
        tbl.append(ro)
    
        # Update main text w/table data:
        readme_txt[i+off1:j] = tbl
    
        # Re-create readme:
        with open(self.readme, 'w') as fh:
            fh.writelines(readme_txt)

        return F'Table in {self.readme.name} was updated.'


    def __repr__(self):
        #msg = "TranscriptMeta Class rep: only prints metadata."
        if self.metadata['has_transcript']:
            without_trx = self.metadata.copy()
            without_trx['formatted_transcript'] = REPR_INFO
            return pformat(without_trx)

        return pformat(self.metadata)


# class MarkdownTpl
# ....................................................................
# - jinja2: Without jinja2, the template would need standard str format
#           delimiters ({,}). Yet, even escaped braces produce a KeyError
#           when the template str is resolved with data from the dict, 
#           e.g.: md_out = md_tpl.format(**metadata).
# - jinja_markdown: Extension enabling jinja2 to read Markdown template;  
#                   Does not provide rendering to Markdown, hence the use
#                   of pandoc.
# - pypandoc (& pandoc): used to convert html from jinja2 `render()` to md.
# The class MarkdownTpl was created to wrap jinjaX objects and provide the
# needed `.render_to_md()` function.

class MarkdownTpl:
    def __init__(self, tpl_dir=DIR_MD_TPL, md_tpl_name=MD_TPL):
        self.jinja_env = Environment(extensions=[MarkdownExtension],
                                     loader=FileSystemLoader(tpl_dir))
        self.tpl = self.jinja_env.get_template(md_tpl_name)
        self.tpl_path = tpl_dir.joinpath(md_tpl_name)
        # For parsing transcript_md files w/o json:
        self.tpl_h2 = ['Key Links', 'Video', 'Transcript']
        self.hdrs_to_keys = OrderedDict([('Transcript', 'transcript_md'),
                                         ('Meetup Event', 'meetup_url'),
                                         ('Slides', 'slides_url'),
                                         ('GitHub Repo', 'repo_url'),
                                         ('Jupyter Notebook', 'notebook_url'),
                                         ('Transcriber', 'transcriber'),
                                         ('Video', ['video_url',
                                                    'yt_video_id',
                                                    'video_href',
                                                    'video_href_src',
                                                    'video_href_alt',
                                                    'video_href_w'])
                                        ])
        
        self.tpl_code = Markdown(filename=self.tpl_path).data
        self.min_header_lines = self.get_min_header_lines()
        self.tpl_keys = self.get_tpl_keys()
        self.html = '' # set by render_to_md()


    def get_min_header_lines(self):
        """
        Number of lines in new header (without transcript)
        minus comments.
        """
        RE_COMMENT = re.compile(r"\<\!\-\-(?:.|\n|\r)*?-->")
        mdcode = self.tpl_code
        n_comments = 0
        for cmt in RE_COMMENT.findall(mdcode):
            n_comments += len(cmt.splitlines())
        return len(mdcode.splitlines()) - n_comments

 
    def get_tpl_keys(self):
        """
        Process by line to preserve order of appearance.
        """
        RE_KW = re.compile(r"{{( *\w+ *)}}")
        okeys = []
        for line in self.tpl_code.split('\n'):
            for kw in RE_KW.findall(line):
                if kw not in okeys:
                    okeys.append(kw)
        return okeys


    def get_n_comment_lines(self):
        RE_COMMENT = re.compile(r"\<\!\-\-(?:.|\n|\r)*?-->")
        n_comments = 0
        for cmt in RE_COMMENT.findall(self.tpl_code):
            n_comments += len(cmt.splitlines())

        return n_comments


    def standardize_pandoc_md(self,converted):
        """
        Convert pandoc 'markdown_mmd' conversion
        to standard md (not rst).
        """
        H1_LINE = re.compile(r"[=]{3,}")
        H2_LINE = re.compile(r"[-]{3,}")
        DIV_LINE0 = re.compile(r"^<div markdown")
        DIV_LINE1 = re.compile(r"^</div>")

        code_lines = converted.splitlines()

        # rst-like underlines for headers:
        for i, line in enumerate(code_lines):
            for rec in [H1_LINE, H2_LINE]:
                found = rec.findall(line)
                if len(found):
                    j = i - 1
                    if j == 0:
                        code_lines[j] = "# " + code_lines[j]
                    else:
                        code_lines[j] = "## " + code_lines[j]
                    code_lines[i] = code_lines[i].replace(found[0],'')

        # video link:
        div_result = []
        for i, line in enumerate(code_lines):
            if len(div_result) == 2:
                break
            for rec in [DIV_LINE0, DIV_LINE1]:
                found = rec.findall(line)
                if len(found):
                    div_result.append([i, found])

        div_part = code_lines[div_result[0][0]:div_result[1][0]+1]
        div_part[0] = div_part[0].replace('markdown="1" ','')

        link_part = ''.join([line for line in div_part[1:-1] if line])
        parts = link_part.split(']')
        v_link = F"""  <a href="{parts[2][1:-1]}" target="_blank">
              <img src="{parts[1][1:-1]}" 
                   alt="{parts[0][3:]}"/>
          </a>
        """
        div_part[1:-1] = [v_link]
        code_lines[div_result[0][0]:div_result[1][0]+1] = div_part
        code_std = '\n'.join([line for line in code_lines])
        code_std = code_std.replace('\n\n\n', '\n\n')

        for ks in list(self.hdrs_to_keys)[:-1]:
            code_std = code_std.replace(ks+':\n', ks+':')
            
        p = code_std.index("## Video")
        end = code_std[p:]
        code_std = code_std[:p].replace('    ','  ')
        code_std = code_std.replace('<','').replace('>','') + end
        return code_std


    def render_to_md(self, data_dict, md_output_name=None):
        """
        Jinja2 with the Markdown extension enable the loading of a Md template
        but the rendering is in html. pypandoc is used to convert the output
        to Markdown.
        """
        self.html = self.tpl.render(data_dict)
        converted = pand.convert_text(self.html, 'markdown_mmd', 'html')
        converted = converted.replace("\r", "")
        
        standard_md = self.standardize_pandoc_md(converted)
        if md_output_name is None:
            # No file saved, i.e. view:
            return standard_md

        md_out = Path(md_output_name)
        save_file(md_out, standard_md) #, replace=True)
        print('Markdown tpl rendered into file:\n', md_out)


def dummy_update(meta_obj, meta_d, video_url, meetup_url,
                 title='Automating Audio Transcription.',
                 titlekw='audio foo',
                 presenter='Cat Chenal, Reshama Shaikh'):
    
    meta_d['video_url'] = video_url
    vsite, vid = split_url(video_url)
    meta_d['yt_video_id'] = vid
    meta_d['video_href'] = HREF_DOM + vid
    meta_d['video_href_src'] = YT_IMG_URL0 + vid + YT_IMG_URL1
    if meta_d['video_href_alt'] == NA:
        meta_d['video_href_alt'] = title
            
    meta_d['meetup_url'] = meetup_url
    meta_d['title'] = title
    meta_d['title_kw'] = titlekw
    meta_d['presenter'] = presenter
    
    extra = "## Other References\n"
    extra += "- Binder:  <url>\n- Paper:  <Paper url or citation>  \n"
    extra += F"- Wiki:  This is an excellent [wiki on {meta_d['title_kw']}]"
    extra += "(http://en.wikipedia.org/wiki/Main_Page) (extra ref 2) \n"""
    meta_d['extra_references'] = extra

    meta_obj.update_metadata(meta_d)
    return

