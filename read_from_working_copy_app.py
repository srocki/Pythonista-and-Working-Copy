#!/usr/bin/env python3
# coding: utf-8

# Appex script to copy a git file, folder, or repo from the Working Copy app

import appex
import os
import shutil
import zipfile
import datetime

from_wc = os.path.abspath(os.path.expanduser('~/Documents'))
# print("from_wc: " + from_wc)


def main():
    if appex.is_running_extension():
        file_paths = appex.get_file_paths()
        assert len(file_paths) == 1, 'Invalid file paths: {}'.format(file_paths)
        srce_path = file_paths[0]
        print(file_paths)
        pathSplitter = ''
        if '/tmp/' in srce_path:
            pathSplitter = '/tmp/'
        else:
            if '/File Provider Storage/Repositories/' in srce_path:
                pathSplitter = '/File Provider Storage/Repositories/'
            else:
                if '/File Provider Storage/' in srce_path:
                    pathSplitter = '/File Provider Storage/'
                else:
                    pathSplitter = '/Repositories/'
        dest_path = srce_path.split(pathSplitter)[-1]
        if srce_path.endswith('.zip'):
            foldername = srce_path.split('/')[-1].replace('.zip', '')
            print('Got me a zip file')
            zf = zipfile.ZipFile(srce_path)
            for info in zf.infolist():
                # print (info.filename)
                newfile = zf.extract(info)
                newfilename = newfile.split('/')[-1]
                file_path = from_wc + '/' + foldername
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                dest_path = file_path + '/' + newfilename
                # print('Copy [' + newfile + '] to [' + dest_path + ']')
                print(shutil.move(newfile, dest_path))
                shutil
        else:
            # print(dest_path)
            dest_path = os.path.join(from_wc, dest_path)
            # print(dest_path)
            file_path, file_name = os.path.split(dest_path)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            if os.path.isdir(srce_path):
                shutil.rmtree(dest_path, ignore_errors=True)
                print(shutil.copytree(srce_path, dest_path))
            else:
                print(shutil.copy2(srce_path, dest_path))
            print('{} was copied to {}'.format(file_name, file_path))
    else:
        print('''* In Working Copy app select a repo, file, or directory to be
copied into Pythonista.  Click the Share icon at the upperight.  Click Run
Pythonista Script.  Pick this script and click the run button.  When you return
to Pythonista the files should be in the 'from Working Copy'
directory.'''.replace('\n', ' ').replace('.  ', '.\n* '))

if __name__ == '__main__':
    main()
    
