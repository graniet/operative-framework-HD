#### opf_console

+ **:status**  =>  print current status started in console

exemple:

```
./bin/opf_console.py (client:stopped/server:started) $ status
client    :   STOPPED
server    :   STARTED
```

+ **config** => show current config

exemple:
```
./bin/opf_console.py (client:stopped/server:stopped) $ config
BACKEND_PORT: 5000
FRONTEND_PORT: 3000
MONGODB_HOST: localhost
MONGODB_PASS: operative
MONGODB_PORT: 27017
MONGODB_USER: operative
OPERATIVE_FRAMEWORK_VERSION: HD 1.0
```

+ **tools** => View external tools loaded in framework

exemple:

```
./bin/opf_console.py (client:stopped/server:stopped) $ tools
Sublist3r: Fast subdomains enumeration tool for penetration testers @aboul3la
```

+ **run_client** => Run operative framework client

exemple:

```
[2018-06-21 22:37:12] WARNING BEWARE YOU DON'T HAVE LOG WHEN YOUR START WITH THIS BIN
[2018-06-21 22:37:12] WARNING START WITH opf_client.py FOR VIEW LOGS.
....
```

+ **run_server** => Run operative framework server

exemple:

```
[2018-06-21 22:37:12] WARNING BEWARE YOU DON'T HAVE LOG WHEN YOUR START WITH THIS BIN
[2018-06-21 22:37:12] WARNING START WITH opf_server.py FOR VIEW LOGS.
....
```

