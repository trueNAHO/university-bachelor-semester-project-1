#!/usr/bin/env python

# The abstract `User` class defines each person the user can impersonate.

import gnupg
import os

class User:
    gnupghome: str = "./.gnupg"

    def __init__(self, name: str) -> None:
        gnupghome: str = self._create_gnupghome(name)

        self.current_key: dict | None = None
        self.gpg: gnupg.GPG = gnupg.GPG(gnupghome = gnupghome)
        self.name: str = name

    # Return the GPG home file path, and create it if it does not exist. Every
    # GPG home is a sub folder of `self.gnupghome` and has the name of the
    # `name` argument.
    def _create_gnupghome(self, name: str) -> str:
        gnupghome: str = "{}/{}".format(self.gnupghome, name)

        if not os.path.exists(gnupghome):
            os.makedirs(gnupghome)

        return gnupghome

    # Return the decrypted `data`.
    def decrypt(self, data: gnupg.Crypt) -> gnupg.Crypt:
        return self.gpg.decrypt(str(data))

    # Sign the file located at `filepath`. `signature_extension` defines the
    # extension for the detached signature file.
    def detach_sign(
            self, filepath: str, signature_extension: str = "sig"
            ) -> None:
        with open(filepath, "rb") as file:
            self.gpg.sign_file(file, detach = True,
                               output = "{}.{}".format(filepath,
                                                       signature_extension))

    # Return the encrypted `data` for the `recipients`.
    def encrypt(self, data, recipients: list[str] | str) -> gnupg.Crypt:
        return self.gpg.encrypt(data, recipients, always_trust = True)

    # Export `keyids` GPG keys.
    def export_keys(self, keyids: str | list[str]) -> str:
        return self.gpg.export_keys(keyids)

    # Generate a new GPG key pair. The `hostname` argument defines the hostname
    # for the GPG key's email.
    def gen_key(self, hostname: str = "encryptinthemiddle") -> gnupg.GenKey:
        return self.gpg.gen_key(
                self.gpg.gen_key_input(
                    name_email = "{}@{}".format(self.name, hostname),
                    name_real = self.name,
                    no_protection = True
                    )
                )

    # Import the `key_data` into the keyring.
    def import_keys(self, key_data: str) -> gnupg.ImportResult:
        return self.gpg.import_keys(key_data)

    # List the keys in the keyring.
    def list_keys(self) -> dict[str, str]:
        return self.gpg.list_keys()

    # Return the verified detached signature by comparing the `filepath_sender`
    # and `filepath_receiver` files. Create the `filepath` file if it does not
    # exists to simplify the code.
    def verify_detached_sign(
            self, filepath_sender: str, filepath_receiver: str,
            signature_extension: str = "sig"
            ) -> gnupg.Verify:
        filepath: str = "{}.{}".format(filepath_sender, signature_extension)

        if not os.path.exists(filepath):
            open(filepath, "a").close()

        with open(filepath, "rb") as file:
            verified: gnupg.Verify = self.gpg.verify_file(file,
                                                          filepath_receiver)

        return verified
