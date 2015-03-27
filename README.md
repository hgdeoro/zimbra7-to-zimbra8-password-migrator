Simple script to migrate passwords from Zimbra 7 to Zimbra 8


Based on:
- http://wiki.zimbra.com/wiki/ShanxT-LDAP-CheatSheet
- http://wiki.zimbra.com/wiki/Setting_zimbra_admin_password_in_LDAP
- http://www.openldap.org/faq/data/cache/347.html
- http://wiki.zimbra.com/wiki/Integrating_PWM_password_manager_with_Zimbra
- https://wiki.zimbra.com/wiki/UNIX_and_Windows_Accounts_in_Zimbra_LDAP_and_Zimbra_Admin_UI
- http://www.math.ucla.edu/~jimc/documents/pimstuff/zimbra.txt


# On Zimbra 7 host:

### Load Zimbra settings / environment variables

    root@zimbra7~$ sudo -u zimbra -i
    zimbra@zimbra7~$ source ~/bin/zmshutil
    zimbra@zimbra7~$ zmsetvars

### Dump account & password hashes:

    zimbra@zimbra7~$ ldapsearch -o ldif-wrap=no -x -H $ldap_master_url \
        -D $zimbra_ldap_userdn -w $zimbra_ldap_password -LLL \
        '(&(objectClass=zimbraAccount)(ou:dn:=people))' \
        dn displayName zimbraMailStatus zimbraMailDeliveryAddress \
        mail userPassword > /dev/shm/dump-zimbra-7.ldif

### Generate the LDIF file:

    zimbra@zimbra7~$ python generate_ldap_diff.py /dev/shm/dump-zimbra-7.ldif > /dev/shm/dump-zimbra-8.ldif 

### Copy the LDIF file to the Zimbra 8 server:

    zimbra@zimbra7~$ scp /dev/shm/dump-zimbra-8.ldif user@zimbra8:/dev/shm

# On Zimbra 8 host, execute:

### Load Zimbra settings / environment variables

    root@zimbra8~$ sudo -u zimbra -i
    zimbra@zimbra8~$ source ~/bin/zmshutil
    zimbra@zimbra8~$ zmsetvars

### Update the passwords:

    zimbra@zimbra8~$ ldapmodify -v -x \
        -H $ldap_master_url \
        -D $zimbra_ldap_userdn \
        -w $zimbra_ldap_password -c -f /dev/shm/dump-zimbra-8.ldif

# Cleanup

After execution, remember to delete the ldif files on both servers!
