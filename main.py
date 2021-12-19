from time import perf_counter
from functools import wraps
import string
from itertools import product


def time_func(function):    # wrapper function to time other functions
    @wraps(function)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = function(*args, **kwargs)
        print(f"It took: {perf_counter() - start} seconds")
        return result
    return wrapper


def user_password():    # returns the password the user want to use
    pw = input("Enter a password: ")
    return pw
    # TODO only accept some characters (a-z), (1-9) etc, max characters


@time_func
def bruteforce_password(pw_max_nchar, pw):
    legal_chars = string.ascii_lowercase + string.ascii_uppercase + string.digits   # stores all the legal characters, in this case (a-z), (A-Z), (1-9)
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


if __name__ == '__main__':
    password = None
    nmb_of_char = 10
    while True:     # main-loop
        while True: # pick-an-option-loop
            try:
                choice = int(input("Please pick an option:\n1. Try your password against a password-list\n"
                                   "2. Try to bruteforce your password\n"
                                   "3. Set password\n"
                                   "4. Set character bruteforce limit\nAnswer: "))
                break
            except:
                print("Invalid option")

        if password is None and choice != 3:    # works but bit weird way to do it
            password = user_password()
            print("not none")

        if choice == 1:
            compare_pwlist(password, "password_lists/100k_common.txt")
        elif choice == 2:
            bruteforce_password(nmb_of_char, password)
        elif choice == 3:
            print(f"Current password is: {password}")
            password = user_password()
        elif choice == 4:
            while True:     # valid-input-loop
                try:
                    print(f"Current limit is: {nmb_of_char}")
                    nmb_of_char = int(input("Up to how many characters do you want to bruteforce? "))   # Maybe unnecessary?
                    break
                except:
                    print("Invalid input")

"""
    TODO
    add keylistener to cancel for example the bruteforce
    add ability to use different wordlists
    add recommended password
    add range to bruteforce (like 3-6 characters)
    add save password and range (like set one time)
    add save output to txt-file    
    add error handling
    maybe add function that take question string as parameter to move the loops from main into functions? makes main look more clean
    add gui(maybe)
"""