from charmhelpers.core import hookenv
from charmhelpers.fetch import (
    apt_install,
    apt_update,
    add_source
)

from charms.reactive import (
    hook,
    set_state,
    remove_state,
    main
)

config = hookenv.config()


@hook('install')
def install():
    hookenv.status_set('maintenance',
                       'Installing Ubuntu OpenStack Installer')
    add_source('ppa:cloud-installer/experimental')
    add_source('ppa:juju/stable')
    apt_update()
    apt_install(['openstack'])
