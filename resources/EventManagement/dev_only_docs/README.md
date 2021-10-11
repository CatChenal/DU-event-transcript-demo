# DEMO Project's Implementation specifications (Python 3.7)
## Author: Cat Chenal
---
---
# SUMMARY: The new EventManagement resource produces timed-paragraphed starter transcripts for Data Umbrella's Events and greatly enhances the Event Creation or Transcript Editing processes via its notebook-based GUI.  

## Environment: 
- Jupyter Lab. [(Installation details)](https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html)  
 -- Limitation with the classic notebook:  
The ipywidgets-based GUI is functional in a Jupyter notebook but will not be optimal as the notebook has a fixed width, which degrades the flexibility afforded by the GUI's EDIT page.
- Browser: Chrome  
No other browser was tested, but the project is 'browser agnostic'. The GUI's EDIT processes will however greatly benefit from a [Grammarly browser extension](https://www.grammarly.com), which will highlight the starter transcript's quirks.
---
---

# Genesis:
I wanted to contribute to Data Umbrella's events transcription, so I looked into the YouTube video metadata (using `pytube`) to download the auto-generated captions as a starter text. As this formatted text still required too much cleaning, I modified `pytube`'s xml-to-text processing function to obtain a more decent one... Then, I had to share!


# Purpose:
This file details the proposed changes to the [data-umbrella/event-transcripts](https://github.com/data-umbrella/event-transcripts) Repo in order to enabled the semi-automation of two main workflows depending on the user's task/role, i.e. add an event or edit an event starter transcript.

# Code:
The code enabling this resides in the 'EventManagement' project folder, which has been added to the existing 'resources' folder. My approach was to split the events management in two main taks:  
* First, the setup of a new event in the README table (new row) along with the creation of the event's Markdown file in the related year folder by an Admin (i.e. someone using the Admin-related functions). This file, referred to as the 'starter transcript', now includes an initial transcript text, which results from the processing of the video captions. 
* Second, the _editing_ of the transcript text by a Contributor. Hence, formerly a Transcriber, the Contributor is now an Editor.  

# Modifications needed for this implementation

| Step | Modification | Applies to | Reasons | Benefits |
| ---  | ---          | ---        | ---     | ---      |
| 1    | Add the `EventManagement` project to `/.resources` | Repo | Functionality | _"Automate the boring stuff"_ |
| 2    | Add a `.gitignore` in repo (prepped to filter out .mp4 files if needed) | Repo | Best practice | Avoid clutter, size limits; mp4 stay local |
| 3    | Move the Note column at the end as 'Notes' | README table | Mostly empty column at end | Esthetics | 
| 4    | Split the comments from the Status & put them into Notes| README table | Data, commit message standardization | Implemented as an Enum, Status could be the trigger for e.g. a GitHub Action if it is changed to PARTIAL_HELP = "Partial (new editor requested)" |
| 5    | **Perform global normalization:** |  Repo | Consistency | Quality control, automation | 
| 5.1  | Replace 'N/A' with 'N.A.' |  Repo | 'N/A' is 'N over A' (math) | Written English |
| 5.2  | Change '? [needs a transcriber]' to '?' | Repo | Redundant | Notes and Status have that information |
| 5.3  | Remove self-referencing link ("- Transcript") | Event md files | Redundant | Simplify |
| 5.4  | Correct sources of UnicodeDecodeError | Event md files | ipython.display.Markdown cannot load it | To render file within nb |
| 5.4  | Add list headings, amend duplicates | Event md files | To enable correct parsing, e.g. a second "- Video" would overwrite the 1st | Parsing |
| 5.5  | Apply unique file naming pattern | Repo | Automated naming | Consistent naming, e.g.: 17-carol-python.md -> 17-carol-willing-python.md |
| 6    | Add a paragraph under the table to urge (plead?) contributors to only use the project for editing | README | It's better | Maintain consistency |
| 7    | Add a note about non-Unicode characters in Markdown file. | README | Error | Correct parsing | 
| .    | . | . | . | .|
| **FUTURE** | **Recommended changes:** (not implemented in this demo) ||||
| F1 | Replace the video href link (under '## Video') with an embed HTML string | Event md files | Readers can watch while reading | Especially good for reviewers (currently used in the GUI-Editing task as Media choice: Audio or Video) |
| F2 | Change 'Transcriber' to 'Editor' | Repo | Most of the transcripts need editing ||
| F3 | Add a column for Reviewer | README table | Assign credit | Encourage contribution? | 
| F4 | Change '- Meetup Event' to the more generic '- Venue' list header| Event md files | More generic | There are alternatives to Meetup (e.g. https://meetingplace.io/, https://colloq.io/)|
| F5 | Add a 'Year' column | README table | Explain why event '01' follows event '20' | Explicitly indicate folder location (Numbering in demo is reset in year folder) |
| F5'| Amend the file links to reveal path| README | E.g.: [2021/21: Command Line Focused Dev](2021/21-nick-command.md) | Alternative to F5. |


### The demo `README.md` reflects the changes associated with the README modifications above listed.
### The events Markdown files in the year folders have been 'header-normalized' to enable a templated approach to document generation. (A good example for this normalization is Event "05".)

<strong>Note:</strong><br>
The added advantage of using a template is to prevent information from a different event transcript file to appear in a new one as a result of a 'cut & paste' operation when that info has escaped the editor's attention. For example, this was the case in `./2020/17-carol-python.md`:
* Presentation title: 'Contributing to Core Python'
* Video thumbnail `alt`: "Data Science and Machine Learning at Scale"
* Video link is missing thumbnail: the template would automatically create one!  
Additionally:   
* It helps prevent inconsistencies, e.g. in the README table, for the transcript '06', the Transcriber is listed as "Reshama / Mark" (which should be changed to "Reshama Shaikh, Mark <last?>"), but in the transcript file, "Mark" is missing.
* It makes the editing task easier, thus fostering greater/better contributing, which is the main claim of this project!


## Template fields (keys) and their order
The current project uses a string for the 'starter transcript' Markdown file header, which is preset with dict keys so that it can be used with the usual string_format function. This (string) template lists the most common entries under the 'Key Links' header.  The field `extra_references` enables the addition of custom 'header' information.  
Template definition in ./resources/EventManagement/manage/EventMeta.py:  
```
HDR_TPL = """# {presenter}: {title}  

## Key Links  
- Meetup Event:  {event_url}  
- Video:  https://youtu.be/{yt_video_id}  
- Slides:  {slides_url}  
- GitHub Repo:  {repo_url}  
- Jupyter Notebook:  {notebook_url}  
- Transcriber:  {transcriber}  
{extra_references}  

## Video
<a href="{video_href}" target="_blank">
    <img src="{video_href_src}" 
         alt="{video_href_alt}"
         width="{video_href_w}"/>
</a>

## Transcript  
{formatted_transcript}  
"""
```
 
#### Nomenclature note
A "H1-header" is a line starting with '# ', and a "H2-header" is one starting with '## " in Markdown. I call "H2-header list header" the portion of the listed items under a H2-header that follows the list marker ("- ") and preceeds the colon (":"). For example, "Jupyter Notebook" is one of the list headers of the "Key Links" H2-header.

The transcript files have a common header (referred to as the "transcript file header"), consisting of the following fields in this order:  
1. First (and unique) H1-header: "# {presenter}: {title}"
2. Followed by three H2-headers:  
  2.1 "## Key Links"  
  2.2 "## Video"  
  2.3 "## Transcript"  
    
#### The 'Key Links' H2-header _lists_ resources that appear in ALL current transcript files:  
* Note: The common list headers must match these (part of the 'header-normalization' for existing transcripts).  
``` 
- Meetup Event:  {event_url}  
- Video:  https://youtu.be/{yt_video_id}  
- Slides:  {slides_url}  
- GitHub Repo:  {repo_url}  
- Jupyter Notebook:  {notebook_url}  
- Transcriber:  {transcriber} 
{extra_references}
```
* The `extra_references` contains any other pair (list heading, value), not in the main ones defined under the 'Key Links' H2 header. For example, this is where "- Binder: <url>" would be defined.  
* Choice of order: 1st: event-related ('Meetup' to 'Slides'), 2nd: code-related (repo, then notebook), 3rd: transcriber(s)-related, then any other.  

## Status Enum class
The 'transcription' Status has been standardized via the following Enum class:
```
class TrStatus(Enum):
    NOREC = "Not recorded"                          # for 'legacy' events or new, non-recorded events
    TODO = "Not yet processed (editor needed)"      # for inital setup of the 'starter transcript'
    PARTIAL_WIP = "Partial (w.i.p.)"                # indicates a partial update by Contributor
    PARTIAL_HELP = "Partial (new editor requested)" # indicates Contributor will not complete the editing
    REVIEW = "Needs reviewer"                       # indicates the editing needs final approval
    COMPLETE = "Complete"                           # indicates the contribution is acceptable
```

## Transcript chunking and formatting
The automated transcription implemented in EventTranscription.py is designed to prevent the following issues seen in the current transcript files (even the 'Complete' ones), all of which could render the editing task overwhelming:
1. Too short lines (as in the auto-generated captions, 50 characters max)  
2. Too wide lines  
3. No or too long paragraphs  

To this end, two parameters are used:  
* `minutes_mark`: it is set with a default of 4 (as per my experimentation, 10 minutes can lead to still too long paragraphs: people talk a lot in 10 minutes!).
* `wrap_width`: set with a default of 120.  
##### To be decided:  Whether to keep the `wrap_width` changeable by the user.

# Other considerations

## Completeness:  
The number of transcript files was small enough for me to check each one of them. It appears to me that there is a need for a definition of completeness as many of the files flagged with 'Complete' do not comply with basic publishing standard (e.g. no capitalization or punctuation, too short/wide line width, etc.). This is to keep the __reader__ as end-user in mind: reading should not be a dreadful experience!  
While the pre-processing of the initial transcript will remedy many of these shortcomings (if used consistently), there ought to be a minimal number of criteria met before marking a contribution complete.  

## People's names:
* Full names: In my opinion, anyone related to an event (presenter(s), transcriber(s), reviewer(s)), should be listed with their full names (First, Last).  
* Add 'new' roles: Add a 'Host' and a 'Reviewer' keys: to show credit when credit is due? (+ add them in the table.)   
* Change 'Transcriber' to 'Editor'.  

## Event numbering (Re: F5 in Modifications table):
The implementation predates any 2021 events: the demo restart numbering at 01 in any new year. With the addition of the first new event of 2021, actually 'event 21', this may have to change.  

## Demo Documentation overview (W.I.P.)

## New folder structure (with partial file listing):  
```
.
|   .gitignore           [Added]
|   CODE_OF_CONDUCT.md
|   CONTRIBUTING.md
|   DEMO.md
|   environent.yml
|   LICENSE
|   README.md            [The modified data-umbrella/event-transcripts/README.md]
|   requirements.txt
|   TODO.md
|   
+---.git
|       
+---2020                   [Year folders for Event files (normalized)]
|   |   03-ty-shaikh-webscraping.md
|   |   [...]
|   |   17-carol-python.md
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
+---2021
|               
+---images
|       .keep      [? Keep local by including it in .gitignore]
|       full_logo_transparent.png
|       
\---resources
    |   plotly-code.ipynb
    |       
    \---EventManagement	[NEW]
        |   README.md
        |       
        +---data
        |   |           
        |   \---meta [- mp4 audio files (stay local: excluded from upload by .gitignore)   
        |             - xml caption files
        |             - starter transcript text files]
        |   |   
        |   +---backup [To save readme before changes]
        |   |       README.md.bkp
        |   |       
        |   \---documentation [Not finalized]
        |
        |   [Files for text clean up:]
        |   corrections.csv  [for corrections & special formatting, e.g. whatsapp->WhatsApp]
        |   title_names.csv  [for titlecasing, company names, products]
        |   title_people.csv [for titlecasing]
        |   title_places.csv [for titlecasing]
        |   upper_terms.csv  [for uppercasing, mostly acronyms]
        |
        +---dev_only_docs 
        |   |   Existing_event_file.md	
        |   |   New_event_file.md
        |   |   README.md	[This file]	
        |          
        +---images	[Mostly for documentation]
        |   Edit_page.png
        |      
        +---manage	[Project's souce code]
        |   |   Audit.py
        |   |   Controls.py
        |   |   EventMeta.py
        |   |   EventTranscription.py
        |   |   Utils.py
        |           
        +---notebooks
        |   |   Audits_Tests.ipynb  
        |   |   How_Tos.ipynb   [Details on amending text processing files & re-processing of initial transcript]
        |   |   ManageGUI.ipynb [The project "GUI in a notebook"]

```
# Comparison of an existing ('normalized') event file with what would be the starter file produced by `EventManagement`.

### Files in /EventManagement/dev_only_docs/: Existing_event_file.md, New_event_file.md    
