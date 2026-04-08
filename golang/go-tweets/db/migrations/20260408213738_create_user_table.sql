-- migrate:up
CREATE TABLE IF NOT EXISTS users (
  id int auto_increment PRIMARY KEY,
  email varchar(255) NOT NULL UNIQUE,
  username varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
)

-- migrate:down
DROP TABLE IF EXISTS users