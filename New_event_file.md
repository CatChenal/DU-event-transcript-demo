# Mridu Bhatnagar:  Building a Conversational Bot for WhatsApp w/Twilio & Python

## Key Links
- Meetup Event:  https://www.meetup.com/nyc-data-umbrella/events/272365664/
- Video:  https://youtu.be/dqab-FcAirA
- Slides:  https://docs.google.com/presentation/d/1IlBnr7UUwIo2kukgSd201JQgsCyVkMuHyd-pK3zwe9I/edit#slide=id.p
- GitHub Repo:  N.A.  
- Jupyter Notebook:  N.A. 
- Transcriber:  ?  

## Video

<a href="http://www.youtube.com/watch?feature=player_embedded&v=dqab-FcAirA" target="_blank">
    <img src="http://img.youtube.com/vi/dqab-FcAirA/0.jpg" 
         alt="Building a Conversational Bot for WhatsApp w/Twilio & Python" width="25%" />
</a>

## Transcript

### Introduction
<!-- Editing Guide: The pipe (|) position in this comment is 120:                                                       | -->

Hey everybody welcome to a Data Umbrella webinar I am joining from New York and I'm just gonna do a a brief introduction  
about Data Umbrella and then we'll get started on the webinar so it'll be it'll sort of go like I'll do the introduction  
we'll do the talk and then you can post any questions in the chat or in the Q&A and we'll sort of answer those as they  
pile up over time and just to let people know this will be recorded and will be available on our YouTube I posted a link  
to YouTube in the chat if you're not able to see it just let me know and I can share it again about me I'm the founder  
of Data Umbrella I'm a statistician data scientist and I am also an organizer for the New York city chapter of PyLadies  
and I am on Twitter at Reshama s OK the mission of Data Umbrella is to provide a welcoming educational inclusive space  
for underrepresented persons in the field of data science and machine learning check out our website we are pretty much  
on every social media platform as Data Umbrella and we are a volunteer-run organization PyLadies is an international  
group there's over 100 active chapters and it's for Python it's for women and gender minorities of all levels of  
programming experience you can follow us on Twitter as well I want to go over a code of conduct we're dedicated to  
providing harassment free experience for everyone be kind be professional and that also applies to the chat as well on  
the Data Umbrella website which is dataumbrella.org there are many resources available for you know responsibility  
ethics inclusivity diversity and also you know learning r and Python and open source so feel free to check those out on  
our website we have the best place to find out about our events are on Meetup I also joined an event for next Tuesday's  
webinar which is on creating nimble data processes which will be which will be fun if you are on LinkedIn I share a lot  
of articles including job postings so if you're interested in that feel free to follow us on LinkedIn feel free to  
subscribe to our YouTube channel for our videos and follow us on Twitter for updates and so now we're going to get  
started I'm going to turn this over who is joining us from central India in dore right yeah thank you so much for  
joining us and it's 9 30 wonder time right [music] I'll just I'll share my screen is the screen visible now I see drag  
and drop files I think it might just be loading yep now we can see your screen all right is it visible yes OK yeah  
hello everyone I'm Mridu Bhatnagar I'm from India and I am a software engineer by profession and when I am not  
programming or building stuff then I love giving talks at various meetups and conferences so during this time I have  
been giving talks all across the group  
 

#### 00:04:00,879::		4 minutes mark -> new paragraph 
 
in every possible Meetup that is possible so into today's session we'll be covering up about building a conversational  
bot for WhatsApp and here is the bot you like on the left hand side you may be seeing what jf this one this is the what  
I had recently built it is vocab but and the features it includes it are it tells you the word definition it tells  
synonyms it tells antonyms and it tells examples based on whatever you query it for so like it is squaring examples for  
amazing so this would return some examples for amazing so this was the board that I had recently built and the session  
for today we would be covering that how you too can build any build any of the bots and bring your ideas to life so  
moving ahead the requirements for this session include that what I have used is I have used Python version 3.6 greater  
than 3.6 and then we will be using Flask for running the web server and then we will be using another package that is  
ngrok ngrok is basically used for testing up our bot with the mobile application so there is there needs to be some way  
where we can just test whether the bot is working as expected or not so for that we will be using ngro and all these  
things that I have mentioned are pip installable so pip is the Python package manager you just have to do pipe like pip  
install Flask paper install ngrok sorry ngrok is not prep installable for ngrok you need to go on to ngrok website and  
from ngrok website you can download ngrok so that is how you install ngrok and then all you need is a smartphone with  
WhatsApp installed on it and then there needs to be a Twilio account so this is the URL at the bottom is for creating  
the Twilio account I can maybe share this link or OK later I can share this link so that if you want you can just open  
up and create your own accounts I will just share it just a second if you are following along or later you want to  
create a Twilio account you can use this URL that I have put up in the chat the initial account trial account is  
basically free so it won't charge you anything so moving ahead here is how you can configure your Twilio WhatsApp  
sandbox so once you have created your account on Twilio you can just go on to Twilio console sms WhatsApp learn this URL  
so first and foremost thing is to create the account on Twilio and then there is something as Twilio sandbox so our  
application basically will be communicating to Twilio so imagine that you have opened your WhatsApp and you are querying  
your WhatsApp with like suppose you wanted word definition or you are saying hi to your WhatsApp so whatever message you  
are sending to the WhatsApp should go to Twilio so we are trying to make a connection between WhatsApp and Twilio so for  
that connection to happen this URL is what is needed connection between  
 

#### 00:08:03,280::		4 minutes mark -> new paragraph 
 
WhatsApp and Twilio so the URL that I had sent above was for connection between WhatsApp and Twilio and if you have  
already created that this account and you go on to this URL this is how your page would look like I'll just expand it  
this is how basically your screen is going to look like once you are on our Twilio sandbox I cannot live like I cannot  
go on the actual website and show you live because there are some secret codes that are there that are not to be shown  
so make sure that whenever you two are using the Twilio application you hide your own codes don't just go and put it up  
on GitHub or somewhere these are your own codes and so the left hand side number that you see here is something that you  
have to store you have to save it on your mobile phone and this is your joining code so once you save this contact  
number on your mobile phone this contact would basically appear on your WhatsApp contacts so this is your WhatsApp  
contact number and this is the joining code and everyone is going to have their different joining codes and joining  
codes code needs to be hidden because after a certain point of time when all the Twilio free credits are over it are  
like every query is chargeable so that's why don't just disclose your secret code otherwise others will be able to use  
it and your free credits will be gone so that is the reason basically to hide it so next step is after you create the  
account just save whatever number comes on to your screen you will have to save it on your phone and then this is the  
joining code so on your WhatsApp what you have to do is the first message you will see is join followed by whatever is  
the code this message you will have to send on the WhatsApp now this whole setup make sure that our WhatsApp is being  
connected to Twilio this is the very first part of the chat bot OK and now as if you have already saved the number so  
this is the initial step of the board that we have already done I saved that number using the name vocab bot you can  
save it by anything that you like so this is the very initial step and now how we will go on doing this programmatically  
is what I what I am going to explain in the next steps so the next steps include creating a Python virtual environment  
so once you create once you have the initial thing set up all you have to do is by create a Python virtual environment  
so I'll just briefly explain what is meant by a virtual environment in case you don't know so what happens is in Python  
we install all the external packages by doing pip install and if we are not using the virtual environment all these  
packages get globally installed on our system so as a result a lot of times between multiple projects there can be  
version conflict suppose you are using Django one suppose you are using Django two in one project and Django three in  
another project then it is difficult for the project to determine that which Django version should I use so to avoid  
scenarios like these we use  
 

#### 00:12:02,480::		4 minutes mark -> new paragraph 
 
Python virtual environment and here are the steps to create the virtual environment so that there is no virgin conflict  
now in case you are a mac or Linux user all you have to do is run the following commands so mkdir is basically for  
creating a new directory that is the WhatsApp bot and the cd was for changing the directory of the bot and then Python  
minus m when WhatsApp bought when you do this command creates the virtual environment when is the package and WhatsApp  
what is your name of the virtual environment that you are going to create if when is not installed on your system you  
will have to install when on your system and then once the virtual environment is like once this virtual environment is  
created all you have to do is activate the virtual environment that is source WhatsApp bin activate so then you have to  
activate this virtual environment and ah you would come to know whether the environment is activated or not by this last  
command so if you are able to see on the left hand side that such a thing is coming like WhatsApp which means that the  
bot has got activated and now I am just installing my requirements I need a Twilio library then I need requests and  
request is the http library in Python it helps us in communicating with the external third party APIs or any kind of  
APIs for that matter and then Flask is a micro web framework in Python and Python.10 is another package it is used to  
save all our secret keys so and if you are a Windows user then the commands are different so for making the directory  
you need to do md WhatsApp bot for changing we have WhatsApp what then we have Python minus and when WhatsApp bot this  
is for again creating the virtual environment then we are trying to activate the virtual environment and then similarly  
you just need to install all the requirements so before we go ahead I would like to tell that Twilio we are installing  
so that from Twilio we are able to send some req response to the bot so if you send any message to your bot the bot must  
reply something and for the getting the reply from the bot we need to install a Twilio application so that it sends us  
some response and request library is for communicating with any third party library Flask Flask is basically the micro  
frame framework that is used for running the server at our back end and then Python.10 we are using so that we don't  
disclose any secret key to anyone it needs to be saved on our part and we'll see everything working later in the session  
and now before I go on with the code are there any questions or anything till now or something that I haven't explained  
in greater detail so you can ask the question if there I didn't I don't see any questions so far except is the webinar  
being recorded which it is but if anybody has any questions feel free to post on the yeah we will have a link to the  
 

#### 00:16:00,959::		4 minutes mark -> new paragraph 
 
slides afterwards OK yeah so moving ahead the next step basically is that how that we need to clear create a Flask  
chatbot service so we are trying to create the service because we need to send some data to the user so the workflow  
basically is user enters the query to the WhatsApp and then instead of a human being replying to you there is a bot  
there and instead of human the bot is basically replying to you so for this whole workflow to take place we need Flask  
applications there needs to be a server running that would keep on replying to your messages so this is how we create  
the very first step is so in the presentation here I won't be explaining the process of building vocab bot but I am  
explaining a general giving a general idea that how you can create your own bots and bring your own ideas to life and  
this is the very basic like hello world of bots we can say like that this is the very basic bot that you can create on  
your own and then feel free to incorporate your own ideas and convert those into bots so I am just explaining a very  
generic process so this is the very first step of creating the Flask service so first I am trying to import Flask class  
so I am doing from Flask import Flask in line 1 and then I am initializing the app from Flask class and all I am doing  
then is app.root hello world so whatever communication is going to take place is going to take place through this  
endpoint hello world I am going to post my messages on hello world endpoint and whatever the user is sending will also  
be coming on this hello world end point so we'll be seeing ahead how this happens and app.run allows us to run the  
server abdul run basically allows us to run the application and by default the application runs on port number 8000  
localhost port 8000 so our initial very initial setup is this now the next step is when I have already created one  
endpoint and I know that this is where I need to send my data the next point is how are we going to receive the incoming  
message from the user so now for that to happen all you need to do is app dot hello world method post we are trying to  
post something and then we do request dot values dot get and body dot lower so what this conveys is that if the request  
message contains a key named as body then we need to we are trying to fetch the value corresponding to this body and if  
it doesn't find any key corresponding to but like if it doesn't find the key body then the message would be empty and  
then I am trying to convert my whole message into lower case so that is the meaning of this whole line request dot  
values dot get I am trying to get the value and whatever is the value that the user  
 

#### 00:20:01,360::		4 minutes mark -> new paragraph 
 
sends to the WhatsApp bot so in your what if you write hi so here in this function your incoming message would be high  
if the user is sending hello the incoming value of incoming message would be hello so line number six is just for  
retrieving the incoming message by the user next step is we we like want to willy to send a message to the user back so  
for that purpose Twilio has a messaging response it has a Twilio ML library in it so if you want to check out all these  
documentation are very well explained on the Twilio's website website itself so whenever you are building one for your  
own you can just check the documentation there wml is the library so what we are trying to do is we are trying to  
initialize this class messaging response then we have a response object with us and in the response I want that I should  
send a message so all I am doing is response dot message and here I am initializing the variable message with it and  
then my app is still running for running my app I am doing app dot run line number eight and line number nine why we are  
doing this is because this is a format that is suggested by Twilio so only when you have this format in your application  
you would be able to send the message back to the user so step one is user is sending the message to Twilio that is line  
number seven line number eight and nine is Twilio is trying to send back something to the user so that is what line  
number 7 8 and 9 are doing and now what we want is that whenever the incoming message is high the output message should  
be hello hope you have a good day so now I am saying that a user is entering the message high so your value of incoming  
message in line number seven would be high and then when you are doing response is equal to messaging response message  
is equal to response dot message when we do this thing from here I am trying to now send the bot is trying to send the  
message to the user so there is another built-in method in that library itself that is message.body so now I am doing is  
hello plus the incoming message so hello would be is a static thing that I am sending and plus the incoming message so  
suppose the incoming message is high so the returned response would be hello hi or suppose if I am sending the incoming  
messages I am sending my name itself so it would say hello if the user is sending word world so the output is hello  
world so this is a very trivial application of how message sending and message receiving takes place in this bot at the  
moment we are stands I am sending some static messages that always this is going to return hello plus the incoming  
message but we can say send dynamic messages as well like I was doing in the vocab bot so for sending dynamic messages  
we need a  
 

#### 00:24:02,159::		4 minutes mark -> new paragraph 
 
we basically need an API so that we'll be discussing ahead but the process of the that workflow of incoming messages and  
outgoing message is this that you see here are there any doubts till now yeah the presentation slides I I'll be sharing  
any doubts apart from the presentation slide thing are there any questions or have I gone too fast I don't see any other  
questions there so that's good OK are things understandable to till now or it is a bit confusing OK so we'll just  
and here I'm sorry I think this is going to be hello plus high so if the incoming message was high the output that our  
function was sending was hello and followed by hello a high this is a very trivial application just to make things  
easier and so that you understand the process of building the bot and usually the way the risk request and response  
Twilio accepts is in the xml format so it is not json format it is xml format and the body keyword that we were using  
was this body keyword and if you have to send any image so for image you need to use media key so all this is very well  
explained in their documentation and just for running your application all you have to do is Python app.py so earlier by  
mistake I have said that we are running the application on port number 8000 so I am sorry for that the port is not 8 000  
the application is running on port port 5000 all right so once all your code is ready and in place all you have to do is  
run your application so now your application is running basically on port 5000 so now what problem do we have is we want  
the bot to run on WhatsApp and WhatsApp is on your mobile and your code is on your laptop so there are two different  
website two different devices that we want to communicate in between so the next step is how how do the communication  
between the two devices happen so that communication happens with the use of this ngrok so initially I had told that you  
need to install ngrok from the from its website so now next step is like you open another terminal on your laptop go on  
to the location where this ngrok has got installed so usually it would be in your downloads folder and then all you have  
to do is run dot slash ngrok http 5000 what this will do is this will run ngrok at port 5000 so now you have on one  
terminal Flask running on another terminal you have this ngrok running there are two things running and now Twilio will  
help us in connecting these two devices so the terminal would look something  
 

#### 00:28:02,640::		4 minutes mark -> new paragraph 
 
like this when you once you run your ngrok the terminal is going to look something like this OK so now next step is  
making a connection with Twilio so now all you have to do is just copy this forwarding URL on everyone's laptop the  
forwarding URL will be different so now next step is for connecting the two devices you have to just copy paste copy the  
URL and then by copying the URL you just need to put the URL in in the Twilio sandbox for WhatsApp you would be able to  
see this Twilio sandbox in the console itself just go on to the Twilio website all these things are available there and  
as I had mentioned above add your ngrok forwarding URL in the text box so you have to add the ngrok URL here and then  
after adding the ngrok URL at the end you have to put slash and followed by the end point hello world that we had used  
so forwarding URL followed by the end point that was hello world so this is basically now everything is set now Twilio  
knows how the communication between the devices needs to take place and now if you test your Flask service again you  
would see that the communication is taking place whenever you send hi will you would send you hello followed by a high  
or based on whatever code that you have written in the in your application so this is a very simple application that I  
had demoed on how to build a bot and the next one was how to how do we send a dynamic response or how dynamic responses  
are to be sent so we in the above example we were sending the static responses that if whenever you send hello it will  
send you high but for dynamic responses what can be done is there are lot of APIs already available so there is some  
examples of APIs are there is Google maps API there is cad pictures API you have Twitter API news API GitHub API now you  
can use all these use cases with your WhatsApp so one use case could be you are sending some location or you are suppose  
sending latitude and longitude and then Google maps returns you the location on the map or you are sending some location  
and the Google map returns you that exact map location or you you are interested in seeing some cat picture so you just  
and start querying that cat pictures API or you are just interested in knowing the trend what is trend trending on  
Twitter and you are interested in seeing that trending Twitter thing on WhatsApp so you can just use the Twitter API or  
you are interested in reading the Google news on WhatsApp so you can use Google news for that if you want your to check  
whether the open source project you are contributing to has some new pull requests on it or has some new issues opened  
on it so instead of opening it up time and again you can just use WhatsApp for it if you are more accustomed to using  
WhatsApp so these are couple of use cases and for the bot that I had basically initially shown you so for that what I am  
also using an API for that so there is a dictionary API that I had used  
 

#### 00:32:00,159::		4 minutes mark -> new paragraph 
 
so the dictionary API was Merriam-Webster API so that Merriam-Webster's API returns all this word definition synonyms  
antonyms and examples and that is how for any random word I was entering the bot was returning me a response dynamic  
response and using Twilio is also net not necessary to leo we are using I am using Twilio but original WhatsApp API can  
be used the problem however with WhatsApp API is that it is not a developer API by this I mean is like first you need to  
be a business owner only then you would be able to use the original WhatsApp API I don't think they have opened the  
WhatsApp API for even the developers to use for their projects so there is some kind of restriction at their end and  
also they are very particular about what kind of messages you send so suppose if someone is trying to spam anyone or  
someone is trying to send incorrect messages then WhatsApp blocks the user so before deciding on to the use case for  
building the bot first before using the APIs the use case needs to be very well thought of that what we are trying to  
send and WhatsApp also has certain restrictions that what should be the template of the messages that the bot is sending  
and also with WhatsApp the thing is you need to get approval from WhatsApp for using all these things so and one way to  
put this bot in production is like if you just want to put your Twilio broad for in production and run it so you can  
maybe deploy it on Heroku so I I use my bot often and I have deployed it on Heroku as I don't own any business and I'm  
not using WhatsApp official APIs so I'm basically I have basically deployed it on Heroku and I have kept the secret keys  
with me so it is just used for private purposes and these days if you would have noticed lot of businesses are using  
WhatsApp as a platform for marketing so it has pretty good business use case attached to it and companies can use it and  
are using it for providing customer support and even some companies are using it for broadcasting the messages regarding  
events and all so there can be various business use cases attached to WhatsApp so this was all I had and if you are  
interested in building the vocab bot itself so here is a blog that I had recently written for Twilio themselves so here  
is the bot URL so whenever you are trying to build it if you want to build the same one or trying to have some idea you  
can just check out this blog the blog has is beginner friendly blog so it has detailed explanation of why a particular  
decision is taken and why I am doing what I am doing so you can just add a lot bought logic based on your own needs and  
requirements so and the last step after discussing these APIs is as throughout we were using Python so in Python just  
for integrating the  
 

#### 00:36:02,240::		4 minutes mark -> new paragraph 
 
API there is a simple module that we use that is requests so if you want to integrate any API to your code all you have  
to do is use requests.get now this method depends whether depends on your API whether it accepts a get request post  
request but all you need to do is install requests and then there is a built-in json module through json what gets done  
is json converts your string data into dictionary data and this dictionary data in the end is parsable so instead of  
sending all your information returning all your information you can just send the needed information to the user so this  
small snippet just explains that part and based on your own use case you can write your own logic and a lot of times it  
it is only about writing conditional statements and if you are interested in exploring all of this further so if you are  
interested in Flask then you can check out the Flask official documentation and blog link I have already shared with you  
all and then GitHub has a long list of public APIs that you can use I have only I had only listed a couple of them so  
you can have a look at all these public APIs as well when you built one of your own so thank you that was all I had for  
the session does anybody have any questions please feel free to post them in the chat and I can read them thanks so much  
for the presentation it was great and thank you thank you OK so I'm just gonna turn on my mic I don't see any  
questions here all right so we'll be sharing the video soon with the link for the slides and a couple of links that you  
posted on in the chat as well yeah those links are there in the presentation as well on the last video OK that's great  
so they'll be in the presentation you'll be able to access them Gabrielle writes I would have liked to learn a little  
bit more on how to publish the bot do you have resources for that for publishing the bot I don't really have resources  
but I have done one another blog for Twilio that talks about this publishing thing so I think I can point to that one  
the Heroku part for publishing that I'm using so OK here is a another use case so this was basically not for OK  
sorry this one is not basically using WhatsApp but it is using Heroku so from here that publishing part you can learn  
that how you can publish your work OK we have another question which is is it possible to add ML cognitive service  
from azure on the bot I am not really into ML and I I am not very sure if that is possible or not but you can check this  
out on Twilio's website on itself they have lot of blogs and there are a lot of people working on lot of interesting  
ideas for  
 

#### 00:40:03,119::		4 minutes mark -> new paragraph 
 
the bot so I think this azure thing you can find it up there if someone has used or not and if this azure service is an  
API itself then it can def definitely be used any kind of API you can integrate with Twilio OK next question I am new  
to Flask what does Flask do Flask I don't know if you have heard of Django or not blood Flask like Django is a web  
framework so web frameworks are basically used to build websites it helps in easing the process of building the websites  
for you so without the framework if you start going and writing the normal Python code so things get pretty complex and  
commercially you need to write a lot of code and it is not viable to do so so that is why we use frameworks for the same  
so a lot of things are already built in and then other parts you have to develop on your own so Flask is basically a web  
framework that is used the next question is thank you for your questions afterwards there's our slack channel where we  
can post them to Data Umbrella has a discord server so and it's on our website there's a link to how to join on the  
website so if you go to dataumbrella.org you can join discord that way it says the publishing link is not found oh yeah  
just a second I think there is some problem [music] you will have to scroll down on this link and then there is a  
section where I am publishing my application on Heroku so from that whole blog you can take that part of how our  
application is published on Heroku OK all right great and if anybody has any more questions now is the time to ask and  
I'm there on Twitter so if there are any further questions so I can take it up there as well that's right has our  
Twitter handle in the event description on Meetup so that's another way all right so it looks like there are no other  
questions so I am going to thank you thank you thanks for sharing the Twitter handle it's at mridu underscore underscore  
yeah great thank you so much for joining us I know it's 10:30PM your time now right yeah I think yeah 10 15. OK and  
we'll be sharing the recording soon thanks for joining us everybody yeah thank you  
 
