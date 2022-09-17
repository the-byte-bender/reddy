# Reddy

Reddy is a Reddit client designed to satisfy the need for an open source, screenreader-accessible reddit client, especially on Linux.

## What environment variables must I configure?

1. `REDDY_CLIENT_ID` - put your reddit client ID there.
2. `REDDY_CLIENT_SECRET` - put your reddit client secret there.
3. `REDDY_DB_PATH` - put a  path to an sqlite database there (will be created  if not exists).

## How can  the environment for this project be created?

1. Make sure you have Pipenv installed. If not, run `pip install pipenv`. 
2. Clone this repository and `cd` into it.
3. Run `pipenv install` to install all dependencies. This will also create a virtual environment for the project.
4. To launch the program, run `pipenv run python reddy.py`.

## License.

The GPL-3.0 license applies to all code in this project. A copy of this license can be found in the file `LICENSE`.