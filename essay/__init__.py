try:
    from fabric.state import env
    env.PYPI_INDEX = 'http://pypi.doubanio.com/simple/'
except ImportError:
    pass


VERSION = '0.0.8'
