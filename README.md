# ![](omerbot-logo-extra-small.png) Omerbot 

Omerbot is a Discord bot to help you count the Omer! For every day of the Omer, at 6:00pm UTC, it posts a message with the upcoming day of the Omer, aspects for the day, and the blessing. 

Example post: 
![](omerbot-example.png)

This bot is adapted from Esther Alter's [Mishnahbot](https://github.com/subalterngames/mishnahbot). 
 
# Covenant

This software uses the MIT license, which you can read [here](LICENSE).

This software was originally made for [Shel Maala](https://www.shelmaala.com/) in order to enable the creation of the Queer Talmud. Alternative use cases, such as the study of the non-queer Talmud, are theoretically possible but not actively supported by the developers. Usage of this software to suppress the Queer Talmud is prohibited.

The user of this software may not be an individual or entity, or a representative, agent, affiliate, successor, attorney, or assign of an individual or entity, identified by the Boycott, Divestment, Sanctions ("BDS") movement on its website ([https://bdsmovement.net/](https://bdsmovement.net/) and [https://bdsmovement.net/get-involved/what-to-boycott](https://bdsmovement.net/get-involved/what-to-boycott)) as a target for boycott. *[Source: The Hippocratic License](https://firstdonoharm.dev/#hippocratic-license-3-0)*

# Setup 
## 1. Discord setup 1
  1. [In the Discord developer portal, create a Discord bot application.](https://www.wikihow.com/Create-a-Bot-in-Discord#Creating-the-Bot-on-Discord) Make sure to copy the bot token, you'll need it for file setup later! 
  1. [Get the OAuth2 client ID of the bot.](https://www.wikihow.com/Create-a-Bot-in-Discord#Sending-the-Bot-to-the-Discord-Server.2FChannel)
  1. [Get the Channel ID for the channel you want the bot to post to.](https://docs.statbot.net/docs/faq/general/how-find-id/) You'll need this for your file setup later!
  1. [Add the (currently empty) bot to the channel.](https://discord.com/oauth2/authorize?&client_id=1097236576062419085&scope=bot&permissions=8) Replace the client ID in this link with your bot's client ID. 

### How to add this bot to a server you don't own 
  1. Get the Channel ID of the channel where you want it to post. Put it in the "channel=" part of your `bot_secrets.txt` (see step 2.2).
  1. Tell someone who is an admin in that server to go to this link: [authorization link for your bot]( https://discord.com/oauth2/authorize?&client_id=1097236576062419085&scope=bot&permissions=8), then select the relevant server from the dropdown menu. 

## 2. Local computer config files 
  1. Clone this repo! the rest of this setup assumes that you've cloned it to `~/omerbot`.
  2. Create a file named `bot_secrets.txt` in the `~/omerbot` directory, formatted like this:
  ```
  token=BOT_TOKEN
  channel=CHANNEL_ID
  ``` 

## 3. Server   
For setup with a traditional remote server, see [Mishnahbot's setup instructions](https://github.com/subalterngames/mishnahbot#setup). 

For setup with a little single-board computer as your server, read on! 

*/ / / Construction Zone / / /*



# Acknowledgements

Thanks to [Esther Alter](https://github.com/subalterngames) for creating Mishnahbot in the first place, and for her kindness and wisdom on Python, Discord bots, and more. 

Thanks to Meli for their [Omer-counting newsletter](https://buttondown.email/OmerCounter), which the format, text, and scheduling of this bot is based upon. 

Thanks to Tim for the borrowed cursed Odroid-C2, where this bot runs from Pesax to Shavuot.  