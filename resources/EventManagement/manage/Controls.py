# -*- coding: utf-8 -*-
# Controls.py
# Programmer: Cat Chenal
#
# TODO: A 'Clear Event' button?
#
from collections import OrderedDict
import ipywidgets as ipw

from manage import (EventMeta as Meta,
                    EventTranscription as TRX,
                    Workflow as FLO,
                    Utils as UTL)

main_readme = Meta.MAIN_README
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
                             align_items='stretch',
                             margin='0px 0px 0px 30px')
        
        self.page_idx = page_idx
        self.status_opts = status_opts
        
        self.df, _ = Meta.df_from_readme_tbl()
        self.yrs = self.df[self.df.year != Meta.NA].year.unique().tolist()
        self.TR = None
        
        if self.page_idx == 0:
            self.verb = 'add'
            # Instanciate obj for new event:
            self.TR = Meta.TranscriptMeta()
            if Meta.DEMO:
                # demo data items
                user_dict = FLO.get_demo_input_dict()  
            else:
                user_dict = FLO.get_new_input_flds()
            entry_group = FLO.get_entry_accordion(user_dict)
            self.page = ipw.VBox(children=[self.get_sel_banner()],
                                 layout=lo_page)
            self.page.children += (entry_group,)
            setattr(self.page, 'user_dict', user_dict)
            
        else:
            self.initial_transcriber = None
            self.initial_status = None
            
            lo_idn_sel_out = ipw.Layout(width='300px', height='15px')
            # output wgts 1st:
            self.idn_sel_out = ipw.Output(layout=lo_idn_sel_out)
            self.load_btn_out = ipw.Output(layout=ipw.Layout(height='30px'))
                
            self.yr_sel = ipw.Select(options=self.yrs, value=None,
                                     layout=ipw.Layout(width='50px'))
            self.yr_sel.observe(self.obs_yr_sel, 'value')
            
            self.idn_sel = ipw.Select(options=[], value=None,
                                      layout=ipw.Layout(width='60px'))
            self.idn_sel.observe(self.obs_idn_sel, 'value')
            
            self.btn_load = ipw.Button(description='LOAD',
                                       button_style='info',
                                       disabled=True)
            self.btn_load.on_click(self.load_btn_click)
        
            if self.page_idx == 1:
                self.verb = 'modify'
            else:
                self.verb = 'edit'
                # add'l widgets:
                
                # used by get_selection_hdr()
                self.editarea = None
                self.av_radio = ipw.RadioButtons(options=['Audio','Video'],
                                                 value='Audio')
                self.transcriber_txt = ipw.Text(value='?')
                self.status_sel = ipw.Select(options=status_opts, value=None,
                                             disabled=True)
                
            # start the page with the selection controls only:
            self.page = ipw.VBox(children=[self.get_selection_hdr()],
                                 layout=lo_page)
            # set by load_btn_click:
            setattr(self.page, 'user_dict', None)
            # aliases to ease resetting: p.load_ref.disabled = True
            #setattr(self.page, 'yrid_ref',
            #        self.page.children[0].children[1].children[0])
            #setattr(self.page, 'load_ref',
            #        self.page.children[0].children[1].children[-1].children[0])
            with self.idn_sel_out:
                print('< File year / File name >')
            
        
    def get_sel_banner(self):
        """Tab form informational header."""
        if self.page_idx == 0:
            sel_banner = '<H3>Provide the Event related data.</H3>'
        elif self.page_idx == 1:
            sel_banner = '<H3>Select the Event Year and Id.</H3>'
        else:
            sel_banner = '<H3>Select the Event Year, Id, AV player '
            sel_banner += '(and if need be, update the Transcriber'
            sel_banner += ' & the Status before saving!).</H3>'
        return ipw.HTML(value=sel_banner)
    
    
    def get_selection_hdr(self):
        """
        ADD|MODIFY Input form header: selection wgts in VBox.
        """
        # Final VBox components/kids:
        k_0 = self.get_sel_banner() #:: 1st child
        # load btn:: last
        lo_btn_vbx = ipw.Layout(flex_flow='row',
                                justify_content='space-between')
        k_1_last = ipw.VBox([self.btn_load, self.load_btn_out],
                            layout=lo_btn_vbx)
        if self.page_idx == 1:
            k_1_0 = ipw.HBox([self.yr_sel, self.idn_sel,
                              self.idn_sel_out])
            k_1 = ipw.HBox([k_1_0, k_1_last])
        else:
            k_1_0 = ipw.HBox([self.yr_sel, self.idn_sel])                                 
            k_1_1 = ipw.VBox([self.av_radio,
                              self.idn_sel_out,
                              self.transcriber_txt])
            k_1 =  ipw.HBox([k_1_0, k_1_1,
                             self.status_sel, #k_1_2
                             k_1_last])
            
        lo_sel_vbx = ipw.Layout(justify_content='space-between',
                                margin='0px 0px 2px 30px')
        sel_vbx = ipw.VBox([k_0, k_1], layout=lo_sel_vbx)
        return sel_vbx

    
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
        """Observe fn for idn slection box."""
        self.idn_sel_out.clear_output()
        if self.page_idx == 2:
            self.transcriber_txt.value = '?'
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
                print(self.yr_sel.value + ' / '+ fname)
            else:
                self.btn_load.disabled = True
                
               
    def load_btn_click(self, b):
        self.load_btn_out.clear_output()
                        
        with self.load_btn_out:
            try:
                self.TR = Meta.TranscriptMeta(self.idn_sel.value,
                                              self.yr_sel.value)
                if self.page_idx == 1:
                    exposed = FLO.load_entry_dict(self.TR)   
                    entry_form = FLO.get_entry_accordion(exposed)
                    self.page.user_dict = exposed  
                    self.page.children += (entry_form,)
                else:       
                    self.status_sel.disabled = False
                    status = self.TR.event_dict['status']
                    if status in self.status_opts:
                        self.status_sel.value = status 
                    else:
                        self.status_sel.value = self.status_opts[-1]
                    self.initial_status = status
                    
                    # reset default if no audio:
                    #TODO: download it
                    if not self.TR.event_dict['audio_track'].exists():
                        self.av_radio.value = 'Video'
                        print("No audio.")
                        
                    if self.av_radio.value == 'Audio':
                        track = self.TR.event_dict['audio_track']
                        AV = ipw.Audio().from_file(track, autoplay=False)
                    else:
                        AV = ipw.HTML(value=self.TR.event_dict['video_embed'])
                        
                    trx_text = self.TR.get_transcript_text()
                    lo_ta = ipw.Layout(display='flex',
                                       flex_flow='column',
                                       width='100%', height='500px')
                    self.editarea = ipw.Textarea(value=trx_text,
                                                 layout=lo_ta)
                    self.page.children += (AV,)
                    self.page.children += (self.editarea,)

                self.yr_sel.disable = True
                self.idn_sel.disable = True
                
                b.disabled = True
                print(F"{self.verb.title()} along!")
            except:
                print("Error loading!")
                

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
        
        # output controls first:
        self.info_out = ipw.Output() # == right-sidebar
        
        self.left_sidebar = self.get_left()
        self.center = self.get_center()
        self.left_sidebar.observe(self.menu_selection, 'value')
        
        self.center.observe(self.info_display, 'selected_index')
        self.dl1 = ipw.dlink((self.left_sidebar, 'selected_index'),
                             (self.center, 'selected_index'))

        self.page = ipw.AppLayout(header=self.get_app_hdr(),
                                  left_sidebar=self.left_sidebar,
                                  center=self.center,
                                  right_sidebar=self.info_out,
                                  footer=None,
                                  pane_widths=[1, 5, 1],
                                  pane_heights=[1, 3, 1]
                                  )
        setattr(self.page, 'data_dict', None)


    def get_app_hdr(self):
        style = "text-align:center;padding:5px;background:#c2d3ef;"
        style += "color:#ffffff;font-size:3em;"
        style += "width:100%,height=50%"
        div = F' <div style="{style}">Data Umbrella Event Management</div>'
        hdr_html = FLO.show_du_logo_hdr(as_html=False) + div
        return ipw.HTML(hdr_html)


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
        tabs.children = [ipw.VBox([ipw.Output()]) for k in ks]
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
        """Right side panel: info about selected op."""
        # Here page. needed bc right_sidebar only defined at
        # page (AppLayout) level.
        self.page.right_sidebar.clear_output()
        wgt = change['owner']
        # Link tab selection index with info panel:
        if wgt.selected_index is None:
            t = 3
        else:
            t = wgt.selected_index
        if t > 3:
            return
        event_fn = {0:'ADD', 1:'MODIFY', 2:'EDIT', 3:'INIT'}
        which = FLO.EventFunction[event_fn[t]]
        EF = FLO.DisplaySectionInfo(which)
        info_val = EF.show_section_info()
        if t < 3:
            #self.msg_out(t, F'owner type(wgt): {type(wgt)}')
            self.left_sidebar.selected_index = t
            self.left_sidebar.children[t].children[0].index = None
        with self.page.right_sidebar:
            display(info_val)
   

    def msg_out(self, idx, msg):
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            display(msg)

    
    def validate(self, idx):
        input_form = self.PC.page.children[1]
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            try:
                self.page.data_dict = FLO.validate_form_entries(input_form,
                                                           self.PC.page.user_dict,
                                                           self.PC.TR)
                print('Validated!')
            except:
                print('Validation Error: Fix & Try again.')
                
    
    def save_entry(self, idx):
        self.center.children[idx].children[0].clear_output()
        with self.center.children[idx].children[0]:
            if self.page.data_dict is None:
                print('Validate first!')
                return
            if self.PC.TR is None:
                print('TR object not instanciated.')
                return
            try:
                self.PC.TR.update_dict(self.page.data_dict)
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
            except:
                if idx == 0:
                    msg = 'Save starter transcript: Something went wrong.'
                else:
                    msg = 'Save transcript: Something went wrong.'
                print(msg)


    def save_edit(self, idx):
        """Save edited transcript."""
        self.center.children[idx].children[0].clear_output()
        #TODO: reset/disabled the selection header?
        with self.center.children[idx].children[0]:
            if self.PC.transcriber_txt.value == '?':
                print("'?' is not a good name!")
            try:
                upd = self.PC.initial_status != self.PC.status_sel.value
                upd = upd or (self.PC.initial_transcriber != self.PC.transcriber_txt.value)
                if upd:
                    self.PC.TR.event_dict['status'] = self.PC.status_sel.value
                    self.PC.TR.event_dict['transcriber'] = self.PC.transcriber_txt.value
                    self.PC.TR.update_readme()
                    print('Updated README.')
            except:
                print('Could not update README.')
                return
            try:
                self.PC.TR.save_transcript_md(new_trx=self.PC.editarea.value)
                # disabled = True?
                self.PC.page.children[0].children[1].children[3].children[0].disabled = False
                self.PC.editarea.value = ''
                print('Updated Event file.')
            except:
                print('Could not update Event file.')


    def show_mdfile(self, idx):
        """Add tab for Md file. Here, idx = tab index"""
        # Add 2nd Output for the file:
        if len(self.center.children[idx].children) == 1:
            self.center.children[idx].children += (ipw.Output(),)
        self.center.children[idx].children[1].clear_output()
        self.center.selected_index = idx
        
        if idx == 3:
            with self.center.children[3].children[1]:
                Meta.show_md_file(main_readme)
        else:
            if self.PC.TR is not None:
                yr = self.PC.TR.event_dict['year']
                fname = self.PC.TR.event_dict['transcript_md']
                mdfile = Meta.REPO_PATH.joinpath(yr, fname)
                if mdfile.exists():
                    with self.center.children[4].children[1]:
                        Meta.show_md_file(mdfile, kind='Transcript')
                else:
                    self.msg_out(4, F'File not found: {mdfile}.')
            else:
                self.msg_out(4, 'PageControls.TR object not instanciated.')


    def menu_tog_sel(self, change):
        wgt = change['owner']
        iparent = wgt.parent_idx
        tog_val = wgt.value

        if iparent == 0:
            if tog_val == 'Enter Info':
                self.PC = PageControls(0)
                entry_group = self.PC.page
                # Add 2nd control in tab vbox => input form:
                self.center.children[0].children += (entry_group,)                
            elif tog_val == 'Validate':
                self.validate(iparent)
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
                self.center.children[1].children += (edit_page, )
            elif tog_val == 'Validate':
                self.validate(iparent)
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
                self.center.children[2].children += (edit_page, )
            elif tog_val == 'Save':
                self.save_edit(iparent)
            elif tog_val == 'Show Readme':
                self.show_mdfile(3)
            elif tog_val == 'Show File':
                self.show_mdfile(4)


    def __repr__(self):
        from pprint import pformat
        return pformat(self.__dict__)
