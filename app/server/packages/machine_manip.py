import os

def shutdown(after=5):
    args = ['shutdown', '/s', '/t', str(after)]
    return os.system(' '.join(args)) == 0

# TODO: define logout function
