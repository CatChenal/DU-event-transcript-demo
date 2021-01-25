# -*- coding: utf-8 -*-
# Controls.py
# Programmer: Cat Chenal
#
from pathlib import Path
from IPython.display import Markdown
import ipywidgets as ipw
from collections import OrderedDict

from manage import EventMeta as Meta, Utils as UTL


# ..............................................................................
defaultsNA = "(defaults to N.A. if not provided)"
autogen = "(Auto-generated if not provided)"
reqd = "(Required)"

def get_new_input_flds():
    """
    GUI exposed metadata info or fields.
    exposed_flds = ['year','presenter', 'title', 'title_kw',
                    'video_url','video_href', 'video_href_src',
                    'video_href_alt','event_url', 'slides_url',
                    'repo_url', 'notebook_url','transcriber',
                    'status', 'notes', 'extra_references']
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
                      ['notes', "Notes in README table", "", None],
                      ['extra_references',
                       'Additional references (beyond those in standard header)',
                       '(header will only have defaults fields if not provided)',
                       None]
                      ]

    new_input_d = OrderedDict([(fld[0],
                                [ipw.Text,
                                 fld[1], fld[2], fld[3]]) 
                                 for fld in new_input_flds]
                             )
    # Last, special case: reset wgt to Textarea
    new_input_d['extra_references'][0] = ipw.Textarea
    return new_input_d


# ..............................................................................
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
                 Meta.TrStatus.TODO.value, 'Dummy event', extra]
    assert len(demo_list) == len(new_input_d.keys())
    
    for i, (k,v) in enumerate(zip(list(new_input_d.keys()), demo_list)):
        # put value from demo_list into the last item of the dict val:
        dlist = new_input_d[k]
        dlist[-1] = v
        new_input_d[k] = dlist
    if new_input_d['transcriber'] is None:
       new_input_d['transcriber'] = '?'
    return new_input_d


# ..............................................................................
def btn_togl_extra_refs_example():
    """ Show a data entry example for the field 'extra_references'."""
    lo_togl_btn = ipw.Layout(display='flex',
                             flex_flow='row',
                             justify_content='center',
                             margin='0px 0px 0px 30px',
                             width='95%')

    lo_togl_out = ipw.Layout(display='flex',
                             flex_flow='column',
                             margin='0px 0px 0px 30px',
                             width='95%')
    
    # Callback for toggle:
    def show_example(togl):
        with togl_out:
            if togl['new']:  
                display(Markdown(UTL.EXTRA_REFS_EXAMPLE))
            else:
                togl_out.clear_output()
                
    desc = "Entry example for 'Extra References'"
    togl = ipw.ToggleButton(description=desc,
                            button_style='info',
                            icon='eye',
                            layout=lo_togl_btn)
    togl_out = ipw.Output(layout=lo_togl_out)
    togl.observe(show_example, 'value')
    return ipw.VBox([togl, togl_out])


def wgtbox_from_kv(k, fld_val):
    """
    Return an ipw Box widget according to param `fld_val`, which is the
    value of k key from the dict returned by `get_new_input_flds()` 
    (or from any other dict with same types).
    :param fld_val (list, len=4): [<wiget type>,<placeholder>,<info>,<value>]
    """
    if len(fld_val) != 4:
        raise ValueError("wgtbox_from_kv::fld_val: len != 4.")
        
    lo_txt = ipw.Layout(width='75%')
    lo_box_form_item = ipw.Layout(display='flex',
                                  flex_flow='row',
                                  justify_content='space-between',
                                  margin='0px 10px 0px 5px', 
                                  width='95%')
    
    (wgt, plc, info, val) = fld_val
        
    color = 'red' if info == reqd else 'black'
    itm1 = ipw.HTML(F"<p><font color='{color}'>{info}&nbsp; </p>")

    if k != "extra_references":
        w_Box = ipw.Box([itm1,
                         wgt(value=val,placeholder=plc,
                             layout=lo_txt)],
                        layout=lo_box_form_item
                        )
    else:
        # add btn to show input example:
        tog_vbx = btn_togl_extra_refs_example()
        
        w_Box = ipw.VBox([ipw.Box([itm1,
                                   wgt(value=val,placeholder=plc,
                                       layout=lo_txt)],
                                   layout=lo_box_form_item),
                          tog_vbx]
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
    lo_accord = ipw.Layout(display='flex',
                           flex_flow='column',
                           border='solid 1px',
                           align_items='stretch',
                           margin='0px 10px 0px 30px',
                           width='85%')

    kids = children or []
    w_acc = ipw.Accordion(children=kids,
                          selected_index=None,
                          layout=lo_accord)
    # get names -> titles
    for i, n in enumerate([child.name for child in w_acc.children]):
        w_acc.set_title(i, n)    
    return w_acc


def get_entry_accordion(input_dict):
    """Return an Accordion populated with input_dict k,v."""
    children = [wgtbox_from_kv(k, v) for k, v in input_dict.items()]
    return wgt_Accord(children)


def load_entry_dict(tm_obj):
    """
    Return a dict of the entries in the TranscriptMeta object 
    (tm_obj) event_dict to be exposed by the Accordion container.
    """
    exposed_d = get_new_input_flds()
    ks = list(tm_obj.event_dict.keys())
    common_ks = set(ks) & set(list(exposed_d.keys()))
    for k in common_ks:
        # load the value= last item:
        exposed_d[k][-1] = tm_obj.event_dict[k]
    return exposed_d


# ..............................................................................
def get_accordion_entries(accord):
    """Dict of (possibly modified) Accordion entries."""
    exposed_ks = list(get_new_input_flds().keys())
    d = dict()
    for i, k in enumerate(exposed_ks):
        if k != 'extra_references':
            child = accord.children[i].children[1]
        else:
            # child inside a vbox
            child = accord.children[i].children[0].children[1]

        val = child.get_interact_value() or Meta.NA
        d[k] = val
    return d


def validate_form_entries(entry_dict, tm_obj):
    """
    Return a copy of TranscriptMeta (tm_obj) event_dict populated
    with user's entries.
    The output dict can then be passed to tm_obj.update_dict().
    :entry_dict: output of get_accordion_entries(accord).
    """ 
    # check:
    exposed = get_new_input_flds()
    exposed_ks = list(exposed.keys())
    user_ks = list(entry_dict.keys())
    assert len(exposed_ks) == len(user_ks)
    
    data_dict = tm_obj.event_dict.copy()

    for i, (k, v) in enumerate(entry_dict.items()):
        #if k != 'extra_references':
        #    child = accord.children[i].children[1]
        #else:
        #    # child inside a vbox
        #    child = accord.children[i].children[0].children[1]

        #val = child.get_interact_value() or Meta.NA
        # check 1: NA but required -> end
        if v == Meta.NA and exposed[k][-2] == reqd:
            #t = accord.get_title(i)
            raise ValueError(F'Cannot save: {k} is required.')
            
        if k == 'transcriber':
            if v == Meta.NA or v == '':
                data_dict['transcriber'] = '?'  
        else:               
            data_dict[k] = v
            if k =='video_url':
                dom, vid = UTL.split_url(v)
                data_dict['yt_video_id'] = vid     
                        
    tm_obj.validate_dict(data_dict)
    return data_dict


# ..............................................................................
status_opts = [s.value for s in Meta.TrStatus][:-1]

class PageControls:
    def __init__(self, page_idx, status_opts=status_opts):
        if page_idx not in [0,1,2]:
            msg = "The page_idx refers to the App.center "
            msg += "tab index for 'ADD', MODIFY' or 'EDIT',"
            msg += " hence only one of [0,1,2] is valid."
            raise ValueError (msg)
            
        lo_page = ipw.Layout(display='flex',
                             flex_flow='column',
                             margin='0px 0px 0px 10px')
        
        self.page_idx = page_idx
        self.status_opts = status_opts
        
        rdmdf, _ = Meta.df_from_readme_tbl()
        self.df = rdmdf
        self.yrs = self.df[self.df.year != Meta.NA].year.unique().tolist()
        self.TR = None
        
        if self.page_idx == 0:
            self.verb = 'add'
            # Instantiate obj for new event:
            self.TR = Meta.TranscriptMeta()
            if Meta.DEMO:
                # demo data items
                user_dict = get_demo_input_dict()  
            else:
                user_dict = get_new_input_flds()
            entry_group = get_entry_accordion(user_dict)
            self.page = ipw.VBox([self.get_sel_banner(),
                                  ipw.VBox([entry_group])],
                                 layout=lo_page)
            setattr(self.page, 'user_dict', user_dict)
        else:
            self.initial_transcriber = None
            self.initial_status = None
            
            lo_idn_sel_out = ipw.Layout(height='20px')
            # output wgts 1st:
            self.idn_sel_out = ipw.Output(layout=lo_idn_sel_out)
            self.load_btn_out = ipw.Output(layout=ipw.Layout(height='30px'))
                
            self.yr_sel = ipw.Select(options=self.yrs, value=None,
                                     layout=ipw.Layout(width='55px',
                                                       height='90px'))
            self.yr_sel.observe(self.obs_yr_sel, 'value')
            
            self.idn_sel = ipw.Select(options=[], value=None,
                                      layout=ipw.Layout(width='55px',
                                                        height='90px'))
            self.idn_sel.observe(self.obs_idn_sel, 'value')
            
            self.btn_load = ipw.Button(description='LOAD',
                                       button_style='info',
                                       disabled=True)
            self.btn_load.on_click(self.load_btn_click)
            
            # Put selection controls into grid 'template':
            self.sel_hdr_grid = self.get_sel_hdr_grid()
        
            if self.page_idx == 1:
                self.verb = 'modify'
            else:
                self.verb = 'edit'
                # add'l widgets:
                
                # for get_selection_hdr():
                self.av_radio = ipw.RadioButtons(options=['Audio','Video'],
                                                 value='Audio')
                self.transcriber_txt = ipw.Text(value='? (transcriber)')
                self.status_sel = ipw.Select(options=status_opts, value=None,
                                             disabled=True)
                lo_ta = ipw.Layout(display='flex',
                                   flex_flow='column',
                                   width='98%', height='500px')
                self.editarea = ipw.Textarea(value=None,
                                             layout=lo_ta)
            
            self.populate_sel_hdr_grid()
            # start page w/selection controls + 1 empty vbx:
            with self.idn_sel_out:
                print('< File year/File name >')
            # prepped for load btn outcome:
            self.page = ipw.VBox([self.sel_hdr_grid,
                                  ipw.VBox([])],
                                 layout=lo_page)
            setattr(self.page, 'user_dict', None)
            
       
    def get_sel_banner(self):
        """Page informational header."""
        if self.page_idx == 0:
            sel_banner = '<H3>Provide the Event related data.</H3>'
        elif self.page_idx == 1:
            sel_banner = '<H3>Select the Event Year and Id.</H3>'
        else:
            sel_banner = '<H3>Select the Event Year, Id, AV player '
            sel_banner += '(and if need be, update the Transcriber'
            sel_banner += ' & the Status before saving!).</H3>'
        return ipw.HTML(value=sel_banner)
    
    
    def get_sel_hdr_grid(self):
        """
        Setup a grid of common widgets common to MODIFY, EDIT.
        Grid empty boxes to be populated as per .page_idx.
        """
        if self.page_idx == 0:
            return
        #lo_sel_vbx = ipw.Layout(justify_content='space-between')
        #                        margin='0px 0px 2px 30px')
        grid = ipw.GridspecLayout(2, 4) #,layout=lo_sel_vbx)
        lo_btn_vbx = ipw.Layout(flex_flow='column',
                                justify_content='space-between')
        
        grid[0, 0:] = self.get_sel_banner()
        
        #if self.page_idx == 1:
        grid[1, 0:3] = ipw.HBox([])
        #else:
        #    grid[1, 0:2] = ipw.HBox([])
        #    #grid[1, 1] = ipw.VBox([]) 
        #    grid[1, 2] = ipw.VBox([])#, layout=lo_btn_vbx)
        
        grid[1, 3] = ipw.VBox([self.btn_load,
                               self.load_btn_out],
                              layout=lo_btn_vbx)
        return grid


    def populate_sel_hdr_grid(self):
        """Populate .sel_hdr_grid."""
        if self.page_idx == 0:
            return
        if self.page_idx == 1:
            # 1 hbx (+ trailing vbx for btn)
            self.sel_hdr_grid[1, 0:2].children = [self.yr_sel, 
                                                  self.idn_sel, 
                                                  self.idn_sel_out]
        else:
            #hbx(yr | idn), vbx(idn_out| av_radio),vbx(transcriber|status)
            #vx = ipw.VBox([self.idn_sel_out, self.av_radio])
            self.sel_hdr_grid[1, 0:3].children = [self.yr_sel,
                                                  self.idn_sel,
                                                  ipw.VBox([self.idn_sel_out,
                                                            self.av_radio]),
                                                  ipw.VBox([self.transcriber_txt,
                                                            self.status_sel])]
            #self.sel_hdr_grid[1, 1].children = [self.idn_sel_out,
            #                                    self.av_radio]
            #self.sel_hdr_grid[1, 2].children = [self.transcriber_txt,
            #                                    self.status_sel]

    
    def obs_yr_sel(self, change):
        """Observe fn for year selection box."""
        yr = change['owner'].value
        if self.idn_sel.value is not None:
            self.idn_sel_out.clear_output()
        idn_opts = self.df[self.df.year == yr].N.sort_values(ascending=False).values.tolist()
        #with self.idn_sel.hold_trait_notifications():
        self.idn_sel.options = idn_opts
        self.idn_sel.index = None

         
    def obs_idn_sel(self, change):
        """Observe fn for idn selection box."""
        self.idn_sel_out.clear_output()
        with self.idn_sel_out:
            if ((self.yr_sel.index is not None) 
                and (self.idn_sel.index is not None)):
                
                msk = (self.df.year==self.yr_sel.value)
                msk = msk & (self.df.N==self.idn_sel.value)
                fname = self.df.loc[msk].name.values[0]
                if self.page_idx == 2:
                    self.transcriber_txt.value = self.df.loc[msk].Transcriber.values[0]
                    if self.initial_transcriber is None:
                        self.initial_transcriber = self.transcriber_txt.value
                self.btn_load.disabled = False
                print(self.yr_sel.value + '/'+ fname)
            else:
                self.btn_load.disabled = True
                

    def download_audio(self):
        if self.TR is None:
            return
        idn, year = self.TR.idn, self.TR.year
        video_url = self.TR.event_dict['video_url']
        vid = self.TR.event_dict['yt_video_id']
        if self.TR.YT is None:
            from manage import EventTranscription as TRX
            self.TR.YT = TRX.YTVAudio(year,idn,video_url,vid)
            self.TR.YT.download_audio()
            self.TR.event_dict['audio_track'] = self.TR.YT.audio_filepath
        return
         
            
    def load_btn_click(self, b):
        """ Load btn on Modify, Edit pages."""
        self.load_btn_out.clear_output()                        
        with self.load_btn_out:
            try:
                self.TR = Meta.TranscriptMeta(self.idn_sel.value,
                                              self.yr_sel.value)
                if self.page_idx == 1:
                    exposed = load_entry_dict(self.TR)
                    self.page.user_dict = exposed
                    entry_form = get_entry_accordion(exposed)
                    
                    with self.page.children[1].hold_trait_notifications():
                        if len(self.page.children[1].children) == 1:
                            self.page.children[1].children = ()
                        self.page.children[1].children += (entry_form,)
                    
                else:       
                    self.status_sel.disabled = False
                    status = self.TR.event_dict['status']
                    if status in self.status_opts:
                        self.status_sel.value = status 
                    else:
                        self.status_sel.value = self.status_opts[-1]
                    if self.initial_status is None:
                        self.initial_status = status
                    
                    # reset default if no audio could be downloaded:
                    if not self.TR.event_dict['audio_track'].exists():
                        print("Audio not found. Downloading...")
                        try:
                            self.download_audio()
                        except:
                            self.av_radio.value = 'Video'
                            print("Problem downloading audio.")
                            
                    use_audio = self.av_radio.value == 'Audio'
                    
                    trx_text = self.TR.get_transcript_text()
                    self.editarea.value = trx_text
                    
                    with self.page.children[1].hold_trait_notifications():
                        if len(self.page.children[1].children) == 2:
                            self.page.children[1].children = ()

                        if use_audio:
                            track = self.TR.event_dict['audio_track']
                            A = ipw.Audio.from_file(track, autoplay=False)
                            self.page.children[1].children += (A,)
                        else:
                            E = ipw.HTML(value=self.TR.event_dict['video_embed'])
                            self.page.children[1].children += (E,)

                        self.page.children[1].children += (self.editarea,)

                b.disabled = True
                print(F"{self.verb.title()} along!")
            except:
                print("Error loading!")
                

def get_app_hdr():
    style = "text-align:center;padding:5px;background:#c2d3ef;"
    style += "color:#ffffff;font-size:3em;"
    style += "width:100%,height=50%"
    div = F' <div style="{style}">Data Umbrella Event Management</div>'
    hdr_html = UTL.show_du_logo_hdr(as_html=False)
    return ipw.HTML(hdr_html + div)
    
    
class AppControls:
    def __init__(self):
        self.actions = OrderedDict([('Add an event',
                                     ['Enter Info','Validate','Save','Show Readme', 'Show File']),
                                    ('Modify an event',
                                     ['Modify Event','Validate','Save','Show Readme', 'Show File']),
                                    ('Edit a transcript',
                                     ['Edit Transcript','Save','Show Readme', 'Show File'])
                                   ])
        
        self.PC = None # Controls.PageControl instance
        self.to_delete = None # set by validate_1()
        
        self.left_sidebar = self.get_left()
        self.left_sidebar.observe(self.menu_selection, 'value')
        
        lo_info_out = ipw.Layout(display='flex',
                                 flex_flow='column',
                                 margin='0px 0px 0px 30px',
                                 width='98%')
        self.info_out = ipw.Output()
        
        self.center = self.get_center()
        self.center.observe(self.info_display, 'selected_index')
        self.dl1 = ipw.dlink((self.left_sidebar, 'selected_index'),
                             (self.center, 'selected_index'))
        
        # Removed header: no 'gui shifting' w/o it. ??
        self.app = ipw.AppLayout(header=None,
                                 #self.get_app_hdr(),
                                 left_sidebar=self.left_sidebar,
                                 center=self.center,
                                 right_sidebar=self.info_out,
                                 footer=None,
                                 pane_widths=[1, 5, 1],
                                 pane_heights=[1, 3, 1]
                                 )
        setattr(self.app, 'data_dict', None)


    def get_center(self):
        """ Create 3 Tabs for actions + 2 for files."""
        lo_tabs = ipw.Layout(display='flex',
                             flex_flow='column',
                             align_items='stretch',
                             justify_content='center',
                             width='98%')
        tabs = ipw.Tab(selected_index=None, layout=lo_tabs)
        # Tabs:
        ks = list(self.actions.keys()) + ['readme', 'file']
        # 1st tab child: message output
        tabs.children = [ipw.VBox([ipw.Output(),
                                   ipw.VBox([])]) for k in ks]
        for i, k in enumerate(ks):
            tabs.set_title(i, k.split()[0].upper())
        return tabs

    
    def get_left(self):
        """
        Create Accordion MENU with VBox for actions.keys as children.
        Populate Accordion MENU with ToggleButtons children that have:
         - a 'parent_idx' attribute
         - observe function for ToggleButtons children
        """
        acc_items = [ipw.VBox(description=k) for k in list(self.actions.keys())]
        menu_acc = ipw.Accordion(children=acc_items,
                                 selected_index=None)
        for i, (k, v) in enumerate(self.actions.items()):
            btn = ipw.ToggleButtons(options=v, value=None,
                                    button_style='info')
            setattr(btn, 'parent_idx', i)
            btn.observe(self.menu_tog_sel, names='value')
            menu_acc.children[i].children = [btn]
            menu_acc.set_title(i, k.upper())
        return menu_acc
    
    
    # left_sidebar.observe
    def menu_selection(change):
        """ 
        Activate Tabs index per left sidebar (menu) index.
        One-way only: menu.index -> tabs.index
        """
        self.center.selected_index = self.left_sidebar.selected_index


    # center.observe
    def info_display(self, change):
        """App header panel: info about selected op.
        """
        self.info_out.clear_output()
        wgt = change['owner']
        # Link tab selection index with info panel:
        if wgt.selected_index is None:
            t = 3
        else:
            t = wgt.selected_index
        if t > 3:
            return
        event_fn = {0:'ADD', 1:'MODIFY', 2:'EDIT', 3:'INIT'}
        which = UTL.EventFunction[event_fn[t]]
        EF = UTL.DisplaySectionInfo(which)
        info_val = EF.show_section_info()
        if t < 3:
            self.left_sidebar.selected_index = t
            self.left_sidebar.children[t].children[0].index = None

            with self.info_out:
                display(info_val)
   

    def msg_out(self, idx, msg):
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            print(msg)

    
    def validate_0(self, idx):
        input_form = self.PC.page.children[1].children[0]
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            try:
                self.PC.page.user_dict = get_accordion_entries(input_form)
                self.app.data_dict = validate_form_entries(self.PC.page.user_dict,
                                                           self.PC.TR)
                print('Validated!')

            except:
                print('Validation Error: Fix & Try again.')

            
    def validate_1(self, idx):
        grid_sel_idn_out = self.PC.page.children[0][1,1].children[-1]
        initial_md = grid_sel_idn_out.outputs[0]['text'][5:-1]
        
        input_form = self.PC.page.children[1].children[0]
        
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            try:
                d = get_accordion_entries(input_form)
                self.PC.page.user_dict = d
                self.app.data_dict = validate_form_entries(self.PC.page.user_dict,
                                                           self.PC.TR)
                print('Validated!')
                d['idn'] = self.PC.TR.idn
                d = self.PC.TR.set_path_keys(d)
                if initial_md != d['transcript_md']:
                    mdfile = UTL.get_subfolder(d['year'], Meta.REPO_PATH)
                    mdfile = mdfile.joinpath(initial_md)
                    self.to_delete = mdfile
                    print(F'File to delete: {initial_md}')
            except:
                print('Validation Error: Fix & Try again.')                
                
    
    def save_entry(self, idx):
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            if self.app.data_dict is None:
                print('Validate first!')
                return
            if self.PC.TR is None:
                print('TR object not instantiated.')
                return
            try:
                self.PC.TR.update_dict(self.app.data_dict)
                print('Update dict: OK!')
            except:
                print('Update dict: Something went wrong.')
                return
            try:
                self.PC.TR.update_readme()
                print('Update readme: OK!')
            except:
                print('Update readme: Something went wrong.')
                return
            try:
                self.PC.TR.save_transcript_md()
                print('Save: Done!')
                if idx == 1:
                    if self.to_delete is not None:
                        self.to_delete.unlink()
                        self.to_delete = None
            except:
                if idx == 0:
                    msg = 'Save starter transcript: Something went wrong.'
                else:
                    msg = 'Save transcript: Something went wrong.'
                print(msg)
        # refresh df:
        newdf, _ = Meta.df_from_readme_tbl()
        self.PC.df = newdf
        if self.PC.verb != 'add':
            self.PC.idn_sel.value = None


    def save_edit(self, idx):
        """Save edited transcript."""
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            if self.PC.transcriber_txt.value.startswith('?'):
                print("'?' is not a good name!")
            try:
                do_readme = self.PC.initial_status != self.PC.status_sel.value
                do_trx = self.PC.initial_transcriber != self.PC.transcriber_txt.value
                if do_readme:
                    self.PC.TR.event_dict['status'] = self.PC.status_sel.value
                if do_trx:
                    self.PC.TR.event_dict['transcriber'] = self.PC.transcriber_txt.value
                if do_readme or do_trx:        
                    self.PC.TR.update_readme()
                    print('Updated README.')
            except:
                print('Could not update README.')
                return
            try:
                self.PC.TR.save_transcript_md(new_trx=self.PC.editarea.value)
                self.PC.btn_load.disabled = False
                self.PC.editarea.value = ''
                print('Updated Event file.')
            except:
                print('Could not update Event file.')
        # refresh df:
        newdf, _ = Meta.df_from_readme_tbl()
        self.PC.df = newdf
        self.PC.idn_sel.value = None


    def show_mdfile(self, idx):
        """Here, idx = tab index"""
        self.center.children[idx].children[0].clear_output()
        # vbx:
        if len(self.center.children[idx].children[1].children) == 0:
            self.center.children[idx].children[1].children += (ipw.Output(),)
        else:
            self.center.children[idx].children[1].children[0].clear_output()
    
        if idx == 3:
            with self.center.children[3].children[1].children[0]:
                Meta.show_md_file(Meta.MAIN_README)
        else:
            if self.PC.TR is not None:
                yr = self.PC.TR.event_dict['year']
                fname = self.PC.TR.event_dict['transcript_md']
                mdfile = Meta.REPO_PATH.joinpath(yr, fname)
                if mdfile.exists():
                    with self.center.children[4].children[1].children[0]:
                        Meta.show_md_file(mdfile, kind='Transcript')
                else:
                    self.msg_out(4, F'File not found: {mdfile}.')
            else:
                self.msg_out(4, 'PageControls.TR object not instantiated.')
        self.center.selected_index = idx


    def menu_tog_sel(self, change):
        wgt = change['owner']
        iparent = wgt.parent_idx
        tog_val = wgt.value

        if iparent == 0:
            if tog_val == 'Enter Info':
                self.PC = PageControls(0)
                entry_group = self.PC.page
                # Add 2nd control in tab 2nd vbox:
                if len(self.center.children[0].children[1].children) == 1:
                    self.center.children[0].children[1].children = ()
                self.center.children[0].children[1].children += (entry_group,)
            elif tog_val == 'Validate':
                self.validate_0(iparent)
            elif tog_val == 'Save':
                self.save_entry(iparent)
            elif tog_val == 'Show Readme':
                self.show_mdfile(3)
            elif tog_val == 'Show File':
                self.show_mdfile(4)

        elif iparent == 1:
            if tog_val == 'Modify Event':
                self.PC = PageControls(1)
                edit_page = self.PC.page
                if len(self.center.children[1].children[1].children) == 1:
                    self.center.children[1].children[1].children = ()
                self.center.children[1].children[1].children += (edit_page,)
            elif tog_val == 'Validate':
                self.validate_1(iparent)
            elif tog_val == 'Save':
                self.save_entry(iparent)
            elif tog_val == 'Show Readme':
                self.show_mdfile(3)
            elif tog_val == 'Show File':
                self.show_mdfile(4)

        elif iparent == 2:
            if tog_val == 'Edit Transcript':
                self.PC = PageControls(2)
                edit_page = self.PC.page
                if len(self.center.children[2].children[1].children) == 1:
                    self.center.children[2].children[1].children = ()
                self.center.children[2].children[1].children += (edit_page,)
            elif tog_val == 'Save':
                self.save_edit(iparent)
            elif tog_val == 'Show Readme':
                self.show_mdfile(3)
            elif tog_val == 'Show File':
                self.show_mdfile(4)


    def __repr__(self):
        from pprint import pformat
        return pformat(self.__dict__)
