# Encrypt-in-the-middle

## About

Encrypt-in-the-middle is a local messaging application that demonstrates the use
of end-to-end encryption to protect against man-in-the-middle attacks in
communication between two individuals.

The application has a flexible and intuitive keyboard-driven TUI, which allows
the user to impersonate the individuals involved in the communication, send and
receive messages, sign and verify messages using GPG, encrypt and decrypt
messages with GPG, manage GPG keys, and select a GPG key pair. The application
can also simulate the actions of a man-in-the-middle attacker, who can intercept
and alter the messages being exchanged.

The application is delivered as a docker container with an installation script
to make the process of running the application easier for the end user.

## How to Use

All demonstrated commands should be run from the root directory of the repository.

### With [Docker](https://docs.docker.com/get-docker/)

If [Docker](https://docs.docker.com/get-docker/) is installed and working, start
the application with

```sh
./install.sh
```

or

```sh
sh install.sh
```

Note that you **must** be in the **same directory** as the installation
**script** for this to work.

### Manual Installation

It is strongly recommended to run the application with the installation script
as it is the only tested environment. This section is only here for completeness
reasons.

Install the [npyscreen](https://npyscreen.readthedocs.io/index.html) and
[python-gnupg](https://pythonhosted.org/python-gnupg/#download) Python modules
with

```sh
pip install npyscreen python-gnupg
```

In order for [python-gnupg](https://pythonhosted.org/python-gnupg/#download) to
work, the GPG executable must be accessible. This seems rather complicated on
Windows. See
[here](https://pythonhosted.org/python-gnupg/#deployment-requirements) for more
information.

Finally run the `./src/main.py` file with

```sh
./src/main.py
```

or

```sh
python src/main.py
```

## Tested

This application was developed and tested entirely on [Arch
Linux](https://archlinux.org/). No tests were done for any other environments.
