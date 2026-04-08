-- migrate:up
CREATE TABLE IF NOT EXISTS posts_likes (
  id int auto_increment PRIMARY KEY,
  user_id int NOT NULL,
  post_id int NOT NULL,
  created_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,

  CONSTRAINT fk_user_id_posts_likes FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_post_id_posts_likes FOREIGN KEY (post_id) REFERENCES posts(id)
)

-- migrate:down
DROP TABLE IF EXISTS posts_likes