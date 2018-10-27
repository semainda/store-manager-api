"""Method that tests owners functions after successful login"""
import json
import pytest

owner_data = dict(
        user_name="semainda",
        password="mk911212"
    )

attendant_data = dict(
    user_name="said",
    password="semainda"
)

def ownner_login(client, user_data):
    """Function where owner loging and access tocken is returned"""
    response = client.post(
        "api/v2/auth/login", data=json.dumps(user_data),
        headers={"content-type": "application/json"})
    return json.loads(response.data.decode())["Token"]

store_users = [
    (dict(
        first_name="Semainda", email="said@ymail.com",
        user_name="saidson"), 400, b"Key last_name not found"),
    (dict(
        last_name="Semainda", email="said@ymail.com",
        user_name="saidson"), 400, b"Key first_name not found"),
    (dict(
        first_name="Said", last_name="Semainda",
        user_name="saidson"), 400, b"Key email not found"),
    (dict(
        first_name="Said", last_name="Semainda", email="said@ymail.com",
        ), 400, b"Key user_name not found"),
    (dict(
        first_name="Said2", last_name="Semainda", email="said@ymail.com",
        user_name="saidson"), 400,
        b"first_name is invalid for it to be created"),
    (dict(
        first_name="Said", last_name="%Semainda", email="said@ymail.com",
        user_name="saidson"), 400, b"last_name is invalid for it to be created"),
    (dict(
        first_name="Said", last_name="Semainda", email="said@ymail.com",
        user_name="saidson$"), 400, b"user_name is invalid for it to be created"),
    (dict(
        first_name="Said", last_name="Semainda", email="said@ymail.com",
        user_name="saidson"), 201, b"User created successful"),
    (dict(
        first_name="Said", last_name="Semainda", email="said@ymail.com",
        user_name="saidson"), 409, b"User already exists")
    ]


@pytest.mark.parametrize("user_data, resp_code, msg", store_users)
def test_create_store_users_accounts(test_client, user_data, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/users", data=json.dumps(
            user_data), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


store_user = [(1, 200), (4, 404)]


@pytest.mark.parametrize("user_id, resp_code", store_user)
def test_get_specific_store_user(test_client, user_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/users/" + str(user_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


def test_get_created_store_users(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/users", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200

role_name = [(1, 200), (4, 404)]


@pytest.mark.parametrize("role_id, resp_code", role_name)
def test_get_specific_store_role(test_client, role_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/roles/" + str(role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


def test_get_created_store_roles(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/roles", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


store_roles = [
    (dict(), 400, b"Key role_name not found"),
    (dict(
        role_name="store_cleck#"), 400,
        b"role_name is invalid for it to be created"),
    (dict(role_name="store_attendant"), 201, b"Role created successful"),
    (dict(role_name="store_manager"), 201, b"Role created successful"),
    (dict(role_name="store_manager"), 409, b"Role already exists")
    ]

@pytest.mark.parametrize("role_name, resp_code, msg", store_roles)
def test_create_store_roles(test_client, role_name, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/roles", data=json.dumps(
            role_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


role = [
    (dict(
        role_name="store_cleck"), 4, 404,
        b"Role with key value '4' does not exists"),
    (dict(role_name="store_owner"), 1, 403, b"Store owner role can't be updated"),
    (dict(
        role_name="store_keeper&"), 3, 400,
        b"role_name is invalid for it to be created"),
    (dict(
        role_name="store_keeper"), 3, 201,
        b"Role with id '3' updated successful")
    ]


@pytest.mark.parametrize("role_name, role_id, resp_code, msg", role)
def test_update_specific_store_role(test_client, role_name, role_id, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.put(
        "api/v2/roles/" + str(role_id), data=json.dumps(role_name), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data

roles = [
    (1, 200,
    b"This role has already being assigned to users.\
    To delete it, revoke it from users"),
    (2, 200, b"Role deleted successful"),
    (4, 404, b"Role with key value '4' does not exists"),]


@pytest.mark.parametrize("role_id, resp_code, msg", roles)
def test_delete_specific_store_role(test_client, role_id, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/roles/" + str(role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


def test_get_user_roles(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/users/roles", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 200


user_roles = [
    (dict(user_id=2), 400, b"Key role_id not found"),
    (dict(role_id=2), 400, b"Key user_id not found"),
    (dict(role_id=2, user_id=2), 201, b"User_Role created successful"),
    (dict(role_id=5, user_id=2), 404, b"Role with key value '5' does not exists"),
    (dict(role_id=2, user_id=4), 404, b"User with key value '4' does not exists")]


@pytest.mark.parametrize("user_role, resp_code, msg", user_roles)
def test__user_role_assignment(test_client, user_role, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/users/roles", data=json.dumps(user_role), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data


user_role = [(2, 200), (4, 404)]


@pytest.mark.parametrize("user_role_id, resp_code", user_role)
def test_get_specific_user_role(test_client, user_role_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/users/roles/" + str(user_role_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


update_role = [
    (dict(), 2, 400, b"Key role_id not found"),
    (dict(role_id=1), 2, 201, b"User_Role with id '2' updated successful"),
    (dict(role_id=1), 4, 404, b"User_Role with key value '4' does not exists"),
    ]


@pytest.mark.parametrize("role_id, user_id, resp_code, msg", update_role)
def test_update_user_role(test_client, role_id, user_id, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.put(
        "api/v2/users/roles/" + str(user_id), data=json.dumps(role_id),
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data


def test_get_created_categoriess(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/categories", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'Categories' does not exists" in response.data


categories = [
    (dict(), 400, b"Key cat_name not found"),
    (dict(
        cat_name="Drinks#"), 400,
        b"cat_name is invalid for it to be created"),
    (dict(cat_name="Drinks"), 201, b"Categorie created successful"),
    (dict(cat_name="Electronics"), 201, b"Categorie created successful"),
    (dict(cat_name="Electronics"), 409, b"Categorie already exists")
    ]

@pytest.mark.parametrize("cat_name, resp_code, msg", categories)
def test_create_categories(test_client, cat_name, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/categories", data=json.dumps(
            cat_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data

cats = [(1, 200), (4, 404)]


@pytest.mark.parametrize("cat_id, resp_code", cats)
def test_get_specific_category(test_client, cat_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/categories/" + str(cat_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


category = [
    (dict(
        cat_name="mobile"), 5, 404,
        b"Categorie with key value '5' does not exists"),
    (dict(
        cat_name="mobile&"), 2, 400,
        b"cat_name is invalid for it to be created"),
    (dict(
        cat_name="clothes"), 1, 201,
        b"Categorie with id '1' updated successful")
    ]

@pytest.mark.parametrize("cat_name, cat_id, resp_code, msg", category)
def test_update_specific_category(test_client, cat_name, cat_id, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.put(
        "api/v2/categories/" + str(cat_id), data=json.dumps(cat_name), 
        headers={
            "content-type": "application/json",
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
    assert msg in response.data


def test_get_created_subcategories(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/subcategories", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'Sub_Categories' does not exists" in response.data


subcategories = [
    (dict(), 400, b"Key sub_cat_name not found"),
    (dict(sub_cat_name="LED Monitors"), 400, b"Key cat_id not found"),
    (dict(
        sub_cat_name="Drinks#", cat_id=1), 400,
        b"sub_cat_name is invalid for it to be created"),
    (dict(
        sub_cat_name="Cocacola", cat_id="two"), 400,
        b"Key cat_id not found"),
    (dict(sub_cat_name="Drinks", cat_id=3), 404, b"Categorie with key value '3' does not exists"),
    (dict(sub_cat_name="HDTV", cat_id=1), 201, b"Sub_Categorie created successful"),
    (dict(sub_cat_name="HDTV", cat_id=1), 409, b"Sub_Categorie already exists"),
    (dict(sub_cat_name="LCD Screen", cat_id=2), 201, b"Sub_Categorie created successful")
    ]

@pytest.mark.parametrize("sub_name, resp_code, msg", subcategories)
def test_create_subcategories(test_client, sub_name, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/subcategories", data=json.dumps(
            sub_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


subs = [(2, 200), (4, 404)]


@pytest.mark.parametrize("sub_id, resp_code", subs)
def test_get_specific_subcategory(test_client, sub_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/subcategories/" + str(sub_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code


subcategories = [
    (dict(), 400, 2, b"Key sub_cat_name not found"),
    (dict(sub_cat_name="LED Monitors"), 400, 2, b"Key cat_id not found"),
    (dict(
        sub_cat_name="Drinks#", cat_id=1), 400, 1,
        b"sub_cat_name is invalid for it to be created"),
    (dict(
        sub_cat_name="Cocacola", cat_id="two"), 400, 2,
        b"Key cat_id not found"),
    (dict(sub_cat_name="Drinks", cat_id=3), 201, 3, b"Categories with key value '3' does not exists"),
    (dict(sub_cat_name="HPTouch", cat_id=1), 201, 1, b"Sub_Categories with id '1' updated successful"),
    (dict(sub_cat_name="HDTV", cat_id=1), 201, 2, b"Sub_Categorie with id '2' updated successful"),
    (dict(sub_cat_name="LCD Screen", cat_id=2), 404, 3, b"Sub_Categorie with key value '3' does not exists")
    ]

@pytest.mark.parametrize("sub_name, resp_code, sub_id, msg", subcategories)
def test_update_subcategories(test_client, sub_name, resp_code, sub_id, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.put(
        "api/v2/subcategories/" + str(sub_id), data=json.dumps(
            sub_name), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data

def test_get_products(test_client):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/products", headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == 404
    assert b"'Products' does not exists" in response.data


products = [
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 201, b"Product created successful"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 409, b"Product already exists"),
    (dict(
        price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400, b"Key prod_name not found"),
    (dict(
        prod_name="HD Curved TV",
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400, b"Key price not found"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        size=43, cat_id=1, sub_cat_id=1), 400, b"Key quantity not found"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, cat_id=1, sub_cat_id=1), 400, b"Key size not found"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, sub_cat_id=1), 400, b"Key cat_id not found"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1), 400, b"Key sub_cat_id not found"),
    (dict(
        prod_name=45, price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=1), 400, b"prod_name is invalid for it to be created"),
    (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=6, sub_cat_id=1), 404, b"Category with key value '6' does not exists"),
     (dict(
        prod_name="HD Curved TV", price=450000,
        quantity=150, size=43, cat_id=1, sub_cat_id=5), 404, b"Sub_Category with key value '5' does not exists")
    ]

@pytest.mark.parametrize("product, resp_code, msg", products)
def test_owner_create_products(test_client, product, resp_code, msg):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.post(
        "api/v2/products", data=json.dumps(
            product), headers={
                "content-type": "application/json",
                "Authorization": "Bearer {}".format(access_token)}
        )
    assert response.status_code == resp_code
    assert msg in response.data


prods = [(1, 200), (4, 404)]


@pytest.mark.parametrize("p_id, resp_code", prods)
def test_get_specific_product(test_client, p_id, resp_code):
    access_token = ownner_login(test_client, owner_data)
    response = test_client.get(
        "api/v2/products/" + str(p_id), headers={
            "Authorization": "Bearer {}".format(access_token)})
    assert response.status_code == resp_code
