import pandas as pd
from math import asin, sin, cos, sqrt, radians, pi
from random import choice


RADIUS_EARTH = 6371  # km


class Worldle():
    def __init__(self):
        print("\nStarting game\n")
        self.data = self.read_data()

    def game_logic(self, country_coords):
        """
        The main game function

        *** Need to implement duplicate guesses feature ***
        *** Improve game loop ***
        *** Implement console ***

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        """
        self.introductions(country_coords)
        target_country = self.random_country(country_coords)
        # print(target_country)
        guess_history = {}
        guess_no = 1
        limit = 25
        while guess_no < limit:
            print(f"\nGuess {guess_no}")
            # hint
            hint_request = None
            if len(guess_history) != 0:
                print(
                    f"You're closest guess was {min(guess_history.values())}km off, would you like a hint?")
                hint_request = input(
                    "Type 'yes' if you would like a hint: ").lower()
                if hint_request == 'yes':
                    hint_list = self.hint(
                        country_coords, guess_history, target_country)
                    print(hint_list)

            # user guess - validation
            guess = self.user_guess(country_coords)
            # is correct?

            guess_no = self.is_correct(guess, target_country, guess_no)
            # calc_distance
            distance = self.calc_distance(
                target_country, guess, country_coords)
            guess_history[guess] = distance
            print(f"\nYou're off by {distance}km!")

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

    def introductions(self, country_coords):
        """
        Introductions

        :param self: --
        :param country_coords: Expects the dictionary contains keys: (country names)
          and the values: (latitude (average)) and longitude (average))
        """
        print("\n\nWelcome to Worldle!")
        print("\nA country will be chosen at random and all you have to do is find it!")
        print("\n** You may type 'exit' at any point to quit the game. **")
        to_view = input("\nIf you have just started a session, I recommend having a look at the list of countries.\nEnter 'yes' if you would like to view the list of countries before starting...\notherwise enter anything to continue: ").strip().lower()
        if to_view == "yes":
            self.view_countries(country_coords)
        elif to_view == "exit":
            self.quit_game()
        print(
            f"\nYou may like to know that circumference of the Earth is {int(2*pi*RADIUS_EARTH)}km")
        return

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
        best_dist = min(guess_history.values())
        # best_guess = [k for k in guess_history if guess_history[k] == best_dist][0]
        hint_list = [country for country in country_coords.keys(
        ) if self.calc_distance(target, country, country_coords) <= best_dist]
        return hint_list

    def user_guess(self, country_coords):
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
        print("\n** Game is currently case and punctuation sensitive **")
        flag = False
        while flag == False:
            guess = input("\nEnter a country: ")
            if any([ch.isnumeric() for ch in guess]):
                print("\nLooks like you've entered a number...")
            elif guess.strip().lower() == "exit":
                self.quit_game()
            elif self.guess_validation(guess, country_coords):
                break
            else:
                print("\n Try again.")
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
            self.winner(guess_no)
        else:
            guess_no += 1
        return guess_no

    def winner(self, guess_no):
        """
        Prints winner messages and asks user if they want to play again

        :param self: --
        :param guess_no: (int)
        """
        print(f"\n*** Congratulations! You got it in {guess_no} guesses ***")
        print("\nDo you want to play again?")
        again = input("Yes or No: ").strip().lower()
        if again == 'yes':
            self.game_logic(self.data)
        elif again == 'no' or again == 'exit':
            self.quit_game()
        else:
            print("Enter 'yes' or 'no'.")
        return

    def quit_game(self):
        """
        Quits the end

        :param self: --
        """
        print("\nEnding game")
        quit()
        return


if __name__ == "__main__":
    Game = Worldle()
    Game.game_logic(Game.data)
    Game.quit_game()
