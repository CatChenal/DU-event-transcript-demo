# -*- coding: utf-8 -*-
# Workflow.py
# Programmer: Cat Chenal
#
# TODO: Split the 'Show Example' toggle for extra references
#       into separate btn at bottom of input group Accordion.
#       -> simpler data retrieval.
#
from pathlib import Path
from collections import OrderedDict
from enum import Enum

from IPython.display import display, HTML, Markdown
import ipywidgets as ipw

from manage import (EventMeta as Meta,
                    EventTranscription as TRX,
                    Utils as UTL)
#..........................................................

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

section_info_add = """
This section pertains to the <strong>Admin</strong> functions related to the creation of a new event, i.e.:  
<ul>
  <li>the creation of a new row in the main table of the README file, and </li>
  <li>the creation of a starter transcript Markdown file, which includes the initial transcript.</li>
</ul>
"""
section_info_modify = """
This section pertains to the <strong>Admin</strong> functions related to the modificaton of an event, 
either via modification of the main table in the README file, or via modification
of the header portion of the transcript Markdown file. A user can:  
<ul>
  <li>Modify an event just added (if that's the case), to e.g.: fix a typo, add a last    
   name, change the Status, add a Note, etc.</li>
"""
section_info_edit = """
This section pertains to the <strong>Editor</strong> functions related to the editing of an event's 
transcript. Only the transcript text will be extracted from and replaced in the associated transcript file. 

<h4>Note</h4>
A recommended task after an editing session, and specifically before pushing  
a PR, is to update the Status (and perhaps the Editor/Reviewer's names) by using     
an Admin function to modify the event.
"""


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
        #marg = 100 if (self.function.name == 'ADD'
        #               or self.function.name == 'INIT') else 40
        #margin-left:{marg}px;
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


def show_du_logo_hdr(as_html=True):
    """
    Return formated HTML(<div>) if as_html=True (default),
    else return the html string.
    """
    logo_src = "https://raw.githubusercontent.com/data-umbrella/"
    logo_src += "event-transcripts/master/images/full_logo_transparent.png"
    logo_link = '<a href="https://www.dataumbrella.org" target="_blank"> '
    logo_link += F'<img src="{logo_src}" width="20%" /></a>'
    div = '<div style="text-align:center;padding:5px;width:98%">' 
    if as_html:
        return HTML(div + F'{logo_link}</div>')
    else:
        return div + F'{logo_link}</div>'

# .......................................................................
# Interactive input: new record:

defaultsNA = "(defaults to N.A. if not provided)"
autogen = "(Auto-generated if not provided)"
reqd = "(Required)"
    
def get_new_input_flds():
    """
    GUI exposed metadata info or fields.
    """
    # items: [field, placeholder, info, value]
    new_input_flds = [["year", str(Meta.CURRENT_YEAR),
                       reqd, None],
                      ["presenter",
                       "Presenter's name (first last) - lower case ok!",
                       reqd, None],
                      ["title", "Presentation title - lower case ok!", 
                       reqd, None],
                      ["title_kw", 
                       "Short, descriptive word(s); part of the transcript file name.",
                       "(E.g., space-separated word(s): flask demo)", None],
                      ["video_url", "URL of the YouTube video",
                       reqd, None],
                      ["video_href", "URL for the video link", 
                       autogen, None],
                      ["video_href_src", "Source url for video link image", 
                       autogen, None],
                      ["video_href_alt", "Video link alt value",
                       autogen, None],
                      ["event_url", "URL of the meeting venue",
                       defaultsNA, None],
                      ["slides_url", "URL of the presenter's slides",
                       defaultsNA, None],
                      ["repo_url", "URL of the presenter's repo",
                       defaultsNA, None],
                      ["notebook_url", "URL of the presenter's notebook",
                       defaultsNA, None],
                      ["transcriber", "Transcriber's name (First Last)",
                       "(Defaults to ? if not provided)", None],
                      ['status', "Status", Meta.TrStatus.TODO.value, None],
                      ['notes', "Notes in README table", "", None]
                      ]

    new_input_d = OrderedDict([(fld[0],
                                [ipw.Text,
                                 fld[1], fld[2], fld[3]]) for fld in new_input_flds]
                             )
    # Last, special case: Textarea
    plc = "Additional references (beyond those in standard header)"
    info = "(header will only have defaults fields if not provided)"
    new_input_d['extra_references'] = [ipw.Textarea, plc, info, None]
    return new_input_d


# ........................................................................
# Layout specs (styles):

lo_txt = ipw.Layout(width='75%')

lo_txtarea = ipw.Layout(display='flex',
                        flex_flow='column',
                        margin='0px 0px 0px 30px',
                        width='90%', height='90px')
    
lo_box_form_item = ipw.Layout(display='flex',
                              flex_flow='row',
                              justify_content='space-between',
                              margin='0px 10px 0px 5px', 
                              width='95%')

lo_togl_btn = ipw.Layout(display='flex',
                        flex_flow='row',
                        justify_content='center',
                        margin='0px 0px 0px 30px',
                        width='90%')

lo_togl_out = ipw.Layout(display='flex',
                             flex_flow='column',
                             margin='0px 0px 0px 30px',
                             width='95%')

# Accordion container:
lo_accord = ipw.Layout(display='flex',
                       flex_flow='column',
                       border='solid 1px',
                       align_items='stretch',
                       margin='0px 10px 0px 30px',
                       width='85%')


def btn_togl_extra_refs_example():
    """ Show a data entry example for the field 'extra_references'."""
    # Callback for toggle:
    def show_example(togl):
        with togl_out:
            if togl['new']:  
                display(Markdown(EXTRA_REFS_EXAMPLE))
            else:
                togl_out.clear_output()
    desc = "Show an example of 'Extra References' entry"
    togl = ipw.ToggleButton(description=desc,
                            icon='eye',
                            layout=lo_togl_btn)
    togl_out = ipw.Output(layout=lo_togl_out)
    togl.observe(show_example, 'value')
    return togl, togl_out
    

def wgtbox_from_kv(k, fld_val):
    """
    Return an ipw Box widget according to param `fld_val`, which is the
    value of k key from the dict returned by `get_new_input_flds()` 
    (or from any other dict with same types).
    :param fld_val (list, len=4): [<wiget type>,<placeholder>,<info>,<value>]
    """
    if len(fld_val) != 4:
        raise ValueError("wgtbox_from_kv::fld_val: len != 4.")
        
    (wgt, plc, info, val) = fld_val
        
    color = 'red' if info == reqd else 'black'
    box_itm1 = ipw.HTML(F"<p><font color='{color}'>{info}&nbsp; </p>")

    if k != "extra_references":
        w_Box = ipw.Box([box_itm1,
                         wgt(value=val, placeholder=plc, layout=lo_txt)],
                        layout=lo_box_form_item
                       )
    else:
        # add btn to show input example
        w_togl, w_togl_out = btn_togl_extra_refs_example()

        w_Box = ipw.VBox([ipw.Box([box_itm1,
                                   wgt(value=val, 
                                       layout=lo_txtarea)],
                                  layout=lo_box_form_item
                                  ),
                          w_togl,
                          w_togl_out]
                        )
            
    setattr(w_Box, 'name', k.replace('_', ' ').upper())
    return w_Box
    

def wgt_Accord(children=None):
    """
    Return ipw.Accordion widget with possible children.
    If given, each child is assumed to have a name attribute, which
    is used for titling of the Accordion parent row.
    Children created by wgtbox_from_kv() have a name attribute.
    """
    if children is None:
        return ipw.Accordion(selected_index=None, layout=lo_accord)
    
    w_acc = ipw.Accordion(children=children, selected_index=None,
                          layout=lo_accord)
    # get names -> titles
    for i, n in enumerate([child.name for child in children]):
        w_acc.set_title(i, n)
        
    return w_acc


def get_entry_accordion(input_dict):
    """Return an Accordion populated with input_dict k,v."""
    children = [wgtbox_from_kv(k, v) for k, v in input_dict.items()]
    return wgt_Accord(children)


def input_wgt_group(new_input_d):
    """
    Input parameter is dict output from get_new_input_flds():
    d[key] = (widget type, placeholder text, req_info, value).
    """
    # TODO: independent 'Show Example' button following accordion
    togl_out = ipw.Output(layout=lo_togl_out)
    @togl_out.capture(clear_output=True)
    def show_example(togl):
        if togl['new']:  
            display(Markdown(EXTRA_REFS_EXAMPLE))

    togl = ipw.ToggleButton(description="Show an example of 'Extra References' entry",
                            disabled=False,
                            icon='eye',
                            layout=lo_togl_btn)
    togl.observe(show_example, 'value')
    # ..................................................................

    # Accordion items:
    form_items = []
    acc_titles = []
    for i, (k, (wgt, plc, lbl, val)) in enumerate(new_input_d.items()):

        acc_titles.append(k.replace('_', ' ').upper())
            
        color = 'red' if lbl == reqd else 'black'
        box_itm1 = ipw.HTML(F"<p><font color='{color}'>{lbl}&nbsp; </p>")
        
        if k != "extra_references":
            form_items.append(ipw.Box([box_itm1, wgt(value=val,
                                                      placeholder=plc,
                                                      layout=lo_txt)],
                                      layout=lo_box_form_item
                                     )
                              )
        else:
            # add btn to show input example
            form_items.append(ipw.VBox([ipw.Box([box_itm1,
                                                  wgt(value=val,
                                                      layout=lo_txt)],
                                                  layout=lo_box_form_item),
                                        togl, togl_out]
                                      )
                             ) 
        
    add_acc = ipw.Accordion(children=form_items, selected_index=None,
                            layout=lo_accord)
    for i, v in enumerate(acc_titles):
        add_acc.set_title(i, v)
        
    return add_acc


def load_entry_dict(tr_obj):
    """
    Return a dict of the entries in the TranscriptMeta object 
    (tr_obj) event_dict that are exposed by the Accordion entry form.
    """
    exposed_d = get_new_input_flds()
    ks = list(tr_obj.event_dict.keys())
    common_ks = set(ks) & set(list(exposed_d.keys()))
    for k in common_ks:
        # load the value, last item:
        exposed_d[k][-1] = tr_obj.event_dict[k]
    return exposed_d


def validate_form_entries(accord, entry_dict, MetaObj):
    """
    Return a copy of MetaObj.event_dict populated with user's entries.
    The output dict can then be passed to MetaObj.update_dict().
    """ 
    # copy main dict: 
    # do not update with wrong data (if event not new):
    data_dict = MetaObj.event_dict.copy()

    for i, (k, v) in enumerate(entry_dict.items()):
        if k != 'extra_references':
            child = accord.children[i].children[1]
        else:
            # child inside a vbox
            child = accord.children[i].children[0].children[1]

        val = child.get_interact_value() or Meta.NA
        # check 1: NA but required -> end
        if val == Meta.NA and v[-2] == reqd:
            t = accord.get_title(i)
            print(t)
            raise ValueError(F'Cannot save: {t} is required.')
            
        if data_dict[k] != val:
            if k in ['presenter', 'transcriber', 'title']:
                val = val.title()
                
            data_dict[k] = val
            if k =='video_url':
                dom, vid = UTL.split_url(val)
                data_dict['yt_video_id'] = vid
        
        if k == 'transcriber':
            if val == Meta.NA or val == '':
                data_dict['transcriber'] = '?'
                
                
    MetaObj.validate_dict(data_dict)
    return data_dict


# ...................................................................
def get_demo_input_dict():
    """ Return dict with preset values for demo."""
    new_input_d = get_new_input_flds()
    
    extra = """- Binder: each listed item should have a 'list header', e.g. '- Binder'  
- Twitter: Use this format: [full name 1](twitter url), etc.     
- Wiki: This is an excellent [wiki on transcription](http://en.wikipedia.org/wiki/Main_Page) """
    # To preset widget boxes with values:
    demo_list = [str(Meta.CURRENT_YEAR),
                 'cat chenal', 'my presentation', 'foo foo', 
                 "https://www.youtube.com/watch?v=MHAjCcBfT_A", None, None, None,
                 None, None, 'https://github.com/CatChenal', None, None,
                 Meta.TrStatus.TODO.value, 'Dummy event', extra ]
    assert len(demo_list) == len(new_input_d.keys())
    
    for i, (k,v) in enumerate(zip(list(new_input_d.keys()), demo_list)):
        # put value from demo_list into the last item of the dict val:
        dlist = new_input_d[k]
        dlist[-1] = v
        new_input_d[k] = dlist
    if new_input_d['transcriber'] is None:
       new_input_d['transcriber'] = '?'
    return new_input_d
