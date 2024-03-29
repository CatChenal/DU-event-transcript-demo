# Thomas Fan: Streamlit for Data Science

## Key Links
- Meetup Event:  https://www.meetup.com/data-umbrella/events/274110563/
- Video:  https://youtu.be/5TCdoWemSXI  
- Slides:  N.A.  
- GitHub Repo:  https://github.com/thomasjpfan/data-umbrella-2020-streamlit-ml
- Jupyter Notebook:  N.A. 
- Transcriber:  ?

## Video

<a href="http://www.youtube.com/watch?feature=player_embedded&v=5TCdoWemSXI" target="_blank">
    <img src="http://img.youtube.com/vi/5TCdoWemSXI/0.jpg"
         alt="Thomas Fan: Using Streamlit for Data Science"
         width="25%" /></a>

<iframe width="560" height="315" 
        src="https://www.youtube-nocookie.com/embed/5TCdoWemSXI?cc_load_policy=1&autoplay=0" 
        frameborder="0">
</iframe>

## Transcript

### Introduction
<!-- Editing Guide: The pipe (|) position in this comment is 120:                                                       | -->

Hello everyone and welcome to Data Umbrella's webinar I'm going to do a brief presentation I'm going to do a quick  
introduction the talk is going to be there and we are going to have a Q&A at the end this talk is being recorded if you  
have any questions there's a Q&A tab on this platform so if you could post questions there that's a good place to  
aggregate them if you happen to place them in the chat I can also easily you know transfer them over to Q&A but it is  
easier if you post them in the Q&A tab this webinar is being recorded a little bit about me briefly I'm a statistician  
data scientist I'm a founder I am the founder of Data Umbrella and I am on Twitter LinkedIn and GitHub as Reshama so  
feel free to follow me if you would like we have a code of conduct we're quite strict with our code of conduct because  
one of the reasons that this community was created is to provide a safe and inclusive environment for people from  
underrepresented groups we take our code of conduct very seriously in fact at our last session somebody posted something  
quite inappropriate in the chat and they're you know they're no longer part of the group so please please you know  
really take this seriously and you know this May not be for everybody but this is sort of the agreements that we have as  
a community to make it professional and inclusive and welcoming for people we are also a volunteer-run organization  
there are numerous ways that you can support Data Umbrella the first and foremost one is to follow our code of conduct  
and contribute to making it welcoming collaborative and professional the second is we have a discord community chat it's  
on our website so feel free to join there and ask and answer questions there we have an open collective of for Data  
Umbrella so if you would like to donate to support us to pay our meet up dues and other expenses that would be great and  
we have an initiative an open source initiative for editing transcripts for these webinars to make them accessible this  
is the GitHub URL for that and feel free to check it out and email us and ask any questions we have we have a bunch of  
people that are working on transcripts as well we have a job board as well which is jobs.org so if you are in the market  
looking for a job feel free to check it out and also there's an option to subscribe to a weekly digest our website has a  
plethora of resources on accessibility diversity responsibility ally ship please check it out at your convenience we  
also have a newsletter which goes out once a month it's you can find it at dataumbrella.stopstack.com we promise not to  
spam you we only send the newsletter out once a month so it's a it's another way to get information about our group we  
are on all social media platforms as Data Umbrella Meetup is the best place to find out about upcoming events our  
website has resources we have Twitter LinkedIn and YouTube if you want to subscribe to YouTube we record all of our  
webinars and post them on YouTube so that's a good place to check out our previous webinars this webinar and upcoming  
ones so in December we have two events contributing to numpy and contributing to Pandas they have not yet been posted on  
Meetup but they will be soon and the best way as I said before join our Meetup group to receive updates today's speaker  
is Thomas fan who is a core developer of scikit-learn he is also a staff associate at the data science institute at  
columbia university and Thomas maintains scorch which is a scikit-learn compatible neural network library that wraps  
around  
 

#### 00:04:01,200::		4 minutes mark -> new paragraph 
 
PyTorch I also want to say that you know Thomas is with the Meetup group there's a New York Python Meetup group in  
fact that's where Thomas introduced me and others to streamline and I reached out and asked him well this is really  
great would you present for us and he said yes so thank you and with that I will keep my fingers crossed and hope that  
can share his screen and get started thank you I'm gonna press this button and see what happens wow all right hi  
everyone good rasheen Reshama can you see the slides yes I can I just turned up mike but yes OK good all right  
welcome everyone today I want to talk to you about streamlets using streamlight for data science most of this is going  
to be a demo of many demos and I'm going to showcase how one could use streamlets to make dashboards so what is  
streamlit streamlets the way I see streamla is that it's a it makes it so that you could quickly create dashboards or  
applications while staying in Python so the workflow looks kind of something like this where you have code on one side  
and then you have something that auto updates when you save your code on the left so this is I'm going to showcase how  
this works in in this talk so most of this talk is demo so I'm gonna provide three demos they get progressively more  
advanced the first one will be something it will showcase streamlight as a library and how it interacts with pac  
plotting libraries and then I'm gonna get into some data science I'm gonna train a model on the data set that we looked  
at from the first demo and then we're gonna train a model in Jupyter notebook in my case Jupyter lab and at the end I'm  
gonna build a dashboard that explains that does local explanations for the predictions of the model I've trained in step  
two in streamlit so as a like as a sample you could so the first thing we're going to build looks it's going to look  
like this you're going to have you know buttons show me penguins and then there's gonna be some graphs plots and yeah  
that we're gonna see how to how we could integrate streamlight with Matplotlib Seaborn and Plotly if you're so and it  
also integrates with other planning libraries but in this talk we're going to we're going to look at those three and  
afterwards we're going to do we're going to have a dashboard we're going to create a dashboard that does explanations of  
predictions in this case predicting the penguin species these cute little penguins we're going to make a model to  
predict them based on features of the penguin and we're going to have explanations about them so let's jump into it so  
it's most of all the material for this is gonna be in the link I'm gonna we're gonna provide it I'm gonna write it in  
the chat and we're gonna and I'm going to private in the description video I'm hoping so the first thing you do to start  
this up is that I'm going to start from from scratch there's going to be nothing in my editor and I'm gonna have a  
terminal window that's that's also here all I have in this folder is some images of the penguins and yeah so I'm gonna  
follow them as an instruction while starting any Python project I'm going to I'm going to create a environment I will  
 

#### 00:08:02,400::		4 minutes mark -> new paragraph 
 
erase that one up huh OK cool so I want to build that the the penguins thing that we have before and I'll show you how  
to do it from the beginning I'm going to have some imports OK cool that's good I'm going to have some imports and then  
like every time I save would update by itself so in this case if I have a title that is something that is show me the  
penguins what I see all right so to run OK so the first thing is all right let me start from the beginning the first  
thing is to run streamlets you need to install the install the libraries that I had in my repo and then you run this  
command called streamlight run and I'm going to put an extra command that says run on save which tells streamlight to  
rerun the application reload every time I save so I'm going to go quickly through this because we had some technical  
issues but we could we'll make it together all right so in this case I want to show me the penguins so when I saved it  
it was it updates the title if I if I don't say sum and I save you see that auto updates as well so this is very  
interactive and I find this very powerful because now I could interactively create interactions such as like let's say I  
want to create a dialog box a radio box I input this I put this in the code and then I could when I save it it it auto  
updates the dashboard in the web in the application so in this case it allows me to select a penguin so this is sc.radio  
and if I print out this species you see that this radio when when I set the radio through the ui it auto updates the  
species in the program itself so in this case I am outputting the species so in this case I have images of the species  
so I could showcase the images like this using Python's f strings and so if when I click on this thing it auto-updates  
to these cute little penguins and so it's very cool so I'm writing pure Python and it auto updates the dashboard without  
without me writing any JavaScript or any yeah so I can stay in pure Python so here I'm going to create a dictionary and  
I want to link it I want to link my species to to the Wikipedia page and I could write peer Markdown so I could write  
some Markdown and I'd use f strings and then it'll give me this this header this header that links to different that  
links to different penguins and so off so if I if I click if I click on ghetto and I click on Wikipedia page it will  
link to the Wikipedia page for the penguin so that's pretty cool now if I try to do eda I have a data set in this folder  
that loads the data set that loads the data I could look at the data like if I want to see the data I could just write  
penguins it would show me the panel's data frame as a rendered HTML so which is so you can see the different features  
you can see the species you can see how big the beef the beak is or the  
 

#### 00:12:02,639::		4 minutes mark -> new paragraph 
 
or the flipper length is and so forth so you can look at the data so if we have any questions we want to ask about the  
data set because let's say you have a question about the inside they say how many how many species are there in our data  
set so you see that I I I put the question in the as a header and then it shows me in the dashboard now so one way to  
answer this is to use use Pandas so you could do you could say the value counts so I could have a penguin's value count  
here and then so this will give me the value count for each species so so it will show me the panel the data frame and  
if I ever want to plot if I want to plot this I could use the Pandas API to plot like so so this will this this will  
help me plot but there's no access so I'm going to create an axis because so this is for those who are familiar with the  
Matplotlib API this will help plot and then for streamlit I have to create I use the map API to create a figure I pass  
the access to the plotting API in Pandas and this will quickly so in three lines of code I could create a bar plot  
showing how many species are there per data set now if I want to answer questions like can what's the flipper length  
could the Fibonacci be used to distinguish between the species and in the aspects just so we could get to the next in  
the we could we could use like we could use in this case Seaborn and Seaborn uses the map pilot bpi so in this case I  
could use this which is this is a new function called the disk plot which plus distributions and I could give it it it's  
very you I could give it different features in the data set and it will help plot it I could give the hue in this case  
species in this case you can see that there's difference that the flipper length could distinguish between the blue  
species and then the green one so so this is an example of using streamlights but with the streamlight API with the  
streamlab API with Matplotlib for those who like Plotly for those who like Plotly we we could have something we can  
answer another question is the human which is the the length of the the beak could that you use to classify species we  
could do a scatter plot and Plotly where in this case I plus I could place x and x and y as the lengths OK so if I  
comment these out you see that auto updates so that the marginals disappear and if I if I add these marginals back in  
you can see that it auto updates and adds a marginal back into my dashboard so this is this allows us to very quickly  
iterate on our visualizations such that yeah so it allows you very quickly early on iteration on our visualizations  
another way another question you asked is how is the body mass for each species distribute it you could use the box plot  
and same thing for those familiar with the plot API this would help in this case I'm applying the species on the x-axis  
and then the body mass on the y-axis and the colors are the gender you can see that if I like yeah so I could remove the  
the  
 

#### 00:16:00,480::		4 minutes mark -> new paragraph 
 
gender piece and it will plot a box plot with the with the genders combined and if I wanted to separate by the gender we  
could separate by just having the color be gender so this is very I'm so this talk is about some streamline so if you  
remember the plot API you could do this with the box and plotting so so this first example showcases how you could you  
extremely could interact with your deploying libraries that you're used to in this case if you use a plot Matplotlib  
Seaborn or Plotly you could use streamlight to showcase your images without and while you're staying in Python so you  
see that this is I'm just writing Python code and it's outputting me a dashboard interactively which is very powerful so  
this is the big thing about this is that you see that every time I create a figure for me to output it to output the  
figure in the dashboard I have to I I'm just I'm placed I'm placing the item on its own line so in this case scatter  
created an object called scat and then I'm to for it to be outputted into the dashboard I write scat by itself in this  
case so that would so streamlab will know to render this object in the dashboard so that that's that is like the basic  
it's very a fairly basic way to use streamlit just for data visual editions me personally I like having questions before  
a visualization because the the question the visualization should answer a question so having its question driven  
visualizations in my mind OK in the interest of time I want to look at the data science piece so the first part of  
data science is to visualize here to do some exploratory data analysis and this is something we've done this on the  
penguin data set the goal of the the model I'm going to create in the Jupyter notebook would be to use the features that  
we looked at to predict the species of the penguin so I'm going to create a very quick model using scikit-learn and I'm  
going to showcase how to create a dashboard around this model so this is so I'm so I'm a data scientist I'm in my  
jubilee notebook I I launched my junior notebook I'm gonna load the I'm gonna load the data the same penguins data set  
we had before I'm gonna have my x values which is my features and my y which is my labels in this case the labels are  
the penguin species I know I'm going to create a pipeline a cycle and pipeline where I'm going to encode the categorical  
features and I'm going to do nothing to the miracle features I do nothing to numerical features in this case because I  
know I'm going to push this into a random forest which doesn't require your numerical features to be scaled so it could  
just take in the miracle features as is so if I create this pipeline you see that in the juvenile notebook this is a  
newish feature in cycle learn it it outputs the visualization of the pipeline so you can see how the data flows through  
a cycle and pipeline and this is enabled by by setting this configuration set config where display equals to diagram all  
this material will be in the repo so you can follow this in when you have time to look over the the material for this  
talk so in this case it will output this visualization in the jubilee notebook now to we're going to train and value the  
model so in this case we're going to do a train that split because we are good data scientists and we're going to train  
on a training set and evaluate on a test set so in this case  
 

#### 00:20:00,799::		4 minutes mark -> new paragraph 
 
this model is pretty good it's it's has 98 accuracy if accuracy is a good metric in this case for for time being  
accuracy accuracy is OK in our case and now we're going to serialize the model so this is going to create a serialized  
version of the model we just trained now so I don't wanna this talk doesn't revolve around cycle learn so let's jump  
back into streamlit so we create so we use Jupyter notebook now we have to build the machine learning model now we want  
to as a we want to build this thing like this like this thing looks supe like very complicated there's two libraries  
there's two separate libraries in here there's a shaft value there's a shaft I use the shaft library to crack the shaft  
values and I use the anchors library to calculate the anchors the shaft values is like a game theory concept where when  
you have many players trying to accomplish a task you want to see how much credit you allocate to each player in this  
case the players are the features and the task is to make is the prediction so how much does each feature contribute to  
each prediction and that's chat values in a nutshell we're gonna and anchors is we're just we're talking about anchors  
when we get to the dashboard and when we develop the dashboard the surprising thing about this dashboard is that it this  
this this whole dashboard takes around a hundred ish lines of code so like it's so because stream allows like extremely  
allows us to create these very interactive dashboards with very few lines of code and you get to stay in Python so I'm  
going to start this from scratch as well let's let's try it alright so that was my intro so my intro was this thing it's  
very quick let's try another one so in this case I'm going to stop that server in this case I'm going to run streamlit  
on the explain so in this case it will run it will open a new thing and and of course it's empty because there's nothing  
in my file so let's start this off so in this case I'm gonna have imports we're gonna use a bunch of these things and  
just like before I'm gonna have some categories I'm gonna have the features just so this is similar in the juvenile  
notebook and I'm gonna have my data my penguin data so just to see some output if I output x you see that the the  
penguins data set is here if I if I output y it's it's the species names so it's all here so for this specific dashboard  
I'm going to need some I want the user to as you can see before I want to I want the user to specify the island and the  
gender and then and I wanted the user to specify some pieces about the I want the user to give me an instance and I want  
my dashboard to explain why my model made this prediction so remember this is x this is explaining the machine learning  
model so I'm going to go through how to build this in streamlit so in the future I'm going to need some of these these  
metadata metadata about my my data set in this case it's very these are very simple the metadata is just the the  
categories for the island category and then the gen the categories for the gender and also I wanted I want the min max  
of each of my numerical features which I'm going to use later  
 

#### 00:24:01,520::		4 minutes mark -> new paragraph 
 
when I set up this this this this interactive selector because I don't want I don't want the user to input a number that  
is outside the bounds of what what's outside the bounds of I want I don't usually put things outside the balance of the  
the data set so so I've saved the minimum vaccine values for the miracle features so to create the video I the radio  
item the radio the thing on the radio selector I'm going to try I'm going to do one first so sidebar that radius I don't  
want to create let me let's let's not do the sidebar yet let's do the radio and here I want to do select and let's say I  
want to select all right so I want to select let's say the cumin length all right actually let's do the island the  
island first select island so if I do this I could since I have the metadata I could do something like this and this  
will create this select item thing but as you can see from here I put this in the sidebar so if I wanted it to be in the  
sidebar I could do instead of sc.radio I do sc.bar sidebar and this will place it on a sidebar so so all all the  
interactions you could place on a sidebar by by preferencing the call by with the word sidebar so in this and this this  
is normal Python and if I want to do many of these let's say I have two of them in this case I could use normal Python  
to write a loop and in this case I want to store the user input into a list so I'm writing normal Python on the left and  
it's outputting java's interactive JavaScript on the right so in this case at this point if I output the user input I  
could see that when I move the metadata I could see that if I change this to male you can see that the user input  
changed to male if I change this island to this island the use input changes so the Python is updating every time I  
interact with the ui which is pretty neat in the interest of time I'm going to quickly look at also look at the  
numerical features in this case the numeric features I have a number input and I'm going to I want these step boxes to  
give me to go up and down in this case so in this case I'm using a sidebar numerical input and which allows me to have  
numerical boxes for the for the user to put in their numerical values and in this case so then you see how the input  
changes as I update these values you see that now it's 202 202 while this is chosen to 202 and I'm going to place this  
in a data frame so if I output the data frame it also also outputs the data frame and I could change this and you see  
how I change it to the female and this change to female OK so this is loading in the data from the user now remember  
we have a a model that we trained it's called penguin underscore clt.job lib so this is the model we could use this to  
make a prediction in the interest of time I will showcase pieces of this in this case on cycle learn you call predict to  
get the prediction of your classifier and and I also want which clash is predicted so this code will help me grab what  
class this my model predicted for this  
 

#### 00:28:01,120::		4 minutes mark -> new paragraph 
 
specific instance in this case I picked this species I could also get the probability by calling predict prabha oh I  
already did that and then at the end over here you can see that I have the probabilities of each species for my  
classifier in this case you see that chin trap has the highest probability so that's the prediction made by the made by  
the the model so remember if you go back you see that I have all this the sharp value stuff here let's quickly look at  
that as well in this case I want to create I want to I want to create some ui some headings for what is what is I make  
what explanation I'm explaining I have the sharp values and since the library doesn't interact well with pipelines  
there's we have to encode our data in using a piece of my of the pipeline so this is cycler and esque but it's still  
Python and and the way so I'm in this case I'm in this case I'm importing the shaft library with tree explainer and if I  
OK so this is fairly involved and I don't have too much time so I'm gonna try to get through this in this case I know  
I call force plot which expects the expected value the shaft values using coded which is the encoding of the this data  
by the pipeline and the thing about this is that this library was built in such a way that it wants the JavaScript to be  
loaded first so one way to do this is to grab the JavaScript first and then directly place it into the HTML so like this  
is like because stream it doesn't understand this library directly like there's there's ways to get around this by  
inputting the JavaScript yourself which allows us to write Python like so what this took what this took to embed this  
shap values into the javas into the dashboard was 20-ish lines of 50 lines of Python which is I I still find very cool  
so yeah so let's get to the anchors anchors is even semi-simpler anchors also doesn't ex anchors is built in such a way  
that it expects numpy arrays so in this case I'm gonna create this angular explain object and they have this interface  
where you want to explain an instance and and if I want the HTML version of this I call as HTML and then it will output  
this this anchor explanation the cool thing about the anchor explanation is is that a good thing about the angry  
explanation is that it could explains your instance in a very specific way using anchors where an anchor explanation is  
a rule that sufficiently anchors the prediction locally such that the changes to the rest of the future values of the  
instance do not matter so in this case in this case you could see that for this instance this is the anchor so it's  
trying to say that if these conditions hold the AI will the in this case the mixture the model would predict this  
species 97 of the time so if you had if we had domain knowledge about penguin species you could say that is  
 

#### 00:32:00,640::		4 minutes mark -> new paragraph 
 
is this counter-intuitive does this make sense and we could we could debug the model this way because this is what the  
model is trying to tell you about how it it got to this prediction this chin chin shot prediction if I tried another  
model let's say if I try another data data point let's say I try using this island and I use male and if I set this to  
49 and then sister 16 you see how every time I'm changing the body the data points the the application updates  
automatically in this case you can see that the shaft values in for the first two species change up and add the line go  
to zero while the the last species again gentle go to one and so in this case the shaft values is telling us that these  
are the features so these are the features and these features push how much each feature pushes the probability to zero  
and in this case how much these features push the probability to one and the anchor explanation is telling us that if  
the def the cubeman def is lower than 17.3 and the body mass is greater than this then at 99.6 percent of the time it  
predicts this species so that's not so this is a gist of anchors it tries to give an explanation with some with it tries  
to give an anchor explanation about your specific instance and if it allows you to debug your model and it gives you a  
view into the machine learning model OK so that's anchors so you see that like the code written here was all in Python  
and it allows me to create this dashboard to have which I could ship to someone I could ship so that anyone could use  
this to explain the predictions so the penguins is a very low stakes prediction but if this was a medical prediction  
like if this was if you have cancer or not cancer a doctor with domain knowledge about cancer could look at these  
anchors or look at these features to see if this model is making sense or that if this model makes sense in his domain  
or his or her domain and so this is very useful in that aspect so yeah so streamlet there's a bit I didn't get into  
today about streamlets there's performance aspects there's alright so the streamlight website and there's a performance  
there's a performance aspect where we have caching and laying out which I didn't explain where you could lay out your  
dashboard how how you want and caching increases performance of your your dashboard there's also a stream that sharing  
which you can sign up for which allows you to create these stream applications and they will help host the shop app the  
application for you to stream the application for you and you could share these with your with others so all the links  
to slides and everything and how they reproduce everything I've mentioned in this talk it's in this repo and yeah so and  
the slides which I have also resources on the shaft values and the anchors and the slides so this is the streamline it's  
very cool it's it allows  
 

#### 00:36:01,280::		4 minutes mark -> new paragraph 
 
I've loved staying in Python and then creating dashboards and not having to write too much JavaScript and it's very  
powerful in that matter and thanks for listening everyone thank you so much Thomas I have to say that when I used to see  
these dashboards in r I was very very envious and I'm so happy that there's a way to make them in Python if anybody has  
any questions feel free to post them on on the Q&A Thomas is here with us for the next 10 or so minutes so it's a great  
opportunity to ask him any questions so I do have a question for you Thomas how did you get started using it it appeared  
on my radar it's weird I could hear you just fine and maybe it's my mic sometimes when there's two mics going I don't  
know do you you know I'll go on mute do you want to check the Q&A and just if it's if you can see the tab and just  
answer the questions there yeah yeah I could do that OK I could read the question too all right all right so I I I I  
use streamlets I got my radar because I'm always looking at different visualization tools and this they just got seed  
funding and it seems very exciting when this this this this goes into the next question in the Q&A like what are the key  
differences between streamline and dash dash so I was using dash for a while to create dashboards just and dash you have  
to very carefully you have to specify the HTML and like that you have to connect the pieces together manually and which  
takes time well my end goal is to create the dashboard without thinking too much about the layout and or like and  
connecting pieces together in this case you see how when I connect the pieces together they auto they automatically  
connect so when I store this input into Python variables and I put the Python variables as input into other objects it  
just automatically updates so like when I click female here it automatically connects this component with components  
with an anchor with a shaft shaft value component and anchors components so it's very flexible in this way what are  
other alternatives to streamlets there's a few there's there's dash which is heavily used there's also vala where it  
converts a Jupyter notebook to a dashboard those are the two that I hear about the most when it comes to writing Python  
first and then converting it to a dashboard in that space the next question is is there a time limit for the external  
API does this stand up for as long as I keep  
 

#### 00:40:01,839::		4 minutes mark -> new paragraph 
 
the server running as you keep this as long as this this this is running it will it'll be OK and as long as your  
machine can run it so so yes only keep the server running everyone so in this case remember this this needs a server  
component to serve the material because there is Python running in the background so when you update these inputs Python  
is running on a server somewhere and in this case my local machine and and updates the ui reactively next question is  
there is a progress bar in the streamlit but I was thinking if there was an async way a way with async io I don't think  
streamlight currently interacts with Python async io currently I'm and look at chat what are the next question is what  
challenges are missing features have you found from streamlet the biggest mixing feature has recently been added which  
is the layout which it's a beta feature so that's so I didn't include it in this talk because it could change but it was  
it was for a while it was extremely hacky to get like two columns in streamlit but now they made it easier with  
something called beta columns and because it's a beta feature which allows you to so if you see here it allows you to  
write Python like instead in this case I want three columns and it uses Python's context manager in such a way where you  
could specify in this case three images to be side by side in three columns so this I I felt that this was the biggest  
feature missing for a long time but they recently added this feature and so I'm happy so yeah I I can't think of any  
more features for myself that I will want from shameless after they have added layouts another question is what is the  
easiest best way to deploy a streamlet app to make it accessible on the web there are two ways the one way I I've I  
didn't show directly in my presentation but in the repo is that you could deploy using Heroku and Heroku deployment is  
pretty simple you just need a profile and a runtime file that specifies the Python version and the proc file to specify  
how to run it and OK of course and a requirements file to specify what other requirements you run it that's one way to  
run it the other way to run it and shoemake is providing the service for now it's providing a service to share your  
streamic application so there's if you look at my the slides there's a sharing stream of sharing you can sign up ashima  
sharing and allows it allows you to share your application with others and they'll host a service for you for now for  
free OK I visited the external ip I external ip  
 

#### 00:44:02,319::		4 minutes mark -> new paragraph 
 
port but I don't see the dashboard it's a positive share dashboard as I'm developing it oh I haven't used that workflow  
before where you could I think it's possible but you you would have to them into the server and then edit the file  
direct like on server I could see other ways to do it but you have to have the server watching the file as you develop  
and I can see that working as long as you do the correct networking to make sure you have access to the server the  
question was I visited the external ip port but I don't see the dashboard is it possible to share the dashboard as I'm  
developing it so there is yes as long as you can access the server and you can and the other person has access to the ip  
next question is is it response is it responsive OK let's so if I if I it's as sponsored as it could be for a  
dashboard that takes this much space you see that how the sidebar closes so that so if I was on the phone I would see  
this which is OK but you see that the dashboard takes up a lot of space in itself the visualization takes up a lot of  
space but it is responsive and as I yeah OK and I think it's I think that's all the questions Thomas thank you so much  
and thank you so much for your patience with our technical difficulties as well I'm glad I'm glad the presentation the  
show did go on so thank you  
 
