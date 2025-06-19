-- 初期スキーマ
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(64) UNIQUE NOT NULL,
  password_hash VARCHAR(128) NOT NULL,
  role VARCHAR(16) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  management_number VARCHAR(32) UNIQUE NOT NULL,
  found_datetime TIMESTAMP NOT NULL,
  found_place VARCHAR(128) NOT NULL,
  category_l VARCHAR(32) NOT NULL,
  category_m VARCHAR(32),
  category_s VARCHAR(32),
  color VARCHAR(32),
  features TEXT,
  status VARCHAR(32) NOT NULL,
  image_path VARCHAR(256),
  registered_by_user_id INTEGER REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_items_found_datetime ON items(found_datetime);
CREATE INDEX idx_items_status_category ON items(status, category_l);

-- 他テーブルも同様に定義
