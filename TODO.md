# TODO.md

## Events table in README.md
[ ] Reason for reindexing events per year?
Q: Is it issue w/df indexing, table update?


## EventMeta.py
[ ] In `TranscriptMeta.parse_md()`: process 'transcriber' data the same way  
 as `presenter` is (to allow multiple editors).


## Documentation
* DEMO.md:
[ ] Add pics to show each of the 3 tabs
[ ] Explain each menu button
* Code
[ ] Implement code docs


## GUI
* 'ADD AN EVENT' tab:
[ ] Add text widget for new `EventMeta.TranscriptMeta.get_video_desc()` 


* 'EDIT A TRANSCRIPT' tab:
[ ] Add better instructions in the tab title:
- current: "Select the Event Year and Id; Select Audio (default) to replay the audio of 
  the video player; (and if need be, update the Editor's name & Editing Status before saving!)."
- new: need to explain 1st thing to do=scan text for recurring typos: the collapsed menu has 
  tools to do global corrections provided some correction file(s) is/are amended.

[ ] Change title to collapsed menu: 
- current: "Globally correct frequently occurring mistakes or improper casing using files (then reprocess)..."
- new: "Do you see many recurring typos? Add your corrections to some clean-up files and reprocess..."

[ ] Add title to widgets, e.g.:
```
#  control.py, line 405?
self.sel_yr = ipw.Select(options=self.yrs, value=None,
                         layout=ipw.Layout(width='55px',
                                           height='90px'))
                                                       
self.sel_yr_title = ipw.HTML('<em>Event Year:</em>')
self.vbx_yr = ipw.VBox([sel_yr_title, self.sel_yr])
```
Q: Will `obs_sel_yr()`, the observe function for sel_yr, still work unchanged?


## DU YouTube Channel video descriptions
* Create audit functions:
[ ] 1. fn1: output video_url and video_desc for all events
[ ] 2. fn2: output video_url and video_desc for all videos in DU channel.
    Output to csv or json. In pd, add column 'update' (bool)
[ ] 3. How different are they?
[ ] Once numbering in readme table is set and video description template is
    agreed, update all channel videos descriptions using file from fn2 where update==True