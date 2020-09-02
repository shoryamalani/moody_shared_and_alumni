from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import random
import sys

def roll_level_two():
    global thesecond, thethird, thefourth
    numbers = []
    thefirst = random.randint(0, 9)
    numbers.append(thefirst)
    loop = ''
    while loop != 'stop':
        thesecond = random.randint(0, 9)
        if thesecond not in numbers:
            numbers.append(thesecond)
            loop = 'stop'
    stop_loop = ''
    while stop_loop != 'stop':
        thethird = random.randint(0, 9)
        if thethird not in numbers:
            numbers.append(thethird)
            stop_loop = 'stop'
    end_loop = ''
    while end_loop != 'stop':
        thefourth = random.randint(0, 9)
        if thefourth not in numbers:
            numbers.append(thefourth)
            end_loop = 'stop'
    return f'{thefirst} {thesecond} {thethird} {thefourth}'

# Used to generate a unique integer to be used in roll_level_two and roll_level_three
def checker(mist):
    global variable
    looper = ''
    while looper != 'stop':
        variable = random.randint(0, 9)
        if variable not in mist:
            mist.append(variable)
            looper = 'stop'
    return variable
    
def roll_level_three():
    please = ''
    while please != 'stop':
        numbers = []
        zafirst = random.randint(0, 9)
        numbers.append(zafirst)
        zasecond = int(checker(numbers))
        zathird = int(checker(numbers))
        zafourth = int(checker(numbers))
        zafifth = int(checker(numbers))
        zasixth = int(checker(numbers))
        value = f'{zafirst} {zasecond} {zathird} {zafourth} {zafifth} {zasixth}'
        if len(str(value)) == 11:
            please = 'stop'
    return value

answer = None
answer_list = []
initial = None
score = 0


class EasyInput(TextInput):
    max_characters = NumericProperty(3)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ""
        TextInput.insert_text(self, substring, from_undo)
    

class HardInput(TextInput):
    max_characters = NumericProperty(5)
    def insert_text(self, substring, from_undo=False):
        if len(self.text) > self.max_characters and self.max_characters > 0:
            substring = ''
        TextInput.insert_text(self, substring, from_undo)


class WinScreen(Screen):
    pass


class TheManager(ScreenManager):
    eguess = ObjectProperty(None)
    hguess = ObjectProperty(None)

    # def on_parent(self, widget, parent):
    #    EasyInput.focus = True
    #    HardInput.focus = True
    #    print("focused")
    
    def clear(self):
        global answer, answer_list, initial, score
        answer = None
        answer_list = []
        initial = None
        score = 0
        self.easylabel.text = "Your Attempt Results"
        self.hardlabel.text = "Your Attempt Results"
        self.score.text = "SOLVED\nscore:"
        self.eguess.text = ''
        self.hguess.text = ''

    def easy(self):
        global answer_list, score
        answer = roll_level_two()
        answer_list = str(answer).split(' ')
        # print(answer_list)
        score = 0
        
    def easyguess(self):
        global guess_list, score, numbers_of_b, numbers_of_c
        initial = self.eguess.text
        score += 1

        # Checks to make sure that the input is valid, and allows user to quit program.
        try:
            integeral = int(initial)
        except ValueError:
            self.easylabel.text += f'\nEnter 4 digit number only.'
        
        # Logs the valid input as guess
        guess = " ".join(initial)
        guess_list = guess.split(' ')

        # Checks to make sure that there will be no IndexError
        if len(guess_list) != 4:
            self.easylabel.text += f'\n{guess}- Enter 4 digit number only.'
        else: 
            # Counts the number of "bull" (correct placement) digits, and number of "cat" (incorrect placement,
            # but in answer) digits
            numbers_of_b = 0
            numbers_of_c = 0
            if guess_list[0] == answer_list[0]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[0] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[1] == answer_list[1]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[1] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[2] == answer_list[2]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[2] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[3] == answer_list[3]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[3] in answer_list:
                    numbers_of_c = numbers_of_c + 1

            # Instance in which the user guesses the correct answer and wins
            if not numbers_of_b == 4:
                self.easylabel.text += f'\n{guess}- {numbers_of_c} cat and {numbers_of_b} bull.'
            elif guess_list == answer_list:
                self.current='win'
                self.score.text += f"{score}"

        self.eguess.text = ''
    

    def hard(self):
        global answer_list, score
        answer = roll_level_three()
        answer_list = str(answer).split(' ')
        # print(answer_list)
        score = 0

    def hardguess(self):
        global guess_list, score, numbers_of_b, numbers_of_c

        initial = self.hguess.text
        score += 1

        # Validates input, allows user to quit program
        try:
            integeral = int(initial)
        except ValueError:
            self.hardlabel.text += f'\nEnter 6 digit number only.'

        # Logs valid input
        guess = " ".join(initial)
        guess_list = guess.split(' ')

        # Checks to make sure that there will be no IndexError
        if len(guess_list) != 6:
            self.hardlabel.text += f'\n{guess}- Enter 6 digit number only.'
        else:
             # Counts the number of "bull" (correct placement) digits, and number of "cat" (incorrect placement,
            # but in answer) digits
            numbers_of_b = 0
            numbers_of_c = 0
            if guess_list[0] == answer_list[0]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[0] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[1] == answer_list[1]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[1] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[2] == answer_list[2]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[2] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[3] == answer_list[3]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[3] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[4] == answer_list[4]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[4] in answer_list:
                    numbers_of_c = numbers_of_c + 1
            if guess_list[5] == answer_list[5]:
                numbers_of_b = numbers_of_b + 1
            else:
                if guess_list[5] in answer_list:
                    numbers_of_c = numbers_of_c + 1

            # Instance in which the user guesses the correct answer and wins
            if not numbers_of_b == 6:
                self.hardlabel.text += f'\n{guess}- {numbers_of_c} cat and {numbers_of_b} bull.'
            elif guess_list == answer_list:
                self.current='win'
                self.score.text += f"{score}"

        self.hguess.text = ''
       
    

class MainApp(App):
    def build(self):
        return TheManager()

    

if __name__ == "__main__":
    MainApp().run()