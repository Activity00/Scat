# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 19:14
"""
import string

import fire
import os
import shutil

TEMPLATES_TO_RENDER = (
    ('scrapy.cfg',),
    ('${project_name}', 'settings.py.tmpl'),
    ('${project_name}', 'items.py.tmpl'),
    ('${project_name}', 'pipelines.py.tmpl'),
    ('${project_name}', 'middlewares.py.tmpl'),
)


class Commands:
    def createproject(self, name, path='.', template_dir=None):
        import scat
        from os.path import join, abspath

        # template_base_dir = template_dir or join(scat.__path__[0], 'templates')
        # self._copytree(template_base_dir, abspath(path))
        #
        # shutil.move(join(path, 'module'), join(path, name))
        # for paths in TEMPLATES_TO_RENDER:
        #     path = join(*paths)
        #     tplfile = join(path, string.Template(path).substitute(project_name=project_name))
        #     render_templatefile(tplfile, project_name=project_name,
        #                         ProjectName=string_camelcase(project_name))
        # print("New Scrapy project %r, using template directory %r, created in:" % \
        #       (project_name, self.templates_dir))
        # print("    %s\n" % abspath(project_dir))
        # print("You can start your first spider with:")
        # print("    cd %s" % project_dir)
        # print("    scrapy genspider example example.com")
        # return 'create project {} path: {}'.format(name, path)

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
