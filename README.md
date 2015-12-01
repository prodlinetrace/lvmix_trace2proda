# trace2proda
tool to synchronize local database to PRODA by Wabco/


Pre-requisites
--------------

- Some Python coding experience
- Basic knowledge of python ctypes

Requirements
------------

- Python 2.7 on Windows
- git

Setup
-----

Below are step-by-step installation instructions:

**Step 1**: Clone the git repository

    $ git clone https://bitbucket.org/wilkpio/trace2proda.git
    $ cd trace2proda

**Step 2**: Create a virtual environment.

For Linux, OSX or any other platform that uses *bash* as command prompt (including Cygwin on Windows):

    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

For Windows users working on the standard command prompt:

    > virtualenv venv
    > venv\scripts\activate
    (venv) > pip install -r requirements.txt

**Step 3**: Start the application:

    (venv) $ python trace2proda.py
    
