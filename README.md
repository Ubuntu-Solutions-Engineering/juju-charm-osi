# Overview
> Runs Ubuntu OpenStack Installer

This is more than likely not what you want, pretty specific to our testing needs.

# Usage

Step by step instructions on using the charm:

```
juju deploy osi
```

Configure the type of install to run

```
juju config osi set install_type=multi
juju config osi set maas_server=10.0.3.1
juju config osi set maas_api_key=abcdefhijklkmonopqursrstvo
juju action do osi/0 run-test
```
