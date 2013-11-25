# coding:utf-8

import re
import sys
import pip
from optparse import OptionParser
from fabric.state import env

from essay.project import create_project, init_project

usage = """es usage: es create/init [project_name]
    Commands available:
        create: create project with full structure
        pinstall: this command help you install package from our pypi server
        and other PIP support command
    """


def init_options():
    parser = OptionParser(usage=usage)

    parser.add_option("-t", "--template", dest="template", default="default",
                      help="project template:[default],[django]")

    return parser.parse_args()


def main():
    help_text = usage

    if len(sys.argv) == 2 and sys.argv[1] == 'init':
        init_project(None, 'init')
    elif len(sys.argv) >= 2 and sys.argv[1] == 'create':
        options, args = init_options()
        project_name = sys.argv[2]
        if re.match('^[a-zA-Z0-9_]+$', project_name):
            create_project(project_name, options.template)
        else:
            print u'无效工程名: ' + project_name
    elif len(sys.argv) >= 2 and sys.argv[1] == 'init':
        options, args = init_options()
        project_name = sys.argv[2]
        if re.match('^[a-zA-Z0-9_]+$', project_name):
            init_project(project_name, options.template)
        else:
            print u'无效工程名: ' + project_name
    elif len(sys.argv) >= 2 and sys.argv[1] == 'pinstall':
        if len(sys.argv) == 2 or sys.argv[2] == '-h':
            print "es pinstall <package>"
            return

        args = sys.argv[1:]
        args[0] = 'install'
        args.append('-i %s' % env.PYPI_INDEX)
        pip.main(args)
    else:
        if len(sys.argv) == 2 and '-h' in sys.argv:
            print help_text
        pip.main()


if __name__ == '__main__':
    main()
