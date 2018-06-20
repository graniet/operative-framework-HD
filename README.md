<img src="https://image.ibb.co/fuPpQd/logo_operative.png" width="450">

**operative framework HD** is the digital investigation framework, you can interact with websites, email address, company, people, ip address ... with basic/graphical view and export with XML, JSON

[![operative framework HD](https://image.ibb.co/cKnzKo/preview_operative_framework.png)](https://www.youtube.com/watch?v=WskQM0JL6Rw)

## How to Install

You need this packages
+ mongoDB
+ NPM
+ Python 2

#### Create mongoDB database 
```
$ mongo
$ use operative_framework
$ db.createUser({user: 'operative', pwd:'operative', roles: [ "readWrite", "dbAdmin" ]})
```
For security restart now mongoDB with --auth argument

#### Install manually a operative framework HD
```
$ sudo pip install -r requirements.txt
$ sudo python framework/load_modules.py
$ cd client
$ npm install
$ cd ..
$ cd bin
$ sudo ./opf_users
$ create operative mypass
$ cd ..
open two shell
1) $ sudo python framework/app.py
2) $ cd client && npm start
```

#### Install globally a operative framework HD
```
$ git clone https://github.com/graniet/operative-framework-HD.git
$ cd operative-framework-HD
$ chmod +x install.sh
$ ./install.sh
$ cd framework
$ python load_modules.py 
```

#### create first user
```
$ sudo opf_users
opf_users > create operative Op3r4tIv3P$$SS
```

#### run operative framework without console
first shell:
```
$ sudo opf_server
```
second shell:
```
$ sudo opf_client
```

#### run operative framework with console
```
$ sudo opf_console
$ opf_console > run_server
$ opf_console > run_client
```
