#!/usr/bin/env python

# The `ManagePGPKeys` form allows users to manage their GPG keys.

import gnupg
import npyscreen

from select_pgp_key import SelectPgpKey

class ManagePGPKeys(npyscreen.ActionFormWithMenus):
    # Add the operations menu for generating new keys.
    def _create_menus(self) -> None:
        self.menu = self.add_menu(name = "Operations")
        self.menu.addItem(text = "Generate New Key", onSelect = self._gen_key)

    # Generate a new GPG key pair and notify the user about it.
    def _gen_key(self) -> None:
        key: gnupg.GenKey = \
                self.parentApp.communication.visit_now.user.gen_key()

        # Update the GPG key list and redraw the screen because of the generated
        # key.
        self._set_keys()
        self.display()

        npyscreen.notify_confirm(
                "Generated new key: {}".format(key.fingerprint)
                )

    # Set the current person to the `Communication` form's current person.
    def _set_current_user(self) -> None:
        self.current_user.value = \
                self.parentApp.communication.visit_now.user.name

    # Set the GPG key list to the `Communication` form's current person.
    def _set_keys(self) -> None:
        self.pgp_keys.values = \
                self.parentApp.communication.visit_now.user.list_keys()

    # Update the `Communication` forms values and switch to the previous form.
    def afterEditing(self) -> None:
        selected_keys = self.pgp_keys.get_selected_objects()

        if selected_keys:
            self.parentApp.communication.visit_now.user.current_key = \
                    selected_keys[0].get("keyid")
            self.parentApp.communication._set_box_name(
                    self.parentApp.communication.visit_now
                    )

        self.parentApp.switchFormPrevious()

    # Update the data to be displayed.
    def beforeEditing(self) -> None:
        self._set_current_user()
        self._set_keys()

    # Initialise the current user, the GPG keys, and the menus.
    def create(self) -> None:
        self.current_user = self.add(npyscreen.TitleFixedText,
                                     name = "Current User")

        self.pgp_keys = self.add(SelectPgpKey, name = "Select PGP Key")

        self._create_menus()
