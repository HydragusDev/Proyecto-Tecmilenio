# Proyecto Biblioteca
librarby

This project is a Windows-based library management system designed for managing books, users, loans, and employee access.

## Overview

The program allows users to:
- register and log in
- browse available books
- request loans
- manage returns
- access different menus depending on their role

It is designed primarily for Windows, although it may work on other operating systems with minor adjustments.

## Database location

On first run, the program creates an SQLite database in the user profile folder:

C:\Users\Username\AppData\Roaming\Proyecto-Tecmilenio\bitacora.db

(Note: it loads into yours specific user folder rather than "Username" itself)

This database stores the program's data locally for each user account and system.

To open the folder quickly on Windows:

Windows + R then type %appdata%\Proyecto-Tecmilenio

For user convenience, a shortcut directing to the location of the current user's database within the appdata folder is included.

To reset the program data, delete this folder. The application will recreate it automatically on the next run.

## Packaging into an executable

The application was bundled into a standalone Windows executable using PyInstaller with the following command:

pyinstaller --onefile --console --collect-all pyfiglet main.py

This is necessary because `pyfiglet` loads its font files at runtime, and those files must be included when packaging the application into a single `.exe` file. Without this option, the ASCII art may not render correctly in the compiled executable.

## Notes

- The program stores user-specific data in the AppData folder.
- It is intended as a proof-of-concept / educational project.
- Currently, any user can choose to register as a regular user or an employee.
- Some features are still unimplemented and may be expanded in future versions.

## Future improvements

Planned enhancements include:
- admin setup on first run
- employee whitelist management
- more advanced user and loan administration
- improved security and permissions

## License

Proyecto Tecmilenio-main  © 1999 by Jorge Martínez Blanco and Enrique Castro is licensed under CC BY-NC-SA 4.0. To view a copy of this license, visit https://creativecommons.org/licenses/by-nc-sa/4.0/
