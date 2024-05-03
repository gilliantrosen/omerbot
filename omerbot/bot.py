from pathlib import Path
from os import getcwd
from pkg_resources import resource_filename
from json import loads
import random
from datetime import datetime
from pyluach import dates as heb_dates
import discord


### File Navigation ### 
    #90: string constructor functions
    #278: test functions 
 
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
        intents = discord.Intents.default()
        super().__init__(intents=intents)

    async def on_ready(self):
        # Connect to the Discord channel.
        channel = self.get_channel(self.channel)
    
        # load data       
        eng_aspects = self.data["eng_aspects"] 
        heb_aspects = self.data["heb_aspects"]
        tl_aspects = self.data["tl_aspects"]
        colors = self.data["colors"]

        greg_today = datetime.today()
        heb_today = heb_dates.HebrewDate.today()
        heb_tonight_day = heb_today + 1        
        omer_start = heb_dates.HebrewDate(heb_today.year,1,16)
        
        # get day of the omer
        omer_day = heb_tonight_day-omer_start+1
        
        if (heb_tonight_day < omer_start) or omer_day > 49: 
            #it's not the omer! close. 
            try: 
                await self.close()
            except Exception as e: 
                self.log(str(e))

    ### STRING CONSTRUCTION ###
             
        greg_string = greg_today.strftime("%A, %B %d")

        # check if there's other stuff happening today 
        eng_extra = self.get_holiday_tonight(heb_tonight_day)

        eng_intro = f"Today is {greg_string}. Last night was {omer_day-1} days.\nAfter sundown tonight, click below to count the Omer!" 
        
        (heb_aspect_string,tl_aspect_string,eng_aspect_string) = self.construct_aspect_strings(omer_day)
        (heb_number_string,tl_number_string,eng_number_string) = self.construct_number_strings(omer_day)

        heb_count_full = f"{heb_number_string} {heb_aspect_string}"
        tl_count_full = f"{tl_number_string} {tl_aspect_string}."    	
        eng_count_full = f"**{eng_number_string}**||\n**{eng_aspect_string}.**"  
        if eng_extra: eng_count_full += f"\n{eng_extra}" 
       
        general_blessing = f"||*If you've counted every day so far, do the blessing first. Otherwise, go right to the counting.*\n{self.data['heb_blessing']}\n{self.data['tl_blessing']}\n{self.data['eng_blessing']}"
        
        post = f"{eng_intro}\n\n{general_blessing}\n\n{heb_count_full}\n{tl_count_full}\n{eng_count_full}"
 
        #self.test()       
        #post = self.test_numbers()
        try:
            # Post.
            await channel.send(post)
            # Quit.
            await self.close()
        except Exception as e:
            self.log(str(e))

 

### Construction Functions ### 

    def construct_number_strings(self, omer_day: int):
        """     
        construct the count strings for the day given. 
        param omer_count: day of the omer 
        """
        heb_numbers_1_11 = self.data["heb_numbers_1-11"] 
        tl_numbers_1_11 = self.data["tl_numbers_1-11"]
        heb_numbers_onesplace = self.data["heb_numbers_onesplace"]
        tl_numbers_onesplace = self.data["tl_numbers_onesplace"]
        heb_numbers_tensplace = self.data["heb_numbers_tensplace"]
        tl_numbers_tensplace = self.data["tl_numbers_tensplace"]
        
        week_count = omer_day // 7
        weekday_count = omer_day % 7
        
        heb_oc = ""
        tl_oc = ""
        eng_day = "days"
        
        heb_week = ""
        tl_week = ""
        eng_week = ""
        
        heb_weekday = ""
        tl_weekday = "" 
        eng_weekday = ""
        
        heb_and = " \u05d5\u05b0"
        tl_and = " v'"
        eng_and = " and "

     ### (Today is) X days
        if omer_day == 1: 
            heb_oc = "\u05d9\u05d5\u05b9\u05dd\u0020\u05d0\u05b6\u05d7\u05b8\u05d3"
            tl_oc = "yom exad"
            eng_day = "day"
        elif omer_day >= 2 and omer_day <= 10:
            # 2 to 10 are 'yamim', rest are 'yom' 
            heb_num = heb_numbers_1_11[omer_day]
            tl_num = tl_numbers_1_11[omer_day]
            heb_oc = f"{heb_num} \u05d9\u05b8\u05de\u05b4\u05d9\u05dd"
            tl_oc = f"{tl_num} yamim"
        elif omer_day == 11: #special little 11
            heb_num = heb_numbers_1_11[omer_day]
            tl_num = tl_numbers_1_11[omer_day]
            heb_oc = f"{heb_num} \u05d9\u05d5\u05b9\u05dd "
            tl_oc = f"{tl_num} yom"
        else: 
            #constructable! ones (and)tens
            #10: " " 20: v' 30: u' 40: v' 
            heb_connector = ""
            tl_connector = ""
            if omer_day > 11 and omer_day < 20:
                heb_connector = " "
                tl_connector = " "
            elif omer_day > 30 and omer_day < 40:
                heb_connector = " \u05d5\u05bc"   
                tl_connector = " u'"
            elif (omer_day > 20 and omer_day < 30) or omer_day > 40: 
                heb_connector = " \u05d5\u05b0"
                tl_connector = " v'"
            tensplace = omer_day // 10
            onesplace = omer_day % 10
            heb_num = f"{heb_numbers_onesplace[onesplace]}{heb_connector}{heb_numbers_tensplace[tensplace]}"
            tl_num = f"{tl_numbers_onesplace[onesplace]}{tl_connector}{tl_numbers_tensplace[tensplace]}"
            heb_oc = f"{heb_num} \u05d9\u05d5\u05b9\u05dd"
            tl_oc = f"{tl_num} yom"

     ### Y weeks and Z days
        if week_count == 0 or weekday_count == 0:
            heb_and = ""
            tl_and = ""
            eng_and = ""
        else:
            if weekday_count == 2 or weekday_count == 3:  
                heb_and = " \u05d5\u05bc"    
                tl_and = " u'"
            if weekday_count == 5:
                heb_and = " \u05d5\u05b7"
                tl_and = " va"
        match week_count:
            case 0:
                eng_week = ""
            case 1: 
                heb_week = "\u05e9\u05c1\u05b8\u05d1\u05d5\u05bc\u05e2\u05b7\u0020\u05d0\u05b6\u05d7\u05b8\u05d3"
                tl_week = "shavua exad"
                eng_week = f"{week_count} week"
            case _: 
                shavuot = "\u05e9\u05b8\u05c1\u05d1\u05d5\u05bc\u05e2\u05d5\u05b9\u05ea"
                heb_week = f"{heb_numbers_1_11[week_count]} {shavuot}"               
                tl_week = f"{tl_numbers_1_11[week_count]} shavuot"
                eng_week = f"{week_count} weeks"
        match weekday_count:
            case 0:
                eng_weekday = ""
            case 1: 
                heb_weekday = "\u05d9\u05d5\u05b9\u05dd\u0020\u05d0\u05b6\u05d7\u05b8\u05d3"
                tl_weekday = "yom exad"
                eng_weekday = f"{weekday_count} day"
            case _:
                yamim = "\u05d9\u05b8\u05de\u05b4\u05d9\u05dd"
                heb_weekday = f"{heb_numbers_1_11[weekday_count]} {yamim}"
                tl_weekday = f"{tl_numbers_1_11[weekday_count]} yamim"
                eng_weekday = f"{weekday_count} days"

     ### Putting it all together ### 
        # break up hebrew for easier editing
        heb_haYom = "\u05d4\u05b7\u05d9\u05bc\u05d5\u05b9\u05dd"
        heb_laOmer = "\u05dc\u05b8\u05e2\u05b9\u05de\u05b6\u05e8"
        heb_1 = f"{heb_haYom} {heb_oc}" 
        heb_2 = f"\u05e9\u05b6\u05c1\u05d4\u05b5\u05dd {heb_week}{heb_and}{heb_weekday} {heb_laOmer}"
        
        heb_numbers_string = ""
        tl_numbers_string = ""
        eng_numbers_string = ""
        
        # if less than a week, just do the first part: 
        if omer_day < 7:
            heb_numbers_string = f"{heb_1} {heb_laOmer}:" 
            tl_numbers_string = f"haYom {tl_oc} laOmer:"
            eng_numbers_string = f"Today is {omer_day} {eng_day} of the Omer:"
        else: 
            heb_numbers_string = f"{heb_1}, {heb_2}:" 
            tl_numbers_string = f"haYom {tl_oc}, she'hem {tl_week}{tl_and}{tl_weekday} laOmer:"
            eng_numbers_string = f"Today is {omer_day} {eng_day}, which are {eng_week}{eng_and}{eng_weekday} of the Omer:"
 
        return (heb_numbers_string,tl_numbers_string,eng_numbers_string)




    def construct_aspect_strings(self,omer_day: int):
        """ 
        construct the strings for the aspects given.
    
        param omer_day: day of the omer
        """ 
        # divide by 7 to get the week, mod 7 for the day
        outer_idx = (omer_day-1) // 7
        inner_idx = (omer_day-1) % 7
       
        heb_aspects = self.data["heb_aspects"]
        tl_aspects = self.data["tl_aspects"]
        eng_aspects = self.data["eng_aspects"] 
        colors = self.data["colors"]
        
        idxs = [inner_idx,outer_idx]
        heb_aspect_strs = ["",""]
        tl_aspect_strs = ["",""]
        eng_aspect_strs = ["",""]
     
        for x in range(2):
            curr_idx = idxs[x]
            # hebrew & transliteration
            heb_aspect_strs[x] = f"{heb_aspects[curr_idx]}"            
            tl_aspect_strs[x] = f"{tl_aspects[curr_idx]}"
            # english 
            heart_string = colors[curr_idx] 
            if heart_string == "red":
                heart_string = ":heart:"
            else:
                heart_string = f":{heart_string}_heart:"
            eng_aspect_strs[x] = f"{heart_string} {tl_aspects[curr_idx]} ({eng_aspects[curr_idx]}) {heart_string}"
                       
        heb_join = "\u05e9\u05c1\u05b6\u05d1\u05bc\u05b0"
        tl_join = "sheb'"
        if outer_idx == 1: # gevurah uses a different connector word
            heb_join = "\u05e9\u05c1\u05b6\u05d1\u05bc\u05b4"
            tl_join = "shebi"
        
        heb_aspect_string = f"{heb_aspect_strs[0]} {heb_join}{heb_aspect_strs[1]}" 
        tl_aspect_string = f"{tl_aspect_strs[0]} {tl_join}{tl_aspect_strs[1]}"
        eng_aspect_string = f"{eng_aspect_strs[0]} within {eng_aspect_strs[1]}" 
        return (heb_aspect_string, tl_aspect_string,eng_aspect_string)



    def get_holiday_tonight(self, heb_tonight_day: heb_dates.HebrewDate) -> str: 
        eng_extra = ""
        holiday_tonight = heb_dates.HebrewDate.holiday(heb_tonight_day)
        if holiday_tonight: 
            eng_extra = f"It is also {holiday_tonight} tonight."
        return eng_extra
 


### Test functions ###

    def test(self) -> bool:
        """
        test function
        """ 
        test_pass = True
        print("test holidays")
        self.test_holidays() # holidays all good!
        print("test aspects")
        self.test_aspects()
        print("test numbers")
        self.test_numbers()
        return test_pass 

    # individual-function testers return a str so that i can post it to discord if i want
    def test_numbers(self) -> str: 
        """ 
        test construct_number_strings() function. 
        """
        for x in range(1,50): #(1,50): 1-49 inclusive
            (h,t,e) = self.construct_number_strings(x)
            print(f"{h}\n{t}\n{e}\n")
           # post =f"{h}\n{t}\n{e}\n"
        return ""

    def test_aspects(self) -> str: 
        """ 
        test construct_aspect_strings() function. 
        """
        for x in range(1,50): # 1-49 inclusive
            (h,t,e) = self.construct_aspect_strings(x)
            print(f"{h}\n{t}\n{e}\n")
        return ""

    def test_holidays(self) -> str:
        """ 
        test get_holiday_tonight() function.
        """
        heb_today = heb_dates.HebrewDate.today()  
        omer_start = heb_dates.HebrewDate(heb_today.year,1,16)
        test_holidays = {
            "normal_day" : omer_start,
            "yom hashoah" : omer_start + 11,
            "lag_baomer": omer_start + 32,
            "rosh_xodesh_sivan" : omer_start + 45
        } 
        for x in range(1,50): #1-49 inclusive
            print(x)
            print(omer_start+x)
            print(self.get_holiday_tonight(omer_start+x))
        return ""


### Logging functions ### 
 
    def log(self, message: str) -> None:
        """
        Log a message.

        :param message: The message.
        """

        if self.logging:
            with Path(getcwd()).joinpath("log.txt").open("at") as f:
                f.write(message + "\n")
