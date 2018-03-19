import asyncio
import unittest
from azure.storage.blob import BlockBlobService, BlobPermissions
from tests import ACCOUNT_KEY, ACCOUNT_NAME

import logging
logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)


TEST_CONTAINER_PREFIX = 'tests'


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

    def OFF_test_delete_container_async(self):
        async def go():
            done = await self.bs.delete_container("newcontainer")

            self.assertTrue(done)

        self.loop.run_until_complete(go())

    def OFF_test_create_container_async(self):
        async def go():
            created = await self.bs.create_container("newcontainernewnew")

            if not created:
                print("Not created!")

        self.loop.run_until_complete(go())

    def OFF_test_get_blob_to_path(self):
        async def go():
            text = await self.bs.get_blob_to_path("tests", "hello-kitty.txt", r"D:\Root\a.txt")
        self.loop.run_until_complete(go())

    def OFF_test_create_blob_from_bytes_async(self):
        async def go():
            done = await self.bs.create_blob_from_bytes("tests", "hello-world-b.txt", b"Hello World! 2018/03/03")

            if not done:
                print("Not deleted!")

        self.loop.run_until_complete(go())

    def OFF_test_generate_account(self):
        a = self.bs.generate_blob_shared_access_signature("tests", "Animal.mp4", BlobPermissions(read=True))
        print(a)

    def OFF_test_multi_upload(self):
        # example of concurrent upload:
        #
        async def go():
            v = [(r"C:\Some\Path\Videos\Example-001.mp4", "Example-001.mp4"),
                 (r"C:\Some\Path\Videos\Example-002.mp4", "Example-002.mp4"),
                 (r"C:\Some\Path\Videos\Example-003.mp4", "Example-003.mp4")]

            tasks = []
            open_files = []

            for a in v:
                f = open(a[0], "rb")
                open_files.append(f)
                tasks.append(self.bs.create_blob_from_stream("tests", a[1], f))

            await asyncio.wait(tasks)

            for f in open_files:
                f.close()

        self.loop.run_until_complete(go())

    def OFFF_test_create_blob_from_path(self):
        async def go():
            with open(r"C:\Some\Path\Videos\Example-004.mp4", "rb", buffering=0) as f:
                done = await self.bs.create_blob_from_stream("tests", "Example-004.mp4", f)

        self.loop.run_until_complete(go())

    def OFF_test_create_blob_from_path(self):
        async def go():
            with open(r"C:\Some\Path\Videos\Example-005.mp4", "rb", buffering=0) as f:
                done = await self.bs.create_blob_from_stream("tests", "Example-005.mp4", f)

        self.loop.run_until_complete(go())

    def test_create_blob_from_stream(self):
        async def go():
            with open(r"C:\Some\Path\Pictures\Zenyatta_portrait.png", "rb") as f:
                done = await self.bs.create_blob_from_stream("tests", "Zenyatta_portrait.png", f)

        self.loop.run_until_complete(go())

    def OFF_test_create_blob_from_text_async(self):
        async def go():
            done = await self.bs.create_blob_from_text("tests", "hello-world.txt", "Hello World! 2018/03/03")

            if not done:
                print("Not deleted!")

        self.loop.run_until_complete(go())

    def OFF_test_download_to_text(self):
        async def go():
            text = await self.bs.get_blob_to_text("tests", "hello-world-b.txt")
            self.assertEqual('Hello World! 2018/03/03', text.content)
        self.loop.run_until_complete(go())

    def OFF_test_download_to_bytes(self):
        async def go():
            text = await self.bs.get_blob_to_bytes("tests", "hello-world-b.txt")
            self.assertEqual(b'Hello World! 2018/03/03', text.content)
        self.loop.run_until_complete(go())

    def OFF_est_get_metadata(self):
        async def go():
            meta = await self.bs.get_blob_metadata("tests", "hello-world-b.txt")
            self.assertIsNotNone(meta)
        self.loop.run_until_complete(go())

    def OFF_test_exists(self):
        async def go():
            exists = await self.bs.exists("tests", "hello-world-b.txt")
            self.assertTrue(exists)

            exists = await self.bs.exists("tests", "asdasda.txt")
            self.assertFalse(exists)
        self.loop.run_until_complete(go())

    def OFF_test_set_blob_metadata(self):
        async def go():
            await self.bs.set_blob_metadata("tests", "hello-world-b.txt", {
                "prova2": "prova"
            })
        self.loop.run_until_complete(go())

    def OFF_test_delete_blob_async(self):
        async def go():
            done = await self.bs.delete_blob("tests", "hello-world.txt")

            if not done:
                print("Not deleted!")

        self.loop.run_until_complete(go())

    def OFF_test_list_blobs_async(self):
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
            await self.bs.create_blob_from_text("tests", "hello-kitty.txt", "Hello Kitty")

        self.loop.run_until_complete(go())

    ## Remove 'OFF_' comment to test; use container of your choice
    def OFF_test_set_blob_metadata_async(self):
        async def go():
            await self.bs.set_blob_metadata("tests", "your_example_file.jpg", {
                "foo": "Example"
            })

        self.loop.run_until_complete(go())