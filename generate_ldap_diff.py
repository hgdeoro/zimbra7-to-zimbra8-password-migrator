# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import base64
import fileinput
import re


SPLITTER = re.compile(r'\s*:+\s*')

"""
For information and instructions, see the README.md file
"""


def generate_dict(current_object_lines):
    splitted = [SPLITTER.split(line) for line in current_object_lines]
    return dict(splitted)


def generate_dict_objects_from_files():
    dict_objects = []
    current_object_lines = []

    # Iterate all the lines
    for line in fileinput.input():
        line = line.strip()
        if line:
            current_object_lines.append(line)
        else:
            if current_object_lines:
                a_dict_object = generate_dict(current_object_lines)
                dict_objects.append(a_dict_object)
                current_object_lines = []

    # Process last lines
    if current_object_lines:
        a_dict_object = generate_dict(current_object_lines)
        dict_objects.append(a_dict_object)
        current_object_lines = []

    return dict_objects


def generate_ldif(dict_objects):
    erroneous_obj = []
    for obj in dict_objects:
        if 'userPassword' not in obj:
            erroneous_obj.append(obj)
            continue

        dn = obj['dn'].strip()
        user_password = base64.b64decode(obj['userPassword'].strip())

        print "# UPDATE {}".format(dn)
        print "dn: {}".format(obj['dn'])
        print "changetype: modify"
        print "replace: userPassword"
        print "userPassword: {}".format(user_password)
        print "-"
        print ""

    for err_obj in erroneous_obj:
        print "# ----- ERROR ----- The flowing object was ignored:"
        for k, v in err_obj.iteritems():
            print "#   {}: {}".format(k, v)


def main():
    dict_objects = generate_dict_objects_from_files()
    print "# {} object found".format(len(dict_objects))
    generate_ldif(dict_objects)


if __name__ == '__main__':
    main()
