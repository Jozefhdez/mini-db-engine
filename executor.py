from storage import Storage

class Executor:
    def __init__(self):
        self.db = Storage()

    def execute(self, command):
        cmd_type = command[0]

        if cmd_type == "CREATE":
            _, name, cols, index_col = command # get values from tuple
            self.db.create_table(name, cols, index_col) # use them
            print(f"Table '{name}' created. Indexed on '{index_col}'." if index_col else f"Table '{name}' created.")

        elif cmd_type == "INSERT":
            _, name, values = command
            self.db.insert_row(name, values)
            print("Row inserted.")

        elif cmd_type == "SELECT":
            _, name, col, val = command
            if col and val:
                rows = self.db.select_where_indexed(name, col, val)
                if rows is not None:
                    print(f"[Planner] Used B-Tree index on '{col}'.")
                else: # fallback in case no index is found
                    print(f"[Planner] No index found on '{col}', doing full table scan instead.")
                    rows = [r for r in self.db.select_all(name) if str(r[col]) == str(val)]
            else:
                rows = self.db.select_all(name)
            for r in rows:
                print(r)

        elif cmd_type == "DELETE":
            _, name, col, val = command
            self.db.delete_where(name, col, val)
            print("Rows deleted.")

        else:
            print("Invalid command.")