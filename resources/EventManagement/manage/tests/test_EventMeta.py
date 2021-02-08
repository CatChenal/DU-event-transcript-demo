# -*- coding: utf-8 -*-
# test_EventMeta.py
#

# import pytests
from pathlib import Path
import shutil
from functools import partial
from collections import OrderedDict, Counter
import pandas as pd
from datetime import datetime as dt
from enum import Enum
from pprint import pformat
from IPython.display import Markdown

from bs4 import BeautifulSoup as soup
from pytube import YouTube
import defusedxml.ElementTree as ET
from html import unescape
import textwrap
import re

from manage import (EventMeta as Meta,
                    EventTranscription as TRX,
                    Controls as CTR,
                    Utils as UTL)

 
mock_readme = """
<!-- main_tbl_start -->
| #  | Speaker             | Talk Transcript  | Transcriber  | Status | Notes |
|--- |---                  |---               |---           |---     |---    | 
| 01| Hugo Bowne-Anderson| Bayesian Data Science| N.A.| Not recorded| | 
| 02| Bruno Goncalves| Time Series Modeling| N.A.| Not recorded| | 
| 03| Ty Shaikh| [Webscraping Poshmark](2020/03-ty-shaikh-webscraping.md)| Ty Shaikh| Needs reviewer| | 
| 04| Ali Spittel| [Navigating Your Tech Career](2020/04-ali-spittel-career.md)| Janine| Needs reviewer| | 
| 05| Andreas Mueller| [Crash Course in Contributing to Scikit-learn](2020/05-andreas-mueller-contributing.md)| Reshama Shaikh| Complete| | 
| 06| Reshama Shaikh| [Example PR for Scikit-learn](2020/06-reshama-shaikh-sklearn-pr.md)| Reshama Shaikh, Mark| Complete| | 
| 07| Shailvi Wakhlu| [Fixing Bad Data and Using SQL](2020/07-shailvi-wakhlu-fixing-data.md)| Juanita| Complete| | 
| 08| Matt Brems| [Data Science with Missing Data](2020/08-matt-brems-missing-data.md)| Barbara| Needs reviewer| | 
| 09| Sam Bail| [Intro to Terminal](2020/09-sam-bail-terminal.md)| Isaack| Complete| | 
| 10| Emily Robinson| [Build a Career in Data Science](2020/10-emily-robinson-career.md)| Kevin| Complete| | 
| 11| Rebecca Kelly| [Kdb Time Series Database](2020/11-rebecca-kelly-kdb.md)| Coretta| Needs reviewer| Paragraphs are too long| 
| 12| Mridu Bhatnagar| [Build a Bot](2020/12-mridu-bhatnagar-bot.md)| ?| Not yet processed (editor needed)| | 
| 13| Liz DiLuzio| [Creating Nimble Data Processes](2020/13-liz-diluzio-data-process.md)| Lily| Complete| | 
<!-- main_tbl_end -->

"""

  
def dummy_update(meta_obj, meta_d, video_url, meetup_url,
                 title='Automating Audio Transcription.',
                 titlekw='audio foo',
                 presenter='Cat Chenal, Reshama Shaikh',
                 include_extra=True):

    meta_d['year'] = CURRENT_YEAR
    meta_d['video_url'] = video_url
    vsite, vid = UTL.split_url(video_url)
    
    meta_d['yt_video_id'] = vid
    meta_d['video_href'] = HREF_DOM + vid
    meta_d['video_href_src'] = YT_IMG_URL0 + vid + YT_IMG_URL1
    if meta_d['video_href_alt'] == NA:
        meta_d['video_href_alt'] = title
    meta_d['repo_url'] = 'https://github.com/CatChenal'       
    meta_d['event_url'] = meetup_url
    meta_d['title'] = title
    meta_d['title_kw'] = titlekw
    meta_d['presenter'] = presenter
    meta_d['notes'] = 'Dummy entry for demo.'
    if include_extra:
        extra = "## Other References\n"
        extra += "- Binder:  <url>\n- Paper:  <Paper url or citation>  \n"
        extra += F"- Wiki:  This is an excellent [wiki on {meta_d['title_kw']}]"
        extra += "(http://en.wikipedia.org/wiki/Main_Page)  \n"""
        meta_d['extra_references'] = extra

    return meta_d


def test_get_tbl_delims():
    TBL0 = '<!-- main_tbl_start -->'
    TBL1 = '<!-- main_tbl_end -->'
    
    mock_md_lines = [lin+'\n' for lin in mock_readme.split('\n')]
    mock_md_lines

    i, j = Meta.get_tbl_delims(mock_md_lines)
    # new one w/o start
    mock1 = mock_readme[i:]
    # new one w/o end:
    mock2 = mock_readme[:j]
    
    msg = 'README table.{} delimiter missing:\n{}'
    try:
        delims0 = Meta.get_tbl_delims(mock1)
    except Exception as e:
        assert isinstance(e, ValueError) == True
        assert e.message == msg.format('start', TBL0)
    try:
        delims1 = Meta.get_tbl_delims(mock1)
    except Exception as e:
        assert isinstance(e, ValueError) == True
        assert e.message == msg.format('end', TBL1)
                         

def test_last_of_yr_info():
    pass


def test_df_from_readme_tbl():
    # main_readme=Meta.MAIN_README
    # test num cols
    # test col names
    pass


def test_add_event():
    tm = TRX.TranscriptMeta()

    # Extract dict for update:
    meta_dict = tm.event_dict

    # dummy data:
    DU_video = 'https://youtu.be/PU1WyDPGePI' #'https://youtu.be/0L1uM_18TTA'
    updated_meta = dummy_update(tm, meta_dict,
                                DU_video,
                                title='Automating Audio Transcription.')

    tm.update_metadata(updated_meta)
    # Updated dict:
    tm.event_dict
    tm.save_meta()
    tm.save_transcript_md()