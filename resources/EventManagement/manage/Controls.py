# -*- coding: utf-8 -*-
# Controls.py
# test for using a class to populate AppLayout.center Tabs wgt.

from typing import (List, Dict, Tuple, Sequence, 
                    NewType, Callable, TypeVar, 
                    Generic, Iterable, Union)

from enum import Enum
from functools import partial
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
        if page_idx not in [0, 1,2]:
            msg = "The page_idx refers to the App.center "
            msg += "tab index for 'ADD', MODIFY' or 'EDIT',"
            msg += " hence only one of [0,1,2] is valid."
            raise ValueError (msg)
            
        lo_page = ipw.Layout(display='flex',
                             flex_flow='column',
                             align_items='stretch',
                             margin='0px 0px 0px 30px')
        self.page_idx = page_idx
        
        df, empty_last_row, delims = Meta.df_from_readme_tbl()
        self.df = df
        self.yrs = df[2:].year.unique().tolist()
        self.idns = df[2:].N.sort_values(ascending=False).values.tolist()
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
            self.page = ipw.VBox(children=(),
                                 layout=lo_page)
            self.page.children += (self.get_sel_banner(),)
            self.page.children += (entry_group,)
            setattr(self.page, 'user_dict', user_dict)
        else:
            self.initial_transcriber = None
            self.initial_status = None
            
            # output wgts 1st:
            self.idn_sel_out = ipw.Output()
            self.load_btn_out = ipw.Output()

            self.yr_sel = ipw.Select(options=self.yrs,
                                     layout=ipw.Layout(width='50px'))
            self.idn_sel = ipw.Select(options=self.idns, value=None,
                                      layout=ipw.Layout(width='60px'))
            self.idn_sel.observe(self.sel_change, 'value')
            self.btn_load = ipw.Button(description='LOAD', button_style='info',
                                       disabled=True)
            self.btn_load.on_click(self.load_btn_click)
        
            if self.page_idx == 2:
                self.verb = 'edit'
                # set by get_selection_hdr()
                self.editarea = None
                self.av_radio = ipw.RadioButtons(options=['Audio','Video'],
                                                 value='Audio')
                self.transcriber_txt = ipw.Text(value=None)
                self.status_opts = status_opts
                self.status_sel = ipw.Select(options=status_opts, value=None,
                                             disabled=True)
            else:
                self.verb = 'modify'

            # start the page with the selection controls only:
            self.page = ipw.VBox(children=(),
                                 layout=lo_page)
            with self.idn_sel_out:
                print('< year / file >')
            self.page.children = (self.get_selection_hdr(),)
            # set by load_btn_click:
            setattr(self.page, 'user_dict', None)
        
        
    def get_sel_banner(self):
        if self.page_idx == 0:
            sel_banner = '<H3>Provide the Event related data.</H3>'
        elif self.page_idx == 1:
            sel_banner = '<H3>Select the Event Year and Id.</H3>'
        else:
            sel_banner = '<H3>Select the Event Year, Id, AV player (and if need be, '
            sel_banner += 'update the Transcriber & the Status before saving!).</H3>'
        return ipw.HTML(value=sel_banner)
    
    
    def get_selection_hdr(self):
        lo_btn_vbx = ipw.Layout(flex_flow='column',
                                justify_content='flex-end') 
        lo_sel_hbx = ipw.Layout(margin='0px 0px 0px 30px')
        
        if self.page_idx == 1:
            yr_idn_hbx = ipw.HBox([self.yr_sel, self.idn_sel,
                                   self.idn_sel_out])
            sel_hbox = ipw.VBox([self.get_sel_banner(),
                                 ipw.HBox([yr_idn_hbx,
                                           ipw.VBox([self.btn_load,
                                                     self.load_btn_out],
                                                    layout=lo_btn_vbx)
                                          ])
                                ], layout=lo_sel_hbx)
        else:
            yr_idn_hbx = ipw.HBox([self.yr_sel, self.idn_sel])
            av_idout_trx_vbx = ipw.VBox([ipw.HBox([self.av_radio]),
                                         self.idn_sel_out,
                                         self.transcriber_txt
                                        ])
            sel_hbox = ipw.VBox([self.get_sel_banner(),
                                 ipw.HBox([yr_idn_hbx,
                                           av_idout_trx_vbx,
                                           self.status_sel,
                                           ipw.VBox([self.btn_load,
                                                     self.load_btn_out],
                                                    layout=lo_btn_vbx)
                                          ])
                                ], layout=lo_sel_hbx)
        return sel_hbox


    def sel_change(self, change):
        """
        TODO
        
        need to populate self.idn_sel according to self.yr_sel.value
        """
        self.idn_sel_out.clear_output()
        with self.idn_sel_out:
            if (self.yr_sel.value is not None 
                and self.idn_sel.value is not None):
                msk = (self.df.year==self.yr_sel.value)
                msk = msk & (self.df.N==self.idn_sel.value)
                fname = self.df.loc[msk].name.values[0]
                if self.page_idx == 2:
                    self.transcriber_txt.value = self.df.loc[msk].Transcriber.values[0]
                    self.initial_transcriber = self.transcriber_txt.value
                self.btn_load.disabled = False
                print(self.yr_sel.value + ' / '+ fname)
                
                
    def load_btn_click(self,b):
        if self.page_idx == 0:
            return
        self.load_btn_out.clear_output()
        with self.load_btn_out:
            try:
                self.TR = Meta.TranscriptMeta(self.idn_sel.value,
                                              self.yr_sel.value)
                if self.page_idx == 1:
                    exposed = FLO.load_entry_dict(self.TR)   
                    entry_form = FLO.get_entry_accordion(exposed)                
                    self.page.children += (entry_form,)
                    self.page.user_dict = exposed
                else:       
                    self.status_sel.disabled = False
                    status = self.TR.event_dict['status']
                    if status in self.status_opts:
                        self.status_sel.value = status 
                    else:
                        self.status_sel.value = self.status_opts[-1]
                    self.initial_status = status
                    
                    # reset default if no audio:    
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
    def __init__(self, app_components_dict):
        self.TR = None
        
        # output wgts 1st:
        self.validate_out = ipw.Output()

        #justify_content='space-between'
    pass

