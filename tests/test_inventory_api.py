from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import os
from datetime import datetime

class InventoryAPITests(APITestCase):


    def setup(self):
        self.token = os.environ["TEST_TOKEN"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_retrieve_inventory_list(self):
        self.setup()
        url = "http://localhost:8000/inventory"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_sku(self):
        self.setup()
        sku = "ETSY-FOREST"
        url = "http://localhost:8000/inventory" + f'?sku={sku}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        for item in data:
            self.assertEquals(item["sku"], sku)

    def test_filter_by_name(self):
        self.setup()
        name = "Etsy Bundle Pack"
        url = "http://localhost:8000/inventory" + f'?name={name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        for item in data:
            self.assertEqual(item["name"], name)

    def test_filter_by_tags(self):
        self.setup()
        tags = "etsy,shopify"
        url = "http://localhost:8000/inventory" + f'?tags={tags}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        for item in data:
            
            resp_tags = set(item["tags"].split(","))
            test_tags = set(tags.split(","))

            self.assertTrue(test_tags.issubset(resp_tags))
        
    def test_filter_by_min_in_stock(self):
        self.setup()
        min_in_stock = 3.0
        url = "http://localhost:8000/inventory" + f'?min_in_stock={min_in_stock}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        for item in data:
            self.assertGreaterEqual(float(item["in_stock"]), min_in_stock)

    def test_created_before(self):
        self.setup()
        created_before="2024-02-13"
        url = "http://localhost:8000/inventory" + f'?created_before={created_before}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        for item in data:

            item_created = datetime.strptime(item["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            created_before = datetime.strptime(created_before, "%Y-%m-%d")

            self.assertTrue(item_created <= created_before)

    def test_created_after(self):
        self.setup()
        created_after = "2024-02-09"
        url = "http://localhost:8000/inventory" + f'?created_after={created_after}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        for item in data:

            item_created = datetime.strptime(item["created"], "%Y-%m-%dT%H:%M:%S.%f%z")
            created_after = datetime.strptime(created_after, "%Y-%m-%d")

            self.assertTrue(item_created >= created_after)

    def test_unauthorized_access(self):
        self.client.credentials()  # Clear credentials
        url = "http://localhost:8000/inventory"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
