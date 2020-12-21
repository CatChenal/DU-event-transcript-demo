# DEMO's README!
## Author: Cat Chenal
---
# Purpose:
This **README** documents proposed changes to the [data-umbrella/event-transcripts](https://github.com/data-umbrella/event-transcripts) Repo (downloaded 11/14/2020), in order to enabled the semi-automation of two workflows depending on the user's task/role, i.e. either as an Administrator or as a Contributor.  
 
The code enabling this resides in the 'EventManagement' project folder, which has been added to the existing 'resources' folder. My approach was to split the events management in two main taks: 
* First, the setup of a new event in the README table (new row) along with the creation of the initial transcript Markdown file in the related year folder by an Administrator.
* Second, the _editing_ of the pre-processed video captions by a Contributor. As this steps takes care of the transcription itself &mdash;by clean up the auto-generated captions as much as possible&mdash; a Contributor's task becomes that of an Editor.

# Modifications needed for this implementation

| Step | Modification | Applies to | Reasons | Benefits |
| ---  | ---          | ---        | ---     | ---      |
| 1    | add the `EventManagement` project to `/.resources` | Repo | functionality | "automate the boring stuff" |
| 2    | add a gitignore in repo (filter out .mp4 files, among other) | Repo |best practice | avoid clutter, size limits; mp4 stay local |
| 3    | replace 'N/A' with 'N.A.' |  Repo | 'N/A' is 'N over A' (math) | written English |
| 4    | change '? [needs a transcriber]' to '?' | Repo | redundant | Occam's |
| 5    | indicate the start & end of table by a comment line | README | enable the identification of the "main table" (in case another table is added to the file in the future) | table becomes a pd.df, which is used for updating |
| 6    | split the comments from the Status & put them into Notes| README table | data standardization | implemented as an Enum, Status could be the trigger for e.g. a Github Action if it is changed to PARTIAL_HELP = "Partial (new editor requested)"|
| 7    | add a paragraph under the table to urge (plead?) contributors to only use the project for editing | it's better | maintain consistency }
| _x_  | move the Notes column at the end | README table | mostly empty column at end | esthetics | 


# Decisions to make related to the implementation

<strong>Note:</strong><br>
The added advantage of using a template is to prevent information from a different event transcript file to appear in a new one as a result of a 'cut & paste' operation when that info has escaped the editor's attention. For example, this is the case in `./2020/17-carol-python.md`:
* Presentation title: 'Contributing to Core Python'
* Video thumbnail `alt`: "Data Science and Machine Learning at Scale"
* Video link is missing thumbnail: the template would automatically create one!  
Additionally it helps prevent inconsistencies, e.g. in the README table, for the transcript '06', the Transcriber is listed as "Reshama / Mark" (which should be changed to "Reshama, Mark"), but in the transcript file, "Mark" is missing.


## Template fields (keys) and their order
As this automation project makes use of jinja templates (with an additional jinja-markdown extension), the 'starter transcript' Markdown file has been turned into a template with the most common entries under the 'Key Links' header turned into keys. Hence, the template (./resources/EventManagement/templates/transcript_header.md) has to be reviewed. 

##### The 'Key Links' portion of the header in the template are:  
```
- Transcript:  https://github.com/data-umbrella/event-transcripts/blob/main/{{year}}/{{transcript_md}}  
- Meetup Event:  {{meetup_url}}  
- Video:  https://youtu.be/{{yt_video_id}}  
- Slides:  {{slides_url}}  
- GitHub repo:  {{repo_url}}  
- Jupyter Notebook:  {{notebook_url}}  
- Transcriber:  {{transcriber}}  
{{extra_references}}
```
The `extra_references` contains any other pair (list heading, value), not in the main ones defined under the 'Key Link' H2 header.


## Status Enum class
The 'transcription' Status has been standardized via the following Enum class:
```
class TrStatus(Enum):
    NOREC = "Not recorded"                            # for 'legacy' events or new, non-recorded events
    TODO = "Not yet processed (editor needed)"        # for inital setup of the 'starter transcript'
    PARTIAL_WIP = "Partial (w.i.p.)"                  # to indicate a partial update by Contributor
    PARTIAL_HELP = "Partial (new editor requested)"   # to indicate Contributor will not complete the editing
    REVIEW = "Needs reviewer"                         # to indicate the editing needs final approval
    COMPLETE = "Complete"                             # to indicate the contribution is acceptable
```

## Transcript chunking and formatting
The automated transcription implemented in EventTranscription.py is designed to prevent the following issues seen in the current transcript files (even the 'Complete' ones), all of which could render the editing task overwhelming:
1. Too short lines (as in the auto-generated captions <= 50 characters)
2. Too wide lines
3. No or too long paragraphs  

To this end, two parameters are used:  
* A `minute_mark`: it is set with a default of 8 (as per my experimentation, 10 minutes can lead to still too long paragraphs: people talk a lot in 10 minutes!), and is currently changeable by the user.
* A `wrap_width`: set with a default of 90 and is also changeable by the user.
##### To be decided:
Whether to keep the `wrap_width` changeable by the user.

## Other considerations

### Completeness:  
The number of transcript files was small enough for me to check each one of them. It appears to me that there is a need for a definition of completeness as many of the files flagged with 'Complete' do not comply with basic publishing standard (e.g. no capitalization or punctuation, too short/wide line width, etc.). This is to keep the __reader__ as end-user in mind: reading should not be a dreadful experience!  
While the pre-processing of the initial transcript will remedy many of these shortcomings (if used consistently), there ought to be a minimal number of criteria met before marking a contribution complete.  

### People's names:
In my opinion, anyone related to an event (presenter(s), transcriber(s), reviwer(s)), should be listed with their full names (First, Last).

### Automated review/re-processing:
Upon incorporation of this project, the existing files could be re-processed in order to apply agreed standardization and/or to provide an audit about which file is problematic. See TODO at bottom.

# Demo Documentation overview (partial, W.I.P.)

## New folder structure (with parial file listing):  
```
.
|   .gitignore
|   CODE_OF_CONDUCT.md
|   CONTRIBUTING.md
|   README.md
|   README_original.md
|   
+---.github
|       
+---2020
|   |   03-ty-shaikh-webscraping.md
|   |   [...]
|   |   17-carol-python.md   [last file as per 11-14-2020 Repo copy used in Demo]
|   |       
|   +---images
|   |   |   1280px-Scikit_learn_logo_small.svg.png
|   |   |   [...]
|   |   |   sklearn_video3.png
|   |   |   
|   |   \---emily_robinson_career
|   |           erc_main.png
|   |           [...]
|   |           erc_s9.png
|   |           
|   \---meta [NEW: contains data dict (json) for starter transcript creation,   
|                  transcript editing and main table update;  
|                  format: transcript str(id).json]
|       |   03_prev.json
|               
+---images
|       .keep
|       full_logo_transparent.png
|       
\---resources
    |   plotly-code.ipynb
    |       
    \---EventManagement [NEW]
        |   README.md [INSTRUCTIONS: which file to use, reqs, etc]
        |   requirements.txt [not finalized]
        |       
        +---data
        |   |   12_dqab-FcAirA.mp4
        |   |   12_dqab-FcAirA.xml
        |   |   
        |   +---backup [to save readme before changes]
        |   |       README_original.md.bkp
        |   |       
        |   \---documentation
        |           topdir_tree.txt
        |           flowchart_examples.txt
        |           
        +---images [mostly for documentation]
        |       
        +---manage
        |   |   EventMeta.py
        |   |   EventTranscription.py
        |   |   Utils.py
        |   |   Workflow.py [not yet functional; Panel dashboard app]
        |   |       
        |   +---Documentation
        |   |       gviz.py
        |   |       port.graphml
        |           
        +---notebooks
        |   |   Documentation.ipynb
        |   |   Implementation.ipynb
        |   |   Workflow.ipynb
        |               
        \---templates [jinja-markdown template, 
                       default str replacements dicts (json)]
            |   transcript_header.md
```

# Workflow 'equations':
## Administrator:
```
   (1) Metadata (created if none exists) 
 + (2) transcript_header.md
=> (3.1) transcript.md;
   (3.2) README update}
```
## Contributor:
```
   (1) Metadata
 + (2) transcript.md
=> (3.1) new transcript.md;
   (3.2) README update}
```

# TODO:
[ ] Create a Panel dashbord with two tabs: "Add Event" | "Edit Transcript"
[ ] Add flowcharts to documentation: if done properly, one picture could explain each task workflow.
[ ] To be decided: re-process all transcript Markdown files to:
- 1. save the metadata
- 2. standardize names/flags
- 3. flag inconsistencies