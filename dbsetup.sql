-- The order of the data matters for parsing, do not re-oder elements! adding after is fine, however.
CREATE TABLE IF NOT EXISTS users(
    username VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    uuid VARCHAR(50) NOT NULL,
    discordid VARCHAR(50) NOT NULL,
    PRIMARY KEY (username)
);