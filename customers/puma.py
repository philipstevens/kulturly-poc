# customers/puma.py

from customers.base_customer import BaseCustomerRenderer

class Puma(BaseCustomerRenderer):
    def __init__(self):
        super().__init__(
            name="Puma",
            data_path="data/puma.json"
        )
    
 