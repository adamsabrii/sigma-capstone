import pandas as pd  # type: ignore
from math import asin, sin, cos, sqrt, radians, pi
from random import choice
from rich.console import Console
from rich.table import Column, Table
import time
import questionary as qty

# Ideas for console:
# Use a table that shows the list of countries
# Use a table that shows the user's guesses

# Plan:
# Start with implementing the console
# I guess just go from there.

RADIUS_EARTH = 6371  # km

console = Console(width=100)


class Worldle():
    def __init__(self):
        with console.status("\nStarting game...\n"):
            self.data = self.read_data()
            self.table = self.init_table()
            time.sleep(1.5)
        console.rule(
            "[green bold] WORLDLE :earth_africa:")

    def init_table(self):
        table = Table(
            Column("Guess No", justify="right"),
            Column("Country", justify="left", no_wrap=True),
            Column("Distance (km)", justify="right"),
            title="")
        return table

    def game_logic(self, country_coords):
        """
        The main game function

        *** Need to implement duplicate guesses feature ***

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        """

        view_flag = self.introductions()
        if view_flag:
            self.view_countries(country_coords)
        target_country = self.random_country(country_coords)
        # print(target_country)
        guess_history = []
        guess_no = 0
        limit = 200

        while guess_no < limit:
            console.rule(
                "[green bold] WORLDLE :earth_africa:")
            console.print(
                "After you've made your first guess, if you would like a hint type 'hint'.")
            console.print(
                f"\nYou may like to know that maximum distance between two countries is {int(pi*RADIUS_EARTH)}km")
            console.print(
                "\n** Game is currently case and punctuation sensitive **")
            if len(guess_history) != 0:
                self.table.add_row(
                    str(guess_no), guess_history[guess_no-1][0], str(guess_history[guess_no-1][1]))
                console.print(self.table, justify="center")

            # user guess - validation - hint
            guess = self.user_guess(
                country_coords, guess_history, target_country)
            # is correct?
            guess_no = self.is_correct(guess, target_country, guess_no)
            # calc_distance
            distance = self.calc_distance(
                target_country, guess, country_coords)
            guess_history.append((guess, distance))
            console.clear()
            print("")

        print(f"You're out of guesses! The country was {target_country}")
        return

    def read_data(self):
        """
        Reads the data named 'country-coord.csv' saved in the same working directory.
        Extension: be able to read the csv if the working directory is from a parent directory.

        :param self: --

        Returns:
        A dictionary with keys: (country names) and the values: (latitude (average)) and longitude (average))
        """
        col_names = ["Country", "Latitude (average)", "Longitude (average)"]
        df = pd.read_csv("country-coord.csv",
                         usecols=col_names, index_col="Country")
        df = df.T
        country_coords = df.to_dict()
        return country_coords

    def introductions(self):
        """
        Introductions

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        """
        console.print("\n[underline]Welcome to Worldle!", justify="center")
        console.print(
            "\nA country will be chosen at random and all you have to do is find it!")
        console.print(
            "\n[red]** You may type 'exit' at [bold]any[/] point to quit the game. **")
        to_view = console.input(
            "\nEnter 'yes' if you would like to view the list of countries before starting...\n\n[italics]Recommended to check spelling\n\notherwise enter anything to continue: ").strip().lower()
        view_flag = False
        if to_view == "yes":
            view_flag = True
        elif to_view == "exit":
            self.quit_game()
        console.clear()
        print("")
        return view_flag

    def view_countries(self, country_coords):
        """
        Prints the country strings to the user

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        """
        countries = list(country_coords.keys())
        print("\n", countries)
        return

    def random_country(self, country_coords):
        """
        Chooses a country at random

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))

        Returns:
        The target country as a string
        """
        target_country = choice(list(country_coords.keys()))
        return target_country

    def hint(self, country_coords, guess_history, target):  # working here!!!
        """
        Docstring for hint

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        :param guess_history: Expects a dictionary that contains keys: (country names)
          and the values: (distance from target)
        :param target: Target country (str)
        :return: The countries within the same radius of their best guess to the target.
        :rtype: list
        """
        # find best guess
        best_dist = min([item[1] for item in guess_history])
        # best_guess = [k for k in guess_history if guess_history[k] == best_dist][0]
        hint_list = [country for country in country_coords.keys(
        ) if self.calc_distance(target, country, country_coords) <= best_dist]
        return hint_list

    def user_guess(self, country_coords, guess_history, target):
        """
        Takes the user input and does some validation.
        *** Validation can be improved for case sensitivity. Could be tricky to conserve the lowercase 'the'
        and 'of' in the names. ***
        The user can type exit (not case sensitive) to quit the game.

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))

        Returns:
        The user's guess as a string.
        """

        while True:
            guess = input("\nEnter a country: ")
            if any([ch.isnumeric() for ch in guess]):
                print("\nLooks like you've entered a number...")
            elif guess.strip().lower() == "exit":
                self.quit_game()
            elif len(guess_history) != 0 and guess.strip().lower() == "hint":
                print(self.hint(
                    country_coords, guess_history, target))
            elif self.guess_validation(guess, country_coords):
                break
            else:
                print("\n Try again...")
        return guess

    def guess_validation(self, guess, country_coords):
        """
        Checks the user's input is in the country data

        :param self: --
        :param guess: The user's guess (str)
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))

        Returns:
        A boolean flag.
        """
        flag_val = False
        if guess in country_coords:
            flag_val = True
            # print("\n The country is in the list")
        else:
            print("\nThe country you've entered didn't match those in the list.")
        return flag_val

    def calc_distance(self, country1, country2, country_coords):
        """
        Calculates the distance between two countries using the Haversine formula.
        The assumptions here are that the Earth is a perfect sphere and the country's position is its average
         latitude and longitude.

        :param self: --
        :param country1: (str)
        :param country2: (str)
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))

        Returns:
        The distance (float) rounded to 2 decimal places.
        """
        global RADIUS_EARTH
        lat_value_1, long_value_1 = country_coords.get(country1).values()
        lat_value_2, long_value_2 = country_coords.get(country2).values()

        phi1, lam1 = radians(lat_value_1), radians(long_value_1)
        phi2, lam2 = radians(lat_value_2), radians(long_value_2)

        distance = round(2 * RADIUS_EARTH * asin(
            sqrt(sin(0.5 * (phi2 - phi1)) ** 2 + cos(phi1)
                 * cos(phi2) * sin(0.5 * (lam2 - lam1)) ** 2)
        ), 2)
        # print(f"Distance between {country1} and {country2} is {distance} km")

        return distance

    def is_correct(self, guess, target, guess_no):
        """
        Checks if the country guessed matches the target country.

        :param self: --
        :param guess: User's guess (str)
        :param target: Random target country (str)
        :param guess_no: The attempt number (int)

        Returns:
        The guess number appended by 1 if the countries don't match, otherwise runs the .winner() method.
        """
        if guess == target:
            self.winner(guess_no+1, guess)
        else:
            guess_no += 1
        return guess_no

    def winner(self, guess_no, guess):
        """
        Prints winner messages and asks user if they want to play again

        :param self: --
        :param guess_no: (int)
        """
        console.clear()
        print("")
        self.table.add_row("[white on green]" +
                           str(guess_no), "[white on green]" +
                           guess, "[white on green]0"
                           )
        console.print(self.table, justify="center")
        console.print(
            f"\n[green bold]Congratulations! You got it in {guess_no} guesses", justify="center")
        # print("\nDo you want to play again?")
        # again = input("Yes or No: ").strip().lower()
        again = qty.select("Would you like to play again?:", choices=[
            'Yes', 'No']).ask()
        if again == 'Yes':
            self.table = self.init_table()
            self.game_logic(self.data)
        elif again == 'No' or again == 'exit':
            self.quit_game()
        else:
            console.clear()
            print("")
        return

    def quit_game(self):
        """
        Quits the end

        :param self: --
        """
        print("\nEnding game")
        time.sleep(1.5)
        console.clear()
        quit()
        return


if __name__ == "__main__":
    Game = Worldle()
    Game.game_logic(Game.data)
    Game.quit_game()
