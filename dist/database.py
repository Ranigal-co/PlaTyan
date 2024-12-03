import sqlite3

class Database:
    def __init__(self, db_name='database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS playlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT,
                playlist_id INTEGER,
                FOREIGN KEY (playlist_id) REFERENCES playlists(id)
            )
        ''')
        self.cursor.execute('''INSERT OR IGNORE INTO playlists (name) VALUES ('Все')''')
        self.conn.commit()

    def add_playlist(self, name):
        try:
            self.cursor.execute('INSERT INTO playlists (name) VALUES (?)', (name,))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_playlist(self, name):
        if name == "Все":
            self.cursor.execute("DELETE FROM songs")
            self.conn.commit()
            print("удалены все песни")
        else:
            self.cursor.execute('DELETE FROM songs WHERE playlist_id = (SELECT id FROM playlists WHERE name = ?)', (name,))
            self.conn.commit()
            self.cursor.execute('DELETE FROM playlists WHERE name = ?', (name,))
            self.conn.commit()
            print(f"удалены песни из плейлиста {name}")

    def get_playlists(self):
        self.cursor.execute('SELECT name FROM playlists')
        return [row[0] for row in self.cursor.fetchall()]

    def add_song_to_playlist(self, song_path, playlist_name):
        playlist_id = self.cursor.execute('SELECT id FROM playlists WHERE name = ?', (playlist_name,)).fetchone()
        id_vse = self.cursor.execute('SELECT id FROM playlists WHERE name = "Все"').fetchone()
        if playlist_id:
             if playlist_name == "Все":
                 self.cursor.execute('INSERT INTO songs (path, playlist_id) VALUES (?, ?)',
                                     (song_path, id_vse[0]))
                 self.conn.commit()
                 print("ok add 1 song to все")
                 return True
             else:
                 self.cursor.execute('INSERT INTO songs (path, playlist_id) VALUES (?, ?)',
                                     (song_path, playlist_id[0]))
                 self.cursor.execute('INSERT INTO songs (path, playlist_id) VALUES (?, ?)',
                                     (song_path, id_vse[0]))
                 self.conn.commit()
                 print(f"ok add 2 song to {playlist_name} and vse")
                 return True
        return False

    def delete_song_from_playlist(self, song_path, playlist_name):
        playlist_id = self.cursor.execute('SELECT id FROM playlists WHERE name = ?', (playlist_name,))
        if playlist_id:
            if playlist_name == "Все":
                self.cursor.execute('DELETE FROM songs WHERE path = ?', (song_path,))
                self.conn.commit()
                print("удалена песня из всех плейлистов")
            else:
                self.cursor.execute(
                    'DELETE FROM songs WHERE path = ? AND playlist_id = (SELECT id FROM playlists WHERE name = ?)',
                    (song_path, playlist_name))
                self.conn.commit()
                print(f"удалена песня {song_path} из плейлиста {playlist_name}")

    def get_songs_from_playlist(self, playlist_name):
        self.cursor.execute('''
            SELECT songs.path FROM songs
            JOIN playlists ON songs.playlist_id = playlists.id
            WHERE playlists.name = ?
        ''', (playlist_name,))
        return [row[0] for row in self.cursor.fetchall()]

    def get_playlists_from_song(self, song_name):
        self.cursor.execute('''
            SELECT playlists.name FROM playlists
            JOIN songs ON playlists.id = songs.playlist_id
            WHERE songs.name = ?''', (song_name,))

    def close(self):
        self.conn.close()