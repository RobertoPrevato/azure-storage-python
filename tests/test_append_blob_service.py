import asyncio
import unittest
from azure.storage.blob import AppendBlobService, BlobPermissions
from tests import ACCOUNT_NAME, ACCOUNT_KEY

import logging
logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)


TEST_CONTAINER_PREFIX = 'tests'




class TestContainers(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

        self.bs = AppendBlobService(account_name=ACCOUNT_NAME,
                                    account_key=ACCOUNT_KEY)

    def tearDown(self):
        # dispose the aiohttp session
        self.loop.run_until_complete(self.bs.httpclient.session.close())

    def OFF_test_create_blob_async(self):
        async def go():
            await self.bs.create_blob('appendtests', 'hello-world.txt')

        self.loop.run_until_complete(go())

    def test_append_blob_from_bytes_async(self):
        async def go():
            await self.bs.append_blob_from_bytes('appendtests', 'hello-world.txt', b'Lorem ipsum\r\n')

        self.loop.run_until_complete(go())
