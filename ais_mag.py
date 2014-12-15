#! /usr/bin/env python
# coding:utf-8
# Copyright (C) 2014 maxint <NOT_SPAM_lnychina@gmail.com>
# Distributed under terms of the MIT license.

"""
Generate HTML posts from XLSX file.
"""

import xlrd
import os
import sys


def read_excel(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_index(0)
    posts = dict()
    for i in range(table.nrows):
        row = table.row_values(i)
        if len(row) == 4 and all(row):
            category = row[0].strip()
            if category not in posts:
                posts[category] = list()
            posts[category].append(dict(date=int(row[1]),
                                        title=row[2].strip(),
                                        url=row[3].strip()))

    return posts


def save_json(filename, obj):
    import json
    with open(filename, 'wt') as fp:
        fp.write(json.dumps(obj, indent=4))


def mkdirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def makepost(filename, post):
    if os.path.exists(filename):
        return

    with open(filename, 'wt') as fp:
        fp.write('''<!DOCTYPE html>
<html>
    <head>
    <meta charset="utf-8" />
    <title>{0}</title>
    </head>
    <body>
        <iframe width="100%" height="800px" src="{1}" />
    </body>
</html>'''.format(post["title"].encode('utf-8'),
                  post["url"].encode('utf-8')))


def main(xlsfilename):
    mag = read_excel(xlsfilename)
    dstdir = os.path.dirname(xlsfilename)

    # format data
    categories = dict()
    count = 0
    posts = list()
    for k, v in mag.iteritems():
        categories[k] = dict(start=count,
                             end=count + len(v))
        count += len(v)
        posts += v
    mag = dict(categories=categories,
               posts=posts)

    postdir = os.path.join(dstdir, 'posts')
    mkdirs(postdir)
    for i, post in enumerate(posts):
        postpath = os.path.join(postdir, str(i) + '.html')
        percent = (i+1) * 100 / len(posts)
        msg = '\r[I] Generating posts ... [{}%]'.format(percent)
        sys.stdout.write(msg)
        sys.stdout.flush()
        makepost(postpath, post)

    jsonpath = os.path.join(dstdir, 'mag.json')
    print ''
    print '[I] Generating', jsonpath
    save_json(jsonpath, mag)

    print 'Done!'


if __name__ == '__main__':
    import argparse

    class readable_file(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            path = values
            if path is None:
                import glob
                files = glob.glob('*.xls*')
                files = filter(lambda x: not x.startswith('~'), files)
                if len(files) == 1:
                    path = files[0]
                else:
                    msg = 'Can not find single Excel file in current directory'
                    parser.error(msg)
            elif not os.path.exists(path):
                msg = '{0} is not a valid file'.format(path)
                raise parser.error(msg)
            setattr(namespace, self.dest, path)

    parser = argparse.ArgumentParser(description='Generate posts')
    parser.add_argument('xlsfile', nargs='?', default=None,
                        action=readable_file,
                        help='Excel file to read post list')

    args = parser.parse_args()
    main(args.xlsfile)

    os.system('pause')
