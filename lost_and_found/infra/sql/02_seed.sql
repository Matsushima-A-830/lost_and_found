-- 管理者ユーザーとサンプルアイテムを挿入（冪等）
INSERT INTO users (id, username, password_hash, role)
VALUES (1, 'admin', '$2b$12$dummyhash', 'admin')
ON CONFLICT (id) DO NOTHING;

INSERT INTO items (id, management_number, found_datetime, found_place, category_l, status)
VALUES (1, 'MNG-0001', NOW(), '駅前', '財布', '保管中')
ON CONFLICT (id) DO NOTHING;
