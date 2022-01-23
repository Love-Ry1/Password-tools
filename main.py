import re
from time import perf_counter
from functools import wraps
import string
from itertools import product
from os import listdir


def time_func(function):    # wrapper function to time other functions
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = function(*args, **kwargs)
        print(f"It took: {perf_counter() - start} seconds")
        return result
    return wrapper


def user_password():    # returns the password the user want to use
    while True:
        print("Allowed characters is: a-z, A-Z, 0-9")
        pw = input("Enter a password: ")
        if allowed_characters(pw):
            return pw


def allowed_characters(strg, search=re.compile(r'[^a-zA-Z0-9]').search):    # returns True if string only contains
    if strg == "":                                                          # a-z, A-Z, 0-9, else returns false
        return False
    return not bool(search(strg))


def choose_pwlist():
    pwlists = listdir("password_lists")
    for x in range(len(pwlists)):   # Is there a moore pythonic way to do this?
        print(f"{x+1}: {pwlists[x]}")

    while True:  # valid-input-loop
        try:
            number = int(input("Please enter the number of the password-list you want to use: "))
            if number <= len(pwlists):
                break
        except Exception:
            print("Invalid input")

    pwlist_name = pwlists[number - 1]
    return pwlist_name


@time_func
def bruteforce_password(pw_max_nchar, pw):
    legal_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits   # stores all the legal characters, in this case (a-z), (A-Z), (0-9)
    n_guesses = 0   # keeps count of number of guesses
    for count in range(1, pw_max_nchar + 1):    # tries every possible solution between 1 char and the pw max length
        new_product = product(legal_chars, repeat=count)    # uses cartesian products to get the possible solutions
        for x in new_product:
            n_guesses += 1
            guess = ''.join(x)
            if guess == pw:
                print(f"{guess} - OK \nThe correct password was: {guess}\nTt took {n_guesses} guesses ")
                return
            print(f"{guess} - NOT OK")


@time_func
def compare_pwlist(pw, pw_list_path):     # Compares the password with password list (needs path to pw-list)
    pw = pw.lower()     # Most pw-lists are only lower-case, therefore it makes more sense to convert the
    current_str = ""                # password to lowercase
    word_count = 0      # keeps count of what number the current word is
    with open(pw_list_path) as file:
        pw_list = file.read()

    for x in range(0, len(pw_list)):
        if pw_list[x] != '\n':
            current_str += pw_list[x]
        elif pw_list[x] == '\n':
            word_count += 1
            if pw == current_str:
                print(f"{current_str} OK \nThe correct password was: {current_str} \n"
                      f"It was place {word_count} in the password list")
                return
            elif pw != current_str:
                print(f"{current_str} NOT OK")
                current_str = ""

    print(f"Your password was not in the password list!")
    return


def int_question_loop(question):    # takes a question as a parameter (string) and returns user input as int
    if isinstance(question, str):
        while True:
            try:
                answer = int(input(question))
                return answer
            except Exception:
                print("Invalid input")
    else:
        print("question is not a string")
        return


if __name__ == '__main__':
    password = None
    nmb_of_char = 5
    pwlist_path = "password_lists/100k_common.txt"
    while True:     # main-loop
        choice = int_question_loop("Please pick an option:\n1. Try your password against a password-list\n"
                                   "2. Try to bruteforce your password\n"
                                   "3. Set password\n"
                                   "4. Set character bruteforce limit\n"
                                   "5. Set a password-list\nAnswer: ")

        if password is None and not (choice == 3 or choice == 5):    # doesn't feel good
            password = user_password()

        if choice == 1:
            compare_pwlist(password, pwlist_path)
        elif choice == 2:
            bruteforce_password(nmb_of_char, password)
        elif choice == 3:
            print(f"Current password is: {password}")
            password = user_password()
        elif choice == 4:
            print(f"Current limit is: {nmb_of_char}")
            nmb_of_char = int_question_loop("Up to how many characters do you want to bruteforce? ")
        elif choice == 5:
            current_pwlist = pwlist_path.split('/')
            print(f"Current password-list is: {current_pwlist[1]}")
            pwlist_path = "password_lists/" + choose_pwlist()

"""
    TODO
    add keylistener to cancel for example the bruteforce
    add recommended password
    add range to bruteforce (like 3-6 characters)
    add save output to txt-file
    add error handling
    add gui(maybe)
"""