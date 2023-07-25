#!/usr/bin/env python

# The `App` class is a framework which starts and ends the application by
# managing its forms.

import npyscreen

from communication import Communication
from manage_pgp_keys import ManagePGPKeys

class App(npyscreen.NPSAppManaged):
    npyscreen.NPSAppManaged.STARTING_FORM = "communication"

    # Add forms to the application.
    def onStart(self) -> None:
        self.communication = self.addForm(npyscreen.NPSAppManaged.STARTING_FORM,
                                          Communication,
                                          name = "Communication")

        self.manage_pgp_keys = self.addForm("manage_pgp_keys", ManagePGPKeys,
                                            name = "Manage PGP Keys")
