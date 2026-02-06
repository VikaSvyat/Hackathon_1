import sqlite3
from datetime import datetime

# connect to the database
conn = sqlite3.connect('game_log.db')
cursor = conn.cursor()

# create sessions table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_name TEXT,
    money INTEGER,
    time_played INTEGER,
    date_played TEXT
)
''')
conn.commit()

# log a game session
def log_game(player_name, money, time_played):
    date_played = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO sessions (player_name, money, time_played, date_played)
        VALUES (?, ?, ?, ?)
    ''', (player_name, money, time_played, date_played))
    conn.commit()

# show leaderboard sorted by money
def show_leaderboard(top_n=50):
    cursor.execute('''
        SELECT player_name, money, time_played, date_played 
        FROM sessions
        ORDER BY money DESC
        LIMIT ?
    ''', (top_n,))
    rows = cursor.fetchall()

    print("\n🏆 LEADERBOARD 🏆")
    print(f"{'Rank':<5} {'Player':<10} {'Money':<6} {'Time':<10} {'Date'}")
    print("-" * 40)
    for i, row in enumerate(rows, start=1):
        player, money, time_played, date_played = row
        print(f"{i:<5} {player:<10} {money:<6} {time_played:<10} {date_played}")
    print("-" * 40)
