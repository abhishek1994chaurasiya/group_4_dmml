
use recomart_transformed;

--A. User Activity Frequency

CREATE TABLE IF NOT EXISTS user_activity_frequency AS
SELECT
    user_id,
    COUNT(*) AS total_interactions
FROM recomart.user_interactions
GROUP BY user_id;


--B. Average Rating per User
CREATE TABLE IF NOT EXISTS user_average_rating AS
SELECT
    user_id,
    AVG(rating) AS average_rating
FROM recomart.user_interactions
WHERE rating IS NOT NULL
GROUP BY user_id;

-- C. Average Rating per Item
CREATE TABLE IF NOT EXISTS item_avg_rating AS
SELECT
    product_id,
    AVG(rating) AS avg_item_rating,
    COUNT(rating) AS rating_count
FROM recomart.user_interactions
WHERE rating IS NOT NULL
GROUP BY product_id;

-- D. Co-occurrence / Similarity-based Features
CREATE TABLE IF NOT EXISTS item_cooccurrence AS
SELECT
    a.product_id AS product_id_1,
    b.product_id AS product_id_2,
    COUNT(*) AS co_occurrence_count
FROM recomart.user_interactions a
JOIN recomart.user_interactions b
  ON a.user_id = b.user_id
 AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id;

