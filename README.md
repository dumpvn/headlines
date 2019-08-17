# headlines

where user can read there daily feeds easily.

## quick run

```bash
pipenv install --dev
pipenv shell
python headlines.py
```


## mod_wsgi (Apache)

- [mod_wsgi@flask](https://flask.palletsprojects.com/en/1.1.x/deploying/mod_wsgi/)

```bash
apt-get install libapache2-mod-wsgi
```

```conf
<VirtualHost *>
    ServerName example.com
    WSGIScriptAlias / /var/www/headlines/headlines.wsgi
    WSGIDaemonProcess headlines
    <Directory /var/www/headlines>
        WSGIProcessGroup headlines
        WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
    </Directory>
</VirtualHost>
```

```bash
sudo a2dissite hello.conf
sudo a2enssite headlines.conf
sudo service apache2 reload
sudo tail -fn 20 /var/log/apache2/error.log
```

```bash
sudo service apache2 reload
```