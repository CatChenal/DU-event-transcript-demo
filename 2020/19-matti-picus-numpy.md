# Matti Picus: Contributing to NumPy

## Key Links
- Meetup Event:  https://www.meetup.com/data-umbrella/events/274689815/
- Video:  https://youtu.be/lHJqOE5j6xE 
- Slides:  https://github.com/numpy/archive/blob/master/content/data_umbrella_dec_2_2020/data_umbrella.ipynb
- GitHub Repo:  N.A.  
- Jupyter Notebook:  N.A.     
- Transcriber:  ? 

## Resources
- NumPy Slack: https://join.slack.com/t/numpy-team/shared_invite/zt-e2d24txg-w3Mq1OJZ2nEAAcGgQOoC0A
- Numpy Docs:  https://numpy.org/devdocs/dev/development_environment.html?highlight=gdb#debugging

## Video

<a href="http://www.youtube.com/watch?feature=player_embedded&v=lHJqOE5j6xE" target="_blank">
    <img src="http://img.youtube.com/vi/lHJqOE5j6xE/0.jpg"
         alt="Matti Picus: Contributing to NumPy"
         width="25%" />
</a>

## Transcript

### Introduction
<!-- Editing Guide: The pipe (|) position in this comment is 120:                                                       | -->

Hello everybody welcome to Data Umbrella's webinar so our our processes usually I do a quick introduction matti will do  
his talk and you know her Q&A if you have questions you can on chat or you can post them in the Q&A tab I can easily  
move questions from the chat over to the Q&A so that's fine and this webinar is being recorded and will be available on  
YouTube usually within a couple of days but sometimes a week depending on how much editing has to be done a quick  
introduction about myself I I'm the founder of Data Umbrella I'm a statistician data scientist by training and I am  
available on Twitter LinkedIn and GitHub at Reshama so feel free to follow me if you'd like we have a code of conduct  
here we're dedicated to providing harassment free experience for everyone this applies to the chat of this webinar as  
well our code of conduct you can link to it on this link to the sticky pad if you want to go to it thanks for making  
this a welcoming and friendly community for all if anybody does sort of put something inappropriate in the chat we will  
remove that person from our community and to let you know that we are a volunteer run organization there are various  
ways that you can support our community the very first way is to follow our code of conduct we want to make it a  
welcoming and inclusive space for underrepresented persons and so following our code of conduct and contributing to  
making a professional is like our top priority otherwise you know it could be like any other community we have a discord  
community chat so feel free to join it it's on our website it's a it's a place to ask and answer questions there we have  
an open collective where people can donate to cover our operational expenses expenses and we also have an initiative  
this video to do a transcript that will be available for people to read later the location of the transcript is on  
GitHub Data Umbrella event transcripts you can also find transcripts for past events there we have a job board which is  
at jobs.dataumbrella.org check it out just if you're curious or if you're on the market on our website which is  
dataumbrella.org we have a lot of resources for open source for accessibility for responsibility social impact of AI so  
please check it out later at your convenience we also have a monthly newsletter which is that dataumbrella.substance.com  
I'll copy the link and put it in the chat later we send out a newsletter once a month so feel free to subscribe we  
promise not to send you spam we are on all social media platforms as Data Umbrella the best place to join really is our  
Meetup group because that's that has our events in it and then there's you know we're on Twitter and LinkedIn and also  
YouTube so this is being recorded and it'll be uploaded to YouTube so you can check out our past events there as well  
and if you subscribe to YouTube you get this notification on your phone which is useful we have two upcoming events  
we're gonna have a contributing to Pandas webinar on December 15 so you can find it on our Meetup page we also have a  
command line setup environment which is on January so you know there's more information on the Meetup group about these  
events and signing up for it today's speaker is matti pikas I hope I'm pronouncing it that right  
 

#### 00:04:02,640::		4 minutes mark -> new paragraph 
 
 matti is an active computer contributor to numpy and a member of the steering council he's also a core developer and  
release manager for pi pi he also contributes to maintaining the scientific Python stack across the ecosystem of  
packaging ci which is continuous integration and documentation since April of 2020 and this year he has worked at  
quansite labs and you can find him on GitHub at matti p and with that I will turn off my video and I will hand it the  
floor over to matti great OK here we go so my talk today is how to get involved in numpy as rashida said my name is  
matti pikas this presentation is in the Jupyter notebook and when we put up the YouTube video we'll we'll actually link  
to that notebook as well I'll be tabbing around my web browser a bit hopefully the lag won't be too bad and won't make  
you too dizzy use the chat and the Q&A there's some ringers in the in the audience some other numpy contributors and  
they'll be happy to answer your questions as we're going along and my goal and the goal the the reason that we'd like to  
talk to you today is to get help with to get you started with helping us with documentation tutorials code and devops so  
numpy is much more than just the code itself we have other ways you can contribute so what are we going to do first of  
all don't panic the project itself is huge it has lots of different corners and I'm gonna talk about some stuff and if  
it doesn't make sense that's OK I'm gonna have a brief history of numpy when was it started by whom and what for what  
drives numpy what are the goals and how do we decide on those goals who are the who decides what happens in the  
community we're going to talk about communication channels and ways you can get in touch with us and the different repos  
there are in GitHub and then we'll demonstrate how to build and test numpy and then we'll take a look at some how to  
find issues and PRs that contributors can work on and then at the end we'll take some questions if there's still time  
but first me my name is matty as I said I'm a kwan site developer quansite is a company that about developers working  
both in open source and for contracted work I was previously employed by the berkeley institute of data science to work  
full-time on numpy I did that for two years before I joined quansite and I'll talk a bit more about that later I'm an  
avid open source evangelist I believe in open source I think that's the best way to produce quality code and software pi  
pi is a pro project to implement Python but not by a c actually by Python by a Python so it's Python that implements  
Python just like the c compiler is written in c if you want to know more about that you can find out about it on  
pipe.org I believe deeply in the power of community that's why I'm doing this talk that's why I've been working on open  
source for the past couple of years I spent a long time in an intentional community in israel called kibbutz spent over  
10 years there and I think that community is is the way that society should be organizing itself and I also believe in  
diversion and inclusion I was lucky enough to have a very smooth course in my life not everybody else does and I'd like  
to help others  
 

#### 00:08:00,240::		4 minutes mark -> new paragraph 
 
move on and become inclu and become able to contribute to society tech and open source in particular OK so back to the  
talk about nunpai numpai as you can see here in 2006 it was started by travis oliphant it grew out of two other  
libraries numerica and nomure as a way to synthesize those two libraries together and it was the cornerstone of what  
travis actually wanted to build which was sci-pi so numpy sits under scipy and it turns out numpy sits under a lot of  
other things as well as time went on the numpy API and the numpy way of looking at a chunk of memory and dividing it up  
into items became very popular was adopted by the deep learning frameworks by a library called coupe which allows you to  
do numpy like operations on data on your GPU das and sparse also use it well you should use the the API and the ideas  
behind numpy as well as numpy itself numpy's quite popular pretty much it's the first thing that people will install if  
they're doing data science and they want to they're building a Python environment we estimate that it's got tens of  
millions of downloads and users worldwide and it's maintained now by about 10 people that's a bit of a stretch maybe six  
people actively maybe full-time equivalents of about two and a half or two people it's over its lifetime it's had 1.4  
million dollars US dollars in lifetime funding about over a million of that was donated by the moore and sloan  
foundations in a joint grant that I was lucky enough to participate in it started about two and a half years ago they  
hired about three developers to work on numpy full-time for two years along with some other things and that really gave  
the library a boost the infographic below shows how nunpai is used pretty much everywhere but of course you all know  
that OK that was a brief history of numpy now we'll talk about what what actually is numpy how do the core people who  
who push numpy forward what do they think the goals of it are so as I said this is all a Jupyter notebook I'm just using  
the the website here because I I'm too lazy to actually write stuff by myself so if you go to the website you can read  
about what numpy is numpy is run by a steering council there's about a dozen people on the steering council the steering  
council is a loose loosely appointed self-appointed group of people who are the currently the active contributors to  
numpy and they're the ones who will decide what direction the the the project will take numpy is made up of a bunch of  
overlapping teams we have teams for might be a bit small here to see this but we have teams for code documentation the  
website for triaging bugs and issues and a small team for getting funding and grants and administrating the project and  
we also have a small number of sponsors I already mentioned the moore and stone foundations chan zuckerberg institute is  
initiative has been active in the past couple years giving us some grants and tide lift gives us monthly support and  
both of these industrial partners institutional partners I've been working I've been lucky enough to work at over the  
past couple years so how how do we decide what not where we're going to go with numpy so if you look at it from the top  
down we can look at it from the bottom up we're going to do that as well but if we look at it from the top down  
 

#### 00:12:00,399::		4 minutes mark -> new paragraph 
 
numpy is it's higher level goals and when we look for funding what we're trying to do is to get actually funding for our  
roadmap the roadmap describes the scope of numpy and our wish list of features we'd like to work on and then  
enhancements large chunks of future work on numpy will be done through numpy enhancement proposals or neps and eps these  
are proposals to change things like the d type a system underlying the the array object or the random number module that  
was in numpy or one of the latest ones that's to put to make all the functions in numpy use processor intrinsics OK so  
that's kind of a higher level viewer but what does numpy think about itself numpy is a very nice way to work with a  
chunk of memory on CPU with stride shape and d type and one of the most important things that we as developers take to  
heart while developing numpy is not to break anything we have a strong commitment to be backward compatible and not to  
break people's workflows we realize that numpy is is a basic core piece of the data science stack in in Python and we're  
trying to be careful not to break things while performance is important interoperability beats performance as I said  
before numpy was started as an initiative to be one piece in a larger puzzle we realized that that that is a is a deep  
commitment and that's part of what numpy views itself is as doing as being the being at the forefront and at the base of  
a large number of Python array type objects and driving that forward so that people can do things with numpy that that  
may that that aren't built into numpy but enable interoperability with other libraries so what do I mean about  
interoperability don't worry if this is a bit of a deep dive and you miss a bit of this it's more of a higher view of of  
how just trying to in trying to emphasize how numpy wants to work nicely with other libraries and to interact with other  
libraries in a nice way we what goes into numpy is actually very tightly controlled we try to keep many things out of  
numpy provide only the minimum tools needed to work with the basic library that numpy is and would rather delegate other  
tasks to other libraries that can move a lot faster and maybe break things where numpy has to be careful not to break  
anything so one of the things that's in numpy is an is an extension to disk disk utils which is a tool to build  
libraries but things like optimizations which are in scipy or loading images which are in psychic image and pillow or  
working on the GPU which are in cooper and jacks they won't ever hopefully come into numpy it's hard to say never but  
they they're probably will never come into numpy there are pieces of of code that are in numpy for historical reasons  
and probably shouldn't be one is a is a minimal FFT implementation the one in scipy is much nicer as is the linear  
algebra routines that are in sci-fi they're much well better thought out polynomial and f2 pi were two pieces of code  
that kind of orphans no one really wants to take care of them so they've stayed in numpy and the random module that's in  
numpy is a best of brand random number generator that we're very proud of and it would it is in numpy but you might  
think that it doesn't actually  
 

#### 00:16:02,160::		4 minutes mark -> new paragraph 
 
 belong in numpy it doesn't actually go with the core mission of numpy in addition numpy provides throughout its code a  
way to take this nd array object that I talked about that that has the chunk of memory on the on the CPU with strides  
and shape and allows you to subclass it via different protocols the array of the dunder array protocol done to a wrap  
protocol down to a raised truck protocol down to array priority protocol all these are useful for subclassing and the  
array in a way that doesn't actually it overrides the behavior of the nd array but it doesn't affect the code in numpy  
itself so it's another way we can interact with others then we determined that these were not enough we need more ways  
for people to be able to override things in nampa and so we provided three new protocols the array euf protocol the  
array function protocol and the array module protocol to also make overriding functions transparent so all those  
protocols are the reason that you can do something like the code that's on this page you can do import numpy as np  
import coupon which as I said was the library that allows you to work on a GPU you can create a coupon zero array by 10  
by 10 of the d type np int and then you can call sum on that now when you call sum on that that's actually calling the  
sum method on this a object but if you call np dot sum that's calling a procedure from the numpy array but because we  
have protocols you can override that and that actually calls back out to coupei to provide their their function as well  
you can override functions OK sum is a u-func if that means anything to anyone mean is a function you can also  
override that with array function and lately our last step in this procedure and one that will be out in the late in the  
in the next release of numpy hopefully next month will be the like keyword which allows you to actually create a new  
array just with the same device type and same kind of format as a so all this needs a lot of fun working underneath the  
hood in numpy to make all these things work even that is not enough so numpy together with the other data libraries and  
together with some industrial partners have started to set up what we're calling a common API for raise and tensor  
Python library so this will cover both numpy and Pandas type objects the Pandas data frame and the idea is to create a  
common API so that anyone who wants to create something that can be that can one for one replace numpy will be able to  
do it so rather than import numpy you may do import my fancy library and as long as it implements all of these API  
functions you will know that it is numpy compatible OK so I hope I've convinced you that numpy tries to be  
interoperable with a lot of other libraries and tries to be a good member of the community and now let's actually talk  
about contributing to numpy and working with numpy like most of the world numpy has moved to GitHub most of our our our  
activity takes place on GitHub we also have a mailing list numpy dot numpy dash discussion for bigger topics ones that  
can't be neatly packaged into an issue or pull request  
 

#### 00:20:00,799::		4 minutes mark -> new paragraph 
 
so how does that look let's take a look at the numpy organization on GitHub we have three or four different repos we'll  
go through them really quickly to see which ones do what so the top repo on in the in the hierarchy is the actual numpy  
slash numpy repo that's where the code and the documentation for the numpy library live the archive the reason it's on  
top is because that's where I put my my talk just now that's where it's been archived and that's where it's you can find  
it so that's why it was updated half an hour ago that's an archive of all kinds of presentations and talks and logos and  
branding about numpy numpy tutorials is a new repo that we've started in the past six months to actually aggregate best  
of brand tutorials on how to work with numpy things we recommend and ways we recommend that it all work numpy.org is the  
numpy website repo and then the only other one that I want to call out and in this long list is the numpy doc repo which  
holds a an extension for sphinx sphynx is a way to document Python libraries it builds a lot of the documentation that  
you'll see if you go into Python document site Python package documentation websites you'll see documentations that have  
been built using sphynx numpy doc is a way to turn doc strings from Python functions into nicely formatted the next  
beforehand documentation right got it OK so that's how you can that's how you kind of wander around the GitHub numpies  
how do you actually build and test and get involved in in working with numpy the library itself not import numpy and  
then working with it but actually building it and testing it so numpy has a nice long contributors guide OK it goes  
through the whole development process with a summary of how to actually create a pull request how to build how to test  
what kind of styles stylistic things you can use how to build the documentations and then even more detail in subsequent  
web pages but you guys are lucky I'm here so we're going to do this together we're going to go through and create a  
directory to work to to actually build numpy we're going to create a conda environment to build numpy we're going to  
clone the repo and we're going to actually build numpy so let's start let's start now I've got a terminal it's a bit  
small let me try and copy paste the commands from here because copy paste is a is a developer's dream and we'll copy  
make deer temp dm test OK and cd temp dm test they always say never live code right and then I want to actually create  
a conda environment so I'm going to create a new condo environment called Data Umbrella using Python 3.8 and the things  
didn't quite work this is  
 

#### 00:24:03,679::		4 minutes mark -> new paragraph 
 
why they say don't live code it's going to take a second to actually resolve all that and we'll tell it to go ahead and  
create that environment I like working in a virtual environment that sets my makes my code makes my my Python  
environment clean I know exactly what's in it and now activate that environment [music] OK now we've got a condo  
environment activated you can see that it's called Data Umbrella and we're gonna clone the the the numpy repo get clone  
GitHub.com https GitHub.com [music] OK and while that clones let's go back and look a bit at the repo what we're  
actually pulling down into this directory so if we go into numpy this is the director we're cloning right now you'll see  
that there's a lot of different files here starting with the readme itself that asks that ask for contributions so among  
these directories the two that are really where we like to work in are the doc directory and the numpy directory because  
we're going to try and build numpy let's take a look at the numpy directory itself we'll dive in and and see what it  
looks like oh my goodness there's way too much here so there's a whole bunch of directories here this is a mixture of  
Python and c code within it within the within one one directory structure you'll see things like f2 pi which I talked  
about which is a library that allows you to use fortran in Python or random or disk utils which is a collection of  
improvements distributes so that it compiles better the one we care about is where the c code actually lives because  
numpy is built in c on top underneath the Python a lot of it is Python but much of the code is c and that's in the core  
directory in the source directory this is where the actual code itself lives that we'll be working with as as numpy  
contributors originally numpy had two different structures two different two different extensions that were built  
they've been unified together one is multi-array and one is umath multi-ray is the thing that holds the nd array so this  
is this is the actual code that builds that ndra object it looks a bit scary but as we'll see as we try and work through  
an issue it's not that horrible OK so we've successfully cloned numpy now we'll cd into the into the GitHub checkout  
and the next thing we want to do is build and test our new checkout of numpy so we do Python the the way you can build a  
that people traditionally build a c extension project within Python within the Python world is with Python space setup  
py numpy has a convenience function called run tasks that surprise surprise runs all the tests so it builds and runs the  
the tests of numpy there's different ways you can run it this is all documented on the website under that contributor  
guideline if you just run run tests which is what  
 

#### 00:28:01,520::		4 minutes mark -> new paragraph 
 
we're going to do in just a minute it will build and run all of the tests that numpy has probably around 12 000 14 000  
different tests if you run it with a minus s it will only test the this module and if you run it with a minus t it will  
only test this particular test because as I said numpy is a c extension module there's problems there's problems there's  
challenges when you want to build it and test it in place when you want to run the actual code that you've built so you  
have this directory and when you build the project not necessarily Python knows how to import it from that directory so  
run test sets everything up in a way that you can do run test minus minus IPython or run test minus minus Python and  
then it will import it will set up your environment so that you can import the newly built numpy every time you build it  
from or build it from build it in you we also have benchmarks within the test suite and you can run the benchmarks to  
see how your code has affect the performance of numpy OK I won't go through everything that that's in the run test  
it's way too much to go through but let's try running it the only argument I'll give it is show [music] build and build  
log which will show the compilation as it's going ah I didn't do something I didn't read the instructions let's go back  
to the instructions what didn't I do I didn't install everything we need to actually build numpy in our condo  
environment so let's paste that command there's a file that has all the requirements we'll install that and now we  
should be ready to go OK so the first thing it does is process psiphon which is a library that takes Python-like code  
and turns it into c and now it begins to compile the pipe the numpy extensions you can see it does a lot of compiling  
things while it does that we'll take one more look at the at the at the directory structure OK I said there were two  
main pieces of the of the code itself of the numpy repo there's the numpy code and then there's the documentation we  
take our documentation seriously we like to have clear and concise documentation about everything that numpy does this  
is where the documentation lives just like in numpy where there was a source directory here there's also a source  
directory and the the documentation is written in a in a format called rst restructured text and the restructured test  
heavily uses the sphinx tool to automate a lot of the building things so if you look at for instance the the index page  
of the of the whole library all you'll see is that it's got a talk tree which is a table of contents and then it refers  
to other pages and these other pages will actually be pulled in and sphinx will help us create from this a nice HTML  
library so let's see how we're doing still compiling OK let's move on a bit and we'll come back to the tests we'll  
come back to see how the run run went in a little bit so it all looked very clean and very  
 

#### 00:32:00,640::		4 minutes mark -> new paragraph 
 
easy for Linux that's usually the way world works but if you're on a Mac OS and Windows there's a few things you might  
have to look out for when you're starting to build numpy Mac OS is pretty close to Linux so it's pretty smooth you may  
have some problems with the accelerate library which is linear algebra library that numpy by mistake will pick up it has  
bugs and numpy won't let you let you use it in its compilation so you'll have to find a way to neutralize that that  
library there's some tips in our developer guide on Windows you're going to have to install a compiler once you've done  
that it should just work hopefully OK much of the code base is written in c and it's not we don't use c plus plus  
basically because we support some very old compilers as I said we try not to break things that means that because it's  
written in c you need to know something about the Python c API and how ref counting works ref counting is a way around  
is a way around the the the problem that Python has in object initialization and throwing things away so objects in  
Python live in a scope if you're writing a Python code you'll see that the the object lives within your little local  
scope of your code and when the object goes out out of scope Python is very clever about destroying it in c we don't  
have that option once you create something in c you have to you're the one who are responsible for for for destroying a  
door for deleting it another trick that we use in numpy is that a lot of the c code is actually generated either from  
Python or from other code in a templating kind of way if you hit that then you'll have to learn about it building  
documentation we talked about documentation how important it is to the numpy ecosystem because our code is self-  
documenting you have to have the version of numpy that you want to use we want to actually document installed in order  
to use it so this might be a little bit of there's some tricks you have to learn to work around this when you're when  
you're compiling numpy and then trying to work on the documentation itself the two versions have to agree with each  
other as I said the doc strings the the code is self documenting so the dot strings for c extension they're injected  
from Python let's see how that works we have a Python file oops not that one this one we have a Python file called add  
docs add new docs that adds the documentation to the c extension modules when you import numpy so let's go down see how  
some of these look if nd enter probably it's not a function most a lot of people use but here's the documentation for  
nditter it's written in are in rst in this restructured text within Python so it's got the triple quotes to turn it into  
a doc string the first line is the high or is the one line summary of what the function actually does and then there's a  
longer summary and then the documentation is written in this very special format that that numpy doc strings use and  
then is parsed and turned into pretty documentation OK let's go back and see how our test run went went pretty well  
OK it finished compiling I'll go back I'll scroll back up this is the end of the compilation and then immediately it  
started to run the tests people have used pi test before this is a pi test output of all the tests that numpy is running  
 

#### 00:36:02,400::		4 minutes mark -> new paragraph 
 
and everything was green there's some tests that are skipped on different platforms and different operating systems  
we'll use the different test testing strategies but everything ran that that could run here and all the test pass it  
just skipped out a bit on the screen here let me see if I can get that there we go pops up a bit we had about 13 000  
tests pass in a little over a minute 85 seconds OK great so we've moved on we've looked at a bit of code we've seen  
how we build numpy now let's take a look at how you can actually dig out a issue or a pull request we have about 10  
minutes left to before we'll take some questions answers to try and look through and and and find some issues you can  
work on typical workflow in in numpy is much like the other lectures you've heard in the in this or the other talks  
you've heard in this series you want to add a failing test we do test driven development the idea behind the failing  
test is you probably just take it right from the issue put that failing code into a test in the proper place in the test  
structure run the test as I did and your test should fail the next thing you need to do is find out where that function  
is implemented and then you have to start from there to figure out what's wrong what's going on in that function that  
trips the test then of course you want to try and fix it then run all the tests not just that one to make sure you  
didn't break anything else very important not to break things then you can push a PR and interact with people so the  
work doesn't end when you push the PR that's only really the beginning that's when the actual work itself starts your  
work will get a review a very careful review some people would call it nitpicky and then you need to react to the  
comments on that review and push it forward until it gets through if it's a simple pull request maybe the whole process  
could take a week or two if they're complicated pull requests well [music] let's take a look at what happens to  
complicated pull requests it's not easy to find good first issues in numpy and I'll just let's open that up and take a  
look at that while I talk about why it's not so easy we have over 2 000 issues in numpy and about 290 open pull requests  
now we'd be very happy to get that down to zero on both ends but there's a lot of reasons we don't if we take a look at  
some of these issues and if we sort them by at least recently updated let's say and we look at something that some of  
these issues from six years ago or from or from for from quite a long time ago [music] the reason that we haven't solved  
these issues is we don't really know how as I said we're very careful about not breaking things in numpy and a lot of  
these issues are good ideas but they would change the way numpy works and so we can't do them same thing with the pull  
requests we have pull requests that have been opened for way too long if I sort them by least recently updated we can  
see there are pull requests from five four years ago that can't be done because they're enhancements that will break  
things that currently work in numpy or that we don't know how to do so a good place to look for issues is either to go  
to the center of the issue stack not the ones that are a week old because people jump on those pretty quick and not the  
ones that are very old because the reason they're there is there are two that we can't fix them  
 

#### 00:40:00,960::		4 minutes mark -> new paragraph 
 
but to look at ones that are maybe three or four months old or maybe a year old OK let's take a look at how if you're  
the one who jumps on the issue first how that all might how you might actually attack it and try and fix it and this  
actually happened now we had a new contributor come along and pick up this issue that someone posted a little about  
three weeks ago and the and we'll try and take a look at what this person did to push this issue and and try and fix it  
so this is how an issue looks when it first comes through the the pipeline new user user comes up and says hey  
something's wrong and they're trying to their best to give a description of actually what's wrong so one of the first  
things you have to do when you when you're triaging an issue is look at it and try and figure out what's going on here  
what is the person actually trying to convey to the number developers and one thing you might notice in this issue is  
that it it's not quite formatted correctly the user doesn't actually didn't actually use the git git hub Markdown code  
formatting format to format their issue and so let's help them out that's something we can do as a triager is to  
reformat their comments and now we can actually see what what the problem is what's going on here OK they do import  
numpy as np that's pretty clear print out the version that's one eighteen five and then they do array three equals np  
dot a range parentheses start equals five and they print out array three so that would be this line anybody see anything  
strange here see what the problem is OK we asked for start equals five what numpy did was stop equals five well that  
looks bad OK if I ask for stop equals eight then numpy will output an error that the required argument start is  
missing if you don't put anything in a range if we go over to the documentation look at it I don't want to do that  
because I don't want to make you guys dizzy with flipping all my tabs around all the time you'll see that you can do a  
range open parentheses close parentheses with nothing in the middle and it will also yell at you that that the that the  
start argument is missing but if you put in one number a range 8 for instance that we will get that will get translated  
to stop and that will print out zero one two three four five six seven eight values OK so we've kind of understood  
what this issue is about there's two problems here one is that for some reason start is being interpreted as stop and  
the other less critical problem is that stop is is when stop alone is put in there is no start equals zero OK so  
people started commenting you'll see how long it took for someone to start commenting was actually no time at all on the  
same day someone had already commented and the person came back and and commented again and then someone actually tried  
to look through the code to see when this when this broke and then we discovered that actually it's not a regression  
this code has been that way for 20 years and no one's ever discovered so because of this comment here that might be a  
nice thing for some newcomer to work on a newcomer actually picked this code up and started working on it and we can see  
that because later on in the issue in the flow of the issue there's actually a pull request here  
 

#### 00:44:01,680::		4 minutes mark -> new paragraph 
 
that comes to fix this so let's take a look at the pro request the first thing we see in the pull request is that it  
says it links back to the actual issue itself that's the way that nice little link showed up in the issue was because  
this pull request actually said I fix issue I'm related to issue 17764. so that's pretty important when you create a  
pull request it kind of marks your territory it says I'm working on this issue please don't also submit a pro request to  
fix it OK and what is the full what does the pull request actually comprise what's in it there are two two files that  
changed OK we'll not look at the let's look first at the second file that changed which was the test so the first  
thing that this person did was write a very nice test of all the different things that are currently untested in a range  
for instance there was no test that a range without any values [music] comes out clean there was no test for step equals  
3 which is also an error and and and so forth and so this is the actual test for the issue that the that the reporter  
raised [music] and if you would run if we would actually check out this branch with only these tests in our in our in  
our repo and run the tests we would see that they would fail so the next thing the the person had to do was find out  
where actually is a range implemented and I'll just go into that in two minutes because I'm kind of running out of time  
here [music] but if we go back to the code let's go back into the code into the source into the core into the source and  
into multi array which I said was where code where most the code lives there's one file that's called multiarray module  
[music] and if we look in this file for for a range with double quotes around it we'll see that somewhere along the line  
way deep in the 4 000 lines of this file there is a dictionary that maps names like a range to functions like a array a  
range nested in theirs is another function it's mapped to npy iter nested hitter so let's try and see how this function  
actually looks is this where we want to be and I'll just finish out this this piece quickly by not by confusing you too  
much with the c code but by saying that well this looks like the right place because this is has a function in it called  
parse tuple and keywords so that's probably what's handling the input of this function this is the place we want to  
start looking around digging around to see where the actual bug might be OK and as I said it got complicated quickly  
that's pretty much what I want to talk about I'd like to take some Q&A now let's see what we can do with that just to  
summarize my goal here was hopefully not to scare you off too much to convince you that numpy is a nice place to to help  
out with we could use help with documentation tutorials code and devops  
 

#### 00:48:00,800::		4 minutes mark -> new paragraph 
 
anything you contribute would be welcome and we don't have any questions so now would be the time to ask questions or  
actually have another poll I'm going to put up another poll where is it the cued start polling to see how I did here if  
you could fill out the poll and tell me if you think you're interested in contributing if you need help contributing we  
can help you out you can reach out to us either open an issue or comment on an issue or reach out to us on the mailing  
list or in some other way and say I'd like to get involved I need a little bit of help to get started we're happy to  
mentor people at the beginning and get them started with with the project yeah so that's pretty much what I wanted to  
say if there's no questions and there's no comments on the chat that I missed rasheeda I think I'll shima sorry I think  
I'll send it back to you question about gdb could you go over briefly ways to use gdb with numpy so Brian are you using  
Windows or Linux I can show you in Linux I can't really show you in Windows so did my my screen made itself smaller let  
me make this font bigger the best way to work with gdb in Linux is you actually need to build a debug build of of numpy  
so the way to do that is to clean it all out get clean xfd that cleans out all the files that we built and when we where  
we ran build tests before and now we're going to set up some c flags to do now this works on my computer I've heard it  
doesn't work in other places o o minus g three so these flags are that's a capital o capital o and then a zero that  
means don't do any optimizations g3 means take care of all the macros that you want don't turn any of them don't inline  
any of the macros and show me all of the values for c macros so now I can I don't want to actually run the tests I just  
want to build numpy so I will do run tests py minus b which is build only this will build a debug version of numpy and  
I'll answer some other questions and I'll show you before I show you how to get into it while it's building do we need  
to be familiar with c language in order to contribute to numpy you don't it helps a lot of the code is written in c and  
a lot of the a lot of the kind of bent of the code reflects c up in the Python language so things like d types really  
take a c kind of mind in order to understand why all of a sudden my d type is overflowing or my d type isn't behaving  
the way I want it to but like I said we could use help with documentation with tutorials with dev op kind of things as  
well as code itself  
 

#### 00:52:03,040::		4 minutes mark -> new paragraph 
 
would be very happy to to help people work around I'll be very happy also to work with people who don't know c and to  
improve our documentation and our onboarding system so that we'll be more friendly to people who don't know c OK so  
but I'll go back to c because of to answer Brian's question so the next thing you need to do is do gdb minus minus args  
Python run tests py minus minus Python which is what I said before is a way you can get this whole thing to run under  
Python and now we've opened up a gdb session we can tell it to run it's now running Python under gdb OK so we've got a  
Python prompt we can do import numpy as [music] np numpy a3 equals a range to get back to the bug that we were looking  
at [music] start equals three never live code OK and now we can stop if we I'm going to hit CTRL c CTRL c will bring  
me into the debugger and I'll say break at array a range it no I did a tab to complete the the line it sets a breakpoint  
because I compiled with the debug version and now if I tell it to continue running no until to continue and I'll hit  
that code again I have now stopped in the debugger at the array a range function I think that's enough with gdb for  
people who know gdp this is enough to get you going for people who don't they were really bored from the past three  
minutes so good more questions chats I'm on Linux so OK someone says they use gdb from sea lion [music] yep and  
there's some other good answers in the chat about pure Python things that could be improved [music] great any more  
questions anymore matti this was such a great talk I can't over overstate like how informative and useful it is on so  
many levels not just for numpy but for Python for debugging for open source for the history of it all it was really just  
amazing really thank you so much thank you I'll stop sharing my screen and you know that this has actually gotten me  
excited about possibly doing a sprint with you great yeah like I said we really love to to onboard new people you know  
even if you on board and and you go somewhere else and work on some other library that's fine you know that's great yeah  
that is great that's sort of the you know the same thought I have with sky kit learn where I have organized a bunch of  
sprints which is like you know this is like for open source if you go and contribute to another library it's still a  
success so and a lot of this information is  
 

#### 00:56:01,040::		4 minutes mark -> new paragraph 
 
transferable with you know from one Python library to another with like slight you know specific tweaks OK so with  
that I will I will end this this recording will be made available within the next two to five days there's a comment  
here if you look at our docs for contributing and find them confused or incomplete we would also appreciate help there  
that's from Melissa yes and actually what I will do also is there's a bunch of links in this chat which I have access to  
later so I will copy all those links over to you know our transcript area so it's available for people when they're  
viewing this recording later again thank you matti and also thank you to the whole numpai team I know there were you  
know there were a lot of other people that that you had collaborated with as well so thank you so much yeah bunch of  
them were in the chat so thanks guys for handling all the chat during the talk  
 
