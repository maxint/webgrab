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
import json


MD5 = hashlib.md5()
IMG_TAG_RE = re.compile(r'<img\s[^>]*src\s*=\s*"([^\'"]*)"[^>]*>')


def short_name(url):
    MD5.update(url)
    return MD5.hexdigest()


def down_image(url, dst, dry_run):
    import urllib
    if not os.path.exists(dst):
        print '[I] Downloading', url
        urllib.urlretrieve(url, dst)
    else:
        print '[W] Skip', url


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def extract_extension(url):
    _, ext = os.path.splitext(url)
    pos = ext.find('?')
    if pos == -1:
        pos = ext.find('&')
    return ext if pos == -1 else ext[:pos]


def convert_post(text, tag_re, dry_run, img_path_prefix):
    ftext = ''
    pos = 0
    images = dict()
    for m in tag_re.finditer(text):
        url = m.group(1).strip()
        span = m.span(1)
        ext = extract_extension(url) or '.jpg' # default is jpg
        if not url.startswith(img_path_prefix) and ext:
            img_name = short_name(url) + ext
            ftext += text[pos:span[0]]
            ftext += img_path_prefix + img_name
            pos = span[1]
            images[img_name] = url
        else:
            print '[W] Ignore URL', url
            images[os.path.basename(url)] = None

    if pos != 0:
        ftext += text[pos:]
    else:
        ftext = None
    return ftext, images


def down_in_post(src_html, img_dir, dry_run):
    img_path_prefix = os.path.basename(img_dir) + '/'
    with open(src_html, 'rt') as fp:
        print '=== Parsing', src_html
        text = fp.read()
        ftext, images = convert_post(text, IMG_TAG_RE, dry_run, img_path_prefix)
        if not dry_run and images:
            for img, url in images.iteritems():
                if url:
                    mkdirs(img_dir)
                    down_image(url, os.path.join(img_dir, img), dry_run)
        return ftext, images


def clean_unused_images(img_dir, all_images, dry_run):
    if not os.path.exists(img_dir):
        return

    import shutil
    # clean unused images
    for img in os.listdir(img_dir):
        if img not in all_images:
            print '[W] Remove unused image', img
            if not dry_run:
                os.remove(os.path.join(img_dir, img))
    if not dry_run:
        if len(os.listdir(img_dir)) == 0:
            print '[W] Remove empty directory', img_dir
            shutil.rmtree(img_dir)


def down(src, dst_dir=None, clean=True, dry_run=False):
    if os.path.isdir(src):
        src_dir = src
        import glob
        src_htmls = glob.glob(os.path.join(src_dir, '*.html'))
    else:
        src_dir = os.path.dirname(src)
        src_htmls = [src]

    if dst_dir is None:
        dst_dir = src_dir

    img_dir = os.path.join(dst_dir, 'images')
    img_js = os.path.join(dst_dir, 'images.js')
    try:
        exists_images = json.load(open(img_js))
    except:
        exists_images = dict()
    all_images = dict()
    for src_html in src_htmls:
        ftext, images = down_in_post(src_html, img_dir, dry_run)
        all_images.update(images)
        if not dry_run and ftext:
            mkdirs(dst_dir)
            dst_html = os.path.join(dst_dir, os.path.basename(src_html))
            print '[I] Writing to', dst_html
            with open(dst_html, 'wt') as fp:
                fp.write(ftext)

    if clean and os.path.isdir(src):
        clean_unused_images(img_dir, all_images.keys(), dry_run)
        for k in exists_images.keys():
            if k not in all_images:
                exists_images.pop(k)

    all_images.update(exists_images)
    json.dump(all_images, open(img_js, 'w'), indent=2)

    print 'Done!'

if __name__ == '__main__':
    import argparse

    class readable(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            path = values
            if not os.path.exists(path):
                msg = '{0} is not a valid path'.format(path)
                parser.error(msg)
            if not os.access(path, os.R_OK):
                msg = '{0} is not a readable path'.format(path)
                parser.error(msg)
            setattr(namespace, self.dest, path)

    parser = argparse.ArgumentParser(description='Download images in <img>')
    parser.add_argument('source', nargs='?', default='posts',
                        action=readable,
                        help='source directory with HTML files or single HTML file (default is "posts")')
    parser.add_argument('--target', '-t', nargs='?', default=None,
                        help='directory to save final HTML files and images')
    parser.add_argument('--dry_run', '-D', action='store_true',
                        help='Do not save result')
    parser.add_argument('--no-clean', '-n', dest='no_clean',
                        action='store_true',
                        help='Do not remove unused images')

    args = parser.parse_args()

    down(args.source, args.target, not args.no_clean, args.dry_run)

    os.system('pause')
