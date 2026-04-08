-- migrate:up
CREATE TABLE IF NOT EXISTS refresh_tokens (
  id int auto_increment PRIMARY KEY,
  user_id int NOT NULL,
  refresh_token text NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_user_id_refresh_tokens FOREIGN KEY (user_id) REFERENCES users(id)
)

-- migrate:down
DROP TABLE IF EXISTS refresh_tokens