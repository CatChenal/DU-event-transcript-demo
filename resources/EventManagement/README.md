# Data Umbrella Audio_Transcription Project - README

This project's goal is to automate portions of the tasks needed to convert the captions of presentation videos in the Data Umbrella [YouTube channel](X).   
The `pytube` library is used to access the video and its metadata, e.g. audio track(s) and automatically generated captions, which constitute the raw text for the formatted transcripts published by year in the `Transcripts` folder of the [Data Umbrella](https://github.com/data-umbrella) (DU) repo.  
Towards this aim, the audio of the video is save locally so that it can be played, stopped, and restarted at will in a Jupyter notebook during the reviewing of the roughly processed auto-generated video captions.

# Transcription by DU repo contributors

Volunteer transcribers indicate their intention to produce the transcript (in part or in whole) by:
* Placing an issue indicating which presentation they chose. Unprocessed presentation transcripts are indicated in the main [Transcripts README file](https://github.com/data-umbrella/event-transcripts/blob/main/README.md).
* Forking the repo and creating a branch for the presentation identifier.

# Here is a brief 'git contribution' commands workflow (amended from [Astropy's documentation](https://astropy.readthedocs.io/en/latest/development/workflow/development_workflow.html#new-to-git)):

0. If not done:
Fork (copy) a GitHub repository in your GitHub space  
Clone the forked GitHub repository on your local system  

1. git fetch 
>gets the latest Repo version, which you will use as the basis for making your changes.

2. git branch 
>makes a logically separate copy of Repo to keep track of your changes.

3. git checkout -b <aname>
>create a branch for each issue/feature you are working on, e.g. 'transcript_<id>'

4. git status 
>see a list of files that have been modified or created.

5. git add 
>stages files you have changed or created for addition to git.

6. git commit -m "<choose a Status from the Status.Enum, e.g. "Partial (w.i.p.)"?>"
> adds your staged changes to the repository.

7. git push 
>copies the changes you committed to GitHub

* See also this brilliant [DEV.to post on fixing git mistakes](https://dev.to/egghead/illustrated-notes-on-fixing-git-mistakes-1c16).


### The task of the transcriber is to:  
* Provide appropriate headers, e.g. "Introduction [by host name] <time stamp>".  
* Apply appropriate capitalization of words.  
* Add punctuation and paragraph breaks.  
* Provide additional sections relevant to the presentation, e.g. extra references.  
* Update the presentation transcript Markdown file via a pull request (PR).  

# Initial setup of transcript Mardown file by the administrator of the YouTube channel 

This project also streamlines the setup of the presentation transcript Mardown file. Once a video is published, the admins can produce the initial transcript file using the related information, e.g.: url of video, presentation title, presenter(s), year, initial transcript file name. 
The function `setup_transcript_md` uses a Mardown template file with a standard header, which is populated with the pertinent information gathered from the admins interactively. The function also outputs the Mardown string for the table row related to the presentation in case the Transcripts README file has not yet been updated.
----

[more needed, to come]