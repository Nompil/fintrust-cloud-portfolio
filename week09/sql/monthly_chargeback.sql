SELECT
    line_item_usage_account_id AS linked_account,
    resource_tags_user_cost_centre AS cost_centre,
    line_item_product_code AS service,
    date_trunc('month', line_item_usage_start_date) AS billing_month,
    ROUND(SUM(line_item_unblended_cost), 2) AS unblended_cost_usd
FROM fintrust_cur
WHERE line_item_usage_start_date >= date_add('month', -3, current_date)
  AND resource_tags_user_cost_centre IS NOT NULL
GROUP BY 1, 2, 3, 4
ORDER BY billing_month DESC, unblended_cost_usd DESC;
