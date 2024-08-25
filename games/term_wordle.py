import random
import string
import os

def get_word():
    cwd = os.getcwd()
    wordle_list = open(cwd+'/games/wordle_words.txt').read().split('\n')
    common_list = open(cwd+'/games/common_words.txt').read().split('\n')

    word = random.choice(common_list)
    
    return word.upper(), wordle_list, common_list

def color_letter(letter, color):
    colors = {
        'green': '\033[42;30m',
        'yellow': '\033[43;30m'
    }
    reset = '\033[0m'
    return f"{colors[color]}{letter}{reset}"

def start_game():
    
    print("\nTERMINAL WORDLE\nType 'exit' to exit game\n")
    
    all_hints = []
    hinted = []
    correct = []
    guesses = 0
    available = list(string.ascii_uppercase)
    
    word, wordle_list, common_list = get_word()
    
    while True:

        yes = 0
        flag = 0
        uflag = 0
        
        available_letters = []

        for av in available:
            if av in correct:
                av = color_letter(av, 'green')
            elif av in hinted:
                av = color_letter(av, 'yellow')
        
            available_letters.append(av)
            
        print(' '.join(a for a in available_letters[:10]))
        print(' '.join(a for a in available_letters[10:20]))
        print(' '.join(a for a in available_letters[20:]))
        
        print()
        
        hints = ['']*5
        guess = input()
        
        if guess.lower() == 'exit':
            return
        
        if guess.lower() not in wordle_list:
            print("invalid guess\n")
            continue
            
        guess = guess.upper()
        
        for g in guess:
            if g not in available:
                print(f"'{g}' is not available")
                uflag = 1
                
        if uflag == 1:
            print()
            continue
        
        wordli = list(word)
        
        for i in range(len(guess)):
            
            if guess[i] in wordli:
                if guess[i] == word[i]:
                    hints[i] = "\U0001F7E9"
                    correct.append(guess[i])
                    yes+=1
                else:   
                    hints[i] = "\U0001F7E8"
                    hinted.append(guess[i])
                
                wordli.remove(guess[i])
                    
            else:
                hints[i] = "  "
                if guess[i] not in word:
                    try:
                        available.remove(guess[i])
                    except:
                        continue
        
        if flag == 0:
            print("------------------")
            all_hints.append(f"{guess} |{''.join(h for h in hints)}")
            for ah in all_hints:
                print(ah)
            print()
            
        if flag == 0:
            guesses += 1
        
        if yes == 5:
            print(f"CONGRATS! YOU FOUND THE WORD IN {guesses} TRIES!")
            break
        
        if guesses == 6:
            print(f"\nANSWER: {word}")
            break