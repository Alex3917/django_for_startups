# django_for_startups

Code for the book Django for Startups

## Instructions for running locally on MacOS with Python 3.8

1. If not already installed, install Homebrew: <https://brew.sh/>.

2. Run `brew update`

3. Install Rust locally on your mac: `brew install rust`

4. Install Postgresql locally on your mac: `brew install postgresql`

5. Start Postgresql locally using: `brew services start postgresql`

6. Install Redis locally on your mac: `brew install redis`

7. Start Redis locally using: `brew services start redis`

8. Create a virtualenv using `python3 -m venv .`

9. Activate the virtualenv with `. bin/activate`

10. Install pip-tools using: `pip install pip-tools`

11. Run `pip-compile --output-file requirements.txt requirements.in`. This generates the requirements.txt file from the requirements.in file. If this doesn't work, try upgrading setuptools.

12. Set the following variables:

    - `export CRYPTOGRAPHY_SUPPRESS_LINK_FLAGS="1"`
    - `export LDFLAGS="-L$(brew --prefix openssl)/lib"`
    - `export CPPFLAGS="-I$(brew --prefix openssl)/include"`

13. Run `pip install -r requirements.txt`. This install the pinned versions specified in the `requirements.txt` file.

## Start server

python django_for_startups/manage.py runserver

## Run tests

python django_for_startups/manage.py test

## Check for outdated root dependencies

python scripts/list_outdated.py
