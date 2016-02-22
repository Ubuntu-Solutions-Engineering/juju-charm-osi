import os
from subprocess import check_call
from charmhelpers.core import hookenv
from charmhelpers.core.templating import render
from charmhelpers.fetch import (
    apt_install,
    apt_update,
    add_source
)

from charms.reactive import (
    hook,
    main
)

config = hookenv.config()
CHARM_DIR = os.getenv('CHARM_DIR')
CHARM_TMP = os.path.join(CHARM_DIR, 'tmp')


def _build_context():
    ctx = {
        'install_type': config['install-type'],
        'openstack_password': config['openstack-password'],
        'openstack_release': config['openstack-release'],
        'ubuntu_series': config['ubuntu-series'],
        'upstream_ppa': config['upstream-ppa']
    }
    return ctx


@hook('install')
def install():
    hookenv.status_set('maintenance',
                       'Installing Ubuntu OpenStack Installer')
    add_source('ppa:cloud-installer/experimental')
    add_source('ppa:juju/stable')
    apt_update()
    apt_install(['openstack', 'python3-pytest', 'git'])
    ctx = _build_context()
    render(source='osi-config.yaml',
           target=os.path.join(CHARM_TMP, 'osi-config.yaml'),
           context=ctx)
    hookenv.status_set('maintenance', 'Cloning openstack-tests')
    hookenv.status_set('maintenance', 'Installing OpenStack')
    check_call(['sudo', 'openstack-install', '-c',
                os.path.join(CHARM_TMP, 'osi-config.yaml')])
    hookenv.status_set('active', 'ready')


@hook('config-changed')
def config_changed():
    hookenv.status_set('maintenance',
                       'Updating OSI Configuration')
    ctx = _build_context()
    render(source='osi-config.yaml',
           target=os.path.join(CHARM_TMP, 'osi-config.yaml'),
           context=ctx)
    hookenv.status_set('active', 'ready')


if __name__ == "__main__":
    main()
