
use recomart_transformed;

--A. User Activity Frequency

INSERT OVERWRITE user_activity_frequency
SELECT
    user_id,
    COUNT(*) AS total_interactions
FROM recomart.user_interactions
GROUP BY user_id;


--B. Average Rating per User
INSERT OVERWRITE user_average_rating
SELECT
    user_id,
    AVG(rating) AS average_rating
FROM recomart.user_interactions
WHERE rating IS NOT NULL
GROUP BY user_id;

-- C. Average Rating per Item
INSERT OVERWRITE item_avg_rating
SELECT
    product_id,
    AVG(rating) AS avg_item_rating,
    COUNT(rating) AS rating_count
FROM recomart.user_interactions
WHERE rating IS NOT NULL
GROUP BY product_id;

-- D. Co-occurrence / Similarity-based Features
INSERT OVERWRITE item_cooccurrence
SELECT
    a.product_id AS product_id_1,
    b.product_id AS product_id_2,
    COUNT(*) AS co_occurrence_count
FROM recomart.user_interactions a
JOIN recomart.user_interactions b
  ON a.user_id = b.user_id
 AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id;

