# -*- coding: utf-8 -*-
# EventTranscription.py
#
from pathlib import Path
import shutil
from pprint import pprint as pp, pformat
from IPython.display import Markdown #, Audio
import pandas as pd
from functools import partial
from collections import OrderedDict
from warnings import warn
from pytube import YouTube
import defusedxml.ElementTree as ET
from html import unescape
import textwrap
import re
import time
import math

from manage import EventMeta as Meta
from manage.Utils import save_file, load_file_contents
# ...................................................

# Main lists for titlecasing:
people_file = Meta.DIR_DATA.joinpath('title_people.csv')
names_file = Meta.DIR_DATA.joinpath('title_names.csv')
places_file = Meta.DIR_DATA.joinpath('title_places.csv')
# List of terms (e.g. acronyms) for uppercasing:
upper_file = Meta.DIR_DATA.joinpath('upper_terms.csv')
substitutions = dict([('names',names_file),
                      ('people', people_file),
                      ('places', places_file),
                      ('upper', upper_file)])

# Replacement dict for special str & those mangled by 
# Google's autocaptioning:
correct_json = Meta.DIR_DATA.joinpath('corrections.json')


readcsv = partial(pd.read_csv, index_col=0)


def search_list(lst_to_search, search_str):
    idx = 'Not found'
    if not isinstance(lst_to_search, list):
        raise ValueError("lst_to_search is not a list.")
    try:
        idx = lst_to_search.index(search_str.lower())
    except ValueError:
        pass
    return idx


def update_substitution_file(which=None, user_list=None, 
                             op='add'):
    """
    Update one of the 4 substitutions csv files:
    For titlecasing: title_names.csv,
                     title_people.csv,
                     title_places.csv;
    For uppercasing: upper_terms.csv
    :param which (str): one of ['names','people','places','upper']
    :param user_list (list): list of terms to add or remove.
    :param op (str): either 'add' or 'remove'.
    Call example:
    update_substitution_file(which='upper',user_list=['nlp','ner'])
    """
    if which is None or user_list is None:
        msg = "EventTranscription.update_substitution_file:: "
        msg += "No parameters."
        warn(msg)
        return

    kind = ['names', 'people', 'places', 'upper']
    ops = ['add', 'remove']
    
    which = which.lower()
    if which not in kind:
        raise ValueError(F"`which` not in {kind}.")
    op = op.lower()
    if op not in ops:
        raise ValueError(F"`op` not in {ops}.")
        
    fname = substitutions[which]
    val_set = set(readcsv(fname)[which].values)
    init_len = len(val_set)
    
    if not isinstance(user_list, list):
        user_list = list(user_list)
        
    fn = val_set.add if op == 'add' else val_set.remove
    
    for v in user_list:
        try:
            fn(v.strip().lower())
        except KeyError:
            pass    

    if len(val_set) != init_len:
        df = pd.DataFrame({which: list(val_set)})
        df.to_csv(fname)

    return


def clean_text(text, TW,
               uppercase_list,
               titlecase_list,
               corrections):
    """
    Clean text using regex and wrap using a 
    pre-defined textwrap.TextWrapper instance.
    :param text (str): paragraph
    :param TW (textwrap.TextWrapper): instance
    :param uppercase_list, titlecase_list (list):
           terms for upper or title casing, respectively.
    :param corrections (dict): all other substitutions.
    """
    # fix spoken time, mo=match obj:
    def time_repl(mo):
        fmt = "{}{}:{}{} "
        o = fmt.format(mo.group(1),mo.group(2),mo.group(3),
                       mo.group(4).upper().replace('.','')) 
        return o
    # truecasing i -> I:
    def perso_i(mo):
        return mo.group(0).upper()
    def upper_repl(mo):
        # allows for plural acronyms, e.g. APIs
        if mo.group(2) is None:
            return mo.group(1).upper()
        return mo.group(1).upper() + mo.group(2)
    # months & days, names, people
    def titlecase_repl(mo):
        return mo.group(0).title()

    re_calendar = r"(((?:(jan|febr)uary)?|(march)?|(april)?|(june)?"
    # capitalize 'may' if not obvious auxiliary
    re_calendar += "|(july)?|(august)?|(?<![(i|you|we|they)] )(may )?"
    re_calendar += "|(?:(sept|nov|dec)ember)?|(october)?)"
    re_calendar += "|(?:(sun|mon|tues|wednes|thurs|fri|satur)day)?)"
    RE_CAL = re.compile(re_calendar)
    RE_UTTER = re.compile(r"\bu[mh]\b")
    RE_SPACES = re.compile(r" {2,}")
    RE_TIME = re.compile(r"(\s*)(\d{1,2}) (\d{1,2}) ([pa].m)(.?)")
    RE_I = re.compile(r"(\bi'{0,1}\b)")
    
    text = RE_UTTER.sub(" ", text)
    text = RE_SPACES.sub(" ", text)
    text = RE_I.sub(perso_i, text)
    text = RE_CAL.sub(titlecase_repl, text)
    text = RE_TIME.sub(time_repl, text)

    for i, lst in enumerate([uppercase_list, titlecase_list]):
        if i:
            repl_fn = titlecase_repl
            case_re = r"(\b{}\b)"
        else:
            repl_fn = upper_repl
            case_re = r"(\b{})(?!\=)(?:(\b|s))"

        for word in lst:
            RE = re.compile(case_re.format(word))
            text = RE.sub(repl_fn, text)
        
    # Wrap for Markdown output:
    md_lines = []
    new_txt = TW.wrap(text)
    for line in new_txt:
        md_lines.append(line + "  \n")
    wrapped = "".join(md_lines)

    # replacements:
    for k, v in corrections.items():
        wrapped = wrapped.replace(k, v)

    return wrapped


class YTAudio:
    """
    Class for downloading audio and auto-denerated captions,
    pre-processing the transcript text.
    """
    
    def __init__(self, TMobj, replace_audio_file=False):
        """
        TMobj is a TranscriptMeta instance.
        :param replace_audio_file (bool): redo download of audio.
        """
        self.TM = TMobj
        self.meta = TMobj.metadata
        self.minutes_mark = 4
        self.wrap_width = 120
        self.redo_audio = replace_audio_file
        self.video = self.set_YT_video()
        self.captions_xml = self.get_xml_captions()

    
    def set_YT_video(self):
        v = None
        try:
            v = YouTube(self.meta['video_url'])
        except Exception as e:
            msg = "YTAudio.YT_video:: "
            if  self.meta.get('video_url', Meta.NA) == Meta.NA:
                raise KeyError(msg + "metadata['video_url'] is not set.")
            else:
                warn(msg + F"YTAudio.YT_video:: failed.\n {e}")
        return v


    def download_audio(self, replace):
        audio = self.video.streams.get_audio_only()
        audio_path = Meta.DIR_DATA.joinpath(self.meta['audio_track'])
        if not audio_path.exists() or replace:
            audio.download(output_path=Meta.DIR_DATA,
                           filename=self.meta['audio_track'])
            print(F"Audio downloaded in:\n{audio_path}")
        return
    
    
    def get_xml_captions(self, replace=False):
        """
        Save auto-generated video captions to xml.
        :param replace(bool): replace (download again) if 
                              file exists.
        """
        xml_fname = self.meta['audio_text'][:-3] + "xml"
        fpath = Meta.DIR_DATA.joinpath(xml_fname)

        if replace or not fpath.exists():
            if self.video is None:
                msg = "YTAudio.get_xml_captions:: Video "
                msg += "not set.\nRun set_YT_video() first."
                warn(msg)
                return None

            en = 'a.en' # pytube v='10.0.0'   
            captions_xml = self.video.captions[en].xml_captions
            save_file(fpath, captions_xml, replace=replace)

        return load_file_contents(fpath)


    @staticmethod
    def float_to_stime(d):
        """
        Convert decimal durations into proper srt format.
        Return a tuple:
          (formatted time duration, whole minute)
        Example:
          float_to_strtime(3.89)
          ('00:00:03,890', 0)
        """    
        fraction, whole = math.modf(d)
        tm_whole = time.gmtime(whole)
        time_fmt = time.strftime("%H:%M:%S,", tm_whole)
        ms = F"{fraction:.3f}".replace("0.", "")
        return time_fmt + ms, tm_whole.tm_min
        
        
    def xml_caption_to_text(self, xml_captions, 
                            uppercase_list, titlecase_list,
                            corrections, 
                            minutes_mark,
                            wrap_to):
        """
        Modified pytube.Caption function for custom output.
        """    
        frmt_tm = "\n#### {}::\t\t{} \n"
        lines = []
        prev_tm = 0
        parag = ''
        
        TW = textwrap.TextWrapper(width=wrap_to,
                                  expand_tabs=False,
                                  replace_whitespace=True)
        
        root = ET.fromstring(xml_captions, forbid_dtd=True)
        for i, child in enumerate(root):
            # need to keep track of min interval to add a paragraph
            start, tm_min = self.float_to_stime(float(child.attrib['start']))
            
            txt = unescape(child.text).strip().lower()
            if i == 0:
                txt = txt[0].upper() + txt[1:]
            parag += txt + " "

            if tm_min > 0:
                if (tm_min % minutes_mark == 0) and (tm_min != prev_tm):
                    msg = F"{minutes_mark:d} minutes mark -> new paragraph \n"
                    parag = clean_text(parag, TW,
                                       uppercase_list, titlecase_list,
                                       corrections)
                    parag += " \n"
                    lines.append(parag)
                    lines.append(frmt_tm.format(start, msg))
                    parag = ""
            prev_tm = tm_min
            
        # last chunk:
        if len(parag):
            parag = clean_text(parag, TW,
                               uppercase_list, titlecase_list,
                               corrections)
            lines.append(parag + " \n")
        return "".join(lines)


    @staticmethod
    def get_first_line(w):
        comment0 = "<!-- Editing Guide: The pipe (|) position "
        comment0 += F"in this comment is {w}: "
        cmt_line = F"{comment0:<{w}}| -->\n\n"
        # host key removed -> staticmethod
        #first_line = F"### Introduction by {self.meta['host']} \n"
        return "### Introduction\n" + cmt_line
    
        
    def get_initial_transcript(self):
        """ 
        Wrapper for xml_caption_to_str.
        Initial call: replace_dict=None, so default_replacements
        dict is generated.
        :param minutes_mark (int,6): for time chuncking of text.
        :param wrap_width (int,90): wrapping width.
        """
        minutes_mark = self.minutes_mark
        wrap_width = self.wrap_width
         # English captions:
        if self.captions_xml is None:
            # In init, replace=False -> change & redo.
            self.captions_xml = self.get_xml_captions(replace=True)
            
        # moved from __init__ because changes to files would
        # require a new instantiation 
        uppercase_list = readcsv(upper_file).upper.tolist()
        titlecase_list = (readcsv(people_file).people.tolist()
                               + readcsv(names_file).names.tolist()
                               + readcsv(places_file).places.tolist())
        corrections = load_file_contents(correct_json)
        
        raw_transcript = self.xml_caption_to_text(self.captions_xml,
                                                  uppercase_list,
                                                  titlecase_list,
                                                  corrections,
                                                  minutes_mark,
                                                  wrap_width)
        
        return self.get_first_line(wrap_width) + raw_transcript
    
