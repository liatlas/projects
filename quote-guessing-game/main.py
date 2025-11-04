import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

class GuessingGame:
    def __init__(self, base_url, url, guesses):
        self._base_url = base_url
        self._url = url
        self._all_quotes = []
        self._remaining_guesses = guesses

    def make_requests(self):
        while self._url:
            result = requests.get(f"{self._base_url}{self._url}")
            print(f"Now scraping {self._base_url}{self._url}")
            soup = BeautifulSoup(result.text, "html.parser")

            self.quotes = soup.find_all(class_="quote")

            for quote in self.quotes:
                self._all_quotes.append({
                        "text": quote.find(class_="text").get_text(),
                        "author": quote.find(class_="author").get_text(),
                        "bio-link": quote.find("a")["href"]
                    })
            next_btn = quote.find(class_="next")
            self._url = next_bin.find("a")["href"] if next_btn else None
            sleep(2)

    def play(self):
        self.quote = choice(self._all_quotes)
        self.print_quote()
        self.guess = ''
        
        while self.incorrect_guess() and self._remaining_guesses > 0:
            self.get_guess()


            if not self.incorrect_guess():
                print("You got it right!")
                break

            self._remaining_guesses -= 1

            hints = {
            3: self.hint_birth_place_date,
            2: self.hint_first_name,
            1: self.hint_last_name
            }

            hint_func = hints.get(self._remaining_guesses)

            if hint_func:
                hint_func()
            else:
                print("Sorry, You're out of guesses")
                print(f"The author was {self.quote['author']}")

    def get_guess(self):
        self.guess = input(
                f"Who said this quote? Guesses remaining {self._remaining_guesses}: "
                )

    def hint_birth_place_date(self):
        result = requests.get(f"{self._base_url}{self.quote['bio-link']}")
        soup = BeautifulSoup(result.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
    
    def hint_first_name(self):
        print(f"Here's a hint: The author's first name starts with: {self.quote['author'][0]}")

    def hint_last_name(self):
        last_initial = self.quote["author"].split(" ")[1][0]
        print(f"Here's a hint: The author's first name starts with: {last_initial}")

    def incorrect_guess(self):
        if self.guess.lower() != self.quote["author"].lower():
            return True
        return False

    def print_quote(self):
        print("Here's a quote: ")
        print(self.quote["text"])



def main():
    base_url = "https://quotes.toscrape.com/"
    url = "/page/1"
    guesses = 4


    g = GuessingGame(base_url, url, guesses)
    
    g.make_requests()

    g.play()

if __name__ == "__main__":
    main()
