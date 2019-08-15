# coding = utf-8

'''fabric自动化部署'''

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = "https://github.com/zw-su/Tdd-Test.git"


def deploy():
    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/Tdd_Test'
    _create_directory_structurn_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    # _update_database(source_folder)


def _create_directory_structurn_if_necessary(site_floder):
    '''创建工作目录'''
    for subfolder in ('static', 'Tdd_Test', 'virtualenv'):
        run(f'mkdir -p {site_floder}/{subfolder}')


def _get_latest_source(source_folder):
    '''git上拉取代码'''
    if exists(source_floder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {source_folder} && git resset --hard {current_commit}')


def _update_settings(source_folder, site_name):
    '''更改django setting.py配置并创建密钥'''
    setting_path = source_folder + '/myproject/settings.py'
    sed(settings_path, 'DEBUG = True', 'DEBUG = False')
    sed(settings_path, 'ALLOWD_HOSTS = .+$',
        f"ALLOWED_HOSTS = ['{site_name}']")
    secret_key_file = source_folder + '/myproject/secret_key'
    if not exists(secret_key_file):
        chars = 'qwertyuiopasdfghjklzxcvbnm0123456789!@#$%^&*()'
        key = ''.join(random.SystemRandom().choices(chars, k=50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(setting_path, f"\nfrom .serte_key import SECRET_KEY")


def _update_virtualenv(source_folder):
    '''创建或更新虚拟环境'''
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')


def _update_static_files(source_folder):
    '''打包静态文件'''
    run(f'cd {source_folder}'
        '&& ../virtualenv/bin/pip manage.py collectstatic --noinput')
