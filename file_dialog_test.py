import Tkinter
import tkFileDialog
import tkMessageBox
import crypt_util
import os


class Application(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        self.source_path = Tkinter.StringVar()
        self.target_path = Tkinter.StringVar()
        self.crypt_mode = Tkinter.IntVar()
        self.target_mode = Tkinter.IntVar()
        self.password = Tkinter.StringVar()

        crypt_group = Tkinter.LabelFrame(
            self, text='Cryptographic Mode', padx=5, pady=5)
        crypt_group.pack(padx=5, pady=5, fill=Tkinter.X)

        Tkinter.Radiobutton(
            crypt_group, text='Encrypt', variable=self.crypt_mode,
            value=1).pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(
            crypt_group, text='Decrypt', variable=self.crypt_mode,
            value=2).pack(side=Tkinter.LEFT)

        target_group = Tkinter.LabelFrame(
            self, text='Target a file or directory', padx=5, pady=5)
        target_group.pack(padx=5, pady=5, fill=Tkinter.X)

        Tkinter.Radiobutton(
            target_group, text='File', variable=self.target_mode,
            value=1, command=self.get_file_mode).pack(side=Tkinter.LEFT)
        Tkinter.Radiobutton(
            target_group, text='Directory', variable=self.target_mode,
            value=2, command=self.get_dir_mode).pack(side=Tkinter.LEFT)

        self.picker_container = Tkinter.Frame(self)
        self.picker_container.pack(fill=Tkinter.X)
        self.target_picker_group = Tkinter.Frame(self.picker_container)
        self.target_picker_group.pack()

        pwd_group = Tkinter.Frame(self, padx=5, pady=5)
        pwd_group.pack(fill=Tkinter.X)
        Tkinter.Label(pwd_group, text='Password:').pack(
            padx=5, pady=5, side=Tkinter.LEFT)
        Tkinter.Entry(pwd_group, textvariable=self.password).pack(
            padx=5, pady=5, fill=Tkinter.X, side=Tkinter.LEFT)

        self.control_group = Tkinter.Frame(self)
        self.control_group.pack()
        Tkinter.Button(
            self.control_group, text='OK', command=self.process_crypt).pack(
                padx=10, pady=5, side=Tkinter.LEFT)
        Tkinter.Button(
            self.control_group, text='Quit', command=self.quit).pack(
                padx=10, pady=5, side=Tkinter.LEFT)

        self.file_options = {
            'filetypes': [('all files', '.*')],
            'initialdir': '..\\',
            'parent': root,
            'title': 'The title'
        }

        self.dir_options = {
            'initialdir': '..\\',
            'parent': root,
            'title': 'The title'
        }

    def get_file_mode(self):

        self.target_picker_group.destroy()
        self.target_path.set('')
        self.source_path.set('')
        self.target_picker_group = Tkinter.LabelFrame(
            self.picker_container, text='Pick file')
        self.target_picker_group.pack(padx=5, pady=5, fill=Tkinter.X)

        source_group = Tkinter.Frame(self.target_picker_group)
        source_group.pack(fill=Tkinter.X)
        Tkinter.Label(
            source_group, text='Source',
            textvariable=self.source_path).pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)
        Tkinter.Label(
            source_group, text='',
            textvariable=self.source_path, bg='white').pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)
        Tkinter.Button(
            source_group, text='Browse',
            command=self.ask_source_filename).pack(
                side=Tkinter.LEFT, padx=5, pady=5)

        target_group = Tkinter.Frame(self.target_picker_group)
        target_group.pack(fill=Tkinter.X)
        Tkinter.Label(
            target_group, text='Target',
            textvariable=self.target_path).pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)
        Tkinter.Label(
            target_group, text='',
            textvariable=self.target_path, bg='white').pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)
        Tkinter.Button(
            target_group, text='Browse',
            command=self.ask_target_directory).pack(
                side=Tkinter.LEFT, padx=5, pady=5)

    def get_dir_mode(self):

        self.target_picker_group.destroy()
        self.target_path.set('')
        self.source_path.set('')
        self.target_picker_group = Tkinter.LabelFrame(
            self.picker_container, text='Pick directory')
        self.target_picker_group.pack(padx=5, pady=5, fill=Tkinter.X)

        source_group = Tkinter.Frame(self.target_picker_group)
        source_group.pack(fill=Tkinter.X)
        Tkinter.Button(
            source_group, text='source',
            command=self.ask_source_directory).pack(
                side=Tkinter.LEFT, padx=5, pady=5)
        Tkinter.Label(
            source_group, text='',
            textvariable=self.source_path, bg='white').pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)

        target_group = Tkinter.Frame(self.target_picker_group)
        target_group.pack(fill=Tkinter.X)
        Tkinter.Button(
            target_group, text='target',
            command=self.ask_target_directory).pack(
                side=Tkinter.LEFT, padx=5, pady=5)
        Tkinter.Label(
            target_group, text='',
            textvariable=self.target_path, bg='white').pack(
                side=Tkinter.LEFT, fill=Tkinter.X, padx=5, pady=5)

    def ask_target_directory(self):

        self.target_path.set(tkFileDialog.askdirectory(**self.dir_options))

    def ask_source_directory(self):

        self.source_path.set(tkFileDialog.askdirectory(**self.dir_options))

    def ask_target_filename(self):

        self.target_path.set(tkFileDialog.askopenfilename(**self.file_options))

    def ask_source_filename(self):

        self.source_path.set(tkFileDialog.askopenfilename(**self.file_options))

    def quit(self):

        self.master.destroy()

    def process_crypt(self):
        if self.password.get().strip() == '':
            tkMessageBox.showwarning(
                    'Password?', 'You need to specify a Password.')
            return
        if (os.path.isdir(self.source_path.get()) or (
                    os.path.isfile(self.source_path.get()) and (
                        os.path.isdir(self.target_path.get())))):

            if self.crypt_mode.get() == 1:

                if self.target_mode.get() == 1:
                    target_file = '.'.join(
                        [os.path.split(self.source_path.get())[1], 'enc'])
                    target_path = os.path.join(
                        self.target_path.get(), target_file)
                    crypt_util.encrypt_file(
                        self.source_path.get(),
                        target_path, self.password.get())
                elif self.target_mode.get() == 2:
                    crypt_util.encrypt_directory(
                        self.source_path.get(),
                        self.target_path.get(),
                        self.password.get())

                tkMessageBox.showwarning(
                    'Success!', 'Encryption complete.')

            elif self.crypt_mode.get() == 2:

                if self.target_mode.get() == 1:
                    target_file = os.path.split(self.source_path.get())[1][:-4]
                    target_path = os.path.join(
                        self.target_path.get(), target_file)
                    crypt_util.decrypt_file(
                        self.source_path.get(),
                        target_path, self.password.get())
                elif self.target_mode.get() == 2:
                    crypt_util.decrypt_directory(
                        self.source_path.get(),
                        self.target_path.get(),
                        self.password.get())

                tkMessageBox.showwarning(
                    'Success!', 'Decryption complete.')
            else:

                tkMessageBox.showwarning(
                    'Crypto?', 'You need to specify "Encrypt" or "Decrypt".')
        else:
            tkMessageBox.showwarning(
                'Files?', '''You need to specify source file or directory
                                  and a target directory.''')


if __name__ == '__main__':

    root = Tkinter.Tk()
    Application(root).pack()
    root.mainloop()
