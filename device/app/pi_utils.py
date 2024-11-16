import os

def is_pi_environment():
    return os.getenv("PI_ENV", "false") == "true"
    