import games.term_connections as tc
import games.term_wordle as tw
import games.term_spelling_bee as tsb

print("TERMINAL NYT GAMES\n")

while True:

    print("[1] WORDLE")
    print("[2] CONNECTIONS")
    print("[3] SPELLING BEE")
    print("[4] EXIT\n")
    
    choice = input("Enter choice: ")
    
    try:
        choice = int(choice)
    except:
        print("\ninvalid choice\n")
        continue
        
    if choice == 1:
        tw.start_game()
    elif choice == 2:
        tc.start_game()
    elif choice == 3:
        tsb.start_game()
    elif choice == 4:
        break
    else:
        print("\ninvalid choice\n")
        continue
        
    print("\nTERMINAL NYT GAMES\n")