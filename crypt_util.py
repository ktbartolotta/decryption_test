import os
import hashlib
import argparse
import getpass
import logging

from Crypto.Cipher import AES
from Crypto import Random


logging.basicConfig(
    filename='status.log',
    format='%(asctime)s %(message)s',
    level=logging.INFO)


def pad(data_str):

    return data_str + (16 - len(data_str) % 16) * chr(16 - len(data_str) % 16)


def unpad(data_str):

    return data_str[0:-ord(data_str[-1])]


def decrypt_message(msg, pwd):

    try:
        iv = msg[16:32]
        salt = msg[:16]
        dk = hashlib.pbkdf2_hmac('sha1', pwd, salt, 65536, 16)
        enc_obj = AES.new(dk, AES.MODE_CBC, iv)
        return unpad(enc_obj.decrypt(msg[32:]))
    except Exception, e:
        logging.error(e)


def decrypt_file(in_file_path, out_file_path, pwd):

    try:
        with open(in_file_path, 'rb') as input:
            with open(out_file_path, 'wb') as output:
                salt = input.read(16)
                iv = input.read(16)
                key = hashlib.pbkdf2_hmac('sha1', pwd, salt, 65536, 16)

                block1 = input.read(16)
                block2 = input.read(16)

                dec_obj = AES.new(key, AES.MODE_CBC, iv)
                content = dec_obj.decrypt(block1)
                if block2 == '':
                    output.write(unpad(content))
                else:
                    output.write(content)
                    while True:

                        iv = block1
                        block1 = block2
                        block2 = input.read(16)
                        dec_obj = AES.new(key, AES.MODE_CBC, iv)
                        content = dec_obj.decrypt(block1)
                        if block2 != '':
                            output.write(content)
                        else:
                            output.write(unpad(content))
                            break
    except Exception, e:
        logging.error('%s %s' % (os.path.abspath(in_file_path), e))


def decrypt_directory(in_dir_path, out_dir_path, pwd):

    try:
        if not os.path.isdir(out_dir_path):
            os.mkdir(out_dir_path)
        for root, dirs, files in os.walk(in_dir_path):
            dir_path = os.sep.join(
                [out_dir_path, root.replace(in_dir_path, '')])
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            for f in files:
                decrypt_file(
                    os.path.join(root, f),
                    os.path.join(dir_path, f)[:-4],
                    pwd)
    except Exception, e:
        raise e


def encrypt_message(msg, pwd):

    try:
        iv = Random.new().read(AES.block_size)
        salt = Random.new().read(AES.block_size)
        dk = hashlib.pbkdf2_hmac('sha1', pwd, salt, 65536, 16)
        enc_obj = AES.new(dk, AES.MODE_CBC, iv)
        return salt + iv + enc_obj.encrypt(pad(msg))
    except Exception, e:
        logging.error(e)


def encrypt_file(in_file_path, out_file_path, pwd):

    try:
        with open(in_file_path, 'rb') as input:
            with open(out_file_path, 'wb') as output:
                output.write(
                    encrypt_message(input.read(), pwd))
    except Exception, e:
        logging.error('%s %s' % (os.path.abspath(in_file_path), e))


def encrypt_directory(in_dir_path, out_dir_path, pwd):

    try:
        if not os.path.isdir(out_dir_path):
            os.mkdir(out_dir_path)
        for root, dirs, files in os.walk(in_dir_path):
            dir_path = os.sep.join(
                [out_dir_path, root.replace(in_dir_path, '')])
            if not os.path.isdir(dir_path):
                os.mkdir(dir_path)
            for f in files:
                encrypt_file(
                    os.path.join(root, f),
                    '.'.join([os.path.join(dir_path, f), 'enc']),
                    pwd)
    except Exception, e:
        raise e


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '-d', '--dir',
        help='''Recursively decrypt all files in directory SOURCE and
                place in directory TARGET.''',
        nargs=2, metavar=('SOURCE', 'TARGET'))
    group.add_argument(
        '-f', '--file',
        help='Decrypt file SOURCE and place in TARGET.', nargs=2,
        metavar=('SOURCE', 'TARGET'))
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument(
        '--encrypt',
        help='Flag on for encrypt mode.',
        action='store_true')
    group2.add_argument(
        '--decrypt',
        help='Flag on for decrypt mode.',
        action='store_true')
    args = parser.parse_args()

    password = getpass.getpass('Secret Key: ')

    try:
        if args.encrypt:
            logging.info('Begin encryption.')
            if args.file:
                encrypt_file(args.file[0], args.file[1], password)
            elif args.dir:
                encrypt_directory(args.dir[0], args.dir[1], password)
            else:
                logging.warning('You for got to indicate file or directory.')
            logging.info('End encryption.')
        elif args.decrypt:
            logging.info('Begin decryption.')
            if args.file:
                decrypt_file(args.file[0], args.file[1], password)
            elif args.dir:
                decrypt_directory(args.dir[0], args.dir[1], password)
            else:
                logging.warning('You forgot to indicate file or directory.')
            logging.info('End decryption.')
        else:
            logging.warning('Decrypt or encrypt?')
    except Exception, e:
        logging.error(e)
