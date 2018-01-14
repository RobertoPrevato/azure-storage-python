import asyncio
import unittest
from azure.storage.blob import BlockBlobService


import logging
logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)


TEST_CONTAINER_PREFIX = 'container'

ACCOUNT_NAME = '<account name>'
ACCOUNT_KEY = '<account key>'


class TestContainers(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(None)

        #self.bs = self._create_storage_service(BlockBlobService, self.settings)
        self.bs = BlockBlobService(account_name=ACCOUNT_NAME,
                                   account_key=ACCOUNT_KEY)
        self.test_containers = []

    def tearDown(self):
        # dispose the aiohttp session
        self.loop.run_until_complete(self.bs.httpclient.session.close())

    def test_list_containers_async(self):
        async def go():
            containers = await self.bs.list_containers()

            for container in containers:
                print(container.name)

        self.loop.run_until_complete(go())

    def test_list_blobs_async(self):
        async def go():
            blobs = await self.bs.list_blobs("tests")

            for blob in blobs:
                print(blob.name)

        self.loop.run_until_complete(go())

    ## Remove 'OFF_' comment to test; use file of your choice
    def OFF_test_get_blob_metadata_async(self):
        async def go():
            metadata = await self.bs.get_blob_metadata("tests", "your_example_file.jpg")
            print(metadata)

        self.loop.run_until_complete(go())

    ## Remove 'OFF_' comment to test; use container of your choice
    def OFF_test_upload_blob_async(self):
        async def go():
            await self.bs.create_blob_from_text("tests", "hello-world.txt", "Hello World")

        self.loop.run_until_complete(go())

    ## Remove 'OFF_' comment to test; use container of your choice
    def OFF_test_set_blob_metadata_async(self):
        async def go():
            await self.bs.set_blob_metadata("tests", "your_example_file.jpg", {
                "foo": "Example"
            })

        self.loop.run_until_complete(go())