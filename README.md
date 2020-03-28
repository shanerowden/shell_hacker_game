# shell_hacker_game
    **WIP**

Hi, it's *shaen* from the town. This is one of my dumb projects. Thanks for looking at it. 

Here's an outdated log.

## Sat Mar 28 11:48:20 UTC 2020
### Setting Up Flask On Your Machine
In order to test out the project as it is, you'll need to 

0. get python3
1. create a venv and source into it.
2. install the requirements.txt file packages using pip.
3. set environment variables: `FLASK_ENV=development` and `FLASK_SECRET_KEY=` to a secret key. (Use `generate_secret.py` if you need to.)
4. Type 'flask run` and open the browser up to the [http://localhost:5000] or wherever you open it..

### On organization of the Flask app
To avoid circular import hell, the package is set up to initializes through a boilerplate `./app.py` which starts up `shell_hacker_game/__init__.py` where the majority of set up, plugins, and other tools used in the app are defined. 

    It's otherwise fairly self explanatory so far if you understand the Jinja2 templating engine.

1. Users can register accounts, login, and what they are shown varies based on authentication. 
2. Passwords are encrypted, databases only store the hashes, and some other input validation is going on.
3. There currently isn't very much to verify emails so you can just use fakes ones easily for now.
4. The login/register pages redirect properly away when there is an active session.
5. A user account gets a player profile. So far this is the only link where I've really done any work. 
6. You can find it under `Account > Player Profile` once you are logged in.

Most of what I have worked on is actually front-end (if you can believe that)...


### On the CSS...

My CSS organization starts with the [slate bootstrap theme](https://bootswatch.com/slate/) and moves into `static/css/bullstrap.css` which is where I write any edits to the original CSS framework, mostly to keep a record of what I've changed and to know the difference.

There are the imports in the `templates/base.html` file:

```html
<link href="static/css/slate.css" type="text/css" rel="stylesheet">
<link href="static/css/bullstrap.css" type="text/css" rel="stylesheet">
<link href="static/css/responsive.css" type="text/css" rel="stylesheet">
<link href="static/css/ripped_google_fonts.css" type="text/css" rel="stylesheet">
<link href="static/css/style.css" type="text/css" rel="stylesheet">
```

Extra media queries go to `responsive.css` for being text-space consuming and randomly particular as I have tried to finagle things into working within bare margins of acceptability.

The fonts are locally hosted but were ripped from a Google import link -- that's all that file is.

And finally, `style.css` is just for any selectors added which I come up with for this project specifically and I try to move inline styling from the HTML to this file when I realize that it's working out for me.

There is yet a few more elements with `style=""` attributes than there should be that I need to clean up.

    I know that my use of Bootstrap classes is not 100% yet 
    I probably use a lot of classes I don't need to and make a mess.
    (and/or I should remember to use others where I'm not always) ...
    My straight CSS is less than 100% but I actually have slightly more experience with that.

### As for JavaScript...
At this point there is no JavaScript in the project that I have personally done, but the bootstrap them does rely on jquery, popper.js, and the bootstrap js lib. I imagine the time will come soon when I have to focus on some JavaScript a bit myself, but it has not happened yet.
