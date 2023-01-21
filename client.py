import sys
import logging
import rds_config
import pymysql

# rds settings

rds_host = "among-us-stats.coj0kcdco6tl.us-west-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

cur = conn.cursor()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")
print("SUCCESS: Connection to RDS MySQL instance succeeded\n")

# SELECT column_name(s)
# FROM table_name
# WHERE condition;

# INSERT INTO table_name (column1, column2, column3, ...)
# VALUES (value1, value2, value3, ...);

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;

# DELETE FROM table_name
# WHERE condition;


def select(columns, table_name, condition):
    cur.execute(f"SELECT {columns} FROM {table_name} WHERE {condition}")
    return cur.fetchall()


def insert(table_name, columns, values):
    cur.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
    conn.commit()
    print(f"Added {cur.rowcount} items from RDS MySQL table")


def update(table_name, columns_values, condition):
    cur.execute(
        f"UPDATE {table_name} SET {columns_values} WHERE {condition}")
    conn.commit()
    print(f"Updated {cur.rowcount} items from RDS MySQL table")


def delete(table_name, condition):
    cur.execute(f"DELETE FROM {table_name} WHERE {condition}")
    conn.commit()
    print(f"Deleted {cur.rowcount} items from RDS MySQL table")


def list_tables():
    cur.execute("SHOW TABLES")
    print("Tables in Among Us Stats:")
    for table in cur:
        print(table)


def list_columns(table_name):
    cur.execute(f"SHOW COLUMNS FROM {table_name}")
    print(f"Columns in {table_name}:")
    print("Column Name, Data Type, Null, Key, Default, Extra")
    for column in cur:
        print(column)


def main():
    continue_menu = True
    while continue_menu:
        # Main Menu
        print("_____________________________________________________________________________________")
        menu_input = input(
            "Main Menu: \n1. Query\n2. Insert\n3. Update\n4. Delete\n5. List Tables\n6. List Columns\n7. Exit\nSelect an option: ")

        if menu_input == "1":
            # Select
            query_input = input(
                "Would you like to query\nA. Match Summary\nB. Player\nC. Role").lower()

            if query_input == "a":
                # Match Summary
                match_summary_input = input(
                    "Would you like to query the match summary\nA. By Match ID\nB. By Date\nC. By Alias").lower()

                if match_summary_input == "a":
                    # Match ID
                    match_id_input = input("Enter match ID: ")
                    match_summary = select(
                        "*", "match_summary", f"match_id = {match_id_input}")
                    print(match_summary)

                elif match_summary_input == "b":
                    # Date
                    date_input = input("Enter date (YYYY-MM-DD): ")
                    match_summary = select(
                        "*", "match_summary", f"date_played = '{date_input}'")
                    print(match_summary)

                elif match_summary_input == "c":
                    # Alias
                    alias_input = input("Enter alias: ")
                    match_summary = select(
                        "*", "match_summary", f"match_alias LIKE '%{alias_input}%'")
                    print(match_summary)

                else:
                    print("\nInvalid input\n")

            elif query_input == "b":
                # Player
                player_input = input(
                    "Would you like to query the players\nA. By Player ID\nB. By Player Name\nC. By Player Alias").lower()

                if player_input == "a":
                    # Player ID
                    player_id_input = input("Enter player ID: ")
                    player = select(
                        "*", "player", f"player_id = {player_id_input}")
                    print(player)

                elif player_input == "b":
                    # Player Name
                    player_name_input = input("Enter player name: ")
                    player = select(
                        "*", "player", f"player_name LIKE '%{player_name_input}%'")
                    print(player)

                elif player_input == "c":
                    # Player Alias
                    player_alias_input = input("Enter player alias: ")
                    player = select(
                        "*", "player", f"player_alias LIKE '%{player_alias_input}%'")
                    print(player)

                else:
                    print("\nInvalid input\n")

            elif query_input == "c":
                # Role
                role_input = input(
                    "Would you like to query the roles\nA. By Role Name\nB. By Role Type").lower()

                if role_input == "a":
                    # Role Name
                    role_name_input = input("Enter role name: ")
                    role = select("*", "role_summary",
                                  f"role_name LIKE '%{role_name_input}%'")
                    print(role)

                elif role_input == "b":
                    # Role Type
                    role_type_input = input("Enter role type: ")
                    role = select("*", "role_summary",
                                  f"role_type_name LIKE '%{role_type_input}%'")
                    print(role)

                else:
                    print("\nInvalid input\n")

            else:
                print("\nInvalid input\n")

        elif menu_input == "2":
            # Insert
            print(
                "From this menu, you can only insert into the match table and the match_results table.")
            insert_input = input(
                "Would you like to insert into the\nA. match table\nB. match_results table?").lower()

            if insert_input == "a":
                # Match
                print()
                match_alias_input = input("Enter match alias: ")
                date_played_input = input("Enter date played (YYYY-MM-DD): ")
                print("\nGame versions:")
                game_versions = select(
                    "*", "game_version", "game_version_id > 0")
                print("game_version_id, version_name, version_number")
                print(game_versions)
                print()
                game_version_input = input("Enter game version ID: ")
                insert("among_us_stats.match", "match_alias, date_played, game_version_id",
                       f"'{match_alias_input}', '{date_played_input}', {game_version_input}")
                print()

            elif insert_input == "b":
                # Match Results
                num_players_input = input("Enter number of players: ")

                for i in range(int(num_players_input)):
                    print()
                    print("Matches:")
                    matches = select(
                        "*", "among_us_stats.match", "match_id > 0")
                    print("match_id, match_alias, date_played, game_version_id")
                    print(matches)
                    print()
                    match_id_input = input("Enter match ID: ")
                    print("\nPlayers:")
                    players = select(
                        "player_id, player_name, player_alias", "player", "player_id > 0")
                    print("player_id, player_name, player_alias")
                    print(players)
                    print()
                    player_id_input = input("Enter player ID: ")
                    print("\nRoles:")
                    roles = select("*", "role_summary", "role_id > 0")
                    print(
                        "role_id, role_name, team_id, team_name, role_type_id, role_type_name")
                    print(roles)
                    print()
                    role_id_input = input("Enter role ID: ")
                    print("\nModifiers:")
                    modifiers = select(
                        "*", "modifier", "modifier_id > 0 ORDER BY modifier_name")
                    print("modifier_id, modifier_name")
                    print(modifiers)
                    print()
                    modifier_id_input = input("Enter modifier ID: ")
                    print("\nDeath Types:")
                    death_types = select("*", "death", "death_id > 0")
                    print("death_id, death_type")
                    print(death_types)
                    print()
                    death_id_input = input("Enter death ID: ")
                    print("\nPotential Killers:")
                    potential_killers = select(
                        "player_id, player_name", "player", "player_id > 0")
                    print("player_id, player_name")
                    print(potential_killers)
                    print()
                    killed_by_input = input(
                        "Enter the player ID of the killer or NULL if there was no killer: ")
                    print("\nDid the player win?")
                    did_win_input = input("Enter 1 for yes or 0 for no: ")
                    insert("among_us_stats.match_results", "match_id, player_id, role_id, modifier_id, death_id, killed_by, did_win",
                           f"{match_id_input}, {player_id_input}, {role_id_input}, {modifier_id_input}, {death_id_input}, '{killed_by_input}', {did_win_input}")
                    print()

            else:
                print("\nInvalid input\n")

        elif menu_input == "3":
            # Update
            print("\nUpdate Menu\n")
            update_table = input(
                "Please enter the table you would like to update: ")
            update_columns = input(
                "Please enter each column, value pair you would like to update separated by commas (column1 = value1, column2 = value2, ...): ")
            update_condition = input(
                "Please enter the condition for the update: ")
            update(update_table, update_columns, update_condition)
            print()

        elif menu_input == "4":
            # Delete
            delete_table = input(
                "\nPlease enter the table you would like to delete from: ")
            delete_condition = input(
                "\nPlease enter the condition for the delete: ")
            delete(delete_table, delete_condition)
            print()

        elif menu_input == "5":
            # List Tables
            print()
            list_tables()
            print()

        elif menu_input == "6":
            # List Columns
            print()
            table_to_list = input(
                "Enter the name of the table you would like to list the columns of: ")
            print()
            list_columns(table_to_list)
            print()

        else:
            # Exit
            print("\nExiting...\n")
            continue_menu = False


if __name__ == "__main__":
    main()
