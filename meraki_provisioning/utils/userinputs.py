def get_input(prompt=""):
    try:
        line = input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_user_input(input_desc: str) -> str:
    """define user input to validate and return in string format"""
    print("\n" + "*" * 80)
    user_input = None
    while not user_input:
        user_input = get_input(f"\nEnter: {input_desc}: ")
        user_input_verify = get_input(f"Verify: {input_desc}: ")
        if user_input != user_input_verify:
            print(f"Inputs do not match. Try again.")
            user_input = None
    return user_input
