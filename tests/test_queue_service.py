import asyncio
import unittest
from azure.storage.queue import QueueService


import logging
logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)


TEST_QUEUE = 'foos'

ACCOUNT_NAME = '<ACCOUNT_NAME>'
ACCOUNT_KEY = '<ACCOUNT_KEY>'


class TestContainers(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

        self.qs = QueueService(account_name=ACCOUNT_NAME,
                               account_key=ACCOUNT_KEY)

    def tearDown(self):
        # dispose the aiohttp session
        self.loop.run_until_complete(self.qs.httpclient.session.close())

    def test_put_message_async(self):
        # works
        async def go():
            await self.qs.put_message(TEST_QUEUE, 'Hello, World!')

        self.loop.run_until_complete(go())

    def OFF_test_get_messages_and_update_async(self):
        # works
        async def go():
            messages = await self.qs.get_messages(TEST_QUEUE)

            self.assertIsNotNone(messages)

            for message in messages:
                print(message.content)

                # testing update message:
                await self.qs.update_message(TEST_QUEUE,
                                             message.id,
                                             message.pop_receipt,
                                             2,
                                             content='Hello, Kitty!')

        self.loop.run_until_complete(go())

    def OFF_test_delete_message_async(self):
        # works
        async def go():
            message = await self.qs.put_message(TEST_QUEUE, 'Hello, World!')

            self.assertIsNotNone(message)

            print(message.content)

            # testing update message:
            await self.qs.delete_message(TEST_QUEUE,
                                         message.id,
                                         message.pop_receipt)

        self.loop.run_until_complete(go())

    def OFF_test_clear_messages_async(self):
        # works
        async def go():
            await self.qs.clear_messages(TEST_QUEUE)

        self.loop.run_until_complete(go())

    def OFF_test_delete_queue_async(self):
        # works
        async def go():
            await self.qs.delete_queue(TEST_QUEUE)

        self.loop.run_until_complete(go())

    def OFF_test_peek_messages_async(self):
        # works
        async def go():
            messages = await self.qs.peek_messages(TEST_QUEUE)

            self.assertIsNotNone(messages)

            for message in messages:
                print(message.content)

        self.loop.run_until_complete(go())

    def OFF_test_exists_async(self):
        # works
        async def go():
            exists = await self.qs.exists(TEST_QUEUE)

            self.assertTrue(exists)

        self.loop.run_until_complete(go())

    def OFF_test_set_queue_metadata_async(self):
        # works
        async def go():
            metadata = await self.qs.set_queue_metadata(TEST_QUEUE, {
                'hello': 'World'
            })

            pass

        self.loop.run_until_complete(go())

    def OFF_test_get_queue_metadata_async(self):
        # works
        async def go():
            metadata = await self.qs.get_queue_metadata(TEST_QUEUE)

            self.assertEqual({'hello': 'World'}, metadata)

        self.loop.run_until_complete(go())

    def OFF_test_get_queue_acl_async(self):
        # works
        async def go():
            acl = await self.qs.get_queue_acl(TEST_QUEUE)

            pass

        self.loop.run_until_complete(go())

    def test_create_queue_async(self):
        # works
        async def go():
            await self.qs.create_queue(TEST_QUEUE)

        self.loop.run_until_complete(go())