import json
import random
import os

def load_tiles():
    cwd = os.getcwd()
    
    with open(cwd+'/data/connections.txt') as ct:
        challenge = random.choice(ct.read().split('\n'))

    challenge_dict = json.loads(challenge)

    tiles = challenge_dict["words"]
    answer_groups = challenge_dict["solution"]["groups"]

    random.shuffle(tiles)
    
    return tiles, answer_groups

def color_word(word, color):
    colors = {
        0: '\033[43;30m',
        1: '\033[42;30m',
        2: '\033[104;30m',
        3: '\033[105;30m'
    }
    reset = '\033[0m'
    return f"{colors[color]}{word}{reset}"

def construct_grid(tiles, biggest):

    grid = []
    row = []

    n=0
    for t in tiles:
        if n+1 < 10:
            r = f"[{n+1}] {t}" + " "*(len(biggest) - len(t))
        else:
            r = f"[{n+1}] {t}" + " "*(len(biggest) - len(t) - 1)
        row.append(r)
        n+=1
        if n%4 == 0:
            grid.append(row)
            row = []
            
    return grid

def start_game():
    tiles, answer_groups = load_tiles()
    biggest = max(tiles, key = len)
    grid = construct_grid(tiles, biggest)

    groups = []
    group = []

    tries = 4

    print("\nTERMINAL CONNECTIONS\nType 'exit' to exit game\n")

    print("\nFOUND:")
    print('\n'.join(' '.join(w for w in g) for g in groups))
    print("\nTILES:")
    print('\n'.join(' '.join(r for r in row) for row in grid))
    print("\n[" + "X"*(4-tries) + "-"*tries + "]")

    while True:

        found = 0
        
        print()
        sequence = input()
        
        if sequence.lower() == 'exit':
            print(f"\nGROUPS FOUND: {len(groups)}\n")
            return
        
        try:
            sequence = [int(s) for s in sequence.split(',')]
        except:
            print("\nSequence must be 4 numbers separated by ','")
            continue
            
        if len(sequence) != 4:
            print("\nSequence must be 4 numbers separated by ','")
            continue
        
        seflag = 0
        for se in sequence:
            if se > len(tiles):
                print("\ninvalid choice\n")
                seflag = 1
                break
                
        if seflag == 1:
            seflag = 0
            continue

        checklist = [tiles[k-1] for k in sequence]

        for ag in answer_groups:
            if sorted(checklist) == sorted(ag["words"]):
                ind = answer_groups.index(ag)
                print("\nCORRECT!")
                print("\n" + color_word("  ", ind) + ' ' + ag["reason"])
                for t in checklist:
                    tiles.remove(t)
                    t = color_word(t, ind)
                    group.append(t)
                groups.append(group)
                group=[]
                grid = construct_grid(tiles, biggest)
                found = 1
                break
        
        if found == 0:
            tries -= 1
            
        print("\nFOUND:")
        print('\n'.join(' '.join(w for w in g) for g in groups))
        print("\nTILES:")
        print('\n'.join(' '.join(r for r in row) for row in grid))
        print("\n[" + "X"*(4-tries) + "-"*tries + "]")
            
        if tries == 0:
            print("\nANSWERS:\n")
            for ag in answer_groups:
                ind = answer_groups.index(ag)
                for t in ag["words"]:
                    t = color_word(t, ind)
                    group.append(t)
                print(' '.join(w for w in group) + f' - {ag["reason"]}\n')
                group=[]
            return
        
        if tiles == []:
            print("\nCONGRATS!")
            return