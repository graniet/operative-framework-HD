#### opf_users

+ **:list**  =>  list user registered

exemple:

```
username: graniet right: Administrator app_id: APP_KNIRKO4J
username: operative right: Administrator app_id: APP_2H61T1TQ
```

+ **create** => create new user with new app_i

exemple:
```
bin/opf_users.py > create test testpass
[2018-06-21 21:51:02] SUCCESS User as successfully added
```

+ **add** => add user to app_id

exemple:

```
bin/opf_users.py > add test2 tst APP_FGKA79KM
[2018-06-21 21:52:01] SUCCESS User as successfully added to app_id: 'APP_FGKA79KM'!
```

+ **delete** => delete user from app_id

exemple:

```
bin/opf_users.py > delete test2 APP_FGKA79KM
[2018-06-21 21:53:15] SUCCESS User as successfully deleted from app_id: 'APP_FGKA79KM'!
```

