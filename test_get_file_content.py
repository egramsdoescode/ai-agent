from config import MAX_CHARS, TRUNC_MSG_LEN
from functions.get_file_content import get_file_content

test_cases = [
    ("calculator", "lorem.txt"),
    ("calculator", "main.py"),
    ("calculator", "pkg/calculator.py"),
    ("calculator", "/bin/cat"),
    ("calculator", "pkg/does_not_exits.py"),
]

output = get_file_content("calculator", "lorem.txt")


for case in test_cases:
    result = get_file_content(case[0], case[1])
    content_length = len(result)
    trunc_message = result[-TRUNC_MSG_LEN:] if content_length > MAX_CHARS else ""
    print(
        f"""
Result for {case[1]}:
{result}
    - Content Length: {content_length}{"\n\t- " + trunc_message if trunc_message else ""}
"""
    )
