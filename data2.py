from json import load, dump
from typing import Type


class Data:
    def __init__(self) -> Type["Data"]:
        """
        Constructor for the Data class.

        Initializes the data of a specific account based on the provided 'account' parameter.

        """

        # Path to the configuration file

        # Name of the account
        self.name = None

        # URL To The Avatar
        self.avatar = None
        # Token for the account
        self.token = None

        # Guild or server the account is associated with
        self.guild = None

        # Channel or room the account is associated with
        self.channel = None

        # Flags indicating the state of various features
        self.gem = False  # Gem collection feature
        self.pray = False  # Praying feature
        self.exp = False  # Experience gain feature
        self.sleep = False  # Sleeping feature
        self.webhook = False  # Webhook feature
        self.commands = False  # Command feature
        self.daily = False  # Daily feature
        self.sell = False  # Selling feature
        self.solve = False  # Solving feature

        # Load the configuration data from the JSON file
        with open("config2.json", "r") as f:
            self.data = load(f)

        # Set the attributes of the class based on the configuration data

    def load(self, account: str) -> Type["Data"]:
        for key, value in self.data[account].items():
            setattr(self, key, value)

        self.name = account

        return self

    def save(self, account: str, data: dict) -> Type["Data"]:
        """
        Save account data to file.

        :param account: str - the account to save data for
        :param data: dict - the data to save
        :return : Type["Data"] - the account's data
        """
        self.data.update({account: data})

        with open("config2.json", 'w') as f:
            dump(self.data, f, ensure_ascii=False, indent=4)

        return self

    def remove(self, account: str) -> None:
        """
        Remove account data from file.

        :param account: str - the account to remove data for
        :return: None
        """
        self.data.pop(account, None)

        with open("config2.json", 'w') as f:
            dump(self.data, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_account() -> dict:
        """
        Get all account names

        :return: dict - all account names
        """

        with open("config2.json", "r") as f:
            return [account for account in load(f)]
