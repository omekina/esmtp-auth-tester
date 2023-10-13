# ESMTP AUTH tester
```
user@something$ python .
Enter SMTP server hostname (example: smtp.test.com): smtp.test.nothing
Enter your username (e-mail): user@test.nothing
Enter your password: 
==========CERT DUMP==============
{   'OCSP': ('_________',),
    'caIssuers': ('____________',),
    'issuer': (   (('countryName', 'US'),),
                  (('organizationName', "Let's Encrypt"),),
                  (('commonName', 'R3'),)),
    'notAfter': '_______________',
    'notBefore': '________________',
    'serialNumber': '____________________________________',
    'subject': ((('commonName', '*.test.nothing'),),),
    'subjectAltName': (('DNS', '*.test.nothing'),),
    'version': 3}
==========END CERT DUMP==========
Trust (y/N)? y
-> Connected
<- Server name: ESMTP Postfix
-> Sent hello
<- Got info
-> Sent username
<- Ok
-> Sent password
<- Ok
Info: Authentication done
```
