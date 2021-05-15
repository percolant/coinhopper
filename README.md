for localhost testing:
$ python3 -m venv venv
add to venv/bin/activate:
export TELEGRAM_API_TOKEN='...' etc.
$ source venv/bin/activate
(venv) $ python3 venv/bin/pip3 install -e .
(venv) $ coinhopper

for server install:
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ python3 venv/bin/pip3 install -e .
