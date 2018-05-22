# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 19:14
"""
import string

import fire
import os
import shutil

import re

TEMPLATES_TO_RENDER = (
    ('manage.py.tmpl',),
    ('start_servers.py.tmpl', ),
    # ('${project_name}', 'settings.py.tmpl'),
)


def render_templatefile(path, **kwargs):
    with open(path, 'rb') as fp:
        raw = fp.read().decode('utf8')

    content = string.Template(raw).substitute(**kwargs)

    render_path = path[:-len('.tmpl')] if path.endswith('.tmpl') else path
    with open(render_path, 'wb') as fp:
        fp.write(content.encode('utf8'))
    if path.endswith('.tmpl'):
        os.remove(path)


CAMELCASE_INVALID_CHARS = re.compile('[^a-zA-Z\d]')


def string_camelcase(string):
    """ Convert a word  to its CamelCase version and remove invalid chars

    >>> string_camelcase('lost-pound')
    'LostPound'

    >>> string_camelcase('missing_images')
    'MissingImages'

    """
    return CAMELCASE_INVALID_CHARS.sub('', string.title())


class Commands:
    def createproject(self, project_name, project_dir='.', template_dir=None):
        import scat
        from os.path import join, abspath

        template_base_dir = template_dir or join(scat.__path__[0], 'templates')
        self._copytree(template_base_dir, abspath(project_dir))
        shutil.move(join(project_dir, 'module'), join(project_dir, project_name))

        for paths in TEMPLATES_TO_RENDER:
            path = join(*paths)
            tplfile = join(project_dir, string.Template(path).substitute(project_name=project_name))
            render_templatefile(tplfile, project_name=project_name, ProjectName=string_camelcase(project_name))

        print("New Scat project %r, using template directory %r, created in:" % (project_name, template_base_dir))
        print("    %s\n" % abspath(project_dir))
        print("You can start your first app with:")
        print("    cd %s" % project_dir)
        print("    scat startapp example")

    def runserver(self, server_name='', mode=''):
        from scat.distributed.master import MASTER_SERVER_MODE, SINGLE_SERVER_MODE, MULTI_SERVER_MODE
        from scat.distributed.master import Master
        if mode == "single":
            if server_name == "master":
                mode = MASTER_SERVER_MODE
            else:
                mode = SINGLE_SERVER_MODE
        else:
            mode = MULTI_SERVER_MODE
            server_name = ''
        master = Master()
        master.start(server_name, mode)

    def start_server(self, server_name):
        from scat.server import ScatServer
        server = ScatServer(server_name)
        server.start()

    def __str__(self):
        return 'Python manage.py COMMANDNAME --paras'

    def _copytree(self, src, dst):
        names = os.listdir(src)
        if not os.path.exists(dst):
            os.makedirs(dst)

        for name in names:
            if name.endswith('.pyc') or name.endswith('.git'):
                continue

            src_name = os.path.join(src, name)
            dst_name = os.path.join(dst, name)
            if os.path.isdir(src_name):
                self._copytree(src_name, dst_name)
            else:
                shutil.copy2(src_name, dst_name)
        shutil.copystat(src, dst)


def execute_from_command_line():
    fire.Fire(Commands)
