import psycopg2

valid_choices = ["0", "1", "2", "3", "4", "5"]

def menu():
    print("\nWelcome to the MMORPG database! Please select your request from the options below, or 0 to quit.\n")
    print("[1] Register a new user")
    print("[2] Create a new character")
    print("[3] Level up a character")
    print("[4] Change a character's spawn location")
    print("[5] View complete data on all of a player's characters")

    choice = input("\nEnter selection here: ")
    while choice not in valid_choices:
        choice = input("Invalid request. Please input a number between 1 and 5 or 0 to exit: ")
    
    return int(choice)

def continue_loop():
    choice = input("Would you like to continue? (Y/N) ")
    while choice != "Y" and choice != "N" and choice != "y" and choice != "n":
        choice = input("Please enter Y for yes or N for no. Would you like to continue? ")
    if choice == "N" or choice == "n":
        return True
    else:
        return False

conn = psycopg2.connect(host="localhost", port=5432, dbname="MMORPG_small", user="smeppu")
cur = conn.cursor()

done = False

while done == False:
    choice = menu()

    if choice == 1:
        #retrieve IDs, to help in the selection of a new one
        query = "select max(player_ID) from player;"
        try:
            cur.execute(query)
            conn.commit()
            for ID in cur:
                last = int(ID[0])
            new_ID = str(last + 1)
            new_ID = new_ID.zfill(8)
            print()
        except psycopg2.Error as e:
            print("An error has occurred. Please try again.")
            print(e)
            conn.rollback()
        
        username = input("Please enter a username at least 1 and no more than 20 characters long: ")
        while len(username) < 1 or len(username) > 20:
            username = input("Your username must be between 1 and 20 characters long. Try again: ")

        query = "insert into player values(%s, %s)"

        try:
            cur.execute(query, (new_ID, username))
            conn.commit()
            print("\nSuccess! Welcome, " + username + "! Your player ID is " + new_ID + ".\n")  
        except psycopg2.Error as e:
            print("An error has occured. Please try again.")
            print(e)
            conn.rollback()

        done = continue_loop()

    elif choice == 2:
        breakCase = False 
        charCreationCase = False
        overwrite = False
        num_char = 1
        player_ID = ''
        cur_list = []
        while breakCase is False:
            try:
                player_name = input("What is your username? ")
                query = "SELECT player_ID, username FROM player WHERE username = %s"
                cur.execute(query, (player_name,))
                conn.commit()
                cur_list = cur.fetchone()
                if not cur_list:
                    conn.rollback()
                    continue
                player_ID = cur_list[0]
                char_query = "SELECT * FROM __character where __character.player_ID = %s"
                cur.execute(char_query, (player_ID,))
                conn.commit()
                cur_list = cur.fetchall()
                if cur_list:
                    if len(cur_list) == 4:
                        answer = input("Would you like to overwrite a character? (Y/N) ")
                        if answer == 'Y' or answer == 'y':
                            query = "SELECT * FROM __character WHERE player_ID = %s"
                            cur.execute(query, (player_ID,))
                            conn.commit()
                            cur_list = cur.fetchall()
                            num_char = 1
                            print("[#]    |num_char     |Player ID     |Name                  |Level  |Race          |Class            |Region                |")
                            print("-------+-------------+--------------+----------------------+-------+--------------+-----------------+----------------------+")
                            for row in cur_list:
                                print("{:<6}".format(num_char), "|", "{:<11}".format(row[0]), "|", "{:<12}".format(row[1]), "|", 
                                "{:<20}".format(row[2]), "|", "{:<5}".format(row[3]), "|", "{:<12}".format(row[4]), "|", 
                                "{:<15}".format(row[5]), "|", "{:<20}".format(row[6]), "|")
                                num_char+=1
                            num_char = int(input("Which number character would you like to overwrite? "))
                            overwrite = True
                        elif answer == 'N' or answer == 'n':
                            charCreationCase = True
                            breakCase = True
                    else:
                        num_char = len(cur_list)+1
                breakCase = True
            except psycopg2.Error as e:
                print(e)
                conn.rollback()
        
        while charCreationCase is False:
            try:
                cur.execute("SELECT race_name, ability_name FROM race")
                conn.commit()
                cur_list = cur.fetchall()
                if not cur_list:
                    print("No race? NOOOOOO")
                    conn.rollback()
                    charCreationCase = True
                
                print("Race         |Ability             ")
                print("-------------+-------------------+")
                for row in cur_list:
                    print("{:<12}".format(row[0]), "|", "{:<20}".format(row[1]))
                
                race = input("Which race would you like your character to have? ")
                cur.execute("SELECT * FROM class")
                conn.commit()
                cur_list = cur.fetchall()
                if not cur_list:
                    print("No class? How could that be???!")
                    conn.rollback()
                    charCreationCase = True
                print("Class           |Ability            ")
                print("----------------+------------------+")
                for row in cur_list:
                    print("{:<15}".format(row[0]), "|", "{:<20}".format(row[1]))

                __class = input("Which class would you like your character to have? ")
                name = input("What should your character be named? ")
                if overwrite:
                    statement = """
                    UPDATE __character SET name = %s, __level = 1, race_name = %s, class_name = %s, region_name = 'Kayimess City'
                    WHERE num_char = %s AND player_ID = %s"""
                    cur.execute(statement,(name, race, __class, num_char, player_ID))    
                else:
                    statement = "INSERT INTO __character VALUES (%s, %s, %s, 1, %s, %s, 'Kayimess City')"
                    cur.execute(statement,(num_char, player_ID, name, race, __class))
                print("New character successfully created!")
                charCreationCase = True
            except psycopg2.Error as e:
                print(e)
                conn.rollback()
        done = continue_loop()

    elif choice == 3:
        player_ID = input("Please enter your eight-digit player ID: ")
        query = "select * from player where player_ID = %s;"
        
        cur.execute(query, (player_ID,))
        conn.commit()
        results = cur.fetchall()
        if len(results) == 0:
            print("This player ID does not exist. Please try again with a valid ID.")
        else:
            query = "select num_char, name, __level from __character where player_ID = %s order by num_char;"
            cur.execute(query, (player_ID,))
            conn.commit()
            results = cur.fetchall()
            if len(results) == 0:
                print("You don't seem to have any characters yet.")
            else:
                print("You have the following characters:\n")
                char_nums = []
                for row in results:
                    print("[" + str(row[0]) + "]", row[1] + ", level", row[2])
                    char_nums.append(str(row[0]))
                num = input("\nPlease input the number of the character you would like to level up: ")
                while num not in char_nums:
                    num = input("Invalid input. Try again: ")
                level = 1
                for row in results:
                    if row[0] == int(num):
                        level = row[2]
                level = level + 1

                query = "update __character set __level = %s where player_ID = %s and num_char = %s;"
                try:
                    cur.execute(query, (level, player_ID, int(num)))
                    conn.commit()

                    print("Success! Your character is now level " + str(level) + ".")
                except psycopg2.Error as e:
                    print(e)
                    conn.rollback()

        done = continue_loop()

    elif choice == 4:
        breakCase = False
        char_match = []
        while breakCase is False:
            try:
                char_name = input("What is your character's name?\n")
                query = "SELECT * FROM __character WHERE __character.name = %s"
                cur.execute(query,(char_name,))
                conn.commit()
                cur_list = cur.fetchall()
                if not cur_list:
                    conn.rollback()
                    continue                
                num_char = 1
                print("[#]   |Name                  |Level  |Race          |Class            |Region                |")   
                print("------+----------------------+-------+--------------+-----------------+----------------------+")      
                for row in cur_list:
                    print("{:<5}".format(row[0]), "|", "{:<20}".format(row[2]), "|", "{:<5}".format(row[3]), "|", "{:<12}".format(row[4]), "|", 
                    "{:<15}".format(row[5]), "|", "{:<20}".format(row[6]), "|")  
                    num_char+=1
                char_match_info = input("Which [#] is your character?\n")
                char_match = cur_list[int(char_match_info)-1]
                breakCase = True
            except psycopg2.Error as e:
                print("An error occurred, please try again.")
                print(e)
                conn.rollback()
        breakCase = False

        while breakCase is False: 
            try:
                print("\nWhere would you like to move your character?")
                cur.execute("SELECT region_name FROM region")
                conn.commit()
                print("Regions:\n")
                for row in cur:
                    print(row[0]+'\n')
                new_region = input("Please enter valid region: ")
                update_statement = """
                UPDATE __character SET region_name = %s WHERE num_char = %s AND player_ID = %s AND name = %s AND __level = %s
                AND race_name = %s AND class_name = %s AND region_name = %s"""
                cur.execute(update_statement, (new_region, char_match[0], char_match[1], char_match[2], char_match[3], char_match[4], 
                char_match[5], char_match[6]))
                conn.commit()
                print("Character location successfully changed to: " + new_region + '!') 
                breakCase = True
            except psycopg2.Error as e:
                print("Please input valid region")
                print(e)
                conn.rollback()
                
        done = continue_loop()

    elif choice == 5:
        breakCase = False
        while breakCase is False:
            try:
                name = input("What is your name? ")
                query = "SELECT player_ID FROM player where username = %s"
                cur.execute(query, (name,))
                conn.commit()
                cur_list = cur.fetchall()
                if not cur_list:
                    print("Name not found, try again.")
                    continue
                char_query = "SELECT * FROM __character WHERE __character.player_ID = %s"
                cur.execute(char_query,(cur_list[0][0],))
                conn.commit()
                print("[#]   |Name                  |Level  |Race          |Class            |Region                |")
                print("------+----------------------+-------+--------------+-----------------+----------------------+")      
                for row in cur:
                    print("{:<5}".format(row[0]), "|", "{:<20}".format(row[2]), "|", "{:<5}".format(row[3]), "|", "{:<12}".format(row[4]), "|", 
                    "{:<15}".format(row[5]), "|", "{:<20}".format(row[6]), "|") 
                breakCase = True
            except psycopg2.Error as e:
                print(e)
                conn.rollback()
        done = continue_loop()

    else:
        done = True

conn.close()
