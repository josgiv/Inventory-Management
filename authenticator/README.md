# Login Webapp (using flask)
A simple login app created with flask micro-framework.

There are 3 routes in this web-app:

**route: '/'**

This is the root route. If the user is logged in it redirects to welcome page. If not loggedin, it redirects to login page.

**route: '/login'**

This is the login route. If the user is logged in, it redirects to welcome page. If not logged in, it opens the login authentication page.

**route: '/welcome'**

This is the welcome page. If already logged in this page opens. If not already logged in, redirects to login page.


**Usage:**

The first two command you need to run only once (`FLASK_ENV` can either be `development` or `production`)
The `--host` option can be your desiered ip address. `0.0.0.0` gives access to all ip addresses in the server
the `--port` option can be yout desiered port number.

```
$ export FLASK_APP=app.py
$ export FLASK_ENV=development
$ flask run --host=0.0.0.0 --port=8080
```

**Testing authentication:**

```
username: admin
password: admin
```



![signature](http://swastiknath.surge.sh/img/swastik-signature.png)
