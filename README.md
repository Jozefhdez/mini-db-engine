# Mini DB Engine

In-memory database engine with B-Tree indexing and query planning, implemented in Python.

> NOTE: Educational / Toy project
>
> This repository implements a small, educational database engine for learning and experimentation.

## Features

* Create tables with optional indexed columns
* Insert, select, and delete rows
* B-Tree index for fast lookups on primary keys
* Simple query planner that detects and uses indexes
* Persistent storage using JSON

---

## File structure

```
mini_db/
├── main.py # Command-line interface
├── parser.py # SQL command parser
├── executor.py # Executes parsed commands
├── storage.py # Handles tables and persistence
└── btree.py # B-Tree index implementation
```

---

## How to run

1. Clone the repository

   ```
   git clone https://github.com/jozefhdez/mini-db-engine
   cd mini-db-engine
   ```

2. Start the engine

   ```
   python3 main.py
   ```

3. Use SQL-like commands

   ```
   db> CREATE TABLE users (id, name, age) INDEX id;
   db> INSERT INTO users VALUES (1, 'Jozef', 19);
   db> INSERT INTO users VALUES (2, 'David', 20);
   db> SELECT * FROM users WHERE id = 2;
   db> SELECT * FROM users;
   db> DELETE FROM users WHERE id = 1;
   db> exit
   ```

---

## Example output

```
Mini DB Engine
Type 'exit' to quit.

db> CREATE TABLE users (id, name, age) INDEX id;
Table 'users' created. Indexed on 'id'.

db> INSERT INTO users VALUES (1, 'Alice', 22);
Row inserted.

db> SELECT * FROM users WHERE id = 1;
[Planner] Used B-Tree index on 'id'.
{'id': '1', 'name': "'Alice'", 'age': '22'}
```

---

## How it works

* **Parser**
  Converts SQL-like text into internal commands using regex.

* **Executor**
  Executes commands, detects indexes, and routes queries through the correct path.

* **Storage**
  Manages tables and rows in a JSON file for persistence.

* **B-Tree**
  Custom implementation that stores `(key, row_index)` pairs and supports insertion, search, and node splitting.

---


### Learning Resources

- [Build-a-Database with Python - Breaking down the abstractions ](https://www.youtube.com/watch?v=Ay9MNXXURBc)
- [B-Tree Implementation](https://www.youtube.com/watch?v=CWI6sDEdBLM)