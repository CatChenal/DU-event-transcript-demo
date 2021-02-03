# -*- coding: utf-8 -*-
# Controls.py
# Programmer: Cat Chenal
#
from pathlib import Path
from IPython.display import Markdown, HTML
import ipywidgets as ipw
from functools import partial
from collections import OrderedDict, Counter

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
    lo_togl = ipw.Layout(display='flex',
                             flex_flow='row',
                             justify_content='center',
                             margin='0px 0px 0px 30px',
                             width='95%')

    lo_out_togl = ipw.Layout(display='flex',
                             flex_flow='column',
                             margin='0px 0px 0px 30px',
                             width='95%')
    
    # Callback for toggle:
    def show_example(togl):
        with out_togl:
            if togl['new']:  
                display(Markdown(UTL.EXTRA_REFS_EXAMPLE))
            else:
                togl_out.clear_output()
                
    desc = "Entry example for 'Extra References'"
    togl = ipw.ToggleButton(description=desc,
                            button_style='info',
                            icon='eye',
                            layout=lo_togl)
    out_togl = ipw.Output(layout=lo_out_togl)
    togl.observe(show_example, 'value')
    return ipw.VBox([togl, out_togl])


def wgtbox_from_kv(k, fld_val):
    """
    Return a Box widget according to param `fld_val`, which is the
    value of key k from the dict returned by `get_new_input_flds()` 
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
    

def wgt_Accord(children=None, lo_accord=None):
    """
    Return ipw.Accordion widget with possible children.
    If given, each child is assumed to have a name attribute, which
    is used for titling of the Accordion parent row.
    Children created by wgtbox_from_kv() have a name attribute.
    :param: lo_accord: ipw.Layout.
    """
    if lo_accord is None:
        lo_accord = ipw.Layout(display='flex',
                               flex_flow='column',
                               #border='solid 1px',
                               align_items='stretch',
                               margin='0px 10px 0px 30px',
                               width='85%')
        
    kids = children or []
    w_acc = ipw.Accordion(children=kids,
                          selected_index=None,
                          layout=lo_accord)
    # get names -> titles
    for i, c in enumerate([child for child in w_acc.children]):
        w_acc.set_title(i, getattr(c, 'name', ''))    
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
        # check 1: NA but required -> end
        if v == Meta.NA and exposed[k][-2] == reqd:
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

def get_info_banner(page_idx):
    """Page informational header."""
    if page_idx == 0:
        sel_banner = '<H3>Provide the Event related data.</H3>'
    elif page_idx == 1:
        sel_banner = '<H3>Select the Event Year and Id.</H3>'
    else:
        sel_banner = '<H3>Select the Event Year, Id, AV player '
        sel_banner += '(and if need be, update the Transcriber'
        sel_banner += ' & the Status before saving!).</H3>'
    return ipw.HTML(value=sel_banner)


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
            self.page = ipw.VBox([get_info_banner(0),
                                  ipw.VBox([entry_group])],
                                 layout=lo_page)
            setattr(self.page, 'user_dict', user_dict)
        else:
            self.initial_transcriber = None
            self.initial_status = None
            
            # output wgts 1st:
            self.out_sel_idn = ipw.Output(layout=ipw.Layout(height='30px'))
            self.out_btn_load = ipw.Output(layout=ipw.Layout(height='30px'))
                
            self.sel_yr = ipw.Select(options=self.yrs, value=None,
                                     layout=ipw.Layout(width='55px',
                                                       height='90px'))
            self.sel_yr.observe(self.obs_sel_yr, 'value')
            
            self.sel_idn = ipw.Select(options=[], value=None,
                                      layout=ipw.Layout(width='55px',
                                                        height='90px'))
            self.sel_idn.observe(self.obs_sel_idn, 'value')
            
            self.btn_load = ipw.Button(description='LOAD',
                                       button_style='info',
                                       disabled=True)
            self.btn_load.on_click(self.click_btn_load)
            
            # Put selection controls into gridbox:
            #self.sel_hdr_grid = self.get_sel_hdr_grid()
            self.sel_hdr_grid = self.get_grid(header_fn=get_info_banner)
        
            if self.page_idx == 1:
                self.verb = 'modify'
            else:
                self.verb = 'edit'
                # add'l widgets:
                
                # for populating sel_hdr_grid:
                self.rad_av = ipw.RadioButtons(options=['Audio','Video'],
                                               value='Audio')
                self.txt_transcriber = ipw.Text(value='? (transcriber)',
                                                description='You?')
                self.sel_status = ipw.Select(options=status_opts, value=None,
                                             disabled=True)
                self.txa_editarea = ipw.Textarea(value=None,
                                                 layout=ipw.Layout(display='flex',
                                                                   flex_flow='column',
                                                                   width='98%',
                                                                   height='500px'))
                # grid footer controls:
                #lo_out = ipw.Layout(height='30px')
                self.out_sel_files = ipw.Output()
                self.out_btn_update = ipw.Output()
                self.out_btn_redo = ipw.Output()
                
                self.btn_update = ipw.Button(description='UPDATE',
                                        tooltip='Validate & save your changes.',
                                        button_style='info')
                self.btn_redo = ipw.Button(description='REPROCESS',
                                      tooltip='Redo the transcription with the new files.',
                                      button_style='info',
                                      #disabled=True
                                          )
                self.txt_input = ipw.Text(layout=ipw.Layout(width='420px'))
                self.sel_files = ipw.widgets.Select(value=None,
                                                    options=['People','Names',
                                                             'Places','Upper',
                                                             'Corrections'])
                self.sel_files.observe(self.obs_sel_files)
                self.btn_update.on_click(self.click_btn_update)
                self.btn_redo.on_click(self.click_btn_redo)

                
            #self.populate_sel_hdr_grid()
            self.populate_grid()
            
            # start page w/selection controls + 1 empty vbx:
            with self.out_sel_idn:
                print('< File year/File name >')
            # prepped for load btn product:
            self.page = ipw.VBox([self.sel_hdr_grid,
                                  ipw.VBox([])],
                                 layout=lo_page)
            setattr(self.page, 'user_dict', None)
    
    
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


    def get_grid(self, grid_name=None, header_fn=None, exclude=None):
        """
        Wrapper to get a starter GridBox with pre-defined areas to
        obtain, at most, a 3x3 grid.
        :param: idx: index referencing a caller widget, i.e. tab index.
        :param: grid_name: Name (attribute) to id the grid
        :param: exclude: None (default), or header|footer areas to exclude,
                e.g ['footer']
        :param: header_fn: Function populating the page header grid area
                           if any; Takes idx as param: header_fn(idx).
        """
        if self.page_idx == 0:
            return

        def lo_grid_area(a):
            return ipw.Layout(width='auto', grid_area=a)

        # always included:
        main = ipw.HBox(children=[],
                        layout=lo_grid_area('main'))
        sidebar = ipw.VBox(children=[],
                           layout=lo_grid_area('sidebar'))

        if exclude is not None:
            if len(exclude) == 2:
                # Assume header & footer excluded
                tpl_areas= '''"main main sidebar"'''
                kids = [main, sidebar]
            else:    
                if 'header' not in exclude:
                    tpl_areas= '''
                        "header header header"
                        "main main sidebar"
                        '''
                    if header_fn is None:
                        header = ipw.HBox(children=[],
                                          layout=lo_grid_area('header'))
                    else:
                        header = header_fn(self.page_idx)

                    kids = [header, main, sidebar]

                if 'footer' not in exclude:
                    tpl_areas= '''
                        "main main sidebar"
                        "footer footer footer"
                        '''
                    footer = ipw.HBox(children=[],
                                      layout=lo_grid_area('footer'))
                    kids = [main, sidebar, footer]
        else:
            tpl_areas= '''
                "header header header"
                "main main sidebar"
                "footer footer footer"
                '''
            if header_fn is None:
                header = ipw.HBox(children=[],
                                  layout=lo_grid_area('header'))
            else:
                header = header_fn(self.page_idx)
            footer = ipw.HBox(children=[],
                              layout=lo_grid_area('footer'))            
            kids = [header, main, sidebar, footer]

        lo_grid = ipw.Layout(grid_template_rows='auto auto auto',
                             grid_template_columns='1fr, 1fr, 1fr', 
                             grid_template_areas= tpl_areas)
        grid = ipw.GridBox(children=kids,
                           layout=lo_grid)
        setattr(grid, 'name', grid_name or '')

        return grid

    
    def get_update_grid(self):
        """
        Return a GridBox with controls for file update.
        """
        vbx = partial(ipw.VBox,
              layout=ipw.Layout(display='flex',
                                flex_flow='column',
                                align_items='flex-start'))
        title = 'Update a file for propercasing or corrections | '
        title += 'Reprocess the transcript'
        g = self.get_grid(title, exclude=['header', 'footer'])
        # preset msg:
        with self.out_sel_files:
            msg = "<h5>Use this text box to enter your entries:</h5>"
            display(HTML(msg))

        g.children[0].children = [self.sel_files,
                                  vbx([self.out_sel_files,
                                       self.txt_input])]
        g.children[1].children = [vbx([self.btn_update,
                                       self.out_btn_update]),
                                  vbx([self.btn_redo,
                                       self.out_btn_redo])]
        return g
    
    
    def populate_grid(self):
        """
        Populate GridBox g main, sidebar and footer (if idx==2) areas.
        """
        if  self.page_idx == 0:
            return
        
        g = self.sel_hdr_grid.children
        if self.page_idx == 1:
            g[1].children = [self.sel_yr, self.sel_idn, self.out_sel_idn]
            g[2].children = [self.btn_load, self.out_btn_load]
        else:
            g[1].children = [self.sel_yr, self.sel_idn,
                             ipw.VBox([self.out_sel_idn, self.rad_av]),
                             ipw.VBox([self.txt_transcriber,
                                       self.sel_status])]
            g[2].children = [self.btn_load, self.out_btn_load]
            # load controls in Accordion:
            lo_accord = ipw.Layout(display='flex',
                       flex_flow='column',
                       align_items='stretch',
                       width='100%'
                      ) 
            g[3].children = [wgt_Accord([self.get_update_grid()],
                                        lo_accord)]

    
    def obs_sel_files(self, change):
        """Observe fn for sel_files."""
        fname = change['owner'].value
        if fname is None:
            msg = "<h5>Use this text box to enter your list of entries:</h5>"
        elif fname == 'Corrections':
            msg = "<h5>Provide your entries as a list of string tuples, "
            msg += "e.g.: <code>('&lt;from&gt;', '&lt;to&gt;'), ...</code><br>"
            msg += "Note: existing keys are not overwritten.</h5>"
        else:
            msg = "<h5>Separate your entries with a comma.</h5>"
        self.out_sel_files.clear_output()
        with self.out_sel_files:
            display(HTML(msg))


    def obs_sel_yr(self, change):
        """Observe fn for year selection box."""
        yr = change['owner'].value
        idn_opts = self.df[self.df.year == yr].N.sort_values(ascending=False).values.tolist()
        with self.sel_idn.hold_trait_notifications():
            if self.sel_idn.index is not None:
                self.out_sel_idn.clear_output()
            self.sel_idn.options = idn_opts
        self.sel_idn.index = None
            
         
    def obs_sel_idn(self, change):
        """Observe fn for idn selection box."""
        self.out_sel_idn.clear_output()
        with self.out_sel_idn:
            if ((self.sel_yr.index is not None) 
                and (self.sel_idn.index is not None)):
                
                msk = (self.df.year==self.sel_yr.value)
                msk = msk & (self.df.N==self.sel_idn.value)
                fname = self.df.loc[msk].name.values[0]
                if self.page_idx == 2:
                    self.txt_transcriber.value = self.df.loc[msk].Transcriber.values[0]
                    if self.initial_transcriber is None:
                        self.initial_transcriber = self.txt_transcriber.value
                self.btn_load.disabled = False
                print(self.sel_yr.value + '/'+ fname)
            else:
                self.btn_load.disabled = True
                

    def click_btn_load(self, b):
        """ Load btn on Modify, Edit pages."""
        self.out_btn_load.clear_output()                        
        with self.out_btn_load:
            try:
                self.TR = Meta.TranscriptMeta(self.sel_idn.value,
                                              self.sel_yr.value)
                if self.page_idx == 1:
                    exposed = load_entry_dict(self.TR)
                    self.page.user_dict = exposed
                    entry_form = get_entry_accordion(exposed)
                    
                    with self.page.children[1].hold_trait_notifications():
                        if len(self.page.children[1].children) == 1:
                            self.page.children[1].children = ()
                        self.page.children[1].children += (entry_form,)
                    
                else:       
                    self.sel_status.disabled = False
                    status = self.TR.event_dict['status']
                    if status in self.status_opts:
                        self.sel_status.value = status 
                    else:
                        self.sel_status.value = self.status_opts[-1]
                    if self.initial_status is None:
                        self.initial_status = status
                    
                    # reset default if no audio could be downloaded:
                    if not self.TR.event_dict['audio_track'].exists():
                        print("Audio not found. Downloading...")
                        try:
                            self.download_audio()
                        except:
                            self.rad_av.value = 'Video'
                            print("Problem downloading audio.")
                            
                    use_audio = self.rad_av.value == 'Audio'
                    
                    trx_text = self.TR.get_transcript_text()
                    self.txa_editarea.value = trx_text
                    
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

                        self.page.children[1].children += (self.txa_editarea,)

                b.disabled = True
                print(F"{self.verb.title()} along!")
            except:
                print("Error loading!")


    def click_btn_update(self, b):
        self.out_btn_update.clear_output()
        # footer :: HBox > Accordion > GridBox
        footer_g = self.sel_hdr_grid.children[3].children[0].children[0]
        #footer_g = page_hdr_grid.children[3].children[0].children[0]
        v_file = footer_g.children[0].children[0].value
        v_entries = footer_g.children[0].children[1].children[1].value or None
        
        if v_file is None or v_entries is None:
            with self.out_btn_update:
                print('Select a file and provide new entries.')
            return
        
        with self.out_btn_update:
            print('Validating...')
                
        valid, msg = validate_user_list(v_entries, v_file)
        if valid is None:
            with self.out_btn_update:
                print(msg)
            return
        
        if v_file == 'Corrections':
            corrections = TRX.get_corrections_dict()
            tot, reduced_list, msg = TRX.check_corrections(corrections,
                                                           valid,
                                                           verbose=False)
            if tot:
                if 'reduced' in msg:
                    if reduced_list:
                        TRX.add_corrections(reduced_list, return_dict=False)
                else:
                    TRX.add_corrections(valid, return_dict=False)
            else:
                with self.out_btn_update:
                    print(msg)
                return
        else:
            
            v_file = v_file.lower()
            fname = TRX.substitutions[v_file]
            current_list = TRX.readcsv(fname)[v_file].tolist()

            tot, reduced_list = TRX.check_list(current_list, valid,
                                               verbose=False)
            if tot:
                if 'reduced' in msg:
                    if reduced_list:
                        TRX.update_conversion_file(v_file, reduced_list)
                else:
                    TRX.update_conversion_file(v_file, valid)
            else:
                with self.out_btn_update:
                    print(msg)

                with self.out_btn_update:
                    print('Doing fake update...')
                update_ok = True
                if update_ok:
                    self.btn_redo.disabled = False
                else:
                    with self.out_btn_update:
                        print('Coud not fake update!')


    def click_btn_redo(self, b):
        self.out_btn_redo.clear_output()
        ok = False
        if ((self.sel_yr.index is None) 
                and (self.sel_idn.index is None)):
            msg = 'Select year and transcript id first!'
        else:
            if self.TR is None:
                self.TR = Meta.TranscriptMeta(self.sel_idn.value,
                                              self.sel_yr.value)
            try:
                self.TR.redo_initial_transcript()
                self.TR.insert_md_transcript()
                ok = True
            except:
                msg = 'Could not redo.'
        if ok:
            msg = 'Done! Collapse this section & LOAD.'
        with self.out_btn_redo:
            print(msg)


# .........................................................
def validate_user_list(entries, file, verbose=False):
    """
    Validate gui entries for propercasing or corrections.
    Return a list of validated entries (None or list) along 
    with a message if verbose=False (default).
    """
    def results(msg, data=None, verbose=None):
        if verbose:
            print(msg)
            return data
        else:
            return data, msg
        
    entries = entries.strip()
    if not entries:
        msg = "No content!"
        return results(msg)

    if entries[-1] == ',':
        entries = entries[:-1]
    ii = entries.find('(') + 1 # 0 if find returns -1
    jj = entries.find(')') + 1
    
    validated = []
    
    if file == 'Corrections':
        if not ii and not jj:
            msg = "Missing parentheses: tuples needed!"
            return results(msg)

        cnt = Counter(entries)
        if cnt['('] != cnt[')']:
            if cnt['('] > cnt[')']:
                msg = "Missing a closing parenthesis!"
            else:
                msg = "Missing an opening parenthesis!"
            return results(msg)
        
        p = entries.partition(')')
        while p[0]:
            p0 = p[0][1:].split(',')
            try:
                str_from = eval(p0[0].strip().lower())
            except:
                str_from = p0[0].strip().lower()
            try:
                str_to = eval(p0[1].strip())
            except:
                str_to = p0[1].strip()
                                
            validated.append((str_from, str_to))
            if p[2] != '':
                p2 = p[2][1:].strip()
                p = p2.partition(')')
            else:
                break
        if not validated:
            msg = "Could not parse tuples!"
    else:
        if ii or jj:
            msg = "Parentheses detected: not for propercasing!"
            return results(msg)
        
        for e in entries.split(','):
            try:
                validated.append(eval(e.strip().lower()))
            except:
                validated.append(e.strip().lower())

        if not validated:
            msg = "Could not parse list!"
            
    if not validated:
        return results(msg)

    return validated, 'OK'
        

def test_validate_user_list(verbose=False):
    corr_val1 = "('dummy', 'Entry')"
    corr_val2 = "('dummy', 'Entry'), ('foo', 'list'), "
    lst_val1 = "'dummy', 'Entry'"
    lst_val2 = "'dummy', 'Entry', 'foo', 'bar', "
    lst_val3 = "'cat chenal', 'will tell', "

    which = ['Corrections','Corrections','Names','Places','People',]
    for i,data in enumerate([corr_val1, corr_val2,lst_val1,lst_val2,lst_val3]):
        out, msg = validate_user_list(data, which[i], verbose)
        print(data, which, ':\n\t', msg, out)
        assert msg == 'OK'
        
    #new tests:
    out, msg = validate_user_list(lst_val1, 'Corrections', verbose)
    print('\nList instead of tuples for Corrections.\n', lst_val1, ':\n\t', msg, out)
    assert out is None
    out, msg = validate_user_list(corr_val1, 'Upper', verbose)
    print('Tuple instead of list for Upper.\n',corr_val1, ':\n\t', msg, out) 
    assert out is None
    

# APP GUI ...............................................................
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
                                     ['Enter Info','Validate','Save',
                                      'Show Readme', 'Show File']),
                                    ('Modify an event',
                                     ['Modify Event','Validate','Save',
                                      'Show Readme', 'Show File']),
                                    ('Edit a transcript',
                                     ['Edit Transcript','Save',
                                      'Show Readme', 'Show File'])
                                   ])
        
        self.PC = None # Controls.PageControl instance
        self.to_delete = None # set by validate_1()
        
        self.left_sidebar = self.get_left()
        self.left_sidebar.observe(self.menu_selection, 'value')
        self.out_info = ipw.Output()
        self.center = self.get_center()
        self.center.observe(self.info_display, 'selected_index')
        self.dl1 = ipw.dlink((self.left_sidebar, 'selected_index'),
                             (self.center, 'selected_index'))
        
        # Removed header: no 'gui shifting' w/o it. ??
        self.app = ipw.AppLayout(header=None, # was get_app_hdr,
                                 left_sidebar=self.left_sidebar,
                                 center=self.center,
                                 right_sidebar=self.out_info,
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
        self.out_info.clear_output()
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

            with self.out_info:
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
