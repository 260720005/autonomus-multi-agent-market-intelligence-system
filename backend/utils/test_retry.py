from backend.utils.retry import retry_with_backoff


attempts = 0


@retry_with_backoff(
    max_retries=3,
    initial_delay=1
)
def test_function():

    global attempts

    attempts += 1

    print(f"Attempt {attempts}")

    if attempts < 3:
        raise Exception("Temporary failure")

    return "Success!"


result = test_function()

print("\nResult:", result)