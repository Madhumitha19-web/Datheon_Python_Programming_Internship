import random
from pathlib import Path

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


def load_words():
    word_file = Path(__file__).with_name('google-10000-english-no-swears.txt')
    if word_file.exists():
        words = [w.strip().lower() for w in word_file.read_text(encoding='utf-8').splitlines()
                 if w.strip().isalpha() and 4 <= len(w.strip()) <= 10]
        if words:
            return words
    return ['python', 'computer', 'flower', 'school', 'planet', 'garden']


def play_game(words):
    secret = random.choice(words)
    guessed = set()
    mistakes = 0
    print('\nWelcome to Hangman!')
    while mistakes < 6:
        print(STAGES[mistakes])
        display = ' '.join(letter if letter in guessed else '_' for letter in secret)
        print('\nWord:', display)
        print('Attempts left:', 6 - mistakes)
        print('Guessed letters:', ', '.join(sorted(guessed)) or 'None')
        if all(letter in guessed for letter in secret):
            print('\nYOU WIN! The word was:', secret.upper())
            return
        letter = input('Guess a letter: ').strip().lower()
        if len(letter) != 1 or not letter.isascii() or not letter.isalpha():
            print('Please enter one English letter.')
        elif letter in guessed:
            print('Already guessed! No attempt deducted.')
        else:
            guessed.add(letter)
            if letter in secret:
                print('Correct!')
            else:
                mistakes += 1
                print('Wrong guess!')
    print(STAGES[6])
    print('\nGAME OVER! The word was:', secret.upper())


def main():
    words = load_words()
    while True:
        play_game(words)
        if input('\nPlay again? (y/n): ').strip().lower() != 'y':
            print('Thanks for playing!')
            break


if __name__ == '__main__':
    main()
