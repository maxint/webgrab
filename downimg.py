#! /usr/bin/env python2
# coding:utf-8
# Copyright (C) 2014 maxint <NOT_SPAM_lnychina@gmail.com>
# Distributed under terms of the MIT license.

"""
Download images in <img> to local "images" directory.
"""

import re
import hashlib
import os

MD5 = hashlib.md5()


def shortname(url):
    MD5.update(url)
    return MD5.hexdigest()


def down_image(url, dst, dryrun):
    import urllib
    if not os.path.exists(dst):
        print '[I] Downloading', url
        urllib.urlretrieve(url, dst)
    else:
        print '[W] Skip', url


def mkdirs(path):
    if not os.path.exists(path):
        os.mkdirs(path)


def down_post(srchtml, imgdir, dryrun):
    with open(srchtml, 'rt') as fp:
        print '=== Parsing', srchtml
        text = fp.read()
        ftext = ''
        pos = 0
        images = []
        for m in re.finditer(r'<img[^>]*src\s*=\s*"([^\'"]*)"[^>]*>', text):
            url = m.group(1).strip()
            span = m.regs[1]
            _, ext = os.path.splitext(url)
            if not url.startswith('images/') and ext:
                imgname = shortname(url) + ext
                dst = os.path.join(imgdir, imgname)
                down_image(url, dst, dryrun)
                ftext += 'images/' + imgname
                ftext += text[pos:span[0]]
                pos = span[1]
                images.append(imgname)
            else:
                print '[W] Skip image', url
                images.append(os.path.basename(url))

        if pos != 0:
            ftext += text[pos:]
        else:
            ftext = None
        return ftext, images

    return None, None


def clean_unused_images(imgdir, allimages, dryrun):
    import shutil
    # clean unused images
    for img in os.listdir(imgdir):
        if img not in allimages:
            print '[W] Remove unused image', img
            if not dryrun:
                shutil.remove(img)
    if not dryrun:
        if len(os.listdir(imgdir)) == 0:
            print '[W] Remove empty directory', imgdir
            shutil.rmtree(imgdir)


def down_dir(srcdir, dstdir=None, clean=True, dryrun=False):
    if dstdir is None:
        dstdir = srcdir

    import glob
    imgdir = os.path.join(dstdir, 'images')
    allimages = []
    for srchtml in glob.glob(os.path.join(srcdir, '*.html')):
        if not dryrun:
            mkdirs(imgdir)
        ftext, images = down_post(srchtml, imgdir, dryrun)
        allimages += images or []
        if not dryrun and ftext:
            mkdirs(dstdir)
            dsthtml = os.path.join(dstdir, os.path.basename(srchtml))
            print '[I] Writing to', dsthtml
            with open(dsthtml, 'wt') as fp:
                fp.write(ftext)

    if clean:
        clean_unused_images(imgdir, set(allimages), dryrun)

    print 'Done!'

if __name__ == '__main__':
    import argparse

    def readable_dir(path):
        if not os.path.isdir(path):
            msg = '{0} is not a valid directory'.format(path)
            raise argparse.ArgumentTypeError(msg)
        if not os.access(path, os.R_OK):
            msg = '{0} is not a readable directory'.format(path)
            raise argparse.argumenttypeerror(msg)
        return path

    parser = argparse.ArgumentParser(description='Download images in <img>')
    parser.add_argument('source', nargs='?', default='posts',
                        type=readable_dir,
                        help='source directory with HTML files')
    parser.add_argument('--target', '-t', nargs='?', default=None,
                        help='directory to save final HTML files and images')
    parser.add_argument('--dryrun', '-D', action='store_true',
                        help='Do not save result')
    parser.add_argument('--no-clean', '-n', dest='no_clean',
                        action='store_true',
                        help='Do not remove unused images')

    args = parser.parse_args()

    down_dir(args.source, args.target, not args.no_clean, args.dryrun)

    os.system('pause')
