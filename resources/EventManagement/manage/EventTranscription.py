# -*- coding: utf-8 -*-
# EventTranscription.py
# Programmer: Cat Chenal
#
from pathlib import Path
from functools import partial
from collections import OrderedDict

from IPython.display import Markdown
import pandas as pd

from pytube import YouTube
import defusedxml.ElementTree as ET
from html import unescape
import textwrap
import re
import time
import math

from manage import (EventMeta as Meta,
                    Utils as UTL)

# ...................................................
readcsv = partial(pd.read_csv, index_col=0)


# Main lists for titlecasing (& file editing):
people_file = Meta.DIR_DATA.joinpath('title_people.csv')
names_file = Meta.DIR_DATA.joinpath('title_names.csv')
places_file = Meta.DIR_DATA.joinpath('title_places.csv')
# List of terms (e.g. acronyms) for uppercasing:
upper_file = Meta.DIR_DATA.joinpath('upper_terms.csv')

# Replacement pairs: (from, to); for special str 
# & those mangled by Google's autocaptioning:
corrections_file = Meta.DIR_DATA.joinpath('corrections.csv')
def get_corrections_dict():
    return readcsv(corrections_file).set_index('k').to_dict()['v']


def get_TextWrapper(wrap_width=120):
    TW = textwrap.TextWrapper(width=wrap_width,
                              expand_tabs=False,
                              replace_whitespace=True)
    return TW
    
    
def clean_text(text,
               uppercase_list,
               titlecase_list,
               corrections,
               TW=None):
    """
    Clean text using regex and wrap using a 
    pre-defined textwrap.TextWrapper instance.
    :param: text (str): paragraph
    :param: uppercase_list, titlecase_list (list):
           terms for upper or title casing, respectively.
    :param: corrections (dict): all other substitutions.
    :param: TW (textwrap.TextWrapper): None (default) or instance.
    """
    def time_repl(mo):
        """Fix spoken time; mo=match obj"""
        fmt = "{}{}:{}{} "
        o = fmt.format(mo.group(1),mo.group(2),mo.group(3),
                       mo.group(4).upper().replace('.','')) 
        return o
    def perso_i(mo):
        """Truecasing i -> I"""
        return mo.group(0).upper()
    def upper_repl(mo):
        """Allows for plural acronyms, e.g. APIs"""
        if mo.group(2) is None:
            return mo.group(1).upper()
        return mo.group(1).upper() + mo.group(2)
    def titlecase_repl(mo):
        return mo.group(0).title()

    re_calendar = r"(((?:(jan|febr)uary)?|(march)?|(april)?|(june)?"
    # capitalize 'may' if not obvious auxiliary
    re_calendar += "|(july)?|(august)?|(?<![(i|you|we|they)] )(may )?"
    re_calendar += "|(?:(sept|nov|dec)ember)?|(october)?)"
    re_calendar += "|(?:(sun|mon|tues|wednes|thurs|fri|satur)day)?)"
    RE_CAL = re.compile(re_calendar)
    RE_UTTERANCES = re.compile(r"\bu[mh]\b")
    RE_SPACES = re.compile(r"( {2,}\b)")
    RE_TIME = re.compile(r"(\s*)(\d{1,2}) (\d{1,2}) ([pa].m)(.?)")
    RE_I = re.compile(r"(\bi'{0,1}\b)")

    text = RE_UTTERANCES.sub("", text)
    text = RE_SPACES.sub(" ", text)
    text = RE_I.sub(perso_i, text)
    text = RE_CAL.sub(titlecase_repl, text)
    text = RE_TIME.sub(time_repl, text)

    # Corrections work on lowercase
    for k, v in corrections.items():
        text = text.replace(k, v)

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
    
    if TW is not None:
        # Wrapped for Markdown output:
        md_lines = []
        new_txt = TW.wrap(text)
        for line in new_txt:
            md_lines.append(line + "  \n")
        wrapped = "".join(md_lines)
        return wrapped
    
    return text


def float_to_stime(duration):
    """
    Convert decimal durations into proper srt format.
    Return a tuple:
      (formatted time duration, whole minute)
    Example:
      float_to_strtime(3.89) -> ('00:00:03,890', 0)
    update: srv3 format: time in milliseconds.
    """    
    fraction, whole = math.modf(duration/1000)
    tm_whole = time.gmtime(whole)
    time_fmt = time.strftime("%H:%M:%S", tm_whole)
    time_fmt += F",{fraction:.3f}".replace("0.", "")
    return time_fmt, tm_whole.tm_min
        
        
class YTVAudio:
    """
    Class for downloading YouTube Video (YTV) audio and 
    auto-generated captions, pre-processing the transcript text.
    """
    
    def __init__(self, year, idn, video_url, vid, replace_xml=False):
        """
        :param: replace_audio_file (bool): redo download of audio.
        """
        self.minutes_mark = 4
        self.wrap_width = 120
        self.video_url = video_url
        self.video = self.set_YT_video()
        self.meta_path = Meta.DIR_META
        self.basename = Meta.meta_basename(year, idn, vid)
        self.audio_filepath = self.meta_path.joinpath(self.basename + '.mp4')
        self.captions_xml = self.get_xml_captions(replace=replace_xml)

    
    def set_YT_video(self):
        v = None
        try:
            v = YouTube(self.video_url)
        except Exception as e:
            raise ValueError(F"YTAudio.video:: set_YT_video failed.\n {e}")
        return v


    def download_audio(self, replace=False):
        if self.video is None:
            return
        audio = self.video.streams.get_audio_only()
        fname = self.basename + '.mp4'
   
        if replace or not self.audio_filepath.exists():
            # pytube has changed: if
            # filename==fname: saved as <idn>_<vid>mp4.mp4
            audio.download(output_path=self.meta_path,
                           filename=self.basename)
            #print(F"Audio saved as:\n{self.audio_filepath}")
            return
    
    
    def get_xml_captions(self, replace=False):
        """
        Save auto-generated video captions to xml.
        :param: replace(bool): replace (download again) if 
                              file exists.
        """
        if self.video is None:
            return
        fname = self.basename + '.xml'
        xml_fname = self.meta_path.joinpath(fname)
        if replace or not xml_fname.exists():
            en = 'a.en' # pytube v='10.0.0'   
            captions_xml = self.video.captions[en].xml_captions
            UTL.save_file(xml_fname, captions_xml, replace=replace)
            #print(F"XML saved as:\n{xml_fname}")

        return UTL.load_file_contents(xml_fname)

        
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
        
        TW = get_TextWrapper(wrap_width=wrap_to)
        
        root = ET.fromstring(xml_captions, forbid_dtd=True)
        #for i, child in enumerate(root):
        for i, child in enumerate(list(root.findall('body/p'))):
            # need to keep track of min interval to add a paragraph
            start, tm_min = float_to_stime(float(child.attrib['t']))
            
            # Not all xml files are lowercase, but clean_text()
            # works with lowercase
            #txt = unescape(child.text).strip().lower()
            
            #txt = ''.join(child.itertext()).strip().lower()
            txt = unescape(''.join(child.itertext())).strip().lower()
            
            if i == 0:
                txt = txt[0].upper() + txt[1:]
            parag += txt + " "

            if tm_min > 0:
                if (tm_min % minutes_mark == 0) and (tm_min != prev_tm):
                    msg = F"{minutes_mark:d} minutes mark -> new paragraph \n"
                    parag = clean_text(parag,
                                       uppercase_list,
                                       titlecase_list,
                                       corrections,
                                       TW)
                    parag += " \n"
                    lines.append(parag)
                    lines.append(frmt_tm.format(start, msg))
                    parag = ""
            prev_tm = tm_min
            
        # last chunk:
        if len(parag):
            parag = clean_text(parag,
                               uppercase_list,
                               titlecase_list,
                               corrections,
                               TW)
            lines.append(parag + " \n")
        return "".join(lines)


    @staticmethod
    def get_first_line(w):
        comment0 = "<!-- Editing Guide: The pipe (|) position "
        comment0 += F"in this comment is {w}: "
        cmt_line = F"{comment0:<{w}}| -->\n"
        return cmt_line + "### Introduction\n\n"
    
        
    def get_initial_transcript(self, replace=False):
        """ 
        Wrapper for xml_caption_to_str.
        """
        minutes_mark = self.minutes_mark
        wrap_width = self.wrap_width
        
        fname = self.basename + '.txt'
        trx_fname = self.meta_path.joinpath(fname)

        if replace or not trx_fname.exists():
            if self.captions_xml is None:
                return
            
            uppercase_list = readcsv(upper_file).upper.tolist()
            titlecase_list = (readcsv(people_file).people.tolist()
                                   + readcsv(names_file).names.tolist()
                                   + readcsv(places_file).places.tolist())
            corrections = get_corrections_dict()

            raw_transcript = self.xml_caption_to_text(self.captions_xml,
                                                      uppercase_list,
                                                      titlecase_list,
                                                      corrections,
                                                      minutes_mark,
                                                      wrap_width)
            text = self.get_first_line(wrap_width) + raw_transcript
            UTL.save_file(trx_fname, text)
        return


# text processing files update ...............................
def check_list(list_to_search, new_terms, verbose=True):
    def search_list(list_to_search, search_str):
        idx = -1
        try:
            idx = list_to_search.index(search_str.lower())
        except ValueError:
            pass
        return idx

    if not isinstance(list_to_search, list):
        raise ValueError("list_to_search is not a list.")
    if not isinstance(new_terms, list):
        new_terms = list(new_terms)
        
    tot = 0
    reduced = []
    for i, t in enumerate(new_terms):
        t = t.lower()
        i = search_list(list_to_search, t)
        if i == -1:
            reduced.append(t)
            tot += 1
            found = '<not found>'
        else:
            found = '<found>'
        if verbose:
            print('\t', t, found)

    if tot == 0:
        msg = '#### All found. Nothing to add.'
    else:
        msg = "#### Next, __run__: `TRX.update_conversion_file` with: "
        msg += " `which`=<one of ['names','people','places','upper']>, "
        if tot == len(new_terms):
            msg += " `user_list`=\<list before check\>)"
        else:
            msg += " `user_list`=\<reduced list\>)"
    
    if verbose:
        display(Markdown(msg))
        return tot, reduced
    else:
        return tot, reduced, msg


def check_corrections(corrections_dict, new_tuples, verbose=True):
    """
    Return total not found, reduced list [, msg if not verbose].
    """
    if not isinstance(corrections_dict, dict):
        raise ValueError("corrections_dict is not a dict.")
    if not isinstance(new_tuples, list):
        raise ValueError("new_tuples is not a list.")
    if not isinstance(new_tuples[0], tuple):
        raise ValueError("new_tuples is not a list of tuples.")    
    tot = 0
    reduced = []
    for i, t in enumerate(new_tuples):
        t = (t[0].lower(), t[1])
        o = corrections_dict.get(t[0], -1)
        if o == -1:
            found = '<not found>'
            reduced.append(t)
            tot += 1
        else:
            if o != t[1]:
                found = F'<different val>: existing: {o}'
            else:
                found = o
        if verbose:
            print(i, t, found)

    if tot == len(new_tuples):
        msg = '#### Next, __run__: `: TRX.add_corrections(<list before check>)`'
    elif tot == 0:
        msg = '#### All found. Nothing to add.'
    else:
        msg = '#### Next, __run__: `: TRX.add_corrections(<reduced list>)`'
    if verbose:
        display(Markdown(msg))
        return tot, reduced
    else:
        return tot, reduced, msg


def add_corrections(new_tuples, return_dict=True):
    """
    Update csv file & return updated dict.
    """
    if not isinstance(new_tuples, list):
        raise ValueError("new_tuples is not a list.")
    if not isinstance(new_tuples[0], tuple):
        raise ValueError("new_tuples is not a list of tuples.")
    if new_tuples:
        df = readcsv(corrections_file)
        imax = df.index.argmax() + 1
        for i, t in enumerate(new_tuples):
            df.loc[imax+i] = [t[0], t[1]]
        df.to_csv(corrections_file)
    if return_dict:
        return get_corrections_dict()
    else:
        return

def update_corrections(new_corrections):
    """
    Wrapper for check_corrections & add_corrections with
    verbose=False.
    :param: new_corrections: list of tuples.
    """
    corrections = get_corrections_dict()
    tot, reduced_list, msg = check_corrections(corrections,
                                               new_corrections,
                                               verbose=False)
    if tot:
        if 'reduced' in msg:
            if reduced_list:
                add_corrections(reduced_list, return_dict=False)
        else:
            add_corrections(new_corrections, return_dict=False)
    return
                    
                    
substitutions = dict([('people', people_file),
                      ('names',names_file),
                      ('places', places_file),
                      ('upper', upper_file),
                      ('corrections', corrections_file)])


def update_conversion_file(which=None, user_list=None, 
                           op='add'):
    """
    Update one of the 4 conversions csv files:
    For titlecasing: title_names.csv,
                     title_people.csv,
                     title_places.csv;
    For uppercasing: upper_terms.csv
    :param: which (str): one of ['names','people','places','upper']
    :param: user_list (list): list of terms to add or remove.
    :param: op (str): either 'add' or 'remove'.
    Call example:
    update_conversion_file(which='upper',user_list=['nlp','ner'])
    """
    if which is None or user_list is None:
        msg = "EventTranscription.update_conversion_file:: "
        msg += "`which` and `user_list` cannot be None."
        raise ValueError(msg)
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


def update_conversions(which_file, new_terms):
    """
    Wrapper for check_list & update_conversion_file
    with verbose=False.
    :param: which_file: one of ['people','names','places','upper']
    :param: new_terms: list of strings.
    """
    which = which_file.lower()
    fname = substitutions[which]
    current_list = readcsv(fname)[which].tolist()

    tot, reduced_list, msg = check_list(current_list,
                                        new_terms,
                                        verbose=False)
    if tot:
        if 'reduced' in msg:
            if reduced_list:
                update_conversion_file(which, reduced_list)
        else:
            update_conversion_file(which, new_terms)
    return

