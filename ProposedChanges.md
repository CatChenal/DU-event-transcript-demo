# DEMO Project's Implementation specifications
## Author: Cat Chenal
---
# Genesis:
I wanted to contribute to Data Umbrella's events transcription, so I looked into the YouTube video metadata (using `pytube`) to download the auto-generated captions as a starter text. As this still required too much cleaning, I modified `pytube`'s xml-to-text processing function to obtain a more decent one... Then, I had to share!

# Purpose:
This file details the proposed changes to the [data-umbrella/event-transcripts](https://github.com/data-umbrella/event-transcripts) Repo in order to enabled the semi-automation of two workflows depending on the user's task/role, i.e. add an event or edit an event starter transcript.

# Code:
The code enabling this resides in the 'EventManagement' project folder, which has been added to the existing 'resources' folder. My approach was to split the events management in two main taks:  
* First, the setup of a new event in the README table (new row) along with the creation of the event's Markdown file in the related year folder by an Admin (i.e. someone using the Admin-related functions). This file, referred to as the 'starter transcript', now includes an initial transcript text, which results from the processing of the video captions. 
* Second, the _editing_ of the transcript text by a Contributor. Hence, the formerly 'Transcriber', now is an Editor.  

# Modifications needed for this implementation

| Step | Modification | Applies to | Reasons | Benefits |
| ---  | ---          | ---        | ---     | ---      |
| 1    | Add the `EventManagement` project to `/.resources` | Repo | Functionality | _"Automate the boring stuff"_ |
| 2    | Add a `.gitignore` in repo (prepped to filter out .mp4 files if needed) | Repo | Best practice | Avoid clutter, size limits; mp4 stay local |
| 3    | **Perform global normalization:** |  Repo | Consistency | Quality control, automation | 
| 3.1  | Replace 'N/A' with 'N.A.' |  Repo | 'N/A' is 'N over A' (math) | Written English |
| 3.2  | Change '? [needs a transcriber]' to '?' | Repo | Redundant | Occam's |
| 3.3  | Remove self-referencing link ("- Transcript") | Event md files | Redundant | Occam's |
| 3.4  | Correct sources of UnicodeDecodeError | Event md files | ipython.display.Markdown cannot load it | To render file within nb |
| 3.4  | Add list headings, amend duplicates | Event md files | To enable correct parsing, e.g. a second "- Video" would overwrite the 1st | Parsing |
| 3.5  | Apply unique file naming pattern | Repo | Automated naming | Consistent naming, e.g.: 17-carol-python.md -> 17-carol-willing-python.md |
| 4    | Split the comments from the Status & put them into Notes| README table | Data, commit message standardization | Implemented as an Enum, Status could be the trigger for e.g. a GitHub Action if it is changed to PARTIAL_HELP = "Partial (new editor requested)" |
| 5    | Move the Note column at the end as 'Notes' | README table | Mostly empty column at end | Esthetics | 
| 6    | Add a paragraph under the table to urge (plead?) contributors to only use the project for editing | README | It's better | Maintain consistency |
| FUTURE | **These changes are recommended:** (not implemented in the demo) ||||
| 1 | Replace the video href link (under '## Video') with an embed HTML string | Event md files | Readers can watch while reading | Especially good for reviewers (currently used in the GUI for the Editing task) |
| 2 | Change 'Transcriber' to 'Editor'    | Repo |||
| 3 | Add a column for Reviewer | README table | Assign credit | Encourage contribution? | 
| 4 | Drop 'Meetup' from list header '- Meetup Event' | Event md files | May not be from Meetup | More generic |  


### The file `README.md` reflects the changes associated with the README modifications above listed.
### The events Markdown files in the 2020 folder have been 'header-normalized' to enable a templated approach to document generation. (A good example for this normalization is Event "05".)

<strong>Note:</strong><br>
The added advantage of using a template is to prevent information from a different event transcript file to appear in a new one as a result of a 'cut & paste' operation when that info has escaped the editor's attention. For example, this is the case in `./2020/17-carol-python.md`:
* Presentation title: 'Contributing to Core Python'
* Video thumbnail `alt`: "Data Science and Machine Learning at Scale"
* Video link is missing thumbnail: the template would automatically create one!  
Additionally:   
* It helps prevent inconsistencies, e.g. in the README table, for the transcript '06', the Transcriber is listed as "Reshama / Mark" (which should be changed to "Reshama Shaikh, Mark"), but in the transcript file, "Mark" is missing.
* It makes the editing task easier, thus fostering greater/better contributing, which is the main claim of this project!


## Template fields (keys) and their order
Note: An initial implementation of this automation project made use of `jinja` templates (with an additional `jinja-markdown` extension and `pypandoc`), but the "markdown" converted text by pandoc still required processing for output in standard Markdown.  Instead, the current project uses a string for the 'starter transcript' Markdown file header, which is preset with dict keys so that it can be used with the usual string_format function. This (string) template lists the most common entries under the 'Key Links' header.  
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
* Choice of order: event-related ('Meetup' to 'Slides'), code-related (repo, then notebook), transcriber(s)-related, then any other.  

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
##### To be decided:  Whether to keep the `wrap_width` changeable by the user.

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
|   ProposedChanges.md     [This file]
|   README.md              [The modified data-umbrella/event-transcripts/README.md]
|   
+---.github
|       
+---2020                   [Event files (normalized)]
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
        |   |           
        |   \---meta [NEW: - mp4 audio files (currently excluded from upload by .gitignore)   
        |                  - xml caption files
        |                  - starter transcript text files]
        |   |   
        |   +---backup [To save readme before changes]
        |   |       README.md.bkp
        |   |       
        |   \---documentation [Not finalized.]
        |
        |   [Files for text clean up:]
        |   corrections.csv  [for corrections & special formatting, e.g. whatsapp->WhatsApp]
        |   title_names.csv  [for titlecasing, company names, products]
        |   title_people.csv [for titlecasing]
        |   title_places.csv [for titlecasing]
        |   upper_terms.csv  [for uppercasing, mostly acronyms]
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
        |   |   Implementation_Details.ipynb [Details about workflow & functions.]
        |   |   WorkflowGUI.ipynb [Temp. Code to build ipywidgets GUI.]

```
# Comparison of an existing ('normalized') event file with what would be the starter file produced by `EventManagement`.
### Files: ./Existing_event_file.md, ./New_event_file.md    
   
# TODO:
[ ] Finish GUI  
[ ] More testing  
[ ] Add flowcharts to documentation: if done properly, one picture could explain each task workflow.  
