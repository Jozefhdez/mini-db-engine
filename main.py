from parser import Parser
from executor import Executor

def main():
    parser = Parser()
    executor = Executor()

    print("Mini DB Engine")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("db> ").strip()
        if query.lower() == 'exit':
            break
        if not query:
            continue
        command = parser.parse(query)
        executor.execute(command)

if __name__ == "__main__":
    main()