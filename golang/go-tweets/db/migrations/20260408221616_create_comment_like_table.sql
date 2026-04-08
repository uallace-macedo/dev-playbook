-- migrate:up
CREATE TABLE IF NOT EXISTS comments_likes (
  id int auto_increment PRIMARY KEY,
  user_id int NOT NULL,
  comment_id int NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_user_id_comments_likes FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_comment_id_comments_likes FOREIGN KEY (comment_id) REFERENCES comments(id)
)

-- migrate:down
DROP TABLE IF EXISTS comments_likes