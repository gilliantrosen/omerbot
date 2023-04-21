from pathlib import Path
from os import getcwd
from pkg_resources import resource_filename
from json import loads
import random
from datetime import datetime
from pyluach import dates as heb_dates
import discord


class Bot(discord.Client):
    """
    Post an omer-counting message once a day at 6pm UTC for the duration of the omer. 
    """
      
    def __init__(self, channel: int, logging: bool = True):
        """
        :param channel: The ID of the channel.
        :param logging: If True, log messages.
        """

        self.channel: int = int(channel)
#        self.mishnah = loads(Path(resource_filename(__name__, "data/mishnah.json")).read_text())
        self.logging: bool = logging
        #TODO: find out how to set minimum intents that i need
        intents = discord.Intents.default()
        print(intents)
        super().__init__(intents=intents)

    async def on_ready(self):
        # Connect to the Discord channel.
        channel = self.get_channel(self.channel)
        print('logged in i think')
        post = 'default post text'       
        greg_today = datetime.today()
        heb_today = heb_dates.HebrewDate.today()
        heb_tonight_day = heb_today + 1       
        # check that we're during the omer
        print(heb_today)   
        # check if there's other stuff happening today
        eng_extra = ""    
        holiday_today = heb_dates.HebrewDate.holiday(heb_today)
        if holiday_today: 
            eng_extra = f"It is also {holiday_today}."
        # get days since passover, divide by 7 to get the week, mod 7 for the day (+1 each)

        # special bit for last day 

        eng_intro = f"Today is{greg_date}. After sundown, count the Omer:"
        eng_oc_string = f"Today is %(num_total)s days, which are {num_week} weeks and {num_weekday} days of the Omer:"
        eng_aspect_string = f"{inner_aspect} within {outer_aspect}"

        heb_general_blessing = f""
        tl_general_blessing = f""
        eng_general_blessing = f""
        
        heb_todays_blessing = f""
        tl_todays_blessing = f""    
        eng_todays_blessing = f"" 


        # Get a random sugye.
#        sugye = self.mishnah[random.randint(0, len(self.mishnah) + 1)]
#        url = f"https://www.sefaria.org/Mishnah_{sugye['Order'].replace(' ', '_')}.{sugye['Chapter']}.{sugye['Verse']}?lang=bi"
        # Get the English text. Convert HTML tags to markdown tags.
#        en = sugye['en'].replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_")
        # Create a citation.
#        citation = f"{sugye['Order']} {sugye['Chapter']}.{sugye['Verse']}"
#        self.log(f"{today}: {citation}")
        # Get the text.
#        he = sugye["he"]
#        text = f"**{citation}**\n{he}\n{en}\n{url}"
        # Split the text into posts of <= 2000 characters.
#        posts = [text[index: index + 2000] for index in range(0, len(text), 2000)]
        
        try:
#            # Post.
            #await channel.send(post)
            #for post in posts:
            #    await channel.send(post)
            # Quit.
            await self.close()
        except Exception as e:
            self.log(str(e))

    def log(self, message: str) -> None:
        """
        Log a message.

        :param message: The message.
        """

        if self.logging:
            with Path(getcwd()).joinpath("log.txt").open("at") as f:
                f.write(message + "\n")
