class TestRoutes:
    """ Тесты API """

    def test_product_stock_positive(self, client):
        """ Тест успешного остатка товара на складе

            создать товар и склад -> сделать IN -> получить остаток
        """

        product_data = {
            "sku": "sku-001",
            "name": "Coffee",
            "price": 100.0
        }
        response_product_create = client.post("/products/", json=product_data)
        assert response_product_create.status_code == 200

        data_product = response_product_create.json()
        product_id = data_product["id"]

        response_warehouse_create = client.post("/warehouses/", params={"warehouse_name": "Склад-1"})
        assert response_warehouse_create.status_code == 200

        data_warehouse = response_product_create.json()
        warehouse_id = data_warehouse["id"]

        movement_data = {
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "type": "IN",
            "qty": 10
        }

        response_in = client.post("/stock/movement/", json=movement_data)
        assert response_in.status_code == 200

        response_stock = client.get(f"/stock/{product_id}", params={"warehouse_id": warehouse_id})

        assert response_stock.status_code == 200
        data_stock = response_stock.json()
        assert data_stock["product_id"] == 1
        assert data_stock["qty"] == 10

    def test_product_stock_negative(self, client):
        """ Тест получение недостаток товара на складе

            создать товар и склад -> сделать OUT
        """

        product_data = {
            "sku": "sku-001",
            "name": "Coffee",
            "price": 100.0
        }
        response_product_create = client.post("/products/", json=product_data)
        assert response_product_create.status_code == 200

        data_product = response_product_create.json()
        product_id = data_product["id"]

        response_warehouse_create = client.post("/warehouses/", params={"warehouse_name": "Склад-1"})
        assert response_warehouse_create.status_code == 200

        data_warehouse = response_product_create.json()
        warehouse_id = data_warehouse["id"]

        movement_data = {
            "product_id": product_id,
            "warehouse_id": warehouse_id,
            "type": "OUT",
            "qty": 10
        }

        response_out = client.post("/stock/movement/", json=movement_data)
        assert response_out.status_code == 400
        assert "Недостаточно товара на складе" in response_out.json()["detail"]

