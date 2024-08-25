import random
import string
import os

def load_dictionary(file_path):
    
    with open(file_path, 'r') as fp:
        wd = fp.read().split('\n')
        
    big_words = [w for w in wd if len(set(list(w))) == 7]
    return wd, big_words

def generate_spelling_bee_letters(dictionary, big_words, min_words=5, max_attempts=1000):

    for ma in range(max_attempts):
        all_letters = set(list(random.choice(big_words)))

        center_letter = random.choice(list(all_letters))
        other_letters = list(all_letters - {center_letter})

        valid_words = [word for word in dictionary if 
                       len(word) >= 4 and
                       center_letter in word and
                       all(letter in all_letters for letter in word)]
        
        if len(valid_words) >= min_words:
            return center_letter, other_letters, len(valid_words), valid_words, ma+1

    return None, None, 0, None, 0
    
def color_word(word, color):
    colors = {
        'yellow': '\033[43;30m'
    }
    reset = '\033[0m'
    return f"{colors[color]}{word}{reset}"
    
def start_game():
    cwd = os.getcwd()
    
    found = []
    foundct = 0
    
    print("\nTERMINAL SPELLING BEE\nType '--exit' to exit game")
    
    word_dict, big_words = load_dictionary(cwd+"/games/spbee_words.txt")
    center, others, num_words, word_list, att = generate_spelling_bee_letters(word_dict, big_words, min_words = 35)
    
    all_lets = []
    all_lets.append(center)
    all_lets.extend(others)
    
    center_disp = color_word(center, 'yellow')
    
    if center == None:
        print("\nERROR MAX TRIES REACHED\n")
        return
        
    curr_rank = 'BEGINNER'
        
    #print(f'Generation attempts: {att}\n')
    print('\n' + ' '.join(o for o in others[:3]) + f'\n  {center_disp}  \n' + ' '.join(o for o in others[3:]) + '\n')
    print(f'FOUND: 0/{num_words} WORDS\nCURRENT RANK: {curr_rank}\n')
    
    while True:
        user_input = input()
        
        if user_input.lower() == '--exit':
            print(f"\nRANK REACHED: {curr_rank}\n")
            return
        
        user_input = user_input.upper().strip()
        
        if user_input in found:
            print(f"\n{user_input} has been found\n")
            continue
        
        if user_input not in word_list:
            print('\ninvalid guess\n')
            continue
        else:
            word_list.remove(user_input)
            found.append(user_input)
            foundct += 1
            
        if set(user_input) == set(all_lets):
            print(f"\n{color_word('PANAGRAM!', 'yellow')}\n")
        
        score = foundct/num_words
        
        if 0 <= score < 0.1:
            curr_rank = 'BEGINNER'
        elif 0.1 <= score < 0.2:
            curr_rank = 'GOOD START'
        elif 0.2 <= score < 0.3:
            curr_rank = 'MOVING UP'
        elif 0.3 <= score < 0.4:
            curr_rank = 'GOOD'
        elif 0.4 <= score < 0.5:
            curr_rank = 'SOLID'
        elif 0.5 <= score < 0.6:
            curr_rank = 'NICE'
        elif 0.6 <= score < 0.7:
            curr_rank = 'GREAT'
        elif 0.7 <= score < 0.85:
            curr_rank = 'AMAZING'
        elif 0.85 <= score < 1:
            curr_rank = 'GENIUS'
        elif score == 1.0:
            curr_rank = 'QUEEN BEE'
        
        print('\n' + ' '.join(o for o in others[:3]) + f'\n  {center_disp}  \n' + ' '.join(o for o in others[3:]) + '\n')
        print(f'FOUND: {foundct}/{num_words} WORDS\nCURRENT RANK: {curr_rank}\n')
        
        if foundct == num_words:
            print("\nCONGRATS!\n")
            return
