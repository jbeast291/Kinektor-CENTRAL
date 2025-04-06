Kinekts (required): 
 - https://github.com/jbeast291/losaltos-DiscordConnector
 - https://github.com/jbeast291/losalots-VelocityConnector
 - you must set up these for proper operation
## Inspiration
  A problem with my friend group is that we play a lot of different games and dont end up talking together a lot. I wanted to create a system that would allow chats of many kinds to be linked together into one room.
## What it does
  Currently, it integrates Minecraft, Discord, and a webpage all into one chat room. When you chat on one platform it sends it to the others for people to see. It essentially links chats together into one. *Kinektion!*
## How I built it
  I started with the central server, I originally started in java but realized the needless complexity of it so I moved over to python/flask. The central server is the connection point for all connected platforms. When you send a message in discord, it goes to the central server and then is broadcasted to the entire network oh kineks. kinekts are the name of an individual connector, the discord and minecraft velocity plugin are both kinekts 

  After getting as much as I could without 1 kinektc runnnig, I started coding the Minecraft Velocity Plugin. It was all written in java and made it far more difficult as my poor laptop couldnt run both the central server and a minecraft server, so I offloaded it to a vps. It took around 11 hours straight to setup the website and Velocity kinekt, where i then moved on and setup the discord which only took an hour, I designed it around being easy to implement new platforms so all a kinekt needs to supply is a incomming and outgoing contents of some kind of chat.

  I also made the logo myself, it just randomly came to me after 13 hours of straight coding
## Challenges I ran into
  Python async being VERY annoying. I almost lost my mind just trying to fix an issue with having two async processes comminicate with each other but I figured out a soluton eventually after an hour or two.

  My laptop was terrible. 8gb of ram is not enough to run the central server, discord bot, minecraft proxy and backend and minecraft at the same time. I mean who could have foreseen that!
## Accomplishments that I'am proud of
  Its in a working state and the logo looks kinda cool ig idk
## What I learned
  I learned alot about websockets in creating a website. I had made mostly static websites in the past and this was my first that shared information back and fourth. I had to learn how to be able to ping the client when a new message.
## What's next for Kinektor
  More kinekts of course!

  ...and more commands, commands that could pull information from the different platforms would change things greatly but it is not built currently for that. It would require more work for each kinekt which sort of defeats the purpose that there supposed to be extremly simple.
