# Mini DB Engine

In-memory database engine with B-Tree indexing and query planning, implemented in Python.

> NOTE: Educational / Toy project
>
> This repository implements a small, educational database engine for learning and experimentation.

## Features

* Create tables with optional indexed columns
* Insert, select, and delete rows
* B-Tree index for fast lookups on primary keys
* Query planner chooses between indexed lookup or full table scan
* Persistent storage using JSON