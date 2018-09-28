import hug


@hug.get('/')
def server_test():
    """Basic 'Hello, World!' test"""
    return 'Hello, Hug!'


if __name__ == '__main__':
    hug.API(__name__).http.serve()
