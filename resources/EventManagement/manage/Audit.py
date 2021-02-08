# -*- coding: utf-8 -*-_json
# Audit.py
# Programmer: Cat Chenal
#
from pprint import pformat #, pprint as pp

from manage import (EventMeta as Meta,
                    EventTranscription as TRX,
                    Controls as CTR,
                    Utils as UTL)


def audit_xml_captions(xml_captions, minutes_mark):
    """
    Get the 1st paragraph from xml lines (chunked with minutes_mark);
    Return True if it is lowercase, else False.
    """
    import defusedxml.ElementTree as ET
    from html import unescape

    prev_tm = 0
    parag = ''
    root = ET.fromstring(xml_captions, forbid_dtd=True)
    for i, child in enumerate(root):
        start, tm_min = TRX.float_to_stime(float(child.attrib['start']))

        txt = unescape(child.text).strip()
        parag += txt + " "

        if tm_min > 0:
            if (tm_min % minutes_mark == 0) and (tm_min != prev_tm):
                xml_islower = parag.islower()
                break
        prev_tm = tm_min
    return xml_islower, parag


def get_all_transcripts(meta_only=False,
                        audit_captions=False,
                        replace_xml=False,
                        replace_trx=False):
    """
    Audit on all events.
    :param: meta_only:  for testing md file parsing (done by __init__)
    :param: replace_xml: 
    :param: replace_trx:
    """
    df, tbl_delims = Meta.df_from_readme_tbl()
    df = df[2:] # exclude not recorded
    
    if audit_captions:
        mins = 1
        print(F'Captions case check (on 1st P with minutes_mark= {mins}):')
        
    for idx, yr in df[['N','year']].values:
        tr = Meta.TranscriptMeta(idx, yr)
                  
        if meta_only:
            continue
            
        tr.set_YT()  # xml captions saved in init
        if audit_captions:
            tr.YT.minutes_mark = mins
            xml_islower, parag = audit_xml_captions(tr.YT.captions_xml, mins)
            print(F'{idx}, {yr}:: Lower= {xml_islower}\n{parag}\n)')
            
        if replace_xml:
            print(idx, yr)
            tr.YT.captions_xml = tr.YT.get_xml_captions(True)
            
        if replace_trx:
            print(idx, yr)
            tr.YT.get_initial_transcript(True)

    what = F"[meta_only={meta_only}, audit_captions={audit_captions}, "
    what += F"replace_xml={replace_xml}, replace_trx={replace_trx}]"
    print(F'get_all_transcripts {what}:: done!')
    return