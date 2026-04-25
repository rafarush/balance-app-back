-- Drop orphaned enum type
DROP TYPE IF EXISTS transactiontype;

-- Drop all tables (reverse order due to FK constraints)
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS "user";
DROP TABLE IF EXISTS role_policy;
DROP TABLE IF EXISTS transaction_category;
DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS policy;