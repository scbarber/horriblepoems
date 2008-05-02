"""
Call this like ``python generate-bootstrap.py``; it will
refresh the appengine-boot.py script
"""
import os
import subprocess
import re

here = os.path.dirname(os.path.abspath(__file__))
script_name = os.path.join(here, 'appengine-boot.py')

import virtualenv

## FIXME: should remove option --unzip-setuptools, --no-site-packages

EXTRA_TEXT = """
import shutil
import re

if sys.version[:3] != '2.5':
    print 'ERROR: you must run this script with python2.5'
    sys.exit(5)

def extend_parser(parser):
    parser.add_option(
        '--paste-deploy',
        dest='paste_deploy',
        action='store_true',
        help='Put into place the structure for a Paste Deploy (e.g., Pylons) application')
    parser.add_option(
        '--app-name',
        dest='app_name',
        metavar='APP_NAME',
        help='The application name (for app.yaml); defaults to the name of DEST_DIR')
    parser.add_option(
        '--app-yaml',
        dest='app_yaml',
        metavar='FILENAME',
        default=os.path.join(os.path.dirname(__file__), 'app.yaml.template'),
        help='File to use as the basis for app.yaml')
    parser.add_option(
        '--app-script',
        dest='app_script',
        metavar='SCRIPT',
        help='Script to run to run the application')
    parser.add_option(
        '--easy-install',
        dest='easy_install',
        metavar='PACKAGE',
        action='append',
        help='Install this package with easy_install immediate (can use more than once)')

def adjust_options(options, args):
    if not args:
        return # caller will raise error
    if not options.app_name:
        options.app_name = os.path.basename(args[0])
    options.unzip_setuptools = True
    if not options.easy_install:
        options.easy_install = []
    if options.paste_deploy:
        options.easy_install.extend(['PasteDeploy', 'PasteScript'])
        if not options.app_script:
            options.app_script = 'paste-deploy.py'
    elif not options.app_script:
        options.app_script = 'main.py'

def after_install(options, home_dir):
    src_dir = join(home_dir, 'src')
    mkdir(src_dir)
    logger.indent += 2
    fixup_distutils_cfg(options, home_dir)
    try:
        packages = [os.path.dirname(os.path.abspath(__file__))] + list(options.easy_install)
        call_subprocess([os.path.abspath(join(home_dir, 'bin', 'easy_install'))] + packages,
                        cwd=home_dir,
                        filter_stdout=filter_python_develop,
                        show_stdout=False)
    finally:
        logger.indent -= 2
    install_app_yaml(options, home_dir)
    if options.paste_deploy:
        install_paste_deploy(options, home_dir)
    logger.notify('\\nRun "%s -m pth_relpath_fixup" before deploying'
                  % join(home_dir, 'bin', 'python'))
    logger.notify('Run "%s Package" to install new packages that provide builds'
                  % join(home_dir, 'bin', 'easy_install'))
    
def fixup_distutils_cfg(options, home_dir):
    distutils_cfg = os.path.join(home_dir, 'lib', 'python%s' % sys.version[:3], 'distutils', 'distutils.cfg')
    if os.path.exists(distutils_cfg):
        f = open(distutils_cfg)
        c = f.read()
        f.close()
    else:
        c = ''
    if 'zip_ok' in c:
        logger.notify('distutils.cfg already has zip_ok set')
        return
    f = open(distutils_cfg, 'a')
    f.write('\\n[easy_install]\\nzip_ok = False\\n')
    f.close()
    logger.info('Set zip_ok = False in distutils.cfg')

def install_app_yaml(options, home_dir):
    f = open(options.app_yaml, 'rb')
    c = f.read()
    f.close()
    c = c.replace('__APP_NAME__', options.app_name)
    c = c.replace('__APP_SCRIPT__', options.app_script)
    dest = os.path.join(home_dir, 'app.yaml')
    if os.path.exists(dest):
        logger.warn('Warning: overwriting %s' % dest)
    f = open(dest, 'wb')
    f.write(c)
    f.close()
    
def install_paste_deploy(options, home_dir):
    shutil.copyfile(os.path.join(os.path.dirname(__file__), 'paste-deploy.py'),
                    os.path.join(home_dir, 'paste-deploy.py'))
    dest = os.path.join(home_dir, 'development.ini')
    msg = 'Wrote paste-deploy.py'
    if os.path.exists(dest):
        logger.notify('Not overwriting development.ini')
    else:
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'development.ini.template'),
                        dest)
        msg += ' and development.ini'
    logger.notify(msg)

def filter_python_develop(line):
    if not line.strip():
        return Logger.DEBUG
    for prefix in ['Searching for', 'Reading ', 'Best match: ', 'Processing ',
                   'Moving ', 'Adding ', 'running ', 'writing ', 'Creating ',
                   'creating ', 'Copying ']:
        if line.startswith(prefix):
            return Logger.DEBUG
    return Logger.NOTIFY
"""

def main():
    text = virtualenv.create_bootstrap_script(EXTRA_TEXT, python_version='2.5')
    if os.path.exists(script_name):
        f = open(script_name)
        cur_text = f.read()
        f.close()
    else:
        cur_text = ''
    print 'Updating %s' % script_name
    if cur_text == 'text':
        print 'No update'
    else:
        print 'Script changed; updating...'
        f = open(script_name, 'w')
        f.write(text)
        f.close()

if __name__ == '__main__':
    main()

