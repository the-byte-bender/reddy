# Reddy

Reddy is a Reddit client designed to satisfy the need for an open source, screenreader-accessible reddit client on Linux.

## Announcement about the accessibility status for Windows and Mac. Linux users should ignore.

The fact that I (meatbag93) use a linux distribution as my main operating system was what initially inspired me to make this client. 
I have made a little prototype that is accessible  on all 3 platforms that I made with wxpython. But I quickly learned that the Orca screenreader completely ignore's  wx.listctrl, wx.treectrl, and a few other widgets. Clearly, there is a problem here. 

I've migrated to the gtk+ GUI library to increase linux accessibility. Despite being cross-platform, GTK+ is only fully accessible on Linux. It was confirmed to be completely inaccessible on Windows last I checked, and I'm quite sure it's the same on Mac.

It's unfortunate, but Windows users already have excellent clients they can use, and I have a good feeling Mac users have the same.

I truly apologize to everyone else; Linux is and will always be the major focus of this project. I won't make any effort to support Windows or Mac unless gtk+ is somehow made natively accessible on these platforms.

## optional environment variables you can configure

1. `REDDY_CLIENT_ID` - put your reddit client ID there. If left out, it will default to Reddy's client ID (recommended).
2. `REDDY_CLIENT_SECRET` - put your reddit client secret there. Do not set this if you are either using the default client ID or your client is not a web app or a personal script. Defaults to None (Reddy's official client is set as an installed app, so no secret is needed.)
3. `REDDY_DB_PATH` - put a  path to an sqlite database there (will be created  if not exists). Defaults to ./reddy.db (this file is gitignored so feel free to keep it at that)

## How can  the environment for this project be created?

1. Make sure you have Pipenv installed. If not, run `pip install pipenv`. 
2. Clone this repository and `cd` into it.
3. Run `pipenv install` to install all dependencies. This will also create a virtual environment for the project.
4. To launch the program, run `pipenv run python reddy.py`.

## License.

The GPL-3.0 license applies to all code in this project. A copy of this license can be found in the file `LICENSE`.
