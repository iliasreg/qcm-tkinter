.headers on
.mode column

DROP TABLE IF EXISTS qcm;
CREATE TABLE qcm (
  id INTEGER PRIMARY KEY,
  name VARCHAR(25),
  filepath VARCHAR(100)
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name VARCHAR(25),
  password VARCHAR(25)
);

DROP TABLE IF EXISTS game;
CREATE TABLE game (
  id_qcm INTEGER,
  id_user INTEGER,
  score INTEGER,
  FOREIGN KEY (id_qcm) REFERENCES  qcm(id),
  FOREIGN KEY (id_user) REFERENCES users(id),
  PRIMARY KEY(id_qcm,id_user)
);