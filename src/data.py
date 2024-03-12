import inquirer
from json import load, dump
from discord import TextChannel
from src.misc import logo


class Data:
    def __init__(self):
        # DEFINING PROPERTIES
        self.path = "config.json"
        self.token = None
        self.guild = None
        self.channel = None
        self.gem = False
        self.pray = False
        self.exp = False
        self.sleep = False
        self.webhook = False
        self.commands = False
        self.daily = False
        self.sell = False
        self.solve = False

        with open(self.path, "r") as f:
            self.data = load(f)

    @property
    def accounts(self):
        return [account for account in self.data]

    def get_account(self):
        account_list = self.accounts.copy()
        account_list.append("Add Account")
        account = inquirer.list_input(
            message="Choose Your Account", choices=account_list)
        if account == "Add Account":
            return "add"
        return account

    def check_data(self):
        if "default" in self.accounts:
            self.load("default")
            return True
        return False

    def load(self, account):
        for key, value in self.data[account].items():
            setattr(self, key, value)

    def get_token(self):
        question = [inquirer.Editor(
            "token", message="Please Enter Your Discord Token")]
        self.token = inquirer.prompt(question)["token"]

    def get_guild(self, guilds):
        guild = inquirer.list_input(
            message="Choose Your Preferred Guild", choices=guilds)
        return int(guild)

    def get_channel(self, channels):
        channel = inquirer.list_input(
            message="Choose Your Preferred Channel", choices=channels)
        return int(channel)

    def get_features(self):
        features = [
            ("Use Gems", "gem"),
            ("Pray", "pray"),
            ("Gain Levels", "exp"),
            ("Avoid Human Verification", "sleep"),
            ("Send Alert Through Webhook", "webhook"),
            ("Extra Commands", "commands"),
            ("Claim Daily", "daily"),
            ("Sell Animals", "sell"),
            ("Solve Verification Captchas", "solve")]

        questions = [inquirer.Checkbox("features",
                                       message="Enable Features That You Want",
                                       choices=features,
                                       default=[
                                           "gem",
                                           "sleep",
                                           "commands"]
                                       )]

        answer = inquirer.prompt(questions)["features"]

        for feature in answer:
            setattr(self, feature, True)

        questions = [
            inquirer.Editor("url", message="Enter Your Webhook URL", validate=lambda self, x: x.startswith(
                "https://discord.com/api/webhooks/"), ignore=lambda x: not self.webhook),
            inquirer.Editor("id", message="Enter UserID To Mention With Webhook", validate=lambda self, x: x.replace(
                "\n", "").isnumeric(), ignore=lambda x: not self.webhook),
            inquirer.Text("commands", message="Enter Your Bot Prefix",
                          validate=lambda self, x: x != "", ignore=lambda x: not self.commands),
            inquirer.List("sell",
                          message="Choose The Animal Rarity You Want To Sell",
                          choices=[
                              ("Common", "c"),
                              ("Uncommon", "u"),
                              ("Rare", "r"),
                              ("Epic", "e"),
                              ("Mythical", "m"),
                              ("Legendary", "l"),
                              ("Gem", "g"),
                              ("All Animals", "a")
                          ],
                          ignore=lambda x: not self.sell)]

        answers = inquirer.prompt(questions)

        if self.webhook:
            self.webhook = {"url": answers["url"].replace(
                "\n", ""), "id": answers["id"].replace("\n", "")}

        if self.commands:
            self.commands = {"prefix": answers["commands"]}

        if self.sell:
            self.sell = {"type": answers["sell"]}

    def save(self, account):
        if "default" in self.data:
            self.data = {}

        self.data.update({
            account:
                {
                    attr: getattr(self, attr) for attr in self.__dict__ if not attr in ("path", "data", "guild")
                }
        }
        )

        with open(self.path, 'w') as f:
            dump(self.data, f, ensure_ascii=False, indent=4)

    def setup(self, client, new):
        if new:
            guilds = [guild for guild in client.guilds]

            guild = client.get_guild(self.get_guild([(guild.name, str(guild.id))
                                                     for guild in guilds]))

            channels = guild.channels

            self.channel = self.get_channel([(channel.name, channel.id)
                                             for channel in channels if isinstance(channel, TextChannel)])

            self.save(client.user.name)

        self.channel = client.get_channel(self.channel)
        self.guild = self.channel.guild
        logo(clear=True)


data = Data()
