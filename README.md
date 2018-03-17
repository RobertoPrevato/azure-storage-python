# Unofficial port of Azure Storage SDK, to support asyncio and aiohttp

This is an unofficial fork of the [Python Azure Storage SDK](https://github.com/Azure/azure-storage-python), edited to work with `asyncio` and `aiohttp`, to support asynchronous non blocking web requests to REST APIs.
Only the code to interact with Azure Table, Blob and Queue services has been ported, the File service wasn't ported. The code to work with Azure Storage Table Service should be compatible also for CosmosDB, but I didn't verify this, yet.

The work on this fork has been described in a blog post, refer to it to know how it was created: [https://robertoprevato.github.io/Upgrading-Azure-Storage-Python-SDK-to-support-asyncio/](https://robertoprevato.github.io/Upgrading-Azure-Storage-Python-SDK-to-support-asyncio/).

This work is done primarily for my private use, tests were run manually; I don't have time to write a proper test suite. The `tests` folder contains the code used for manual testing (they can be used removing the 'OFF_' prefix from function names). 

## Getting started
As usual for Python projects:
```bash
# create virtual environment
python -m venv env

# activate virtual environment (Linux:)
source env/bin/activate

# activate virtual environment (Windows:)
env\Scripts\activate

# install dependencies
pip install -r requirements.txt

# enjoy
```

To verify how this code works, simply see the content of `tests` folder for working examples, code is kept simple and stupid there; it's sufficient to provide valid account name and admin key.

```python
# replace with valid values;
ACCOUNT_NAME = '<ACCOUNT_NAME>'
ACCOUNT_KEY = '<ACCOUNT_KEY>'
```

## Why
The official Python Azure Storage SDK is designed to work with both Python 2 and 3, and is using `requests` library to make web requests to Azure REST APIs; thus making synchronous and blocking web requests. The fork is created to take advantage of new `async` and `await` syntax and Python 3 built-in support for event loops through `asyncio`.


