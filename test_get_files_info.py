from functions.get_files_info import get_files_info

test_cases = [
    ("calculator", "."),
    ("calculator", "pkg"),
    ("calculator", "/bin"),
    ("calculator", "../"),
]

for case in test_cases:
    print(
        f""" 
Result for {"current" if case[1] == "." else f"'{case[1]}'"} directory:
{get_files_info(*case)}"""
    )
