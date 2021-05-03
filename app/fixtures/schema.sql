DROP TABLE IF EXISTS Games;
DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Moves;

CREATE TABLE Games (
  game_id INTEGER PRIMARY KEY AUTOINCREMENT,
  players VARCHAR NOT NULL,
  game_columns INTEGER NOT NULL,
  game_rows INTEGER NOT NULL,
  game_state TEXT NOT NULL,
  winner TEXT,
  FOREIGN KEY (winner) REFERENCES Players (player_name) 
);

CREATE TABLE Players (
  player_id INTEGER PRIMARY KEY AUTOINCREMENT,
  player_name TEXT UNIQUE NOT NULL
);

CREATE TABLE Moves (
  move_id INTEGER PRIMARY KEY AUTOINCREMENT,
  move_number INTEGER NOT NULL,
  move_column INTEGER NOT NULL,
  move_row INTEGER NOT NULL,
  game_id INTEGER NOT NULL,
  player_id TEXT NOT NULL,
  FOREIGN KEY (game_id) REFERENCES Games (game_id),
  FOREIGN KEY (player_id) REFERENCES Players (player_name) 
);