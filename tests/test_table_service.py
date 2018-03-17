import asyncio
import unittest
from azure.storage.table import TableService, Entity


import logging
logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s', level=logging.INFO)


TEST_CONTAINER_PREFIX = 'tests'

ACCOUNT_NAME = '<ACCOUNT_NAME>'
ACCOUNT_KEY = '<ACCOUNT_KEY>'


class TestContainers(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

        self.bs = TableService(account_name=ACCOUNT_NAME,
                               account_key=ACCOUNT_KEY)
        self.test_containers = []

    def tearDown(self):
        # dispose the aiohttp session
        self.loop.run_until_complete(self.bs.httpclient.session.close())

    def OFF_test_list_tables_async(self):
        # works
        async def go():
            containers = await self.bs.list_tables()

            for container in containers:
                print(container.name)

        self.loop.run_until_complete(go())

    def OFF_test_create_table_async(self):
        async def go():
            success = await self.bs.create_table('versions')

            self.assertTrue(success)

        self.loop.run_until_complete(go())

    def OFF_test_delete_table_async(self):
        async def go():
            success = await self.bs.delete_table('pippe')

            self.assertTrue(success)

        self.loop.run_until_complete(go())

    def OFF_test_exists_async(self):
        async def go():
            exists = await self.bs.exists('versions')

            self.assertTrue(exists)

        self.loop.run_until_complete(go())

    def OFF_test_get_table_service_properties_async(self):
        async def go():
            data = await self.bs.get_table_service_properties()

            self.assertIsNotNone(data)

        self.loop.run_until_complete(go())

    def OFF_test_insert_entity_async(self):
        async def go():
            entity = Entity()
            entity.Foo = 'Foo'
            entity.Ufo = 'Ufo'
            entity.Number = 1
            entity.PartitionKey = 'app'
            entity.RowKey = '2'

            data = await self.bs.insert_entity('versions', entity)

            self.assertIsNotNone(data)

        self.loop.run_until_complete(go())

    def OFF_test_query_entity_async(self):
        async def go():
            data = await self.bs.query_entities('versions')

            self.assertIsNotNone(data)
            for item in data:
                print(item.RowKey)

        self.loop.run_until_complete(go())

    def OFF_test_get_entity_async(self):
        async def go():
            data = await self.bs.get_entity('versions', 'app', '1')

            self.assertIsNotNone(data)

        self.loop.run_until_complete(go())

    def OFF_test_delete_entity_async(self):
        async def go():
            await self.bs.delete_entity('versions', 'app', '1')

        self.loop.run_until_complete(go())

    def OFF_test_delete_entity_async(self):
        async def go():
            await self.bs.merge_entity('versions', 'app', '1')

        self.loop.run_until_complete(go())