<img src="https://image.ibb.co/fuPpQd/logo_operative.png" width="450">

**operative framework HD** is the digital investigation framework, you can interact with websites, email address, company, people, ip address ... with basic/graphical view and export with XML, JSON

[![operative framework HD](https://image.ibb.co/cKnzKo/preview_operative_framework.png)](https://www.youtube.com/watch?v=WskQM0JL6Rw)

## How to Install

You need this packages
+ mongoDB
+ Node & NPM
+ Python

#### Create mongoDB database 
```
$ mongo
$ use operative_framework
$ db.createUser({user: 'operative', pwd:'operative', roles: [ "readWrite", "dbAdmin" ]})
```
For security restart now mongoDB with --auth argument


#### Install globally a operative framework HD
```
$ apt-get install nodejs
$ git clone https://github.com/graniet/operative-framework-HD.git
$ cd operative-framework-HD
$ chmod +x install.sh
$ ./install.sh
$ cd client/ && npm install && npm start
$ cd framework/ && python load_modules.py && cd ../
```


#### Or install manually a operative framework HD
```
$ sudo pip install -r requirements.txt
$ sudo python framework/load_modules.py
$ cd client
$ npm install
$ cd ..
$ cd bin
$ sudo ./opf_users.py
$ create operative mypass
$ cd ..
$ cd framework/
$ python load_modules.py
$ cd ..
open two shell
1) $ sudo python framework/app.py
2) $ cd client && npm start
```

#### create first user
```
$ sudo opf_users
opf_users > create operative Op3r4tIv3P$$SS
```


#### (If you have a problem) Update client configuration for backend interaction :

folder: /client/src/components/Config/index.jsx

```javascript
let config = {
        'protocol': 'http://',
        'server':'127.0.0.1',
        'port': '5000',
    };

```
