YT changed captions timing format:

### old:
```
<?xml version="1.0" encoding="utf-8" ?>
<transcript>  # root
<text start="3.439" dur="4.241">okay</text>
<text start="5.04" dur="3.599">hello and welcome to data umbrella&amp;#39;s</text>
...
</transcript>
```

### new: "Internally, their adapted TTML format is called SRV3"
Ref1: https://js-jrod.medium.com/the-first-complete-guide-to-youtube-captions-f886e06f7d9d
> Internally, [YouTube] adapted TTML format is called SRV3.
Ref2: https://github.com/pytube/pytube/issues/1077
>Also the root element, in this case `<timedtext>` has only one child `<body>`, so the iteration in xml_caption_to_srt has to be done for the elements of body.
```
<?xml version="1.0" encoding="utf-8" ?>
<timedtext format="3"> #root
<head>
<ws id="0"/>
<ws id="1" mh="2" ju="0" sd="3"/>
<wp id="0"/>
<wp id="1" ap="6" ah="20" av="100" rc="2" cc="40"/>
</head>
<body>
<w t="0" id="1" wp="1" ws="1"/>
<p t="3439" d="4241" w="1">
  <s ac="255">okay</s>
</p>
<p t="5030" d="2650" w="1" a="1"></p>
<p t="5040" d="3599" w="1">
  <s ac="255">hello</s>
  <s t="480" ac="255"> and</s>
  <s t="719" ac="255"> welcome</s>
  <s t="1200" ac="255"> to</s>
  <s t="1680" ac="255"> data</s>
  <s t="2000" ac="255"> umbrella&#39;s</s>
</p>
<p t="7670" d="969" w="1" a="1"></p>
<p t="7680" d="4240" w="1">
  <s ac="255">webinar</s>
  <s t="560" ac="255"> for</s>
</p>
<p t="8629" d="3291" w="1" a="1"></p>
...
</body>
</timedtext>
```
### Detailed explanation from Ref1:
```
<!-- Paragraph/Cue Tag -->
<p
   t="0000"       <!-- Timestamp in ms (required) -->
   d="0000"       <!-- Duration in ms (required)  -->
   ws="#"         <!-- <ws> ID   -->
   wp="#"         <!-- <wp> ID   -->
   w="#"          <!-- <w> parent ID -->
   a="0|1"        <!-- used by auto captions for padding  -->
  />
<!-- Span Tag -->
<s
   p="#"          <!-- <pen> ID  -->
   t="#"          <!-- Timestamp (relative to <p> parent) -->
   ac="#"         <!-- Unused (found in auto captions)    -->
  />
<!-- Window/Region Tag (for scrolling text) -->
<w
   id="#"         <!-- Tag ID -->
   t="0000"       <!-- Timestamp (child <p> timestamps relative) -->
   ws="#"         <!-- <ws> ID   -->
   wp="#"         <!-- <wp> ID   -->
  />
```

# Solution from Ref2:

```
for i, child in enumerate(list(root.findall('body/p'))):

#and change duration, start variables to
start = float(child.attrib["t"])
duration = float(child.attrib["d"])
```
Also:
>I fixed it by changing line 63 in captions.py:
`fraction, whole = math.modf(d)` to `fraction, whole = math.modf(d/1000)`.
Just have to change milliseconds to seconds.
