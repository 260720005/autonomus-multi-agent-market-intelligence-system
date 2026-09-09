# As our limit reaches in Groq we will add retry + backoff to run the code correctly.
import time
from functools import wraps #Hum function ko decorator se wrap kar rahe hain:

def retry_with_backoff(  #Jis function pr use hoga usko Retry Kara Sakta Hai
    max_retries = 4,
    initial_delay=5
):
    """
    Retry a function when it fails.

    Each retry waits longer than the previous attempt.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs): # *args aur **kwargs ka matlab Original function ko jo bhi arguments mil rahe hain, unhe accept kar lo.

            delay = initial_delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    if attempt == max_retries:
                        print(
                            f"❌ {func.__name__} failed "
                            f"after {max_retries} retries."
                        )
                        raise

                    print(
                        f"⚠️ {func.__name__} failed. "
                        f"Retrying in {delay}s..."
                    )

                    time.sleep(delay)

                    delay *= 2

        return wrapper

    return decorator