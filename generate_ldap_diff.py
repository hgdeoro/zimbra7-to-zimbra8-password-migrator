# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import base64
import fileinput
import pprint
import re


"""

# Based on:
#  - http://wiki.zimbra.com/wiki/ShanxT-LDAP-CheatSheet
#  - http://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP
#  - http://www.openldap.org/faq/data/cache/347.html
#  - http://wiki.zimbra.com/wiki/Integrating_PWM_password_manager_with_Zimbra
#  - https://wiki.zimbra.com/wiki/UNIX_and_Windows_Accounts_in_Zimbra_LDAP_and_Zimbra_Admin_UI
#  - http://www.math.ucla.edu/~jimc/documents/pimstuff/zimbra.txt


On Zimbra 7 host, execute:

    root@zimbra7~$ sudo -u zimbra -i
    zimbra@zimbra7~$ source ~/bin/zmshutil
    zimbra@zimbra7~$ zmsetvars

    zimbra@zimbra7~$ ldapsearch -o ldif-wrap=no -x -H $ldap_master_url \
        -D $zimbra_ldap_userdn -w $zimbra_ldap_password -LLL \
        '(&(objectClass=zimbraAccount)(ou:dn:=people))' \
        dn displayName zimbraMailStatus zimbraMailDeliveryAddress \
        mail userPassword > /dev/shm/dump-zimbra-7.ldif

    zimbra@zimbra7~$ python generate_ldap_diff.py /dev/shm/dump-zimbra-7.ldif > /dev/shm/dump-zimbra-8.ldif 

    zimbra@zimbra7~$ scp /dev/shm/dump-zimbra-8.ldif user@zimbra8:/dev/shm

On Zimbra 8 host, execute:

    root@zimbra8~$ sudo -u zimbra -i
    zimbra@zimbra8~$ source ~/bin/zmshutil
    zimbra@zimbra8~$ zmsetvars

    zimbra@zimbra8~$ ldapmodify -v -x \
        -H $ldap_master_url \
        -D $zimbra_ldap_userdn \
        -w $zimbra_ldap_password -c -f /dev/shm/dump-zimbra-8.ldif


"""

SPLITTER = re.compile(r'\s*:+\s*')


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
