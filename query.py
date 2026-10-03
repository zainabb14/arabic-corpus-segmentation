import sqlite3
from collections import Counter
import ast

# Connect to the SQLite database
conn = sqlite3.connect('C:\\Users\\User\\Desktop\\ACS\\instance\\database.db')
cursor = conn.cursor()

# Query to get the prefixes
cursor.execute(
    "SELECT camel_prefix, pyaramorph_prefix FROM words WHERE camel_prefix != '[]' OR pyaramorph_prefix != '[]';")
rows = cursor.fetchall()


# Function to safely parse the string representation of a list
def parse_list(s):
    try:
        return ast.literal_eval(s)
    except (ValueError, SyntaxError):
        return []


# Counter to count occurrences of each prefix
prefix_counter = Counter()

# Process each row
for row in rows:
    camel_prefix = parse_list(row[0])
    pyaramorph_prefix = parse_list(row[1])

    # Update the counter with prefixes from both columns
    prefix_counter.update(camel_prefix)
    prefix_counter.update(pyaramorph_prefix)

# Print the counts of each prefix
for prefix, count in prefix_counter.items():
    print(f"{prefix}: {count}")

# Close the database connection
conn.close()
