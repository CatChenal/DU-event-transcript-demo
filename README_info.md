# DEMO Project's README!
## Author: Cat Chenal
---
# Genesis:
I wanted to contribute to Data Umbrella's events transcription, so I looked into the YouTube video metadata (using `pytube`) to download the auto-generated captions as a starter text. As this still required too much cleaning, I modified `pytube`'s xml-to-text processing function to obtain a more decent one... Then, I had to share!

# Purpose:
This **README** documents proposed changes to the [data-umbrella/event-transcripts](https://github.com/data-umbrella/event-transcripts) Repo (downloaded 11/14/2020), in order to enabled the semi-automation of two workflows depending on the user's task/role, i.e. either as an Administrator (Admin) or as a contributing Editor.  

# Code:
The code enabling this resides in the 'EventManagement' project folder, which has been added to the existing 'resources' folder. My approach was to split the events management in two main taks:  
* First, the setup of a new event in the README table (new row) along with the creation of the initial transcript Markdown file in the related year folder by an Admin (i.e. someone using the Admin-related functions).  
* Second, the _editing_ of the pre-processed video captions by a Contributor. As this steps takes care of the transcription itself &mdash;by clean up the auto-generated captions as much as possible&mdash; the formerly 'Transcriber', now is an Editor.  

# Modifications needed for this implementation

| Step | Modification | Applies to | Reasons | Benefits |
| ---  | ---          | ---        | ---     | ---      |
| 1    | add the `EventManagement` project to `/.resources` | Repo | functionality | "automate the boring stuff" |
| 2    | add a `.gitignore` in repo (filter out .mp4 files, among other) | Repo |best practice | avoid clutter, size limits; mp4 stay local |
| 3    | replace 'N/A' with 'N.A.' |  Repo | 'N/A' is 'N over A' (math) | written English |
| 4    | change '? [needs a transcriber]' to '?' | Repo | redundant | Occam's |
| 5    | indicate the start & end of table by a comment line | README | enable the identification of the "main table" (in case another table is added to the file in the future) | table becomes a pd.df, which is used for updating |
| 6    | split the comments from the Status & put them into Notes| README table | data standardization | implemented as an Enum, Status could be the trigger for e.g. a GitHub Action if it is changed to PARTIAL_HELP = "Partial (new editor requested)"|
| 7    | add a paragraph under the table to urge (plead?) contributors to only use the project for editing | it's better | maintain consistency |
| _x_  | move the Notes column at the end | README table | mostly empty column at end | esthetics | 

### The file `README_new.md` reflects the changes associated with the README modifications above listed.
### The transcripts Markdown files in the 2020 folder have been 'header-normalized' to enable a templated approach to document generation. (A good example for this normalization is Event "05".)

# Decisions to make related to the implementation

<strong>Note:</strong><br>
The added advantage of using a template is to prevent information from a different event transcript file to appear in a new one as a result of a 'cut & paste' operation when that info has escaped the editor's attention. For example, this is the case in `./2020/17-carol-python.md`:
* Presentation title: 'Contributing to Core Python'
* Video thumbnail `alt`: "Data Science and Machine Learning at Scale"
* Video link is missing thumbnail: the template would automatically create one!  
Additionally:   
* It helps prevent inconsistencies, e.g. in the README table, for the transcript '06', the Transcriber is listed as "Reshama / Mark" (which should be changed to "Reshama Shaikh, Mark"), but in the transcript file, "Mark" is missing.
* It makes the editing task easier, thus fostering greater/better contributing, which is the main claim of this project!


## Template fields (keys) and their order
As this automation project makes use of `jinja` templates (with an additional `jinja-markdown` extension), the 'starter transcript' Markdown file has been turned into a template with the most common entries under the 'Key Links' header turned into keys. Hence, the template (./resources/EventManagement/templates/transcript_header.md) has to be reviewed.  

#### Nomenclature note
A "H1-header" is a line starting with '# ', and a "H2-header" is one starting with '## " in Markdown. I call "H2-header list header" the portion of the listed items under a H2-header that follows the list marker ("- ") and preceeds the colon (":"). For example, "Jupyter Notebook" is one of the list headers of the "Key Links" H2-header.

The transcript files have a common header (referred to as the "transcript file header"), consisting of the following fields in this order:  
1. First (and unique) H1-header: "# {{presenter}}: {{title}}"
2. Followed by three H2-headers:  
  2.1 "## Key Links"  
  2.2 "## Video"  
  2.3 "## Transcript"  
    
#### The 'Key Links' H2-header _lists_ resources that are common to all current transcript files:  
* Note: The common list headers must match these (part of the 'header-normalization' for existing transcripts).  

```
- Transcript:  https://github.com/data-umbrella/event-transcripts/blob/main/{{year}}/{{transcript_md}}  
- Meetup Event:  {{meetup_url}}  
- Video:  https://youtu.be/{{yt_video_id}}  
- Slides:  {{slides_url}}  
- GitHub Repo:  {{repo_url}}  
- Jupyter Notebook:  {{notebook_url}}  
- Transcriber:  {{transcriber}} 
{{extra_references}}
```
* The `extra_references` contains any other pair (list heading, value), not in the main ones defined under the 'Key Links' H2 header. For example, this is where "- Binder: <url>" would be defined.  
* Choice of order: event-related ('Transcript' to 'Slides'), code-related (repo, then notebook), transcriber(s)-related, then any other.  


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
1. Too short lines (as in the auto-generated captions, 50 characters max)  
2. Too wide lines  
3. No or too long paragraphs  

To this end, two user parameters are used:  
* A `minutes_mark`: it is set with a default of 4 (as per my experimentation, 10 minutes can lead to still too long paragraphs: people talk a lot in 10 minutes!).
* A `wrap_width`: set with a default of 120.  
##### To be decided:
Whether to keep the `wrap_width` changeable by the user.

## Other considerations

### Completeness:  
The number of transcript files was small enough for me to check each one of them. It appears to me that there is a need for a definition of completeness as many of the files flagged with 'Complete' do not comply with basic publishing standard (e.g. no capitalization or punctuation, too short/wide line width, etc.). This is to keep the __reader__ as end-user in mind: reading should not be a dreadful experience!  
While the pre-processing of the initial transcript will remedy many of these shortcomings (if used consistently), there ought to be a minimal number of criteria met before marking a contribution complete.  

### People's names:
* Full names: In my opinion, anyone related to an event (presenter(s), transcriber(s), reviewer(s)), should be listed with their full names (First, Last).  
* Add 'new' roles: Add a 'Host' and a 'Reviewer' keys: to show credit when credit is due? (+ add them in the table.)   
* Change 'Transcriber' to 'Editor'.  
    
#### Other:
Change 'Meetup Event' to the more generic 'Venue': The main event link may not always come via Meetup, plus, there are alternatives to Meetup (e.g. https://meetingplace.io/, https://colloq.io/).

# Demo Documentation overview (W.I.P.)

## New folder structure (with partial file listing):  
```
.
|   .gitignore                 [Added]
|   CODE_OF_CONDUCT.md
|   CONTRIBUTING.md
|   README_info.md             [This file]
|   README_new.md              [The modified data-umbrella/event-transcripts/README.md]
|   
+---.github
|       
+---2020
|   |   03-ty-shaikh-webscraping.md
|   |   [...]
|   |   17-carol-python.md     [Last file as per 11-14-2020 Repo copy used in Demo]
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
|   \---meta [NEW: contains metadata dict (json) for starter transcript creation,   
|                  transcript editing and main table update;  
|                  format: transcript str(id).json]
|       |   03.json
|               
+---images
|       .keep      [? Keep local by including it in .gitignore]
|       full_logo_transparent.png
|       
\---resources
    |   plotly-code.ipynb
    |       
    \---EventManagement [NEW]
        |   README.md [INSTRUCTIONS: which file to use, reqs, etc]
        |   environment.yml [Not finalized, add requirements.txt]
        |       
        +---data
        |   |   12_dqab-FcAirA.mp4 [mp4 excluded from upload by .gitignore]
        |   |   [...]
                [New files for text clean up:]
        |   |   corrections.json  [for corrections & special formatting, e.g. whatsapp->WhatsApp]
        |   |   title_names.csv   [for titlecasing, company names, products]
        |   |   title_people.csv  [for titlecasing]
        |   |   title_places.csv  [for titlecasing]
        |   |   upper_terms.csv   [for uppercasing, mostly acronyms]
        |   |   
        |   +---backup [To save readme before changes]
        |   |       README_new.md.bkp
        |   |       
        |   \---documentation [Not finalized.]
        |           
        +---images [Mostly for documentation]
        |       
        +---manage
        |   |   EventMeta.py
        |   |   EventTranscription.py
        |   |   Utils.py
        |   |   Workflow.py [W.I.P. UX functions.]
        |   |       
        |   +---documentation [Not finalized. Code for documenting.]
        |           
        +---notebooks
        |   |   Implementation.ipynb [Details about workflow & functions.]
        |   |   Workflow.ipynb [Temp. Code to build ipywidgets GUI.]
        |               
        \---templates [jinja-markdown template]
            |   transcript_header.md
```

# TODO:
[ ] Finish GUI  
[ ] More testing  
[ ] Add flowcharts to documentation: if done properly, one picture could explain each task workflow.  
