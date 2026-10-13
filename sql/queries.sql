-- PR7: именованные запросы сервиса поиска мастеров.
-- Параметры ? передаются из Python через sqlite3.execute(sql, values).

-- name: masters_list
-- Список мастеров: SELECT, сортировка по рейтингу.
SELECT id, name, specialty, experience, rating, price_per_hour
FROM masters ORDER BY rating DESC, name;

-- name: services_list
-- Список услуг: SELECT, сортировка по категории.
SELECT id, name, category, estimated_hours, master_id, price
FROM services ORDER BY category, name;

-- name: users_list
-- Список клиентов: SELECT.
SELECT id, name, role, phone FROM users ORDER BY name;

-- name: master_by_id
-- Поиск одного мастера: WHERE с параметром.
SELECT id, name, specialty, experience, rating, price_per_hour
FROM masters WHERE id = ?;

-- name: masters_min_rating
-- Поиск мастеров по минимальному рейтингу: WHERE.
SELECT id, name, specialty, experience, rating, price_per_hour
FROM masters WHERE rating >= ? ORDER BY rating DESC, name;

-- name: services_by_category
-- Фильтрация услуг по категории: WHERE.
SELECT id, name, category, estimated_hours, master_id, price
FROM services WHERE category = ? ORDER BY name;

-- name: service_categories
-- Категории для формы поиска.
SELECT DISTINCT category FROM services WHERE category <> '' ORDER BY category;

-- name: orders_on_date
-- Заказы на дату: WHERE с параметром.
SELECT id, master_id, user_id, service_id, booking_date, status
FROM orders WHERE booking_date = ? ORDER BY id;

-- name: orders_joined
-- Заказы с именами мастера, клиента и услуги: JOIN.
SELECT o.id, o.booking_date, o.status,
       m.id AS master_id, m.name AS master_name,
       m.specialty, m.experience, m.rating, m.price_per_hour,
       u.id AS user_id, u.name AS user_name, u.role, u.phone,
       s.id AS service_id, s.name AS service_name,
       s.category, s.estimated_hours, s.master_id AS service_master_id,
       s.price
FROM orders AS o
JOIN masters AS m ON m.id = o.master_id
JOIN users AS u ON u.id = o.user_id
JOIN services AS s ON s.id = o.service_id
ORDER BY o.booking_date DESC, o.id DESC;

-- name: order_by_id
-- Карточка заказа с тремя связанными объектами: JOIN и WHERE.
SELECT o.id, o.booking_date, o.status,
       m.id AS master_id, m.name AS master_name,
       m.specialty, m.experience, m.rating, m.price_per_hour,
       u.id AS user_id, u.name AS user_name, u.role, u.phone,
       s.id AS service_id, s.name AS service_name,
       s.category, s.estimated_hours, s.master_id AS service_master_id,
       s.price
FROM orders AS o
JOIN masters AS m ON m.id = o.master_id
JOIN users AS u ON u.id = o.user_id
JOIN services AS s ON s.id = o.service_id
WHERE o.id = ?;

-- name: master_orders
-- Заказы выбранного мастера с названием услуги: JOIN и WHERE.
SELECT o.id, o.booking_date, o.status, s.name AS service_name
FROM orders AS o JOIN services AS s ON s.id = o.service_id
WHERE o.master_id = ? ORDER BY o.booking_date DESC;

-- name: total_orders
-- Агрегат COUNT по активным заказам.
SELECT COUNT(*) AS total FROM orders WHERE status = 'Создан';

-- name: average_rating
-- Агрегат AVG по рейтингу мастеров.
SELECT ROUND(AVG(rating), 2) AS average_rating FROM masters;

-- name: orders_by_master
-- Статистика заказов по мастерам: JOIN, COUNT, GROUP BY.
SELECT m.id, m.name, COUNT(o.id) AS orders_count
FROM masters AS m
LEFT JOIN orders AS o ON o.master_id = m.id AND o.status = 'Создан'
GROUP BY m.id, m.name ORDER BY orders_count DESC, m.name;

-- name: orders_by_service
-- Статистика заказов по услугам: JOIN, COUNT, GROUP BY.
SELECT s.id, s.name, COUNT(o.id) AS orders_count
FROM services AS s
LEFT JOIN orders AS o ON o.service_id = s.id AND o.status = 'Создан'
GROUP BY s.id, s.name ORDER BY orders_count DESC, s.name;

-- name: popular_masters
-- Группы с минимумом активных заказов: GROUP BY и HAVING.
SELECT m.id, m.name, COUNT(o.id) AS orders_count
FROM masters AS m JOIN orders AS o ON o.master_id = m.id
WHERE o.status = 'Создан'
GROUP BY m.id, m.name HAVING COUNT(o.id) >= ?
ORDER BY orders_count DESC, m.name;

-- name: available_masters
-- Свободные мастера на дату: NOT EXISTS и параметризованный WHERE.
SELECT m.id, m.name, m.specialty, m.experience, m.rating, m.price_per_hour
FROM masters AS m
WHERE NOT EXISTS (
    SELECT 1 FROM orders AS o
    WHERE o.master_id = m.id AND o.booking_date = ?
      AND o.status = 'Создан'
)
ORDER BY m.rating DESC, m.name;

-- name: master_busy_on_date
-- Проверка доступности одного мастера на дату: WHERE с двумя параметрами.
SELECT COUNT(*) AS busy FROM orders
WHERE master_id = ? AND booking_date = ? AND status = 'Создан';
