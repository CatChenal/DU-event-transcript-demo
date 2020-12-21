# -*- coding: utf-8 -*-
# Workflow.py

from pathlib import Path
import pandas as pd
import json
from collections import OrderedDict
from enum import Enum
from datetime import datetime as dt
from pprint import pprint as pp, pformat
from IPython.display import display, HTML, Markdown, Audio
import ipywidgets as ipw

from manage import EventMeta as Meta
#from manage.Utils import save_file, load_file_contents #get_project_dirs,

#..........................................................

SHOW_EXTRA_REFS_EXAMPLE = """
<div style="overflow:auto;">
<h3>The `extra_references` value is a Markdown str that should conform to the entries preceding it:</h3>
<div style="overflow:auto;margin-left: 5%;">
<pre style="width:900px;">
# For example, to add several separate sections (## level),
# you would type the lines within the double quotes below:
""
## Other References  
- Binder: url  
- Paper:  url or citation.  
## Wiki of Note  
- Wiki: This is an excellent [wiki on audio transcription](http://en.wikipedia.org/wiki/Main_Page)  
""
</pre>
</div>  

### The rendered output under the templated header items would be:
## Other References\n- Binder: url  \n- Paper:  Paper url or citation. (extra ref 1)  \n
## Wiki of Note\n- Wiki: This is an excellent [wiki on audio transcription](http://en.wikipedia.org/wiki/Main_Page) \n
---
</div>
"""

def show_du_logo_hdr(as_html=True):
    """
    Return formated HTML(<div>) if as_html=True (default),
    else return the html string.
    """
    logo_src = "https://raw.githubusercontent.com/data-umbrella/"
    logo_src += "event-transcripts/master/images/full_logo_transparent.png"
    logo_link = '<a href="https://www.dataumbrella.org" target="_blank"> '
    logo_link += F'<img src="{logo_src}" width="30%" /></a>'
    div = '<div style="text-align:center;padding:5px;width:98%">' 
    if as_html:
        return HTML(div + F'{logo_link}</div>')
    else:
        return div + F'{logo_link}</div>'


def show_local_readme(main_readme):
    """Return Markdown(filename=main_readme)"""
    return Markdown(filename=main_readme)


class EventFunction(Enum):
    ADD = 'Add a Data Umbrella Event'
    MODIFY = 'Modify a Data Umbrella Event'
    EDIT = 'Edit a Data Umbrella Event Transcript'


section_info_add = """
This section pertains to the functions related to the creation of a new event, i.e.:  
<ul>
  <li>the creation of a new row in the main table of the README file, and </li>
  <li>the creation of a starter transcript Markdown file (without the transcript text).</li>
</ul>
These functions are associated with the (functional) user role of  <i>Admin</i>.
"""
section_info_modify = """
This section pertains to the functions related to the modificaton of an event, 
either via modification of the main table in the README file, or  via modification
of the header portion of the transcript Markdown file. A user can:  
<ul>
  <li>Modify an event just added (if that's the case), to e.g.: fix a typo, add a last    
   name, change the Status, add a Note, etc.</li>
  <li>Modify a different event.  </li>
These functions are associated with the (functional) user role of <i>Admin</i>.
"""
section_info_edit = """
This section pertains to the functions related to the editing of an  event's 
transcript (whose download and pre-processing is automated). Only the transcript
text (whether partial or complete) will be replaced in the associated transcript file. 
These functions are associated with the (functional) user role of <i>Editor</i> or 
<i>Reviewer</i>.
<h4>Note</h4>
A recommended task after an editing session, and specifically before pushing  
a PR, is to update the Status (and perhaps the Editor/Reviewer's names) by using     
an Admin function to modify the event.
"""

EventInfo = OrderedDict([('ADD', section_info_add),
                         ('MODIFY', section_info_modify),
                         ('EDIT', section_info_edit)]
                       )
   
    
class DisplaySectionInfo():
    
    def __init__(self, EventFunction):
        self.function = EventFunction
        self.info = EventInfo[EventFunction.name]
        
    def show_section_hdr(self, as_html=True):
        """
        Return formated HTML(<div>) if as_html=True(default),
        else return the html string.
        """
        style = "text-align:center;padding:5px;background:#c2d3ef;"
        style += "color:#ffffff;font-size:3em;width:98%"
        div = F'<div style="{style}">{self.function.value}</div>'
        if as_html:
            return HTML(div)
        else:
            return div
        
    def show_section_info(self, as_html=True):
        """
        Return formated HTML(<div>) if as_html=True(default),
        else return the html string.
        """
        marg = 100 if self.function.name == 'ADD' else 40
        style = F"text-align:justify;margin-left:{marg}px;"
        style += "font-size:2em;width:90%;"
        div = F'<div style="{style}">{self.info}</div>'
        if as_html:
            return HTML(div)
        else:
            return div
    
    def show_header_with_info(self):
        """Return both section header & info,"""
        div = self.show_section_hdr(as_html=False)
        div += self.show_section_info(as_html=False)
        return HTML(div)


# ........................................................................
# Interactive input: new record:

defaultsNA = "(defaults to N.A. if not provided)"
reqd = "(required)"
    
def get_new_input_flds():
    """
    GUI exposed metadata info or fields.
    """
    # tuples: (field, placeholder, info, value)
    new_input_flds = [["year", str(Meta.CURRENT_YEAR), reqd, None],
                      ["presenter",
                       "Presenter's name (first last) - lower case ok!",
                       reqd, None],
                      ["title", "Presentation title - lower case ok!", 
                       reqd, None],
                      ["title_kw", 
                       "Sort word(s) for naming the transcript, e.g. flask demo",
                       reqd, None],
                      ["video_url", "URL of the YouTube video", reqd, None],
                      ["video_href", "URL for the video link", 
                       "(Built by TranscriptMeta.default_href() if not provided)",
                       None],
                      ["video_href_src", "Source url for video link image", 
                       "(defaults to first frame png if not provided)", None],
                      ["video_href_alt", "Video link alt value",
                       "(defaults to title if not provided)", None],
                      ["meetup_url", "URL of the meeting venue", defaultsNA, None],
                      ["slides_url", "URL of the presenter's slides",defaultsNA, 
                       None],
                      ["repo_url", "URL of the presenter's repo",defaultsNA, None],
                      ["notebook_url", "URL of the presenter's notebook",defaultsNA,
                       None],
                      ["transcriber", "Transcriber's name (First Last)",
                       "(defaults to ? if not provided)", None]
                      ]

    new_input_d = OrderedDict([(fld[0],
                                [ipw.Text,
                                 fld[1], fld[2], fld[3]]) for fld in new_input_flds]
                             )
    # Special case:
    plc = "Additional references (beyond those in standard header)"
    info = "(header will only have defaults fields if not provided)"
    new_input_d['extra_references'] = [ipw.Textarea, plc, info, None]
    return new_input_d


def get_demo_input_dict():
    """ Return dict with preset values for demo."""
    new_input_d = get_new_input_flds()
    
    # To preset widget boxes with values:
    demo_list = ['2020', 'cat chenal', 'my presentation title', 'bar foo foo', 
                 "https://www.youtube.com/watch?v=MHAjCcBfT_A", None, None, None,
                 None, None, 'https://github.com/CatChenal', None, None, None ]
    assert len(demo_list) == len(new_input_d.keys())
    
    for i, (k,v) in enumerate(zip(list(new_input_d.keys()), demo_list)):
        dlist = new_input_d[k]
        dlist[-1] = v
        new_input_d[k] = dlist
    return new_input_d


# Layout specs (styles):

txt_layout = ipw.Layout(width='75%')

form_item_layout = ipw.Layout(display='flex',
                              flex_flow='row',
                              justify_content='space-between',
                              margin='0px 10px 0px 5px', 
                              width='95%')

btn_layout = ipw.Layout(display='flex',
                        flex_flow='row',
                        justify_content='center',
                        margin='0px 0px 0px 30px',
                        width='85%')

# Output layout of toggle btn:
togl_out_layout = ipw.Layout(display='flex',
                             flex_flow='column',
                             margin='0px 0px 0px 30px',
                             width='85%')

# Accordion container:
acc_style = ipw.Layout(display='flex',
                       flex_flow='column',
                       border='solid 2px',
                       align_items='stretch',
                       margin='0px 10px 0px 30px',
                       width='85%')


def btn_togl_show_extra_refs_example():
    """ Show a data entry example for the field 'extra_references'. """
    # Callback for toggle:
    def show_example(togl):
        with togl_out:
            if togl['new']:  
                display(Markdown(SHOW_EXTRA_REFS_EXAMPLE))
            else:
                togl_out.clear_output()
    desc = "Show an example of 'Extra References' entry"
    togl = ipw.ToggleButton(description=desc,
                            disabled=False,
                            icon='eye',
                            layout=btn_layout)
    togl_out = ipw.Output(layout=togl_out_layout)
    togl.observe(show_example, 'value')
    return togl, togl_out
    

def wgt_from_flds_dict(k, fld_val):
    """
    Return an ipw Box widget according to param `fld_val`, which is the
    value of key k from the dict returned by `get_new_input_flds()` 
    (or from any other dict with same types).
    :param fld_val (list, len=4): [<wiget type>,<placeholder>,<info>,<value>]
    """
    if len(fld_val) != 4:
        raise ValueError("wgt_from_flds_dict::fld_val: len != 4.")
        
    (wgt, plc, info, val) = fld_val
        
    color = 'red' if info == reqd else 'black'
    box_itm1 = ipw.HTML(F"<p><font color='{color}'>{info}&nbsp; </p>")

    if k != "extra_references":
        w_Box = ipw.Box([box_itm1,
                         wgt(value=val, placeholder=plc, layout=txt_layout)],
                        layout=form_item_layout
                       )
    else:
        # add btn to show input example
        w_togl, w_togl_out = btn_togl_show_extra_refs_example()

        w_Box = ipw.VBox([ipw.Box([box_itm1,
                                   wgt(value=val, layout=txt_layout)],
                                  layout=form_item_layout),
                         w_togl, w_togl_out]
                        )
            
    setattr(w_Box, 'name', k.replace('_', ' ').upper())
    return w_Box
    

def wgt_Acc(children=None):
    """
    Return ipw.Accordion widget with possible children.
    If given, each child is assumed to have a name attribute, which
    is used for titling of the Accordion parent row.
    Children created by wgt_from_flds_dict have a name attribute.
    """
    if children is None:
        return ipw.Accordion(selected_index=None, layout=acc_style)
    
    w_acc = ipw.Accordion(children=children, selected_index=None,
                          layout=acc_style)
    # get names -> titles
    for i, n in enumerate([child.name for child in children]):
        w_acc.set_title(i, n)
        
    return w_acc


def validate_form_entries(entry_form, entry_dict, MetaObj):
    """
    Return a copy of MetaObj.metadata dict populated with user's entries.
    The output dict can then be passed to MetaObj.update_metadata().
    """ 
    # copy main dict: do not update with wrong data:
    data_dict = MetaObj.metadata.copy()
    
    # ref the Accordion child:
    acc = entry_form #.children[0] : previous

    for i, (k, v) in enumerate(entry_dict.items()):
        if k != 'extra_references':
            child = acc.children[i].children[1]
        else:
            # child inside a vbox
            child = acc.children[i].children[0].children[1]

        val = child.get_interact_value() or Meta.NA

        # check 1: NA but required -> end
        if val == Meta.NA and v[-2] == reqd:
            t = acc.get_title(i)
            raise ValueError(F'Cannot save: {t} is required.')

        if k =='video_url':
            dom, vid = Meta.split_url(val)
            data_dict['yt_video_id'] = vid
        else:
            data_dict[k] = val
    
    return data_dict


def input_wgt_group(new_input_d):
    """
    Input parameter is dict output from get_new_input_flds():
    d[key] = (widget type, placeholder text, req_info, value).
    * Second value no longer used but could be tooltip.
    """

    # Layout specs (styles):
    form_item_layout = ipw.Layout(display='flex',
                                  flex_flow='row',
                                  justify_content='space-between',
                                  margin='0px 10px 0px 5px', 
                                  width='95%')

    txt_layout = ipw.Layout(width='75%')

    btn_layout = ipw.Layout(display='flex',
                            flex_flow='row',
                            justify_content='center',
                            margin='0px 0px 0px 30px',
                            width='85%')

    # Output layout of toggle btn:
    togl_out = ipw.Layout(display='flex',
                          flex_flow='column',
                          margin='0px 0px 0px 30px',
                          width='85%')

    # Accordion container:
    acc_style = ipw.Layout(display='flex',
                           flex_flow='column',
                           border='solid 2px',
                           align_items='stretch',
                           margin='0px 10px 0px 30px',
                           width='85%')

    # Callback for toggle:
    def show_example(togl):
        with togl_out:
            if togl['new']:  
                display(Markdown(SHOW_EXTRA_REFS_EXAMPLE))
            else:
                togl_out.clear_output()

    # ..................................................................
    togl = ipw.ToggleButton(description="Show an example of 'Extra References' entry",
                            disabled=False,
                            icon='eye',
                            layout=btn_layout)
    togl_out = ipw.Output(layout=togl_out)
    togl.observe(show_example, 'value')

    # Accordion items:
    form_items = []
    acc_titles = []
    for i, (k, (wgt, plc, lbl, val)) in enumerate(new_input_d.items()):

        acc_titles.append(k.replace('_', ' ').upper())
            
        color = 'red'
        if i > 4:
            color = 'black'

        box_itm1 = ipw.HTML(F"<p><font color='{color}'>{lbl}&nbsp; </p>")
        
        if k != "extra_references":
            form_items.append(ipw.Box([box_itm1, wgt(value=val,
                                                      placeholder=plc,
                                                      layout=txt_layout)],
                                      layout=form_item_layout
                                     )
                              )
        else:
            # add btn to show input example
            form_items.append(ipw.VBox([ipw.Box([box_itm1,
                                                  wgt(value=val,
                                                      layout=txt_layout)],
                                                  layout=form_item_layout),
                                        togl, togl_out]
                                      )
                             ) 
        
    add_acc = ipw.Accordion(children=form_items, selected_index=None,
                            layout=acc_style)
    for i, v in enumerate(acc_titles):
        add_acc.set_title(i, v)
        
    return add_acc
