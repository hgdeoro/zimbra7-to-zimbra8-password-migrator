# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import fileinput
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
        mail userPassword > /dev/shm/dump.ldif

"""

SPLITTER = re.compile(r':+')


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
            a_dict_object = generate_dict(current_object_lines)
            dict_objects.append(a_dict_object)
            current_object_lines = []

    # Process last lines
    if current_object_lines:
        a_dict_object = generate_dict(current_object_lines)
        dict_objects.append(a_dict_object)
        current_object_lines = []

    return dict_objects


def main():
    dict_objects = generate_dict_objects_from_files()
    print "{} object found".format(len(dict_objects))
    import pprint
    pprint.pprint(dict_objects)


if __name__ == '__main__':
    main()
