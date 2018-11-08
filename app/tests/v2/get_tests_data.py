"""Module that defines all data required to run tests cases"""

# Administrator login data

admin_login_data = [
    (dict(), 400, b"Key user_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(user_name="semainda"), 400, b"Key password is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        user_name="semainda",
        password="ahfjhf"), 401, b"Invalid username/password supplied"),
    (dict(
        user_name="semainda",
        password="mk911212"), 201, b"Holaa! You Logged in as semainda.")
]

# Attendant login data

attendant_login_data = [
    (dict(), 400, b"Key user_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(user_name="said"), 400, b"Key password is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        user_name="said",
        password="ahfjhf"), 401, b"Invalid username/password supplied"),
    (dict(
        user_name="said",
        password="semainda"), 201, b"Holaa! You Logged in as said.")
]

# Store users data
get_users_data = [(1, 200), (4, 404)]

create_users_data = [
    (dict(
        first_name="semainda", email="said@ymail.com",
        user_name="saidson"), 400,
        b"Key last_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        last_name="semainda", email="said@ymail.com",
        user_name="saidson"), 400,
        b"Key first_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        first_name="said", last_name="semainda",
        user_name="saidson"), 400,
        b"Key email is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        first_name="said", last_name="semainda",
        email="said@ymail.com"), 400,
        b"Key user_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        first_name="said2", last_name="semainda", email="said@ymail.com",
        user_name="saidson"), 400,
        b"first_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        first_name="said", last_name="%jemainda",
        email="said@ymail.com", user_name="saidson"), 400,
        b"last_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        first_name="said", last_name="semainda", email="said@ymail.com",
        user_name="saidson$"), 400,
        b"user_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        first_name="said", last_name="semainda", email="said@ymail.com",
        user_name="said"), 201,
        b"User 'said' created successful"),
    (dict(
        first_name="yousuph", last_name="nuru", email="semainda@go.com",
        user_name="yousuph"), 201,
        b"User 'yousuph' created successful"),
    (dict(
        first_name="said", last_name="semainda", email="said@ymail.com",
        user_name="saidson"), 409, b"User 'said@ymail.com' already exists"),
    (dict(
        first_name="said", last_name="semainda", email="said@gmail.com",
        user_name="said"), 409, b"User 'said' already exists")
]

# Store roles data

get_roles_data = [(1, 200), (5, 404)]

create_roles_data = [
    (dict(), 400,
    b"Key role_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        role_name="store_cleck#"), 400,
        b"role_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        role_name="attendant"), 201,
        b"Role 'attendant' created successful"),
    (dict(
        role_name="store_manager"), 201,
        b"Role 'store_manager' created successful"),
    (dict(
        role_name="store_driver"), 201,
        b"Role 'store_driver' created successful"),
    (dict(
        role_name="store_manager"), 409,
        b"Role 'store_manager' already exists")
]

update_role_data = [
    (dict(
        role_name="store_cleck"), 5, 404,
        b"Role 'role_id: 5' does not exists"),
    (dict(role_name="attendant"), 2, 409,
        b"Role 'attendant' already exists"),
    (dict(role_name="store_owner"), 1, 403,
        b"store_owner role can not be updated"),
    (dict(
        role_name="store_keeper&"), 3, 400,
        b"role_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        role_name="store_keeper"), 3, 200,
        b"Role 'role_id: 3' updated successful")
]

delete_role_data = [
    (1, 403,
    b"This role has already being assigned to users.To delete it, revoke it from users"),
    (3, 200, b"Role 'role_id: 3' deleted successful"),
    (5, 404, b"Role 'role_id: 5' does not exists")
]

# Store user_roles

get_user_role = [(1, 200), (5, 404)]

create_user_roles = [
    (dict(
        user_id=2), 400,
        b"Key role_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        role_id=2), 400,
        b"Key user_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        role_id=1, user_id=1), 409,
        b"User_role '(1, 1)' already exists"),
    (dict(
        role_id=2, user_id=2), 201,
        b"User_role '(2, 2)' created successful"),
    (dict(
        role_id=4, user_id=3), 201,
        b"User_role '(4, 3)' created successful"),
    (dict(
        role_id=5, user_id=2), 404,
        b"Role 'role_id: 5' does not exists"),
    (dict(
        role_id=1, user_id=4), 404,
        b"User 'user_id: 4' does not exists")
]

update_users_role = [
    (dict(), 2, 400,
    b"Key role_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        role_id=1), 4, 200,
        b"User_role 'role_id for : [{'user_id': 3}]' updated successful"),
    (dict(
        role_id=1), 5, 404,
        b"User_role 'role_id: 5' does not exists"),
]

# Categories data

create_categories_data = [
    (dict(), 400,
    b"Key cat_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        cat_name=20), 400,
        b"cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        cat_name="Drinks#"), 400,
        b"cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        cat_name="Drinks"), 201,
        b"Category 'drinks' created successful"),
    (dict(
        cat_name="Drinks"), 409,
        b"Category 'drinks' already exists"),
    (dict(
        cat_name="Electronics"), 201,
        b"Category 'electronics' created successful"),
    (dict(
        cat_name="Electronics"), 409,
        b"Category 'electronics' already exists")
]

get_categories_data = [(1, 200), (4, 404)]

update_category_data = [
    (dict(), 1, 400,
    b"Key cat_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        cat_name=20), 1, 400,
        b"cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        cat_name="mobile"), 5, 404,
        b"Category 'cat_id: 5' does not exists"),
    (dict(
        cat_name="mobile&"), 2, 400,
        b"cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        cat_name="clothes"), 1, 200,
        b"Category 'cat_id: 1' updated successful"),
    (dict(
        cat_name="clothes"), 1, 409,
        b"Category 'clothes' already exists")
]

# Sub Categories data

create_sub_categories = [
    (dict(), 400,
    b"Key sub_cat_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        sub_cat_name="LED Monitors"), 400,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        sub_cat_name="soda#", cat_id=1), 400,
        b"sub_cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        sub_cat_name="soda", cat_id="two"), 400,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        sub_cat_name="soda", cat_id=3), 404,
        b"Category 'cat_id: 3' does not exists"),
    (dict(
        sub_cat_name="soda", cat_id=1), 201,
        b"SubCategory 'soda' created successful"),
    (dict(
        sub_cat_name="water", cat_id=1), 201,
        b"SubCategory 'water' created successful"),
    (dict(
        sub_cat_name="water", cat_id=1), 409,
        b"SubCategory 'water' already exists"),
    (dict(
        sub_cat_name="LCD Screen", cat_id=2), 201,
        b"SubCategory 'lcd screen' created successful"),
    (dict(
        sub_cat_name="LCD Screen", cat_id=2), 409,
        b"SubCategory 'lcd screen' already exists")
]

get_sub_categories_data = [(1, 200), (4, 404)]

update_sub_categories_data = [
    (dict(), 400, 2,
    b"Key sub_cat_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        sub_cat_name="LED Monitors"), 400, 2,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        sub_cat_name="Drinks#", cat_id=1), 400, 1,
        b"sub_cat_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        sub_cat_name="Cocacola", cat_id="two"), 400, 2,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        sub_cat_name="soda", cat_id=3), 404, 3,
        b"Category 'cat_id: 3' does not exists"),
    (dict(
        sub_cat_name="juice", cat_id=1), 200, 1,
        b"SubCategory 'sub_id: 1' updated successful"),
    (dict(
        sub_cat_name="desktop pc", cat_id=2), 200, 2,
        b"SubCategory 'sub_id: 2' updated successful"),
    (dict(
        sub_cat_name="LCD Screen", cat_id=2), 409, 3,
        b"SubCategory 'lcd screen' already exists")
]

# Admin Products data

create_products_data = [
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 201,
        b"Product 'hd curved tv' created successful"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 409,
        b"Product 'hd curved tv' already exists"),
    (dict(
        price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key prod_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        prod_name="HD Curved TV",
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key price is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key quantity is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, cat_id=1, sub_cat_id=1), 400,
        b"Key size is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, sub_cat_id=1), 400,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1), 400,
        b"Key sub_cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name=45, price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"prod_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        prod_name="HD Curved", price=450000,
        quantity=150, size=43, cat_id=6, sub_cat_id=1), 404,
        b"Category 'cat_id: 6' does not exists"),
     (dict(
        prod_name="HD Curved", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=5), 404,
        b"SubCategory 'sub_id: 5' does not exists")
]

# Attendant Products data

attendant_products_data = [
    (dict(
        prod_name="cocacola", price=1000,
        quantity=500, size=500, cat_id=1, sub_cat_id=1), 201,
        b"Product 'cocacola' created successful"),
    (dict(
        prod_name="cocacola", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 409,
        b"Product 'cocacola' already exists"),
    (dict(
        price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key prod_name is not found or value given is not of required type.Make sure a value is 'string' type"),
    (dict(
        prod_name="HD Curved TV",
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key price is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        size=43, cat_id=1, sub_cat_id=1), 400,
        b"Key quantity is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, cat_id=1, sub_cat_id=1), 400,
        b"Key size is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, sub_cat_id=1), 400,
        b"Key cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1), 400,
        b"Key sub_cat_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_name=45, price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400,
        b"prod_name value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        prod_name="HD Curved", price=450000,
        quantity=150, size=43, cat_id=6, sub_cat_id=1), 404,
        b"Category 'cat_id: 6' does not exists"),
     (dict(
        prod_name="HD Curved", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=5), 404,
        b"SubCategory 'sub_id: 5' does not exists")
]


get_product_data = [(1, 200), (4, 404)]

# forbiden attendant get endpoints data

atttendant_forbiden_get_endpoints = [
    ("api/v2/users"),
    ("api/v2/roles"),
    ("api/v2/roles/1"),
    ("api/v2/users/1"),
    ("api/v2/users/roles"),
    ("api/v2/users/roles/1"),
    ("api/v2/categories"),
    ("api/v2/categories/1"),
    ("api/v2/subcategories"),
    ("api/v2/subcategories/1"),
    ("api/v2/sales"),
    ("api/v2/sales/1"),
    ("/api/v2/sales/1"),
    ("/api/v2/products/status"),
    ("/api/v2/products/status"),
    ("/api/v2/sales/summary"),
    ("/api/v2/sales/summary/1"),
    ("/api/v2/sales/store/summary")
]

# products status data

get_products_status_data = [(1, 200), (5, 404)]


# products sales deta
get_sales_by_user_id_data = [
    (1, 404), (2, 200), (5, 404)
]

get_attendant_own_sales_by_sale_id_data = [
    (1, 200)
]

get_sales_summary_by_user_id_data = [
    (1, 404), (2, 200), (5, 404)
]

create_sale_data = [
    (dict(
        prod_id="two", quantity=20), 400,
        b"Key prod_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_id=1, quantity="ten"), 400,
        b"Key quantity is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        quantity=20), 400,
        b"Key prod_id is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_id=1), 400,
        b"Key quantity is not found or value given is not of required type.Make sure a value is 'integer' type"),
    (dict(
        prod_id=1, quantity=-20), 400,
        b"quantity value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        prod_id=-1, quantity=20), 400,
        b"prod_id value is not of valid type.Make sure a value is not empty and is of valid type"),
    (dict(
        prod_id=1, quantity=50), 201,
        b"Sale 'hd curved tv' created successful" 
    ),
    (dict(
        prod_id=1, quantity=100), 201,
        b"Sale 'hd curved tv' created successful" 
    ),
    (dict(
        prod_id=1, quantity=100), 209,
        b"Sorry this product 'hd curved tv' is out of stock for now.Try again when new stock has arraived"
    ),
    (dict(
        prod_id=2, quantity=600), 209,
        b"This product 'cocacola' has only '500' items in stock.So sale order should not exceed this value"
    ),
    (dict(
        prod_id=4, quantity=50), 404,
        b"Product 'prod_id: 4' does not exists"
    )
]
