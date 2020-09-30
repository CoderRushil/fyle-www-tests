# fyle-www-tests - An Amazing project

This repository contains tests for Fyle's website (https://www.fylehq.com). This is under active development.
This is a public repository - please do not check in any passwords or keys.

# Development

* Create virtualenv and install requirements using:

```
virtualenv venv --python=python3.7
source venv/bin/activate
pip install -r requirements.txt
```

Next, you'll need to setup at webdrivers for Chrome and Safari to run the tests.

# Setup Chrome WebDriver

Download and install Chrome webdriver from chromium site [here](https://chromedriver.chromium.org/downloads)

# Setup Safari WebDriver

Please follow instructions from Apple [here](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari)

# Running tests

Before running the tests, choose the browser by setting the environment variable (by default, tests will choose Chrome):

```
export BROWSER=chrome
# or
export BROWSER=safari
```

To run all tests, use this command.

```
python -m pytest
```

You should see output like this:

```
(venv) laptop:fyle-www-tests siva$ python -m pytest
============================================= test session starts =============================================
platform darwin -- Python 3.7.4, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
rootdir: /Users/siva/src/fyle-www-tests, inifile: pytest.ini
collected 3 items                                                                                             

homepage/test_getdemo.py::test_bad_email PASSED                                                         [ 33%]
homepage/test_getdemo.py::test_missing_firstname PASSED                                                 [ 66%]
homepage/test_getdemo.py::test_success PASSED                                                           [100%]

============================================= 3 passed in 40.07s ==============================================
```


To run only tests for homepage:

```
python -m pytest homepage/
```

To run only getdemo tests in homepage:

```
python -m pytest homepage/test_getdemo.py
```

To run only one specific test:

```    
python -m pytest homepage/test_getdemo.py::test_success
```

# Contributing

Please raise PRs for contributing to tests. Run pylint checks and they're clean before raising a PR. Example:

```
PYTHONPATH="." pylint homepage/
```

Include the output of the above command (against your directory) as part of the PR description. If there are any errors or warnings, the PR will not be approved.
