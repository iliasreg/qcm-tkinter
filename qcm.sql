.headers on
.mode column

DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS qcms;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE qcms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    creator_id INTEGER,
    questions_json TEXT NOT NULL,
    FOREIGN KEY (creator_id) REFERENCES users (id)
);

CREATE TABLE scores (
    user_id INTEGER,
    qcm_id INTEGER,
    score INTEGER,
    PRIMARY KEY (user_id, qcm_id),
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (qcm_id) REFERENCES qcms (id)
);

INSERT INTO users (username, password) VALUES 
('admin', 'admin'),
('user1', 'password1'),
('user2', 'password2');

INSERT INTO qcms (title, creator_id, questions_json) VALUES 
('Math Quiz', 1, '[{"question": "What is 2+2?", "options": ["3", "4", "5", "6"], "correct": 1}, {"question": "What is the square root of 16?", "options": ["2", "4", "6", "8"], "correct": 1}]'),
('Science Quiz', 1, '[{"question": "What is H2O?", "options": ["Water", "Oxygen", "Hydrogen", "Helium"], "correct": 0}]');

INSERT INTO scores (user_id, qcm_id, score) VALUES
(2, 1, 2),
(3, 1, 1),
(2, 2, 1);