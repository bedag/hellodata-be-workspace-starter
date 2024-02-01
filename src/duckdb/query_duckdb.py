import duckdb

# Create an in-memory DuckDB database
conn = duckdb.connect(database=":memory:", read_only=False)

# Execute a simple query
result = conn.execute("SELECT 'Hello, Data Engineering World!' AS Greeting").fetchall()

# Print the result
print(result)

result = conn.execute(
    "CREATE TABLE tbl (i INTEGER); CREATE TABLE tbl2 (v VARCHAR);"
).fetchall()

# List all tables
tables = conn.execute("SHOW TABLES").fetchall()

# Print the results
print("Tables in the database:", tables)
