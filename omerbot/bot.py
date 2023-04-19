from pathlib import Path
from os import getcwd
from pkg_resources import resource_filename
from json import loads
import random
from datetime import datetime
import discord


class Bot(discord.Client):
    """
    Post a random mishnah sugye every day.
    """

    def __init__(self, channel: int, logging: bool = True):
        """
        :param channel: The ID of the channel.
        :param logging: If True, log messages.
        """

        self.channel: int = int(channel)
        self.mishnah = loads(Path(resource_filename(__name__, "data/mishnah.json")).read_text())
        self.logging: bool = logging
        super().__init__()

    async def on_ready(self):
        # Connect to the Discord channel.
        channel = self.get_channel(self.channel)
        today = datetime.today()
        # Get a random sugye.
        sugye = self.mishnah[random.randint(0, len(self.mishnah) + 1)]
        url = f"https://www.sefaria.org/Mishnah_{sugye['Order'].replace(' ', '_')}.{sugye['Chapter']}.{sugye['Verse']}?lang=bi"
        # Get the English text. Convert HTML tags to markdown tags.
        en = sugye['en'].replace("<b>", "**").replace("</b>", "**").replace("<i>", "_").replace("</i>", "_")
        # Create a citation.
        citation = f"{sugye['Order']} {sugye['Chapter']}.{sugye['Verse']}"
        self.log(f"{today}: {citation}")
        # Get the text.
        he = sugye["he"]
        text = f"**{citation}**\n{he}\n{en}\n{url}"
        # Split the text into posts of <= 2000 characters.
        posts = [text[index: index + 2000] for index in range(0, len(text), 2000)]
        try:
            # Post.
            for post in posts:
                await channel.send(post)
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
