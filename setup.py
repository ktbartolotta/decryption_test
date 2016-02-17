import cx_Freeze as freeze

freeze.setup(
    name="Crypt_Util",
    version="0.1",
    description="GUI based decryption and encryption utility.",
    executables=[
        freeze.Executable("crypt_util_ui.py", base='Win32GUI')
    ]
)
