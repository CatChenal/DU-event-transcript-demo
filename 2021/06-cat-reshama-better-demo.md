# Cat Chenal, Reshama Shaikh: Automating Audio Tanscription.  

## Key Links  
- Meetup Event:  N.A.  
- Video:  https://youtu.be/MHAjCcBfT_A  
- Slides:  N.A.  
- GitHub Repo:  N.A.  
- Jupyter Notebook:  N.A.  
- Transcriber:  Mae Song  
## Other References

                  - Binder:  <url>
- Paper:  <Paper url or citation>  

                  - Wiki:  This is an excellent [wiki]  

                  (http://en.wikipedia.org/wiki/Main_Page)  
  

## Video
<a href="http://www.youtube.com/watch?feature=player_embedded&v=MHAjCcBfT_A" target="_blank">
    <img src="http://img.youtube.com/vi/MHAjCcBfT_A/0.jpg" 
         alt="Automating Audio Tanscription."
         width="25%"/>
</a>

## Transcript 
<!-- Editing Guide: The pipe (|) position in this comment is 120:                                                       | -->
### Introduction

Okay hello and welcome to Data Umbrella's webinar for October so I'm just going to go over the agenda I'm going to do a  
brief introduction then there will be the workshop by Hugo and James and you can ask questions along the way in the chat  
or actually the best place to ask questions is the Q&A and there's an option to upvote as well so yet asking the Q&A if  
you happen to post it on the chat by mistake I can also transfer it over to Q&A so that would be fine too and this  
webinar is being recorded briefly about me I am a statistician and data scientist and I am the founder of Data Umbrella  
I am on a lot of platforms as Reshama so feel free to follow me on Twitter and LinkedIn we have a code of conduct we're  
dedicated to providing harassment free experience for everyone thank you for helping to make this a welcoming friendly  
professional community for all and this code of conduct applies to the chat as well so our mission is to provide an  
inclusive community for underrepresented persons in data science and we are an all volunteer run organization you can  
support Data Umbrella by doing the following things you can follow our code of conduct and keep our community a place  
where everybody wants to keep coming to you can donate to our open collective and that helps to pay meet-up dues and  
other operational costs and you can check out this link here on GitHub we have this new initiative where all the videos  
are being transcribed and so is to make them more accessible so we take the YouTube videos and we put the raw there and  
so we've had a number of volunteers help us transcribe it so feel free to check out this link and maybe if you do this  
video maybe the two speakers will follow you on Twitter I can't promise anything but it's possible Data Umbrella has a  
job board and it's at jobs.org and once this gets started I'll put some links in the chat the job that we are  
highlighting today is is the machine learning engineer job by development seed and development seat is based in  
Washington DC and Lisbon Portugal and they do I'm going to go to the next slide what they do is they're doing social  
good work and so they're doing for instance mapping elections from Afghanistan to the US analyzing public health and  
economic data from Palestine to Illinois and leading the strategy and development behind data world bank and some other  
organizations and I will share a link to their job posting in the chat as well as soon as I finish this brief  
introduction check out our website for resources there's a lot of resources on learning Python and r also for  
contributing to open source also for guides on accessibility and responsibility and allyship we have a monthly  
newsletter that goes out towards the end of the month and it has information on our upcoming events we have two great  
events coming up in November and December on open source so subscribe to our newsletter to be in the know we are on all  
social media platforms as Data Umbrella Meetup is the best place to join to find out about upcoming events our website  
has resources follow us on Twitter we also share a lot of information on LinkedIn and if you want to subscribe to our  
YouTube channel we record all of our talks and post them there within about a week of the talk so it's a good way to get  
information OK and now we are ready to get started  
 

#### 00:04:03,120::		4 minutes mark -> new paragraph 
 
so I will hand it over to put myself on mute and I will hand it over to Hugo and James and let you take over but thank  
you all for joining I just want to thank Reshama Christina and and everyone else who tied all the tireless effort that  
that goes into putting these meet-ups and these online sessions together I I think one thing I want to say is actually  
the the last in-person workshop I gave either at the end of February or early March was data umbrellas in inaugural  
tutorial and Meetup if I if I recall correctly on on bayesian bayesian thinking and hacker statistics and simulation and  
that type of stuff so it's it's just wonderful to be back particularly with my colleague and friend friend James we're  
building really cool distributed data science products at coiled we'll say a bit about that but we'll do some  
introductions in in a bit I just wanted to get you all accustomed to it was February thank you Reshama we're working  
with Jupyter notebooks in a GitHub repository the repository is pinned to the top of the chat this is what it looks like  
these are all the files this is the file system now we use something called Binder which is a project out of and related  
to project project Jupyter which provides infrastructure to run notebooks without any local installs so there are two  
ways you can you can code along on this tutorial the first is and I won't get you to do this yet is to launch Binder the  
reason I won't get you to do that yet is because once you launch it we have 10 minutes to start coding or the Binder  
session times out I've been burnt by that before actually several times I'm surprised I even remembered it this time the  
other thing you can do is install everything locally by cloning the repository downloading anaconda creating a conda  
environment if you haven't done that I suggest you do not do that now and you launch launch the Binder James is going to  
start by telling us a few a few things about about GAs and distributed compute in general my question for you James is  
if we get people to launch this now will we get to execute a cell code cell in 10 minutes I would let's hold off for now  
maybe yep maybe I'll indicate when we should launch Binder OK fantastic cool and just what I'm looking at right now is  
the GitHub repository on your browser OK exactly so I will not launch Binder now I will not get you to now I've I'm  
doing this locally and we see that I'm in notebook zero and if you want to actually have a look at this notebook before  
launching Binder it's in the notebooks Data Umbrella subdirectory and its notebook zero and we're going to hopefully  
make it through the overview then chatting about Dask Dask delayed and and data framing and machine learning great so we  
have Hashim has said you could open in VSCode as well you could I mean that would require all your local installs and  
that that type of stuff as well but we're to introduce me and James we we work at coiled where we build products for  
distributed compute in infrastructure as we'll see one of the big problems with like bursting to the cloud is all the  
like Kubernetes AWS docker stuff so we build a one-click host of deployments for das but for data science and machine  
learning in general James maintains task along with Matt Matt Rocklin who created Dask with a team people who was  
working with Continuum Anaconda at the time and James is a software engineer at called and I run data science evangelism  
marketing work on a bunch of product product stuff as well wear a bunch of different different hats  
 

#### 00:08:01,680::		4 minutes mark -> new paragraph 
 
occasionally there are many ways to think about distributed compute and how to do it in in Python we're going to present  
hey James you're muted I'm taking it I went away based on what I see in the chat you did you did but now we're back I've  
introduced you I've introduced me I've mentioned that there are many ways to do distributed compute in the Python  
ecosystem and we'll be chatting about one called Dask and maybe I'll pass you in a second but I'll say one thing that I  
really like about my background isn't in distributed compute my background's in pythonic data science when thinking  
about bursting to larger data sets and larger models there are a variety of options the thing that took me attracted me  
to desk originally I saw Cameron's note the ghost in the machine aren't playing nice tonight I think that ain't that the  
truth is that dark plays so nicely with the entire PyData ecosystem so as we'll see if you want to write dash code for  
data frames dash data frames it really mimics your Pandas code same with numpy same with scikit-learn OK and the other  
thing is dark essentially runs the Python code under the hood so your mental model of what's happening is actually  
corresponds to the code being being executed OK now I'd like to pass over to James but it looks like he's disappeared  
again I'm still here if you can hear me I've just turned my camera off oh yeah OK great I'm gonna turn my camera  
hopefully that will help yeah and I might do do the same for bandwidth bandwidth issues so if if you want to jump in and  
and talk about dark at a high level I'm sharing my screen and we can scroll through yeah that sounds great so that's  
sort of a nutshell you can think of it as being composed of two main well components the first we call collections these  
are the user interfaces that you use to actually construct a computation you would like to compute in parallel or on  
distributed hardware there are a few different interfaces that desk implements for instance there's Dask array for doing  
nd array computations there's das data frame for working with tabular data you can think of those as like GAsk array as  
a parallel version of numpy das data frame has a parallel version of Pandas and so on there are also a couple other  
interfaces that we'll be talking about das delayed for instance we'll talk about that today we'll also talk about the  
futures API those are sort of for lower level custom algorithms in sort of paralyzing existing existing code the main  
takeaway is that there are several sort of familiar APIs that desk implements and that will use today to actually  
construct your computation so that's the first part of desk it is these dash collections you then take these collections  
set up your steps for your computation and then pass them off to the second component which are desk schedulers and  
these will actually go through and execute your computation potentially in parallel there are two flavors of schedulers  
that desk offers the first is a are called single machine schedulers and these just take advantage of your local  
hardware they will spin up a a local thread or process pool and start submitting tasks in your computation to to be  
executed in parallel either on multiple threads or multiple processes there's also a distributed scheduler or maybe a  
better term for would actually be called the advanced scheduler because it works well on a single machine but it also  
scales out to multiple machines so for instance as you'll see later we will actually spin up a distributed scheduler  
that has workers on remote  
 

#### 00:12:00,160::		4 minutes mark -> new paragraph 
 
machines on AWS so you can actually scale out beyond your local resources like say what's on your laptop kind of  
scrolling down then to the image of the cluster we can see the main components of the distributed scheduler and James I  
might get people to spin up the Binder now because we're going to execute codes now is a good point yep so just here's a  
quick break point before you know a teaser for schedulers and what's happening there I'll ask you to in the repository  
there's also the link to the Binder click on launch Binder I'm going to open it in a new tab and what this will create  
is an environment in which you can just execute the code in in the notebooks OK so hopefully by the time we've gotten  
gone through this section this will be ready to start executing code so if everyone wants to do that to code along  
otherwise just watch or if you're running things locally also cool thanks James yeah yeah no problem thank you so so  
yeah looking at the image for the distributed scheduler we're not gonna have time to go into the a lot of detail about  
the distributed scheduler in this workshop so but we do want to provide at least a high level overview of the the  
different parts and components of the distributed scheduler so the first part I want to talk about is in the diagram  
what's labeled as a client so this is the user facing entry point to a cluster so wherever you are running your Python  
session that could be in a Jupyter lab session like we are here that could be in a Python script somewhere you will  
create and instantiate a client object that connects to the second component which is the das scheduler so each desk  
cluster has a single scheduler in it that sort of keeps track of all of the state for all of the the state of your  
cluster and all the tasks you'd like to compute so from your client you might start submitting tasks to the cluster the  
schedule will receive those tasks and compute things like all the dependencies needed for that task like say you're  
implementing you say you want to compute task c but that actually requires first you have to compute task b and task a  
like there are some dependency structures there it'll compute those dependencies as well as keep track of them it'll  
also communicate with all the workers to understand what worker is working on which task and as space frees up on the  
workers it will start farming out new tasks to compute to the workers so in this particular diagram there are three das  
distributed workers here however you can have as you can have thousands of workers if you'd like so the workers are the  
things that actually compute the tasks they also store the results of your tasks and then serve them back to you and the  
client the scheduler basically manages all the state needed to perform the computations and you submit tasks from the  
client so that's sort of a quick whirlwind tour of the different components for the distributed scheduler and at this  
point I think it'd be great to actually see see some of this in action Hugo would like to take over absolutely thank you  
for that wonderful introduction to darsk and and the schedulers in particular and we are going to see that with dark in  
action I'll just note that this tab in which I launched the Binder is up and running if you're going to execute code  
here click on notebooks click on Data Umbrella oop and then go to the overview notebook and you can drag around we'll  
see the utility of these these dashboards in a second but you can you know drag your stuff around to to make you know  
however you want to want to structure it and then you can execute code in here I'm not going to do that I'm going to do  
this locally at the moment but just to see dust in action to begin with I'm going to I'm actually going to  
 

#### 00:16:02,720::		4 minutes mark -> new paragraph 
 
restart kernel and clear my outputs so I'm going to import from dash distributed the client the sorry the other thing I  
wanted to mention is we made a decision around content for this we do have a notebook that we we love to teach on  
schedulers but we decided to switch it out for machine learning for this workshop in particular we are teaching a  
similar although distinct workshop at PyData global so we may see some of you there in which we'll be going more in  
depth into schedulers as well so if you want to check that out definitely do so we instantiate the client which as James  
mentioned is kind of what we work with as the user to submit our code so that will take take a few seconds OK it's got a  
port in you so it's going going elsewhere what I'll just first get you to notice is that it tells us where our dashboard  
is and we'll see those tools in a second tells us about our cluster that we have four workers eight cores between eight  
and nine gigs of of ram OK now this is something I really love about Dask all the diagnostic tools if I click on the  
little desk thing here and we've modified the Binder so that that exists there as well we can see I'll hit search and it  
should that now corresponds to the the scheduler now I want to look at the task stream which will tell us in real time  
what's happening I also want to look at the cluster map so we see here this is already really cool we've got all of our  
workers around here and our scheduler scheduler there and when we start doing some compute we'll actually see  
information flowing between these and the other thing maybe I'll yeah I'll include a little progress and that can be an  
alternate tab to ask I'm wondering perhaps I also want to include something about the workers yeah OK great so we've got  
a bunch of stuff that's that's pretty interesting there and so the next thing I'm going to do we've got a little utility  
file which downloads some of the data and this is what it does is if you're in Binder it downloads a subset of the data  
if you're anywhere else it loads a larger set for this particular example we're dealing with a small data set you see  
the utility of dark and distributed compute when it generalizes to larger data sets but for pedagogical purposes we're  
going to sit with a smaller data set so that we can actually run run the code there's a trade-off there so actually that  
was already downloaded it seems but you should all see it download I'm actually going to run that in the Binder just to  
you should start seeing downloading nyc flights data set done extracting creating json data etc OK now what we're going  
to do is we're going to read in this data as a Dask data frame and what I want you to notice is that it really the das  
code mimics Pandas code so instead of pd read csv we've got dd read csv we've got you know this is the file path the  
first argument we're doing some parse date setting some data types OK we've got a little wild card regular expression  
there to to join to do a bunch of them and then we're performing a group by OK so we're grouping by the origin of these  
flight flight data we're looking at the the mean departure delay group by origin the the one difference I want to make  
clear is that in das we need a compute method that's because das performs lazy computation it won't actually do anything  
because you don't want it to do anything on really large data sets until you explicitly tell it tell it to compute so  
I'm going to execute this now and we should see some information  
 

#### 00:20:01,520::		4 minutes mark -> new paragraph 
 
transfer between the scheduler and the workers and we should see tasks starting starting to be done OK so moment of  
truth fantastic so we call this a pew pew plot because we see pew pew pew we saw a bunch of data transfer happening  
between them these are all our cause and we can see tasks happening it tells us what tasks there are we can see that  
most of the time was spent reading reading csvs then we have some group bias on chunks and and that type of stuff so  
that's a really nice diagnostic tool to see what most of your work is is actually doing under dark work as you can see  
memory used CPU use more fine-grained examples there so I I'd love to know if in the Q&A I'm going to ask were you able  
to execute this code and if you were in Binder just a thumb up a vote would be no would be fantastic much appreciated so  
as we've mentioned I just wanted to say a few things about tutorial goals the goal is to cover the basics of dark and  
distributed compute we'd love for you to walk away with an understanding of when to use it when to not what it has to  
offer we're going to be covering the basics of Dask delayed which although not immediately applicable to data science  
provides a wonderful framework for thinking about Dask how dark works and understanding how it works under the hood then  
we're going to go into dark data frames and then machine learning hopefully due to the technical considerations with  
we've got less time than than we thought we would but we'll definitely do the best we can we may have less time to do  
exercises so we've had two people who are able to execute this code if you if you tried to execute it in Binder and were  
not able to perhaps post that in the Q&A but we also have several exercises and I'd like you to take a minute just to do  
this exercise the I I'm not asking you to do this because I want to know if you're able to print hello world I'm  
essentially asking you to do it so you get a sense of how these exercises work so if you can take 30 seconds to print  
hello world then we'll we'll move on after that so just take 30 seconds now and it seems like we have a few more people  
who are able to execute code which which was great OK fantastic so you will put your solution there for some reason I  
have an extra cell here so I'm just going to clip that and to see a solution I'll just get you to execute this cell and  
it provides the solution and then we can execute it and compare it to the the output of what you had OK hello world so  
as as we saw I've done all this locally you may have done it on Binder there is an option to work directly from the  
cloud and I'll I'll take you through this there are many ways to do this as I mentioned we're working on one way with  
coil and I'll explain the rationale behind that in in a second but I'll show you how easy it is to get a cluster up and  
running on on AWS without even interacting with AWS for free for example you can follow along by signing into coiled  
cloud to be clear this is not a necessity and it does involve you signing up to our product so I just wanted to be  
absolutely transparent about that it does not involve any credit card information or anything  
 

#### 00:24:01,520::		4 minutes mark -> new paragraph 
 
along those lines and in my opinion it does give a really nice example of how to run stuff on the cloud to do so you can  
sign in at cloud dot coiled dot io you can also pip install coiled and then do authentication you can also spin up this  
this hosted coiled notebook so I'm going to spin that up now and I'm going to post that here actually yep I'm gonna post  
that in the ch chat if you let me get this right if you've if you've never logged in to code before it'll ask you to  
sign up using gmail or GitHub so feel free to do that if you'd like if not that's also also cool but I just wanted to be  
explicit about that the reason I want to do this is to show how dars can be leveraged to do work on really large data  
sets so you will recall that I had between eight and nine gigs of ram on my local system oh wow Anthony says on ipad  
unable to execute on Binder incredible I don't have a strong sense of how Binder works on ipad I do know that I was able  
to to check to use a Binder on my iphone several years ago on my way to scipy doing code review for someone for Eric  
Maher I think for what that that's worth but back to this we have this nyc taxi data set which is over 10 gigs it won't  
even I can't even store that in local memory I don't have enough ram to store that so we do need either to do it locally  
in an out of core mode of some sort or we can we can burst to the cloud and we're actually going to burst to the cloud  
using using coiled so the notebook is running here for me and but I'm actually gonna do it from my local local notebook  
but you'll see and once again feel free to code along here it's spinning up a notebook and James who is is my co-  
instructor here is to be I'm I'm so grateful all the work is done on our notebooks in coiled you can launch the cluster  
here and then analyze the entire over 10 gigs of data there I'm going to do it here so to do that I import coiled and  
then I import the dash distributed stuff and then I can create my own software environment cluster configuration I'm not  
going to do that because the standard coiled cluster configuration software environment works now I'm going to spin up a  
cluster and instantiate a client now because we're spinning up a cluster in in the cloud it'll take it'll take a minute  
a minute or two enough time to make a cup of coffee but it's also enough time for me to just talk a bit about why this  
is important and there are a lot of a lot of good good people working on on similar things but part of the motivation  
here is that if you want to you don't always want to do distributed data science OK first I'd ask you to look at instead  
of using dark if you can optimize your Pandas code right second I'd ask if you've got big data sets it's a good question  
do you actually need all the data so I would if you're doing machine learning plot your learning curve see how accurate  
see how your accuracy or whatever your metric of interest is improves as you increase the amount of data right and if it  
plateaus before you get to a large data size then you may as well most of the time use your small data see if sub  
sampling can actually give you the results you need so you can get a bigger bigger access to a bigger machine so you  
don't have to burst to the cloud but after all these things if you do need to boast burst to the cloud until recently  
you've had to get an AWS account you've had to you know set up containers with docker and or Kubernetes and do all of  
these kind of  
 

#### 00:28:00,640::		4 minutes mark -> new paragraph 
 
I suppose devopsy software engineering foo stuff which which if you're into that I I absolutely encourage you encourage  
you to do that but a lot of working data scientists aren't paid to do that and I don't necessarily want to so that's  
something we're working on is thinking about these kind of one-click hosted deployments so you don't have to do all of  
that having said that I very much encourage you to try doing that stuff if if you're interested we'll see that the the  
cluster has just been created and what I'm going to do we see that oh I'm sorry I've done something funny here I'm I'm  
referencing the previous client anna James yeah it looks like you should go ahead and connect a new client to the coil  
cluster and making sure not to re-execute the cluster creation exactly so would that be how would I what's the call here  
I would just open up a new cell and say client equals capital client and then pass in the cluster like open parentheses  
cluster yeah great OK fantastic and what we're seeing is a slight version this we don't need to worry about this this is  
essentially saying that the environment on the cloud mis is there's a slight mismatch with my with my local environment  
we're fine with that I'm going to look here for a certain reason the the dashboard isn't quite working here at the  
moment James would you suggest I just click on this and open a new yeah click on the ecs dashboard link oh yes fantastic  
so yep there's some bug with the local dashboards that we're we're currently currently working on but what we'll see now  
just a SEC I'm going to remove all of this we'll see now that I have access to 10 workers I have access to 40 cores and  
I have access to over 170 gigs of memory OK so now I'm actually going to import this data set and it's the entire year  
of data from 2019 and we'll start seeing on on the diagnostics all the all the processing happening OK so oh actually  
not yet because we haven't called compute OK so it's done this lazily we've imported it it shows kind of like Pandas  
when you show a data frame the column names and data types but it doesn't show the data because we haven't loaded it yet  
it does tell you how many partitions it is so essentially and we'll see this soon das data frames correspond to  
collections of Pandas data frames so they're really 127 Pandas data frames underlying this task data frame so now I'm  
going to do the compute well I'm going to set myself up for the computation to do a group by passenger gown and look at  
the main tip now that took a very small amount of time we see the IPython magic timing there because we haven't computed  
it now we're actually going to compute and James if you'll see in the chat Eliana said her coil coiled authentication  
failed I don't know if you're able to to help with that but if you are that would be great and it may be difficult to  
debug in but look as we see we have the task stream now and we see how many you know we've got 40 cores working together  
we saw the processing we saw the bytes stored it's over 10 gigs as I said and we see we were able  
 

#### 00:32:01,519::		4 minutes mark -> new paragraph 
 
to do our basic analytics we were able to do it on a 10 plus gig data set in in 21.3 seconds which is pretty pretty  
exceptional if any any code based issues come up and they're correlated in particular so if you have questions about the  
code execution please ask in the Q&A not in the chat because others cannot vote it and I will definitively prioritize  
questions on technical stuff particularly ones that up that are upvoted but yeah I totally agree thanks thanks very much  
so yeah let's jump into into data frames so of course we write here that in the last exercise we used ask delayed to  
parallelize loading multiple csv files into a Pandas data frame we're not we we haven't done that but you can definitely  
go through and have a look at that but I think perhaps even more immediately relevant for a data science crowd and an  
analytics crowd is which is what I see here from the reasons people people have joined is jumping into Dask data frames  
and as I said before adas data frame really feels like a Pandas data frame but internally it's composed of many  
different different data frames this is one one way to think about it that we have all these Pandas data frames and the  
collection of them is a dark data frame and as we saw before they're partitioned we saw when we loaded the taxi data set  
in the dash data frame was 127 partitions right where each partition was a normal panda Pandas data frame and they can  
live on disk as they did early in the first example dark in action or they can live on other machines as when I spun up  
a coiled cluster and and did it on on AWS something I love about darth's data frames I mean I ran about this all the  
time it's how it's the Pandas API and and Matt Matt Rocklin actually has a post on on the blog called a brief history of  
Dask in which he talks about the technical goals of us but also talks about a social goal of task which in Matt's words  
is to invent nothing he wanted and the team wanted the Dask API to be as comfortable and familiar for users as possible  
and that's something I really appreciate about it so we see we have element element wires on operations we have the our  
favorite row eyes selections we have loc we have the common aggregations we saw group buyers before we have is-ins we  
have date time string accessors oh James we forgot to I forgot to edit this and I it should be grouped by I don't know  
what what a fruit buy is but that's something we'll make sure the next iteration to to get right at least we've got it  
right there and in the code but have a look at the dash data frame API docs to check out what's happening and a lot of  
the time dash data frames can serve as drop in replacements for Pandas data frames the one thing that I just want to  
make clear as I did before is that you need to call compute because of the lazy laser compute property of das so this is  
wonderful to talk about when to use data frames so if your data fits in memory use Pandas if your data fits in memory  
and your code doesn't run super quickly I wouldn't go to Dask I'd try to I'd do my best to optimize my Pandas code  
before trying to get gains gains and efficiency but dark itself becomes useful when the data set you want to analyze is  
larger than your machine's ram where you normally run into memory errors and that's what we saw  
 

#### 00:36:01,520::		4 minutes mark -> new paragraph 
 
with the taxicab example the other example that we'll see when we get to [music] machine learning is you can do machine  
learning on a small data set that fits in memory but if you're building big models or training over like a lot of  
different hyper parameters or different types of models you can you can parallelize that using using dark so there is  
you know you want to use dash perhaps in the big data or medium to big data limit as we see here or in the medium to big  
model limit where training for example takes and takes a lot of time OK so without further ado let's get started with  
das data frames you likely ran this preparation file to get the data in the previous notebook but if you didn't execute  
that now we're going to get our file names by doing doing a few joins and we see our file is a string data nyc flights a  
wildcard to access all of them dot dot csv and we're going to import our Dask dust.dataframe and read in our dataframe  
parsing some dates setting some sending some data types OK I'll execute that we'll see we have 10 partitions as we noted  
before if this was a Pandas data frame we'd see a bunch of entries here we don't we see only the column names and the  
data types of the columns and the reason is as we've said it explicitly here is the representation of the data frame  
object contains no data it's done Dask has done enough work to read the start of the file so that we know a bit about it  
some of the important stuff and then further column types and column names and data types OK but we don't once again we  
don't let's say we've got 100 gigs of data we don't want to like do this call and suddenly it's reading all that stuff  
in and doing a whole bunch of compute until we explicitly tell it to OK now this is really cool if you know a bit of  
Pandas you'll know that you can there's an attribute columns which prints out it's well it's actually the columns form  
an index right the Pandas index object and we get the we get the column names there cool Pandas in dark form we can  
check out the data types as well as we would in Pandas we see we've got some ins for the day of the week we've got some  
floats for departure time maybe we'd actually prefer that to be you know a date time at some point we've got some  
objects which generally are the most general on objects so generally strings so that's all pandasey type stuff in  
addition das data frames have an attribute n partitions which tells us the number of partitions and we saw before that  
that's 10 so I'd expect to see 10 here hey look at that now this is something that we talk about a lot in the delayed  
notebook is really the task graph and I don't want to say too much about that but really it's a visual schematic of of  
the order in which different types of compute happen OK and so the task graph for read csv tells us what happens when we  
call compute and essentially it reads csv 10 ten times zero indexed of course because Python it reads csv ten different  
times into these ten different Pandas Pandas data frames and if there were group buys or stuff after that we'd see them  
happen in in the in the graph there and we may see an example of this in a second so once again as with Pandas we're  
going to view the the head of the data frame great and we see a bunch of stuff you know we we see the first first five  
rows I'm actually also gonna gonna have a look at the  
 

#### 00:40:02,240::		4 minutes mark -> new paragraph 
 
the tail the final five rows that may take longer because it's accessing the the final I I there's a joke and it may not  
even be a joke how much data analytics is actually biased by people looking at the first five rows before actually you  
know interrogating the data more more seriously so how would all of our results look different if if our files were  
ordered in in a different way that's another conversation for a more philosophical conversation for another time so now  
I want to show you some computations with dark data frames OK so since dash data frames implement a Pandas like API we  
can just write our familiar Pandas codes so I want to look at the column departure delay and look at the maximum of that  
column I'm going to call that max delay so you can see we're selecting the column and then applying the max method as we  
would with Pandas oh what happened there gives us some da scala series and what's happened is we haven't called compute  
right so it hasn't actually done the compute yet we're going to do compute but first we're going to visualize the task  
graph like we did here and let's try to reason what the task graph would look like right so the task graph first it's  
going to read in all of these things and then it'll probably perform this selector on each of these different Pandas  
data frames comprising the dash data frame and then it will compute the max of each of those and then do a max on all  
those maxes I think that's what I would assume is happening here great so that's what we're what we're doing we're  
reading this so we read the first perform the first read csv get this das data frame get item I think is that selection  
then we're taking the max we're doing the same for all of them then we take all of these max's and aggregate them and  
then take the max of that OK so that that's essentially what's happening when I call compute which I'm going to do now  
moment of truth OK so that took around eight seconds and it tells us the max and I I'm sorry let's let's just get out  
some of our dashboards up as well huh I think in this notebook we are using the single machine scheduler Hugo so I don't  
think there is a dashboard to be seen exactly yeah thank you for that that that catch James great is even better James  
we have a question around using dark for reinforcement learning can you can you speak to that yeah so it depends on this  
I mean yeah short answer yes you can use GAs to train reinforcement learning models so there's a package that Hugo will  
talk about called desk ML that we'll see in the next notebook for distributing machine learning that paralyzes and and  
distributes some existing models using desks so for instance things like random forces forest inside kit learn so so yes  
you can use das to do distributed training for models I'm not actually sure if GAskml implements any reinforcement  
learning models in particular but that is certainly something that that can be done yeah and I'll I'll build on that by  
saying we are about to jump into machine  
 

#### 00:44:00,000::		4 minutes mark -> new paragraph 
 
learning I don't think as James said I don't think there's reinforcement learning explicitly that that one can do but  
you of course can use the das scheduler yourself to you know to distribute any reinforcement learning stuff you you have  
as well and that's actually another another point to make that maybe James can speak to a bit more is that the dark team  
of course built all of these high-level collections and task arrays and dust data frames and were pleasantly surprised  
when you know maybe even up to half the people using dust came in all like we love all that but we're going to use the  
scheduler for our own bespoke use cases right yeah exactly yeah the original intention was to like make basically a num  
like a parallel numpy so that was like the desk array stuff like run run numpy and parallel on your laptop and and yeah  
so in order to do that we ended up building a distributed scheduler which sort of does arbitrary task computations so  
not just things like you know parallel numpy but really whatever you'd like to throw at it and it turns out that ended  
up being really useful for people and so yeah now people use that sort of on their own just using the distributed  
scheduler to do totally custom algorithms in parallel in addition to these like nice collections like you saw Hugo  
presents the dash data frame API is you know the same as the panda's API so there is this like familiar space you can  
use things like the high-level collections but you can also run whatever custom like Hugo said bespoke computations you  
might have exactly and it's it's been wonderful to see so many people so many people do that and the first thing as  
we'll see here the first thing to think about is if if you're doing lifestyle compute if there's anything you can you  
know parallelize embarrassingly as they say right so just if you're doing a hyper parameter search you just run some on  
one worker and some on the other and there there's no interaction effect so you don't need to worry about that as  
opposed to if you're trying to do you know train on streaming data where you may require it all to happen on on on the  
same worker OK yeah so even think about trying to compute the standard deviation of a of a a univariate data set right  
in in that case you can't just send you can't just compute the standard deviation on two workers and then combine the  
result in some some way you need to do something slightly slightly more nuanced and slightly slightly clever more clever  
I mean you still can actually in in that case but you can't just do it as naively as that but so now we're talking about  
parallel and distributed machine learning we have 20 minutes left so this is kind of going to be a whirlwind tour but  
you know whirlwinds when safe exciting and informative I just want to make clear the material in this notebook is based  
on the open source content from darsk's tutorial repository as there's a bunch of stuff we've shown you today the reason  
we've done that is because they did it so well so I just want to give a shout out to all the das contributors OK so what  
we're going to do now is just break down machine learning scaling problems into two categories just review a bit of  
psychic learn in passing solve a machine learning problem with single Michelle single Michelle I don't know who she is  
but single Michelle wow single machine and parallelism with psychic learning job lib then solve an l problem with an ML  
problem with multiple machines and parallelism using dark as well and we won't have time to burst for the cloud I don't  
think but you can also play play around with that OK so as I mentioned before when thinking about distributed compute a  
lot of people do it when they have large data they don't necessarily think about the large model limit and this  
schematic kind of speaks to that if you've got a small model that fits in ram you don't need to think about  
 

#### 00:48:00,480::		4 minutes mark -> new paragraph 
 
distributed compute if your data size if your data is larger than your ram so your computer's ram bound then you want to  
start going to a distributed setting or if your model is big and CPU bound such as like large-scale hyper-parameter  
searches or like ensembl blended models of like machine learning algorithms whatever it is and then of course we have  
the you know big data big model limit where distributed computer desk is incredibly handy as I'm sure you could imagine  
OK and that's really what I've what I've gone through here a bird's-eye view of the strategies we think about if it's in  
memory in the bottom left quadrant just use scikit-learn or your favorite ML library otherwise known as psychic learn  
for me anyway I was going to make a note about xg boost but I but I won't for large models you can use joblib and your  
favorite circuit learn estimator for large data sets use our dark ML estimators so we're gonna do a whirlwind tour of  
psychic learn in in five minutes we're going to load in some data so we'll actually generate it we'll import scikit-  
learn for our ML algorithm create an estimator and then check the accuracy of the model OK so once again I'm actually  
going to clear all outputs after restarting the kernel OK so this is a utility function of psychic learn to create some  
data sets so I'm going to make a classification data set with four features and 10 000 samples and just have a quick  
view of some of it so just a reminder on ML x is the samples matrix the size of x is the number of samples in terms of  
rows number of features as columns and then a feature or an attribute is what we're trying to predict essentially OK so  
why is the predictor variable which we're where which we're or the target variable which we're trying to predict so  
let's have a quick view of why it's zeros and ones in in this case OK so yep that's what I've said here why are the  
targets which are real numbers for regression tasks or integers for classification or any other discrete sets of values  
no words about unsupervised learning at the moment we're just going to support we're going to fit a support vector  
classifier for this example so let's just load the appropriate scikit-learn module we don't really need to discuss what  
support vector classifiers are at the moment now this is one of the very beautiful things about the scikit-learn API in  
terms of fitting the the model we instantiate a classifier and we want to fit it to the features with respect to the  
target OK so the first argument is the features second argument is the target variable so we've done that now I'm not  
going to worry about inspecting the learn features I just want to see how accurate it was OK and once we see how  
accurate it was I'm not gonna do this but then we can make a prediction right using estimator dot predict on a new a new  
data set so this estimator will tell us so this score will tell us the accuracy and essentially that's the proportion or  
percentage a fraction of the results that were that the estimator got correct and we're doing this on the training data  
set we've just trained the model on this so this is telling us the accuracy on the on the training data set OK so it's  
90  
 

#### 00:52:01,760::		4 minutes mark -> new paragraph 
 
accurate on the training data set if you dive into this a bit more you'll recognize that if we we really want to know  
the accuracy on a holdout set or a test set and it should be probably a bit lower because this is what we use to fit it  
OK but all that having been said I expect you know if if this is all resonating with you it means we can really move on  
to the distributed stuff in in a second but the other thing that that's important to note is that we've trained it but a  
lot of model a lot of estimators and models have hyper parameters that affect the fit but you that we need to specify up  
front instead of being learned during training so you know there's a c parameter here there's a are we using shrinking  
or not so we specify those we didn't need to specify them because there are default values but here we specify them OK  
and then we're going to look at the score now OK this is amazing we've got 50 accuracy which is the worst score possible  
just think about this if if you've got binary classification task and you've got 40 accuracy then you just flip the  
labels and that changes to 60 accuracy so it's amazing that we've actually hit 50 accuracy we're to be congratulated on  
that and what I want to note here is that we have two sets of hyper parameters we've used one's created 90 actual model  
with 90 accuracy another one one with 50 accuracy so we want to find the best hyper parameters essentially and that's  
why hyper parameter optimization is is so important there are several ways to do hyper parameter optimization one is  
called grid search cross validation I won't talk about cross validation it's essentially a more robust analogue of train  
test split where you train on a subset of your data and compute the accuracy on a test on a holdout set or a test set  
cross validation is a as I said a slightly more robust analog of this it's called grid search because we have a grid of  
hyper parameters so we have you know in this case we have a hyper parameter c we have a hyper parameter kernel and we  
can imagine them in a in a grid and we're performing we're checking out the score over all this gr over this entire grid  
of hyper parameters OK so to do that I import grid search csv now I'm going to compute the estimator over over these  
train the estimator over over this grid and as you see this is taking time now OK and what I wanted to make clear and I  
think should be becoming clearer now is that if we have a large hyper parameter sweep we want to do on a small data set  
das can be useful for that OK because we can send some of the parameters to one worker some to another and they can  
perform them in parallel so that's embarrassingly parallel because you're you're doing the same work as you would  
otherwise but sending it to a bunch of different workers we saw that took 30 seconds which is in my realm of comfort as  
a data scientist I'm happy to wait 30 seconds if I had to wait much longer if this grid was bigger I'd start to get  
probably a bit frustrated but we see that it computed it for c is equal to all combinations of these essentially OK so  
that's really all I wanted to say there and then we can see the best parameters and the best score so the best score was  
0.098 and it was c10 and the kernel rbf a radial basis function it doesn't even matter what that is though for the  
purposes of this so we've got 10 minutes left we're going to we're going to make it I can feel it I have a good I have a  
good sense  
 

#### 00:56:00,400::		4 minutes mark -> new paragraph 
 
 a good after the I mean this demo is actually going incredibly well given the initial technical hurdles so touchwood  
Hugo OK so what we've done is we've really segmented ML scaling problems into two categories CPU bound and ram bound and  
I I really I can't emphasize that enough because I see so many people like jumping in to use new cool technologies  
without perhaps taking it being a bit mindful and intentional about it and reasoning about when things are useful and  
and when not I suppose the one point there is that sure data science is a technical discipline but there are a lot of  
other aspects to it involving this type of reasoning as well so we then carried out a typical sklearn workflow for ML  
problems with small models and small data and we reviewed hyper parameters and hyper parameter optimization so in this  
section we'll see how job lib which is a set of tools to provide lightweight pipelining in Python gives us parallelism  
on our laptop and then we'll see how dark ML can give us awesome parallelism on on clusters OK so essentially what I'm  
doing here is I'm doing exactly the same as above with a grid search but I'm using the quark the keyword argument n jobs  
which tells you how many tasks to run in parallel using the cause available on your local workstation and specifying  
minus one jobs means the it just runs them the maximum possible OK so I'm going to execute that great so we should be  
done in a second feel free to ask any questions in the chat oh alex has a great question in the Q&A does das have see a  
sequel and query optimizer I'm actually so excited that [music] and James maybe you can provide a couple of links to  
this we're really excited to have seen dark dust SQL developments there recently so that's dark hyphen hyphen SQL and  
we're actually we're working on some some content and a blog post and maybe a live live coding session about that in in  
the near future so if anyone if you want updates from from coyle feel free to go to our website and sign up for our  
mailing list and we'll let you know about all of this type of stuff but the short answer is yes alex and it's getting  
better and if James is able to post post a link there that would be that would be fantastic so we've done link in the  
chat fantastic [music] and so we've we've seen how we have [music] single machine parallelism here using the using the  
end jobs quark and in the final minutes let's see multiple multi-machine parallelism with Dask OK so what I'm going to  
do is I'm going to do my imports and create my client incentive my client and check it out OK so once again I'm working  
locally I hit search and that'll task is pretty smart in terms of like knowing which which client I want to check out do  
the tasks stream because it's my favorite I'll do the cluster map otherwise known as the pew pew map and then I want  
some progress we all we all crave progress don't we and maybe my workers tab OK great so we've got that up and running  
now I'm going to do a slightly larger hyper parameter search OK so remember we had just a couple for c a couple for  
kernel we're going to do more we have some for shrinking now I'm actually going to comment that out because I don't know  
how long that's going to take if you're coding them on Binder now this May actually take far far too long for you but  
we'll we'll see so I'll execute this code and we should see just sick no we shouldn't see any work happening yet but  
what I'm doing here is oh looks like OK my clusters back up great we're doing our grid search but we're going to use  
Dask as as the back end right and this is a context manager where we're asserting that and and we can just discuss the  
the syntax there but it's not particularly important currently I'm going to execute this now and let's see fantastic  
we'll see all this data transfer happening here we'll see our tasks happening here we can see these big batches of fit  
and score fit so fitting fitting the models then finding how well they perform via this k-fold cross validation which is  
really cool and let's just yep we can see what's happening here we can see we currently have 12 processing we've got  
seven in memory and we have several more that we need to do our desk workers we can see us oh we can see our CPU usage  
we can see how we can see CPU usage across all the workers which is which is pretty cool seeing that distribution is is  
really nice whenever some form of b swarm plot if you have enough would would be useful there or even some form of  
cumulative distribution function or something like that not a histogram people OK you can go to my bayesian tutorial  
that I've taught here before to hear me rave about the the horrors of histograms so we saw that talk a minute which is  
great and we split it across you know eight cores or whatever it is and now we'll have a look once again we get the same  
best performer which is which is a sanity check and that's pretty cool I think we have a we actually have a few minutes  
left so I am gonna just see if I can oh let me think yeah I will see if I can burst burst to the cloud and and and do  
this that will take a minute a minute or two to create the cluster again but while we're while we're doing that I'm  
wondering if we have any any questions or if anyone has any feedback on on this workshop I very much welcome welcome  
that perhaps if there are any final messages you'd you'd like to say James while we're spinning this up you can you can  
let me know yeah sure I just also first off wanted to say thanks everyone for attending and like bearing  
 

#### 01:04:01,119::		4 minutes mark -> new paragraph 
 
bearing with us with the technical difficulties really appreciate that real quick I'm just yeah so if you have if you  
have questions please post in the Q&A section while the cold cluster's spinning up theodore posted in the last largest  
example of grid search how much performance gain did we get from using das and not just in jobs hmm that's a great  
question and we actually didn't see let's see so it took 80 seconds ah let me get this they're actually not comparable  
because I did the grid search over a different set of hyper parameters I did it over a larger set of hyper parameters  
right so when I did end jobs I did it there were only it was a two by two grid of hyper parameters whereas when I did it  
with with Dask it was a one two three four five six six by three so let's just reason about that this one was eighteen  
six by three is eighteen which took eighty seconds and this one was two by two so it was four and it took 26 seconds so  
a minor gain I think with this hyper parameter search if you multiply that by by four you'll well 4.2 4.5 you'll need  
that would have taken maybe two minutes or something something like that so we saw some increase in efficiency not a  
great deal but James maybe you can say more to this part of the reason for that is that we're doing it on kind of a very  
small example so we won't necessarily see the gains in efficiency with a data set this size and with a small hyper  
parameter suite like this is that right yeah yeah and yeah exactly and I guess also this is more of an kind of an  
illustrative point here I guess so you're just using directly using in jobs with something like job lib by default we'll  
use local threads and processes on like whatever machine you happen to be running on so like in this case on Hugo's  
laptop one of the real advantages of using job lib with the das back in will actually dispatch back to to run tasks on a  
dash cluster is that your cluster can expand beyond what local resources you have so you can run you know you can  
basically scale out like for instance using the coil cluster to have many many CPUs and a large amount of ram that you  
wouldn't have on your locally table to run and there you'll see both large performance gains as well as you'll be able  
to expand your the set of possible problems you can solve to larger than ram scenarios so you're out of out of core  
training exactly and thank you Jack this was absolutely unplanned and we didn't plan that question but that's a  
wonderful segue into me now performing exactly the same compute with the same code using the dasc as the parallel back  
end on a on a coiled cluster which is an AWS cluster right so we can I'm more currently anyway so I will execute this  
code and it's exactly the same as we did whoa OK great so we see our tasks task stream here you see once again we see  
the majority is being batch fit and and getting the scores out similarly we see the same result being the best I'll just  
notice that for this for this small task doing it on the cloud took 20 seconds doing it locally for me took 80 seconds  
so that's a four-fold increase in performance on a very small task so imagine what that does if you can take the same  
code as you've written  
 

#### 01:08:00,240::		4 minutes mark -> new paragraph 
 
here and burst to the cloud with with one click or however however you do it I think that that's incredibly powerful and  
that the fact that your code and what's happening in the back end with Dask generalizes immediately to the new setting  
of working on a cluster I personally find very exciting and if you work with larger data sets or building larger models  
or big hyper parameter sweeps I'm pretty sure it's an exciting option for all of you also so on that note I'd like to  
reiterate James what James said and thanking you all so much for joining us for asking great questions and for bearing  
with us through some some technical technical hurdles but it made it even even funner when when we got up and running  
once again I'd love to thank Mark Christina and and the rest of the organizers for doing such a wonderful job and doing  
such a great service to the data science and machine learning community and ecosystem worldwide so thank you once again  
for having us thank you Hugo and James I have to say like with all the technical difficulties I was actually giggling  
because it was kind of funny yeah but we're very sorry and we thank you for your patience and sticking through it and I  
will be editing this video to you know make it as efficient as possible and have that available Tim supercard thank you  
great and I'll just ask you if you are interested in checking out coiled go to our website if you want to check out our  
product go to cloud.coil.io we started building this company in February we're really excited about building a new  
product so if you're interested reach out we'd love to chat with you about what we're doing and what we're up to and  
it's wonderful to be in the same community as you all so thanks  
 
