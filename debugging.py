import sys
import traceback

# See https://stackoverflow.com/a/58938751
def format_stacktrace():
    parts = ["Traceback (most recent call last):\n"]
    parts.extend(traceback.format_stack(limit=25))
    parts.extend(traceback.format_exception(*sys.exc_info()))
    return "".join(parts)

def ptraceback():
    print(format_stacktrace())
