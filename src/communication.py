#!/usr/bin/env python

# The `Communication` class is a form that allows conversations between two
# people that a man-in-the-middle attacker managed to intercept.

import gnupg
import npyscreen

from box_multi_line_edit import BoxMultiLineEdit
from lib import Lib
from user import User

class Communication(npyscreen.ActionFormWithMenus):
    box_padding: int = 1
    default_box_footer: str = "PGP Status"
    default_box_value: str = ""
    filepath_detached_sign_visit_now: str = "visit_now.txt"
    filepath_detached_sign_visit_previous: str = "visit_previous.txt"
    man_in_the_middle_attacker: User = User("Person M")
    people: list[User] = [User("Person A"), User("Person B")]

    # Overwrite the box footer with its default value.
    def _clear_box_footer(self, box) -> None:
        box.footer = self.default_box_footer

    # Overwrite the box value with its default value.
    def _clear_box_value(self, box) -> None:
        box.set_value(self.default_box_value)

    # Clear the footer and value from all boxes.
    def _clear_boxes(self) -> None:
        for box in [self.box_left, self.box_middle, self.box_right]:
            self._clear_box_footer(box)
            self._clear_box_value(box)

    # Keep the data up-to-date when moving between widgets.
    def _control_flow(self) -> None:
        # This represents the base case when both `visit_previous` and
        # `visit_now` point to the first `box_left` box. In this case nothing
        # happens.
        if self.visit_previous == self.visit_now == self.box_left:
            pass

        # This case represents moving from the left to the the middle box. Send
        # the previous person's message to the next person and update its footer
        # as well as redraw the entire box.
        elif (self.visit_previous == self.box_left
              and self.visit_now == self.box_middle):
            self.visit_now.set_value(self.visit_previous.value)
            self._set_box_footer(self.visit_now)
            self.box_middle.update()

        # This case represents moving from the middle to the the right box. Send
        # the previous person's message to the next person and update its footer
        # as well as redraw the entire box.
        elif (self.visit_previous == self.box_middle
              and self.visit_now == self.box_right):
            self.visit_now.set_value(self.visit_previous.value)
            self._set_box_footer(self.visit_now)
            self.visit_now.update()

        # This case represents moving from the right to the the middle
        # box. Clear the current person's message and box footer as well as
        # redraw the entire box.
        elif (self.visit_previous == self.box_right
              and self.visit_now == self.box_middle):
            self._clear_box_value(self.visit_previous)
            self._clear_box_footer(self.visit_previous)
            self.visit_previous.update()

        # This case represents moving from the middel to the the right
        # box. Clear the current person's message and box footer as well as
        # redraw the entire box.
        elif (self.visit_previous == self.box_middle
              and self.visit_now == self.box_left):
            self._clear_box_value(self.visit_previous)
            self._clear_box_footer(self.visit_previous)
            self.visit_previous.update()

        # This case represents all other cases. In this case nothing happens.
        else:
            pass

    # Add the left, middle, and right boxes with their corresponding person.
    def _create_boxes(self, nextrely: int = 1) -> None:
        useable_width: int = self.widget_useable_space()[1]
        max_width: int = useable_width // 3 - self.box_padding * 2

        self.box_left = self.add(BoxMultiLineEdit,
                                 footer = self.default_box_footer, relx = 1,
                                 rely = nextrely, max_width = max_width)

        self.box_middle = self.add(BoxMultiLineEdit,
                                   footer = self.default_box_footer,
                                   relx = (useable_width - max_width) // 2 + 1,
                                   rely = nextrely, max_width = max_width)

        self.box_right = self.add(BoxMultiLineEdit,
                                  footer = self.default_box_footer,
                                  relx = -max_width - 3, rely = nextrely,
                                  max_width = max_width)

        self._set_box_user(self.box_left, self.people[0])
        self._set_box_user(self.box_middle, self.man_in_the_middle_attacker)
        self._set_box_user(self.box_right, self.people[1])

    # Add menus to this form.
    def _create_menus(self) -> None:
        self.menu_forms = self.add_menu(name = "Forms")
        self.menu_operations = self.add_menu(name = "Operations")
        self.menu_operations_people = \
                self.menu_operations.addNewSubmenu(name = "People")
        self.menu_application = self.add_menu(name = "Application")

        self.menu_forms.addItem(text = "PGP Keys", onSelect = lambda:
                                self.parentApp.switchForm("manage_pgp_keys"))

        self.menu_operations.addItem(text = "Decrypt message",
                                     onSelect = self._decrypt_message)

        self.menu_operations.addItem(text = "Encrypt message",
                                     onSelect = self._encrypt_message)

        self.menu_operations.addItem(text = "Export current Key",
                                     onSelect = self._export_key)

        self.menu_operations.addItem(text = "Import Key",
                                     onSelect = self._import_key)

        self.menu_operations_people.addItem(
                text = "Set sender to {}".format(self.people[0].name),
                onSelect = lambda: (
                    self._swap_box_users(self.box_left, self.box_right)
                    if self.people[0] != self.box_left.user else
                    None
                    )
                )

        self.menu_operations_people.addItem(
                text = "Set sender to {}".format(self.people[1].name),
                onSelect = lambda: (
                    self._swap_box_users(self.box_left, self.box_right)
                    if self.people[1] != self.box_left.user else
                    None
                    )
                )

        self.menu_application.addItem(text = "Exit", onSelect = self._exit)

    # Set the `visit_now` and `visit_previous` visit pointer to the left box.
    def _create_users(self):
        entry_point = self.box_left

        self.visit_now = entry_point
        self.visit_previous = entry_point

    # Decrypt the current person's message. Notify the user, if this fails.
    def _decrypt_message(self) -> None:
        decrypted_data: gnupg.Crypt = self.visit_now.user.decrypt(
                self.visit_now.value
                )

        if not decrypted_data.ok:
            npyscreen.notify_confirm(decrypted_data.status, "Decrypt message")
            return

        self.visit_now.value = str(decrypted_data)

    # Encrypt the current person's message. Notify the user, if this fails.
    def _encrypt_message(self) -> None:
        encrypted_data: gnupg.Crypt = self.visit_now.user.encrypt(
                self.visit_now.value,
                self.box_middle.user.name if self.visit_now == self.box_left else self.box_right.user.name
                )

        if not encrypted_data.ok:
            npyscreen.notify_confirm(encrypted_data.status, "Encrypt message")
            return

        self.visit_now.value = str(encrypted_data)

    # Exit application on user confirmation.
    def _exit(self) -> None:
        if npyscreen.notify_yes_no("Are you sure you want to exit?", "Exit"):
            self.parentApp.switchForm(None)
        else:
            pass

    # Export the current person's key. Notify the user, if this fails.
    def _export_key(self) -> None:
        current_user: User = self.visit_now.user

        if not current_user.current_key:
            npyscreen.notify_confirm("No key selected. Nothing to export.",
                                     "Export current key")
            return

        self.visit_now.value = \
                current_user.export_keys(current_user.current_key)
        self.visit_now.update()

    # Import the exported key in the current user's box. Notify whether this
    # operation was successful or not.
    def _import_key(self) -> None:
        user_import_keys: gnupg.ImportResult = \
                self.visit_now.user.import_keys(self.visit_now.value)

        if user_import_keys.returncode:
            npyscreen.notify_confirm(
                    "No key was exported. Exit status: {}.".format(
                        user_import_keys.returncode
                        ),
                    "Import Key"
                    )
            return

        npyscreen.notify_confirm(
                "Imported key: {}".format(user_import_keys.fingerprints[0]),
                "Import key"
                )

    # Set the box footer to its corresponding GPG status.
    def _set_box_footer(self, box) -> None:
        verified: None | gnupg.Verify = self._verify_detached_sign()

        if verified == None:
            return

        box.footer = "{}: {}".format(verified.status.title(), verified.key_id)
        box.update()

    # Set the box name before redrawing it.
    def _set_box_name(self, box) -> None:
        box.name = "{} ({})".format(box.user.name,
                                    box.user.current_key or "n/a")
        box.update()

    # Set the name and user of the box.
    def _set_box_user(self, box, user: User) -> None:
        box.user = user
        self._set_box_name(box)

    # Update `visit_previous` and `visit_now`.
    def _set_box_visit(self, next_visit) -> None:
        if not next_visit in [self.box_left, self.box_middle, self.box_right]:
            return

        self.visit_previous = self.visit_now
        self.visit_now = next_visit

    # Swap the users of two boxes.
    def _swap_box_users(self, box_1, box_2):
        user_1 = box_1.user

        self._set_box_user(box_1, box_2.user)
        self._set_box_user(box_2, user_1)

    # Return the detached signature verification by comparing the content of the
    # previous and current box. Return `None` if no signature is verified.
    def _verify_detached_sign(self) -> None | gnupg.Verify:
        if not self.visit_now in [self.box_middle, self.box_right]:
            return

        Lib.string_to_file(
                self.visit_previous.value,
                self.filepath_detached_sign_visit_previous
                )

        Lib.string_to_file(
                self.visit_now.value,
                self.filepath_detached_sign_visit_now
                )

        self.visit_previous.user.detach_sign(
                self.filepath_detached_sign_visit_previous
                )

        return self.visit_now.user.verify_detached_sign(
                self.filepath_detached_sign_visit_previous,
                self.filepath_detached_sign_visit_now
                )

    # Update the box footer and redraw the entire box.
    def adjust_widgets(self) -> None:
        # Potentially exit early to improve performance.
        if not self.visit_now in [self.box_middle, self.box_right]:
            return

        self._set_box_footer(self.visit_now)
        self.visit_now.update()

    # Create the boxes and menus. Define the left box to be this form's enty
    # point.
    def create(self) -> None:
        self._create_boxes()
        self._create_menus()
        self._create_users()

    # Clear the content from all fields on user confirmation.
    def on_cancel(self) -> None:
        if not npyscreen.notify_yes_no("Clear the content from all fields?",
                                       "Reset"):
            return

        self._clear_boxes()

    # Write a new message on user confirmation.
    def on_ok(self) -> None:
        if not npyscreen.notify_yes_no("Write a new message?", "New Message"):
            return

        self._clear_boxes()

    # Update the user pointers and initiate the control flow.
    def while_editing(self, next_visit) -> None:
        self._set_box_visit(next_visit)
        self._control_flow()
