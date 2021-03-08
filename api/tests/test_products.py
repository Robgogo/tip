# coding=utf-8
import json
import os

from django.apps import apps
from django.urls import reverse
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.local'

client = APIClient()


class CreateProductTest(APITestCase):
    
    def setUp(self):
        self.valid_product = {
            "name": "Test Case",
            "description": "Test Case Description",
            "country": "Ethiopia",
            "species_id": "ecc7f319-c14c-4595-b7ba-9040e3a33baa",
            "brand_id": "f9310dd9-5b76-4042-bf6a-e5a678516553",
            "category_id": "fbf07188-79ec-4a32-a3c8-6b6e29d6026c"
        }
        self.invalid_product = {
            "name": "Test Case",
            "description": "Test Case Description",
            "country": "Ethiopia",
        }

    def create_valid_product(self):
        response = client.post(
            reverse('products'),
            data=json.dumps(self.valid_product),
            content_type='application/json'
        )
        print(response.data)
        return response
    
    def create_invalid_product(self):
        response = client.post(
            reverse('products'),
            data=json.dumps(self.invalid_product),
            content_type='application/json'
        )
        return response

    # def test_create_valid_product(self):
    #     response = self.create_valid_product()
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    # def test_create_invalid_product(self):
    #     response = self.create_invalid_product()
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_products(self):
        response = client.get(
            reverse('products')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
