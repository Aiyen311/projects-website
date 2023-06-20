-- name: get-all-projects
-- Get a list of all of the companies.
SELECT title, EXTRACT(YEAR FROM created_at) FROM projects;