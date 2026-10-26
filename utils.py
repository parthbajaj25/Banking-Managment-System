def line():
    print("=" * 58)


def title(text):
    print()
    line()
    print(text.center(58))
    line()


def pause():
    input("\nPress Enter to continue...")


def read_amount(prompt, allow_zero=False):
    try:
        amount = float(input(prompt).strip())
        if amount != amount or amount == float("inf") or amount == float("-inf"):
            raise ValueError
        if amount < 0 or (amount == 0 and not allow_zero):
            print("Enter a valid positive amount.")
            return None
        return round(amount, 2)
    except ValueError:
        print("Please enter a valid number.")
        return None
