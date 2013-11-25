#coding:utf-8

import web
import settings

urls = (
    '/', 'index'
)

class index:
    def GET(self):
        return "Hello, world!"

def main():
    print 'version:', settings.__version__
    print 'git version:', settings.__git_version__
    print 'release time', settings.__release_time__

    app = web.application(urls, globals())
    app.run()  

if __name__ == '__main__':
    main()
