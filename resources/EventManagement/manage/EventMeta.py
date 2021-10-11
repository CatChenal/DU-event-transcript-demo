# -*- coding: utf-8 -*-
# EventMeta.py
# Programmer: Cat Chenal
#
from pathlib import Path
import shutil
from collections import OrderedDict
import pandas as pd
from bs4 import BeautifulSoup as soup
from datetime import datetime as dt
from enum import Enum
import re
from pprint import pformat
from IPython.display import Markdown

from manage import Utils as UTL
#..........................................................
#DEFAULT_HOST = "Reshama Shaikh"  # not used
CURRENT_YEAR = dt.today().year

# Repo info, the parent folder of ./resources:
REPO_PATH = Path(__file__).parents[3]
REPO_NAME = REPO_PATH.name

# EventManagement project folders:
DIR_DATA, DIR_IMG = UTL.get_project_dirs()
DIR_META = UTL.get_subfolder('meta', parent_dir=DIR_DATA)

#'event-transcripts-demo' 
# '-demo': for this proof of concept only, else will be 'event-transcripts'
DEMO = REPO_NAME.endswith('demo')
DEMO_README = 'README.md' # was README_new.md

def main_readme_path():
    md_file = DEMO_README if DEMO else 'README.md'
    return REPO_PATH.joinpath(md_file)

MAIN_README = main_readme_path()

# Data Umbrella's github repo for transcripts:
DU_GH = 'https://github.com/data-umbrella/event-transcripts/'

NA = 'N.A.' # 'Not Applicable or Not Available; 'N/A' is 'N over A'.
def isNA(txt):
    return txt in [NA, 'N/A']

def key_isna(k, d):
    return isNA(d[k])
    

# YouTube domains
YT_URL = "https://youtu.be/"
#  thumbnail: YT_IMG_URL0 + vid + YT_IMG_URL1
YT_IMG_URL0 = "http://img.youtube.com/vi/"
YT_IMG_URL1 = "/0.jpg"
DEF_IMG_W = "25%"
HREF_DOM = "http://www.youtube.com/watch?feature=player_embedded&v="

#..................................................................
flds_internals = ['year',
                  'idn', # index of new row in main readme table
                  'video_url',
                  'title_kw', # topic or space-sep'd topics from title
                  'transcript_md', # filename for saving & linking
                  'audio_track', # ../data/meta/<year>_<idn>_<video_id>.mp4
                  'audio_text',  # ../data/meta/<year>_<idn>_<video_id>.txt
                  'has_transcript', # bool
                  'trans_idx', # index of '## Transcript'
                  'status', # to enable status update
                  'notes', # to enable notes update
                  'video_embed' # to play video within the gui
                 ]

H2_HDRS = ['Key Links', 'Video', 'Transcript']
H2_HDRS_KEYS = OrderedDict([('Meetup Event', 'event_url'),
                            ('Slides', 'slides_url'),
                            ('GitHub Repo', 'repo_url'),
                            ('Jupyter Notebook', 'notebook_url'),
                            ('Transcriber', 'transcriber'),
                            ('Video', ['yt_video_id',
                                       'video_href',
                                       'video_href_src',
                                       'video_href_alt',
                                       'video_href_w',
                                       'video_embed'])
                            ])

REQ_FLDS = ['year', 'idn', 'presenter', 'title', 'title_kw',
            'video_url', 'yt_video_id', 'status']

HDR_TPL = """# {presenter}: {title}  

## Key Links  
- Meetup Event:  {event_url}  
- Video:  https://youtu.be/{yt_video_id}  
- Slides:  {slides_url}  
- GitHub Repo:  {repo_url}  
- Jupyter Notebook:  {notebook_url}  
- Transcriber:  {transcriber}  
{extra_references}  

## Video
<a href="{video_href}" target="_blank">
    <img src="{video_href_src}" 
         alt="{video_href_alt}"
         width="{video_href_w}"/>
</a>

## Transcript  
{formatted_transcript}  
"""
V_EMBED = """
<iframe width="560" height="315" 
        src="https://www.youtube-nocookie.com/embed/{}?cc_load_policy=1&autoplay=0" 
        frameborder="0">
</iframe>
"""

# ............................................
class TrStatus(Enum):
    COMPLETE = "Complete"
    PARTIAL_WIP = "Partial (w.i.p.)"
    PARTIAL_HELP = "Partial (new editor requested)"
    REVIEW = "Needs reviewer"
    TODO = "Not yet processed (editor needed)"
    NOREC = "Not recorded"


def split_tbl_line(txt):
    """Split a Markdown table row into its values."""
    t = [w.strip() for w in txt.split('|')]
    return t[1:-1]


def get_tbl_delims(md_text):
    """
    Return indices of the README table
    delimiters (html comments).
    """
    # Delimiters in README must match:
    TBL0 = '<!-- main_tbl_start -->'
    TBL1 = '<!-- main_tbl_end -->'
    
    msg = 'README table.{} delimiter missing:\n{}'
    try:
        idx0 = md_text.index(TBL0+'\n')
    except:
        raise ValueError(msg.format('start', TBL0))
    try:
        idx1 = md_text.index(TBL1+'\n')
    except:
        raise ValueError(msg.format('end', TBL1))
    return idx0, idx1

                         
def get_table_info(main_readme):
    """
    Extract the table portion of the readme text.
    Return info about the table, e.g:
    Example:
    tbl_info = get_table_info(main_readme)
    with parts:
      tbl_info[0]: header -> df.columns
      tbl_info[1]: rows
      tbl_info[2]: start/end markers indices, [s,e]
      tbl_info[-1]: whether last row was empty
    """
    readme_text = UTL.get_file_lines(main_readme)
    
    idx0, idx1 = get_tbl_delims(readme_text)
    
    tbl = readme_text[idx0+1:idx1]
    cols = split_tbl_line(tbl[0].replace('#', 'N'))
    
    # check: empty last row?
    empty = '|' * (len(cols)+1) + '\n'
    last_row = tbl[-1].replace('?', '').replace(' ', '')
    empty_last_row = last_row == empty
    # rows only, no headers
    tbl = tbl[2:]
        
    return cols, tbl, [idx0, idx1], empty_last_row


def df_from_readme_tbl(main_readme=MAIN_README):
    """
    Return the table in README as a pandas df.
    See `get_table_info` docstring.
    """
    tbl_info = get_table_info(main_readme)

    tbl_arr = []
    for e in tbl_info[1]:
        tbl_arr.append(split_tbl_line(e))
    df = pd.DataFrame(tbl_arr, columns=tbl_info[0])

    #empty_last_row = tbl_info[-1]
    if tbl_info[-1]:
        #empty_last_row
        df.drop(df.index.argmax())

    # Add columns 'year', 'name'
    vals = df['Talk Transcript'].values
    md = ([v.split('](')[1][:-1].split('/') 
           if v.startswith('[') else [NA, NA]
           for v in vals])
    df['year'] = [v[0] for v in md]
    df['name'] = [v[1] for v in md]
    
    return df, tbl_info[2]


def meta_basename(year, idn, vid):
    """
    Basename for event meta files (audio, xml, text).
    """
    return F"{year}_{idn}_{vid}"
   
        
def idn_frmt(i):
    return F"{int(i):02d}"


def default_href(vid):
    return HREF_DOM + vid


def default_href_src(vid):
    return YT_IMG_URL0 + vid + YT_IMG_URL1


# ....................................................................
# class TranscriptMeta
REPR_INFO = "< NOT SHOWN (can be VERY long).\nTo view  it, run "
REPR_INFO += "print(TranscriptMeta.event_dict['formatted_transcript']) >"

class TranscriptMeta:
    
    def __init__(self, idn=None, year=CURRENT_YEAR):
        if year is None:
            year=CURRENT_YEAR
        yr = str(year)
        if len(yr) == 2: yr = '20' + yr
        self.year = yr
        self.readme = MAIN_README
        
        self.tbl_info = df_from_readme_tbl(self.readme)
        self.df, self.tbl_delims = self.tbl_info
        self.row_offset = 2
        
        self.TPL = HDR_TPL
        self.TPL_KEYS = self.get_tpl_keys()
        
        self.NEW = False
        if idn is None:
            self.NEW = True
            self.event_dict = self.new_event_dict()
        else:
            self.idn = idn_frmt(idn)
            self.event_dict = self.parse_md()
            
        # TRX.YTVAudio class:
        self.YT = None
        # To override defaults in redo_initial_transcript:
        self.new_minutes_mark = None
        self.new_wrap_width = None
        # set by update_dict():
        self.to_delete = None
        
            
    def refresh_tbl_info(self):
        self.tbl_info = df_from_readme_tbl(self.readme)
        # rm: self.empty_lastrow, 
        self.df, self.tbl_delims = self.tbl_info
        
 
    def get_tpl_keys(self):
        """
        Process by line to preserve order of appearance.
        """
        RE_KW = re.compile(r"{( *\w+ *)}")
        okeys = []
        for line in self.TPL.split('\n'):
            for kw in RE_KW.findall(line):
                if kw not in okeys:
                    okeys.append(kw)
        return okeys
    

    def get_event_dict(self):
        """
        Return dict from TPL_KEYS with all values = NA
        """
        all_keys = self.TPL_KEYS + flds_internals
        assert(len(all_keys) == len(set(all_keys)))

        event_dict = OrderedDict()
        for k in all_keys:
            event_dict[k] = NA
        return event_dict

    
    def last_of_yr_info(self):
        yrdf = self.df.loc[self.df.year == self.year]
        yrdf = yrdf.sort_values(['year','N'])
        if yrdf.shape[0]:
            last_idx = yrdf.index.max()
            N = yrdf.loc[last_idx,'N']
        else:
            last_idx = self.df.index.max()
            N = 0
        return last_idx, N


    def new_event_dict(self):
        """
        Create a 'starter' event dict with event id generated
        from the readme table df.
        """
        new_dict = self.get_event_dict()

        # Update dict with defaults:
        new_dict['year'] = self.year
        
        last_idx, N = self.last_of_yr_info()
        self.idn = idn_frmt(int(N) + 1)
        new_dict['idn'] = self.idn
        new_dict['transcriber'] = '?'
        new_dict['extra_references'] = ''
        new_dict['has_transcript'] = False
        new_dict['status'] = TrStatus.TODO.value
        new_dict['notes'] = ''
        # thumbnail, currently; should be embed:
        new_dict['video_href_w'] = DEF_IMG_W
        
        v1 = self.insertion_idx(self.TPL.format(**new_dict))
        new_dict['trans_idx'] = v1
        return new_dict

  
    @staticmethod
    def set_path_keys(d):
        """
        Set the value of keys: transcript_md & title_kw.
        Assume validation is done.
        File name pattern:
        <idn>-<presenter first>-<presenter last>[-<title_kw>]
        """
        presenter = d['presenter'].lower()
        if ',' in presenter:
            # retrieve first names (up to 2):
            names = [n.split() for n in presenter.split(',')[:2]]
            # if multi, use first names only
            pres_first, pres_last = names[0][0], names[1][0]
        else:
            pres_first, pres_last = presenter.split()
            
        transx = F"{d['idn']}-{pres_first}-{pres_last}"
        
        if d.get('title_kw') is None:
            d['title_kw'] = NA
            
        if not key_isna('title_kw', d):
            tkw = d['title_kw'].replace(' ', '-').lower()
            transx += F"-{tkw}"
        d['transcript_md'] = transx + ".md"
        
        return d

    
    @staticmethod
    def set_audiov_keys(d):
        """
        Set the value of 'audio & video' keys: 
         - audio_track, audio_text (filenames);
         - video_href, video_href_src, video_href_alt, video_href_w;
         Assume validation is done.
        """
        vid = d['yt_video_id']
        
        base = meta_basename(d['year'], d['idn'], vid)
        audio_track = DIR_META.joinpath(base + '.mp4')
        audio_text = DIR_META.joinpath(base + '.txt')                    
        d['audio_track'] = audio_track
        d['audio_text'] = audio_text
        
        if (d['video_href'] == NA or d['video_href'] is None):
           d['video_href'] = default_href(vid)
        
        if (d['video_href_src'] == NA
            or d['video_href_src'] is None):
           d['video_href_src'] = default_href_src(vid)
        
        if (d['video_href_alt'] == NA 
            or d['video_href_alt'] is None):
           d['video_href_alt'] = d['title'].split('(https')[0]
        
        if (d['video_href_w'] == NA
            or d['video_href_w'] is None):
           d['video_href_w'] = DEF_IMG_W
        
        d['video_embed'] = V_EMBED.format(vid)
        
        return d
    
    
    def validate_key(self, k, d):
        if key_isna(k, d):
            msg = F"validate_key :: d['{k}']={NA}"
            raise ValueError(msg)


    def validate_dict(self,d):
        """Check for required fields."""
        for req in REQ_FLDS:
            self.validate_key(req, d)


    @staticmethod
    def titleize(d):
        d['presenter'] = d['presenter'].title()
        d['title'] = d['title'].title()
        d['transcriber'] = d['transcriber'].title()
        return d


    def update_dict(self, new_meta):
        """
        Update event_dict with new data.
        Added: check new values in transcript_md
        """
        current_yr = self.event_dict['year']
        current_id = self.event_dict['idn']
        
        new_meta['idn'] = idn_frmt(new_meta['idn'])
        new_yr = new_meta['year']
        
        ok = True
        if not self.NEW:
            # Cannot change existing yr or idn
            # bc it could create events with same idn
            ok = not ((current_yr != new_yr) 
                      or (current_id != new_meta['idn']))
            if not ok:
                msg = 'TranscriptMeta.update_dict :: cannot change '
                msg += 'existing event year or idn. Request PR for '
                msg += 'implementation.'
                raise ValueError(msg)
            
        if new_meta['status'] == NA:
            new_meta['status'] = TrStatus.TODO.value
        self.validate_dict(new_meta)

        new_meta = self.titleize(new_meta)
        new_meta['title_kw'] = new_meta['title_kw'].replace(' ','-').lower()
        new_meta = self.set_path_keys(new_meta)
        new_meta = self.set_audiov_keys(new_meta)

        if current_yr != new_yr:
            self.year = new_yr
        if current_id != new_meta['idn']:
            self.idn = new_meta['idn']
            
        current_md = self.event_dict['transcript_md']   
        if (current_md != new_meta['transcript_md']
            or current_yr != new_yr):
            mdfile = UTL.get_subfolder(current_yr, REPO_PATH)
            mdfile = mdfile.joinpath(current_md)
            if mdfile.exists():
                self.to_delete = mdfile
            else:
                self.to_delete = None
                
        # Finally, update the insertion index given
        # the lines generated by the data:
        v1 = self.insertion_idx(self.TPL.format(**new_meta))
        new_meta['trans_idx'] = v1 
        
        self.event_dict = new_meta
   

    def set_YT(self):
        if self.YT is not None:
            return
        from manage import EventTranscription as TRX
        
        self.YT = TRX.YTVAudio(self.year,
                               self.idn,
                               self.event_dict['video_url'],
                               self.event_dict['yt_video_id'])

        
    @staticmethod
    def redo_transcript_cleanup(formatted_transcript):
        """
        Return cleaned up event_dict['formatted_transcript'].
        Wrapper to reprocess the current transcript.
        Use case: At least one of the text-processing files
        was amended => repeat text cleanup.
        """
        if not len(formatted_transcript):
            return ''
        from manage import EventTranscription as TRX
        
        comment_line = ''
        line1_idx = formatted_transcript.find('\n')
        if line1_idx > 0 :
            line1 = formatted_transcript[:line1_idx]
            comment_line = line1 if line1.startswith('<!--') else ''
            formatted_transcript = formatted_transcript[line1_idx:]

        txt_len = len(formatted_transcript)
        chunksize = (1024 * 4)
        n_chunks = TRX.math.ceil(txt_len/chunksize)

        uppercase_list = TRX.readcsv(TRX.upper_file).upper.tolist()
        titlecase_list = (TRX.readcsv(TRX.people_file).people.tolist()
                        + TRX.readcsv(TRX.names_file).names.tolist()
                        + TRX.readcsv(TRX.places_file).places.tolist())
        corrections = TRX.get_corrections_dict()

        md_parags = []
        prev_e = 0
        if n_chunks > 1:
            for e in range(chunksize, txt_len, chunksize):
                parag = formatted_transcript[prev_e:e]
                new_parag = TRX.clean_text(parag,
                                           uppercase_list,
                                           titlecase_list,
                                           corrections)
                md_parags.append(new_parag)
                prev_e = e
        # last one (or only one):
        parag = formatted_transcript[prev_e:]
        new_parag = TRX.clean_text(parag,
                                   uppercase_list,
                                   titlecase_list,
                                   corrections)
        md_parags.append(new_parag)
        new_txt = comment_line + "".join(md_parags)
        return new_txt



    def redo_initial_transcript(self):
        """
        Wrapper to instantiate YT class & redo
        initial transcription & save it in data/.
        => All amendments will be lost!
        """
        self.set_YT()

        if self.new_minutes_mark is not None:
            self.YT.minutes_mark = self.new_minutes_mark
        if self.new_wrap_width is not None:
            self.YT.wrap_width = self.new_wrap_width
        self.YT.get_initial_transcript(replace=True)
        return
    
        
    def insert_md_transcript(self, new_trx=None):
        """
        If new_trx is None:: raw_text, if found,
        else new_trx = updated text.
        """
        idn, year = self.idn, self.year
        # Use reduced df:
        idf = self.df.loc[(self.df.N==idn) & (self.df.year==year)]
        md_name = idf.name.values[0]
 
        mdfile = REPO_PATH.joinpath(year, md_name)
        md_txt = UTL.load_file_contents(mdfile)
        
        trans_idx = self.insertion_idx(md_txt)
        text = md_txt[:trans_idx]
        
        if new_trx is None:
            raw = self.event_dict['audio_text']
            if not raw.exists():
                self.redo_initial_transcript()
                
            new_trx = UTL.load_file_contents(raw)
     
        text += '\n' + new_trx
        with open(mdfile, 'w') as fh:
            fh.write(text)
            
        self.event_dict['trans_idx'] = trans_idx
        self.event_dict['formatted_transcript'] = new_trx
        self.event_dict['has_transcript'] = True
        return


    @staticmethod
    def parse_href(href_block):
        """Parse html video link w/soup."""
        href_html = soup(href_block, 'html.parser')
        # meta keys needed: 
        video_hrefs = OrderedDict([('yt_video_id',NA),
                                   ('href',NA),
                                   ('src',NA),
                                   ('alt',NA),
                                   ('width',NA)])
        
        for link in href_html.find_all('a', {'href': True}):
            video_hrefs['href'] = link.get('href')
            _, vid = UTL.split_url(video_hrefs['href'])
            video_hrefs['yt_video_id'] = vid
            
            for c in link.find_all('img'):
                if c.has_attr('src'):
                   video_hrefs['src'] = c.get('src')
                    
                if c.has_attr('alt'):
                    video_hrefs['alt'] = c.get('alt')
                    
                if c.has_attr('width'):
                    video_hrefs['width'] = c.get('width')
 
            return video_hrefs

    
    @staticmethod
    def insertion_idx(text):
        v1 = text.find("## Transcript")
        if v1 != -1:
            v1 += len("## Transcript") + 1
        return v1

    
    def parse_md(self):
        """Parse exsisting transcript.md file and extract 
           data into dict.
        """
        idn, year = self.idn, self.year
        # Use reduced df:
        idf = self.df.loc[(self.df.N==idn) & (self.df.year==year)]
        md_name = idf.name.values[0]
        if md_name == NA:
            msg = "**This event may not have a transcript:** either it was not "
            msg += "recorded or the README table was not updated.<br>"
            # col idx -2: don't display cols of extracted data
            ro = idf[idf.columns[:-2]].style.render()
            msg += F"<div>{ro}</div>"
            return Markdown(msg)
        
        fname = REPO_PATH.joinpath(year, md_name)
        try:
            mdlines = Markdown(filename=fname).data
        except UnicodeDecodeError as e:
            print(fname, '\n', e)
            return
   
        msg = "File is missing '{}' header."
        video_hdr = "## Video"
        v0 = mdlines.find(video_hdr)
        if v0 == -1:
            raise ValueError(msg.format('## Video'))
        v1 = self.insertion_idx(mdlines)
        if v1 != -1:
            txt_len = len(mdlines)
            rem = len(mdlines) + 2 - len(mdlines[v1:])
            has_transcript = rem <= txt_len
        else:
            raise ValueError(msg.format('## Transcript'))

        href_block = mdlines[v0:v1].replace(video_hdr,'')
        href_block = href_block.replace('\n\n','').replace('\n',' ')
        vhrefs = self.parse_href(href_block)
        
        # Init dict:
        event_dict = self.get_event_dict()
        # Fill dict with available so far:
        event_dict['year'] = year
        event_dict['idn'] = idn
        event_dict['transcript_md'] = md_name
        event_dict['status'] = idf.Status.values[0]
        event_dict['notes'] = idf.Notes.values[0]
        event_dict['trans_idx'] = v1
        event_dict['has_transcript'] = has_transcript
        
        # Split text for line iteration:
        md_lines = mdlines.splitlines()
        n_lines = len(md_lines)
    
        # Get 1st line => presenter, title
        pt = md_lines[0][1:].split(':')
        presenter = pt[0].strip()
        event_dict['presenter'] = presenter
        event_dict['title'] = pt[1].strip()
        if ',' in presenter:
            # retrieve first names (up to 2):
            names = [n.split() for n in presenter.split(',')[:2]]
            # first names only if multi
            pres_first, pres_last = names[0][0].lower(), names[1][0].lower()
        else:
            pres_first, pres_last = presenter.lower().split()
            
        title_kw = md_name.partition(pres_last)[2][1:-3].replace('-',' ')
        event_dict['title_kw'] = title_kw
        
        # <h2> headers list from template:
        h2_hdrs = H2_HDRS
        h2_subheaders = list(H2_HDRS_KEYS.keys())
        HDR2 = '## '
        LST = '- '
        trans_idx = None # to retrieve any existing Transcript text
        extra = ''
        add_key = False
        for i, s in enumerate(md_lines):
            if s.startswith(HDR2):
                hdr = s.split(HDR2)[1].strip()
                if hdr == 'Transcript':
                    trans_idx = i
                    # done: processing further would parse
                    # the transcript text following "## Transcript"
                    break
                elif hdr == 'Video':
                    if vhrefs['yt_video_id'] == '':
                        _, vid = UTL.split_url(event_dict['video_url'])
                        event_dict['yt_video_id'] = vid
                    else:
                        event_dict['yt_video_id'] = vhrefs['yt_video_id']
                    vid = event_dict['yt_video_id']
                    event_dict['video_href'] = vhrefs['href']
                    event_dict['video_href_src'] = vhrefs['src']
                    event_dict['video_href_alt'] = vhrefs['alt']
                    event_dict['video_href_w'] = vhrefs['width']
                    base = meta_basename(year, idn, vid)
                    audio_track = DIR_META.joinpath(base + '.mp4')
                    event_dict['audio_track'] = audio_track
                    audio_text = DIR_META.joinpath(base + '.txt')
                    event_dict['audio_text'] = audio_text
                    event_dict['video_embed'] = V_EMBED.format(vid)
        
                add_key = hdr in h2_hdrs
                if not add_key:
                    # treat all 'custom' items as extra links:
                    extra += HDR2 + hdr + '\n'
                continue
            elif s.startswith(LST):
                kval = s.split(LST)[1].split(':', maxsplit=1)
                k = kval[0].strip()
                if add_key and k in h2_subheaders:
                    if k == 'Video':
                        k = 'video_url'
                    else:
                        k = H2_HDRS_KEYS.get(k)
                    event_dict[k] = kval[1].strip()
                else:
                    extra += LST + k + ':  ' + kval[1].strip() + ' \n'
                    
        if extra:
            event_dict['extra_references'] = extra
        else:
            event_dict['extra_references'] = NA

        if has_transcript:
            text = '\n'.join(md_lines[trans_idx+1:])
            event_dict['formatted_transcript'] = text
        
        return event_dict

    
    def get_transcript_text(self):
        txt = self.event_dict.get('formatted_transcript', NA)
        if txt == NA:
            self.insert_md_transcript()
        return self.event_dict['formatted_transcript']


    def update_readme(self):
        """
        Add (update) table row as per meta.
        """
        bkp = DIR_DATA.joinpath('backup', self.readme.name)
        # Backup the file
        shutil.copy(self.readme, bkp)

        # Get the text
        try:
            readme_txt = UTL.get_file_lines(self.readme)
        except FileNotFoundError:
            # try reverting to previously backup copy
            shutil.copy(bkp, self.readme)
            readme_txt = UTL.get_file_lines(self.readme)

        # Get the start/end of the md table data:
        s, e = self.tbl_delims
        off1 = 3  # offset == 1 delim row + 2 header rows
        #off2 = -1 if self.empty_lastrow else 0

        try:
            # Talk Transcript, md link: [title](year/readme)
            talk = F"[{self.event_dict['title']}]({self.event_dict['year']}"
            talk += F"/{self.event_dict['transcript_md']})"

            # fields to match df columns:
            fields = [self.event_dict['idn'],
                      self.event_dict['presenter'],
                      talk, 
                      self.event_dict['transcriber'],
                      self.event_dict['status'],
                      self.event_dict['notes'],
                      self.event_dict['year'],
                      self.event_dict['transcript_md']
                     ]
            data = dict(list(zip(self.df.columns.tolist(), fields)))
            last_idx, N = self.last_of_yr_info()
            newdf = self.df.copy()

            if self.NEW:
                # Update df with new row data:
                # fake idx for insertion:
                new_idx = last_idx + 0.5
                line = pd.DataFrame(data, index=[new_idx])
                newdf = newdf.append(line)
                newdf = newdf.sort_index().reset_index(drop=True)
            else:
                idx = last_idx
                while newdf.loc[idx].N != self.idn:
                    idx -= 1
                    if newdf.loc[idx].N == self.idn:
                        break
                newdf.loc[idx] = data

            # Construct md table rows:
            pipes = '| '
            md_tbl = []
            for _, fields in enumerate(newdf[newdf.columns[:-2]].values):
                md_tbl.append(pipes + pipes.join(fields) + pipes + '\n')

            # Update main text w/table data:
            readme_txt[s+off1:e] = md_tbl

            # Re-create readme:
            with open(self.readme, 'w') as fh:
                fh.writelines(readme_txt)

            # Refresh info:
            self.refresh_tbl_info()
            #F'Table in {self.readme.name} was updated.'
        except:
            # rollback
            shutil.copy(bkp, self.readme)
            print('README not updated on error.')
        return
   

    def save_transcript_md(self, new_trx=None):
        """
        Save new transcript.
        """
        self.validate_key('transcript_md',self.event_dict)
        md_out = REPO_PATH.joinpath(self.year,
                                    self.event_dict['transcript_md'])
        new_md = self.TPL.format(**self.event_dict)
        with open(md_out, 'w') as fh:
            fh.write(new_md)
            
        # Include initial transcript text:
        self.insert_md_transcript(new_trx)
        
        if not self.NEW and self.to_delete is not None:
            # Delete file with diff name after an update:
            self.to_delete.unlink()
            self.to_delete = None
        return


    def get_video_desc(self, include_extra=True):
        """
        Get the starter text for the video description, e.g:
        ```
        Speakers: Hugo Bowne-Anderson and James Bourbeau
        Transcript: https://github.com/data-umbrella/even...
        Meetup Event: https://www.meetup.com/data-umbrella/...
        Video: https://youtu.be/MHAjCcBfT_A
        Jupyter notebook: https://github.com/coiled/data-scienc...
        GitHub repo: https://github.com/coiled/data-scienc...
        ```
        Always included headings: 
          - Speakers, Transcript, Meetup Event, Video;
        If include_extra=True, the contents of the extra_references key
        will follow.
        """
        desc = ""
        if "," in self.event_dict['presenter']:
            desc += f"- Speakers: {self.event_dict['presenter'].replace(',', ' and ')} \n"
        else:
            desc += f"- Speaker: {self.event_dict['presenter']} \n"
        desc += f"- Transcript:  {DU_GH}blob/main/{self.event_dict['transcript_md']} \n"
        desc += f"- Meetup Event:  {self.event_dict['event_url']} \n"
        desc += f"- Video:  {self.event_dict['video_url']} \n"
        
        if include_extra:
            # rem: this entry is a Markdown string
            desc += f"{self.event_dict['extra_references']}"
            
        return desc
        
        
    def __repr__(self):
        #msg = "TranscriptMeta Class rep: only prints metadata."
        if self.event_dict['has_transcript']:
            without_trx = self.event_dict.copy()
            without_trx['formatted_transcript'] = REPR_INFO
            return pformat(without_trx)
        return pformat(self.event_dict)


# .................................................................
dummy_kv_pairs = [('presenter', 'cat Chenal, Reshama Shaikh'),
                  ('title','Automating Audio tanscription.'),
                  ('title_kw','audio demo'),
                  ('video_url','https://youtu.be/MHAjCcBfT_A'),
                  ('extra_references', 
                  """## Other References\n
                  - Binder:  <url>\n- Paper:  <Paper url or citation>  \n
                  - Wiki:  This is an excellent [wiki]  \n
                  (http://en.wikipedia.org/wiki/Main_Page)  \n""")]

def get_dummy_data(year=CURRENT_YEAR,
                   new_kv_pairs=dummy_kv_pairs,
                   include_extra=True):
    """Return a dict."""
    tm = TranscriptMeta(year=year)
    d = tm.event_dict.copy()
    del tm
    
    for i, (k,v) in enumerate(new_kv_pairs):
        # abort on key mismatch:
        if d.get(k) is None:
            raise KeyError(F"get_dummy_data::Invalid key: {k}")
            
        if k == 'video_url':
            _, vid = UTL.split_url(v)
            d['video_url'] = v
            d['yt_video_id'] = vid
        
        elif k == 'extra_references' and include_extra:
            d['extra_references'] = v
        else:
            d[k] = v
 
    return d
