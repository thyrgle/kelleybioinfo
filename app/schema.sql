DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS history;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  points   INTEGER DEFAULT 0
);

CREATE TABLE history (
  id INTEGER,
  award INTEGER,
  time_stamp TEXT
);
