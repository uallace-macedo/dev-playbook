-- migrate:up
CREATE TABLE IF NOT EXISTS posts (
  id int auto_increment PRIMARY KEY,
  user_id int NOT NULL,
  title varchar(255) NOT NULL,
  content LONGTEXT NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  deleted_at timestamp NULL,

  CONSTRAINT fk_user_id_posts FOREIGN KEY (user_id) REFERENCES users(id)
)

-- migrate:down
DROP TABLE IF EXISTS posts