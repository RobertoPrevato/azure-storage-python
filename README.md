# Forked and edited to use asyncio

This is a fork of the official [Python Azure Storage SDK](https://github.com/Azure/azure-storage-python), edited to work with `asyncio` and `aiohttp`, to support asynchronous non blocking web requests to REST APIs.

The official Python Azure Storage SDK is designed to work with both Python 2 and 3, and is using `requests` library to make web requests to Azure REST APIs; thus making synchronous and blocking web requests. The fork is created to take advantage of new `async` and `await` syntax and Python 3 built-in support for event loops through `asyncio`.

The work on this fork has just started (beginning of January 2018) and is a work in progress. I cannot promise I will complete it - my commitment here is just tentative.

The initial work on this fork has been described in a blog post, refer to it to know how it was created: [https://robertoprevato.github.io/Upgrading-Azure-Storage-Python-SDK-to-support-asyncio/](https://robertoprevato.github.io/Upgrading-Azure-Storage-Python-SDK-to-support-asyncio/).
