<article>
<!-- Part of app that retrieves and processes the auto-generated captions of a YouTube video;
     (Any transcript text pre-existing the app is preserved.)
-->

{% markdown %}

# {{presenter}}: {{title}}
<!-- presenter: full name. If multiple, separate with comma, e.g.: 
       full name 1, full name 2, 
-->

## Key Links
- Transcript:  https://github.com/data-umbrella/event-transcripts/blob/main/{{year}}/{{transcript_md}}  
- Meetup Event:  {{meetup_url}}  
- Video:  https://youtu.be/{{yt_video_id}}  
- Slides:  {{slides_url}}  
- GitHub repo:  {{repo_url}}  
- Jupyter Notebook:  {{notebook_url}}  
- Transcriber:  {{transcriber}}  
{{extra_references}}  

<!-- extra_references: should conform to above entries, i.e. Markdown string, e.g.: 
     """- Binder: <url>
        - Ref1: x  
        - Ref2: y
     """
     See the EventMeta.dummy_update() for example. 

     Below, use of div to set the width to by pass pandoc-to-Markdown
     conversion problem => ![alt](url) :: no way to set width.
--> 

## Video
<div width="{{video_href_w}}">
    <a href="{{video_href}}" target="_blank">
        <img src="{{video_href_src}}" 
             alt="{{video_href_alt}}"/>
    </a>
</div>


## Transcript
{{formatted_transcript}}  


{% endmarkdown %}
</article>