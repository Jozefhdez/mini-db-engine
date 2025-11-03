import re
import shlex

class Parser:
    '''
    Simple SQL parser using regex.
    Parses queries and returns tuples
    '''
    def parse(self, query):
        query = query.strip().rstrip(";") # remove leading/trailing whitespace and semicolons
        # CREATE TABLE table_name (col1, col2, ...) INDEX col_name
        if match := re.match(r"create table (\w+)\s*\((.*?)\)(?: index (\w+))?$", query, re.I):
            table_name = match.group(1)
            columns = [c.strip() for c in match.group(2).split(",")]
            index_col = match.group(3)  # None if not specified
            return ("CREATE", table_name, columns, index_col)
        
        # INSERT INTO table_name VALUES (val1, val2, ...)
        if match := re.match(r"insert into (\w+)\s*values\s*\((.*?)\)$", query, re.I):
            table_name = match.group(1)
            raw_values = match.group(2)
            lexer = shlex.shlex(raw_values, posix=True)
            lexer.whitespace_split = True
            lexer.whitespace = ","
            values = [token.strip() for token in lexer]
            return ("INSERT", table_name, values)
        
        # SELECT * FROM table_name [WHERE col = value]
        if match := re.match(r"select \* from (\w+)(?: where (\w+)\s*=\s*'?([\w\s]+)'?)?$", query, re.I):
            table_name = match.group(1)
            where_col = match.group(2) # None if no WHERE clause
            where_val = match.group(3) # None if no WHERE clause
            return ("SELECT", table_name, where_col, where_val)
        
        # DELETE FROM table_name WHERE col = value
        if match := re.match(r"delete from (\w+) where (\w+)\s*=\s*'?([\w\s]+)'?$", query, re.I):
            table_name = match.group(1)
            where_col = match.group(2)
            where_val = match.group(3)
            return ("DELETE", table_name, where_col, where_val)

        # no match found
        return ("INVALID",)