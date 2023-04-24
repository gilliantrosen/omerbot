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
        self.data = loads(Path(resource_filename(__name__, "data/omerdata.json")).read_text())
        self.logging: bool = logging
        #TODO: find out how to set minimum intents that i need
        intents = discord.Intents.default()
        print(intents)
        super().__init__(intents=intents)

    async def on_ready(self):
        # Connect to the Discord channel.
        channel = self.get_channel(self.channel)
        print('logged in i think')
    
        # load data       
        eng_aspects = self.data["eng_aspects"] 
        heb_aspects = self.data["heb_aspects"]
        tl_aspects = self.data["tl_aspects"]
        colors = self.data["colors"]

        greg_today = datetime.today()
        heb_today = heb_dates.HebrewDate.today()
        heb_tonight_day = heb_today + 1        
        omer_start = heb_dates.HebrewDate(heb_today.year,1,16)
        
        #get day of the omer
        omer_day = heb_tonight_day-omer_start+1
        print(omer_day)
        # divide by 7 to get the week, mod 7 for the day
        outer_idx = (omer_day-1) // 7
        inner_idx = (omer_day-1) % 7
        # 'index for my JSON file' and 'actual day/week count' are related but very slightly different! 
        # gonna construct them separately to keep track. 
        week_count = omer_day // 7
        weekday_count = omer_day % 7
 
        # Get the English text. Convert HTML tags to markdown tags.
#        en = sugye['en'].replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_")

        # Split the text into posts of <= 2000 characters.
#        posts = [text[index: index + 2000] for index in range(0, len(text), 2000)]
    #    inner_idx = 5
    #    outer_idx = 6
        idxs = [inner_idx,outer_idx]
        print(idxs)
        aspect_strs = ["",""]
        for x in range(2):
            curr_idx = idxs[x]
            
            heart_string = colors[curr_idx] 
            if heart_string == "red":
                heart_string = ":heart:"
            else:
                heart_string = f":{heart_string}_heart:"
            curr_str = f"{heart_string}{tl_aspects[curr_idx]}{heart_string}"
            aspect_strs[x] = curr_str            
 
### STRING CONSTRUCTION ###
     
        greg_string = greg_today.strftime("%A, %B %d")
        day_string = "days"
        week_string = ""
        weekday_string = ""
        and_string = " and "
        eng_extra = "" 

        if omer_day == 1: day_string = "day"
        if week_count == 0 or weekday_count == 0:
            and_string = ""
        match week_count:
            case 0:
                week_string = ""
            case 1: 
                week_string = f"{week_count} week"
            case _: 
                week_string = f"{week_count} weeks"
        match weekday_count:
            case 0:
                weekday_string = ""
            case 1: 
                weekday_string = f"{weekday_count} day"
            case _:
                weekday_string = f"{weekday_count} days"

        # check if there's other stuff happening today 
        holiday_tonight = heb_dates.HebrewDate.holiday(heb_tonight_day)
        if holiday_tonight: 
            eng_extra = f"It is also {holiday_today}."

        eng_intro = f"Today is {greg_string}. After sundown, count the Omer:" 
        eng_oc_string = f"Today is {omer_day} {day_string}, which are {week_string}{and_string}{weekday_string} of the Omer:"
        eng_aspect_string = f"{aspect_strs[0]} within {aspect_strs[1]}" 

        heb_general_blessing = f""
        tl_general_blessing = f""
        eng_general_blessing = f""
        
        heb_todays_blessing = f""
        tl_todays_blessing = f""    
        eng_todays_blessing = f"" 
 	
        full_intro =  f"{eng_intro}\n\n**{eng_oc_string}\n{eng_aspect_string}.**"  
        if eng_extra: full_intro += f"\nIt's also {eng_extra}." 
        post = full_intro
        try:
            # Post.
            await channel.send(post)
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
