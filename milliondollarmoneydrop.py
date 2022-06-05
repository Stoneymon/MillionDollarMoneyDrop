import tkinter
import requests
import random
from tkinter import messagebox
import database


class Game:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title('Million Dollar Money Drop')
        self.root.geometry('1000x700')
        self.questions = None

    def winning_screen(self, username, money):
        '''
        :param username: Username of the Player
        :param money: The amount of money the player won
        :return:
        '''
        frame = tkinter.Frame(self.root)
        frame.pack()

        messagebox.showinfo(title='Winner', message=f'Congratulations! You won ${money}!')

        database.update(username, money)
        user = database.get_user(username)

        menu_button = tkinter.Button(frame, text='Main Menu', command=lambda: [self.main_menu(username, user[0][2]), frame.destroy()])
        menu_button.pack()

    def losing_screen(self, username):
        '''
        :param username: Player's username
        :return:
        '''
        messagebox.showinfo(title='Loser', message=f'Better luck next time!')

        frame = tkinter.Frame(self.root)
        frame.pack()


        database.update(username, 0)
        user = database.get_user(username)

        menu_button = tkinter.Button(frame, text='Main Menu', command=lambda: [self.main_menu(username, user[0][2]), frame.destroy()])
        menu_button.pack()

    def singleplayer(self, username, iteration, money):
        '''
        :param username:
        :param iteration: starts with 1, there are 10 questions, this variable keeps count of which question to use
        :param money: Starting from 1 Million, gets updated with every question
        shows the question and 4 (questions 1-5) or 3 (questions 6-10) possible answers
        you can bet the money you have in they entry boxes
        after you press the submit button, it submits the money you bet on the answers and after the answers are validated
        it calls the function again with iteration+1
        :return:
        '''
        sp_screen = tkinter.Frame(self.root)
        sp_screen.pack()

        top = tkinter.Frame(sp_screen)
        top.pack()

        user = tkinter.Label(top, text='User: ' + username)
        user.grid(row=0, column=0)

        money_left = tkinter.Label(top, text='Money: $' + str(money))
        money_left.grid(row=0, column=1)

        question_nr = tkinter.Label(top, text='Question: ' + str(iteration) + '/10')
        question_nr.grid(row=0, column=2)

        q_screen = tkinter.Frame(sp_screen)
        q_screen.pack()

        q = self.questions[iteration - 1]['question']
        q_label = tkinter.Label(q_screen, text=q)
        q_label.pack()

        a_screen = tkinter.Frame(sp_screen)
        a_screen.pack()

        #in the first 5 questions there are 4 answers after that only 3
        if iteration <= 5:
            answers = self.questions[iteration - 1]['incorrectAnswers']
        else:
            answers = self.questions[iteration - 1]['incorrectAnswers'][0:2]

        correct_answer = (self.questions[iteration - 1]['correctAnswer'])
        answers.append(correct_answer)
        random.shuffle(answers)

        answer1_label = tkinter.Label(a_screen, text='A: ' + answers[0])
        answer1_label.grid(row=0, column=1)

        a1 = tkinter.Label(a_screen, text='$')
        a1.grid(row=1, column=0, sticky=tkinter.E)

        answer1_entry = tkinter.Entry(a_screen)
        answer1_entry.insert(0, '0')
        answer1_entry.grid(row=1, column=1, sticky=tkinter.W + tkinter.E)

        answer2_label = tkinter.Label(a_screen, text='B: ' + answers[1])
        answer2_label.grid(row=2, column=1)

        a2 = tkinter.Label(a_screen, text='$')
        a2.grid(row=3, column=0, sticky=tkinter.E)

        answer2_entry = tkinter.Entry(a_screen)
        answer2_entry.insert(0, '0')
        answer2_entry.grid(row=3, column=1, sticky=tkinter.W + tkinter.E)

        answer3_label = tkinter.Label(a_screen, text='C: ' + answers[2])
        answer3_label.grid(row=4, column=1)

        a3 = tkinter.Label(a_screen, text='$')
        a3.grid(row=5, column=0, sticky=tkinter.E)

        answer3_entry = tkinter.Entry(a_screen)
        answer3_entry.insert(0, '0')
        answer3_entry.grid(row=5, column=1, sticky=tkinter.W + tkinter.E)

        #4th answer only exists for questions 1-5
        if iteration <= 5:
            answer4_label = tkinter.Label(a_screen, text='D: ' + answers[3])
            answer4_label.grid(row=6, column=1)

            a4 = tkinter.Label(a_screen, text='$')
            a4.grid(row=7, column=0, sticky=tkinter.E)

            answer4_entry = tkinter.Entry(a_screen)
            answer4_entry.insert(0, '0')
            answer4_entry.grid(row=7, column=1, sticky=tkinter.W + tkinter.E)

        def answer_check():
            '''
            checks if the answers are valid
            (for the first questions 1-5 max 3 answers, for questions 6-10 max 2 answers)
            answers have to be integers greater than 0 and you can only bet up to the amount of money you have left
            if inputs are not valid they get set to 0, if you bet more money than you have it shows an errorbox and
            you have to answer the question again
            :return:
            '''
            answer1 = answer1_entry.get()
            try:
                answer1 = int(answer1)
            except ValueError:
                answer1 = 0
            answer2 = answer2_entry.get()
            try:
                answer2 = int(answer2)
            except ValueError:
                answer2 = 0
            answer3 = answer3_entry.get()
            try:
                answer3 = int(answer3)
            except ValueError:
                answer3 = 0
            if iteration <= 5:
                answer4 = answer4_entry.get()
                try:
                    answer4 = int(answer4)
                except ValueError:
                    answer4 = 0
            else:
                answer4 = 0

            if answer1 < 0:
                answer1 = 0
            if answer2 < 0:
                answer2 = 0
            if answer3 < 0:
                answer3 = 0
            if iteration <= 5 and answer4 < 0:
                answer4 = 0

            if (answer1 + answer2 + answer3 + answer4) > int(money):
                messagebox.showerror(title=None, message="You don't have that much money!")
                sp_screen.pack_forget()
                sp_screen.destroy()
                return self.singleplayer(username, iteration, money)

            answered = 0
            if answer1 != 0:
                answered += 1
            if answer2 != 0:
                answered += 1
            if answer3 != 0:
                answered += 1
            if iteration <= 5 and answer4 != 0:
                answered += 1

            if iteration <= 5:
                if answered == 4:
                    messagebox.showerror(title=None, message="You're only allowed to bet on 3 answers!")
                    sp_screen.pack_forget()
                    sp_screen.destroy()
                    return self.singleplayer(username, iteration, money)

            else:
                if answered > 2:
                    messagebox.showerror(title=None, message="You're only allowed to bet on 2 answers!")
                    sp_screen.pack_forget()
                    sp_screen.destroy()
                    return self.singleplayer(username, iteration, money)

            if answers[0] == correct_answer:
                return answer1
            elif answers[1] == correct_answer:
                return answer2
            elif answers[2] == correct_answer:
                return answer3
            else:
                return answer4

        if iteration < 10:
            lock_in_button = tkinter.Button(a_screen, text='Lock In', command=lambda: [answer_check(), self.singleplayer(username, iteration + 1, answer_check()), sp_screen.pack_forget(), sp_screen.destroy()])
            lock_in_button.grid(row=8, column=0, columnspan=2)
        else:
            lock_in_button = tkinter.Button(a_screen, text='Lock In', command=lambda: [answer_check(), self.winning_screen(username, answer_check()), sp_screen.pack_forget(), sp_screen.destroy()])
            lock_in_button.grid(row=8, column=0, columnspan=2)

        if money == 0:
            sp_screen.destroy()
            self.losing_screen(username)

    def set_difficulty(self, difficulty):
        if difficulty == 0:
            self.questions = requests.get(f'https://the-trivia-api.com/api/questions?limit=10&difficulty=easy').json()
        elif difficulty == 1:
            self.questions = requests.get(f'https://the-trivia-api.com/api/questions?limit=10&difficulty=medium').json()
        elif difficulty == 2:
            self.questions = requests.get(f'https://the-trivia-api.com/api/questions?limit=10&difficulty=hard').json()

    def show_history(self, username, money):
        '''
        shows the last 10 games you played (username, how much money you won, date)
        :return:
        '''
        hist = database.get_history(username)

        frame = tkinter.Frame(self.root)
        frame.pack()

        user_label = tkinter.Label(frame, text='User')
        user_label.grid(row=0, column=0)
        money_label = tkinter.Label(frame, text='Money won')
        money_label.grid(row=0, column=1)
        date_label = tkinter.Label(frame, text='Date')
        date_label.grid(row=0, column=2)

        if len(hist) > 10:
            i = 1
            for match in range(len(hist) - 1, len(hist) - 11, -1):
                user = tkinter.Label(frame, text=hist[match][0])
                user.grid(row=i, column=0)
                money_made = tkinter.Label(frame, text=hist[match][1])
                money_made.grid(row=i, column=1)
                date = tkinter.Label(frame, text=hist[match][2])
                date.grid(row=i, column=2)
                i += 1
            back_button = tkinter.Button(frame, text='Back',
                                         command=lambda: [self.main_menu(username, money), frame.destroy()])
            back_button.grid(row=11, column=1)

        elif len(hist) > 0 and len(hist) < 10:
            for match in range(len(hist)):
                user = tkinter.Label(frame, text=hist[match][0])
                user.grid(row=match + 1, column=0)
                money_made = tkinter.Label(frame, text=hist[match][1])
                money_made.grid(row=match + 1, column=1)
                date = tkinter.Label(frame, text=hist[match][2])
                date.grid(row=match + 1, column=2)
            back_button = tkinter.Button(frame, text='Back', command=lambda: [self.main_menu(username, money), frame.destroy()])
            back_button.grid(row=match + 2, column=1)

        else:
            nothing = tkinter.Label(frame, text='no games found')
            nothing.grid(row=1, column=1)
            back_button = tkinter.Button(frame, text='Back', command=lambda: [self.main_menu(username, money), frame.destroy()])
            back_button.grid(row=2, column=1)

    def main_menu(self, username, money):
        '''
        Main Menu - shows username and total amount of money on top
        slider for difficulty - easy, medium, hard
        play button - starts the game with the difficulty you chose
        previous games button - shows the last 10 games you played
        exit button - closes the game
        :return:
        '''
        menu_screen = tkinter.Frame(self.root)
        menu_screen.pack()

        top = tkinter.Frame(menu_screen)
        top.pack(side=tkinter.TOP)
        bottom = tkinter.Frame(menu_screen)
        bottom.pack(side=tkinter.TOP)

        user = tkinter.Label(top, text='User: ' + username)
        user.pack(side=tkinter.LEFT)

        score = tkinter.Label(top, text='Total Money: $' + str(money))
        score.pack(side=tkinter.RIGHT)

        scale_labels = {
            0: 'easy',
            1: 'medium',
            2: 'hard'
        }

        def scale_labelss(value):
            difficulty.config(label=scale_labels[int(value)])

        difficulty = tkinter.Scale(bottom, from_=0, to=2, orient=tkinter.HORIZONTAL, showvalue=False, command=scale_labelss)
        difficulty.pack()
        scale_labelss(difficulty.get())

        sp_button = tkinter.Button(bottom, text='Play', command=lambda: [self.set_difficulty(difficulty.get()), self.singleplayer(username, 1, 1000000), menu_screen.pack_forget(), menu_screen.destroy()])
        sp_button.pack()

        history_button = tkinter.Button(bottom, text='Previous Games', command=lambda: [self.show_history(username, money), menu_screen.destroy()])
        history_button.pack()

        exit_button = tkinter.Button(bottom, text='Exit', command=self.root.destroy)
        exit_button.pack()

    def login_screen(self):
        '''
        First screen that shows up, you can type in a username and a password and either log in or signup if you dont
        have and account yet
        :return:
        '''
        signup_screen = tkinter.Frame(self.root)
        signup_screen.pack()
        top = tkinter.Frame(signup_screen)
        top.pack(side=tkinter.TOP)
        bottom = tkinter.Frame(signup_screen)
        bottom.pack(side=tkinter.BOTTOM)

        def next_screen(username, money):
            signup_screen.pack_forget()
            signup_screen.destroy()
            self.main_menu(username, money)

        def login_button():
            username = username_entry.get()
            password = password_entry.get()

            user = database.get_user(username)

            if password == user[0][1]:
                next_screen(username, user[0][2])

        def signup_button():
            username = username_entry.get()
            password = password_entry.get()

            database.add_user(username, password)

            next_screen(username, 0)

        username_label = tkinter.Label(top, text='Username:')
        username_label.grid(row=0, column=0)

        username_entry = tkinter.Entry(top)
        username_entry.insert(0, '')
        username_entry.grid(row=0, column=1)

        password_label = tkinter.Label(top, text='Password:')
        password_label.grid(row=1, column=0)

        password_entry = tkinter.Entry(top, show='*')
        password_entry.insert(0, '')
        password_entry.grid(row=1, column=1)

        login = tkinter.Button(bottom, text='Login', command=login_button)
        login.pack()

        signup = tkinter.Button(bottom, text='Sign Up', command=signup_button)
        signup.pack()

        exit = tkinter.Button(bottom, text='Exit', command=self.root.destroy)
        exit.pack()

    def main_game(self):
        self.login_screen()
        tkinter.mainloop()


if __name__ == "__main__":
    database.start()
    game = Game()
    game.main_game()
