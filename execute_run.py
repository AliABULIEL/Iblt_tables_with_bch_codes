import subprocess

def execute_command(command):
    """Executes a given command and prints its output."""
    process = subprocess.run(command, capture_output=True, text=True)

    print("Running command:", " ".join(command))
    print("Output:")
    print(process.stdout)

    if process.stderr:
        print("Errors:")
        print(process.stderr)

def run_iblt_tests():
    # Test with strings
    commands = [
        ['python', 'run.py', '--size', '10', '--r', '3', '--d', '1', '--data', 'hello', 'world', '--list_entries'],
        # ['python', 'run.py', '--size', '10', '--r', '4', '--d', '3', '--insert', 'newdata', '--delete', 'world', '--list_entries']
    ]

    # Test with integers
    # commands += [
    #     ['python', 'run.py', '--size', '10', '--r', '4', '--d', '3', '--data', '123', '456', '--list_entries'],
    #     ['python', 'run.py', '--size', '10', '--r', '4', '--d', '3', '--insert', '789', '--delete', '123', '--list_entries']
    # ]

    for command in commands:
        execute_command(command)

if __name__ == '__main__':
    run_iblt_tests()
