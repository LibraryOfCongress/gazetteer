#this is a fabfile, use it with fab from http://fabfile.org/
#
# initial setup (eg):
# fab gazetteer_in setup
#
# deploy changes (eg):
# fab gazetteer_in deploy
#


from os.path import join 
from fabric.api import run, local, sudo, put, env

env.project_user = 'gazetteer'
env.hosts = ['%(project_user)s@topomancy.com'%env, ]

def gazetteer_in():
    env.project_root = '/srv/gazetteer.in'

def dev_gazetteer_in():
    env.project_root = '/srv/dev.gazetteer.in'

def nypl_gazetteer_in():
    env.project_root = '/srv/nypl.gazetteer.in'

def dev_nypl_gazetteer_in():
    env.project_root = '/srv/dev.nypl.gazetteer.in'

def git_pull():
    run('cd %(project_root)s;git pull'%env)     

def virtual_run(cmd, *a, **kw):
    cmd = 'cd %s; source bin/activate; %s' % (env.project_root, cmd)
    run(cmd, *a, **kw)

def update_requirements():
    run('pip -E %(project_root)s install -r %(project_root)s/requirements.txt'%env)

def setup():
    """
    Setup a fresh virtualenv - FIXME: make work with all steps required to setup on server
    """
    local('bzr push --use-existing-dir bzr+ssh://%(host)s%(project_root)s'%env)
    run('cd %(project_root)s; test -e .bzr/checkout || bzr checkout'%env)
    run('virtualenv %(project_root)s'%env)
    put(join('settings', '%(host)s.py'%env), join(env.project_root, env.project_name, 'local_settings.py'))
    update_requirements()

def deploy():   
    git_pull()
    virtual_run('python manage.py collectstatic --noinput'%env)
    virtual_run('python manage.py build_js')
    run('touch %(project_root)s/wsgi/django.wsgi'%env)
