import sqlite3


def main():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()


if __name__ == '__main__':
    main()
