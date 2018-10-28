# store-manager-api

## Introduction

API for Store Manager web application that helps store owners manage sales and product inventory records.

[![Build Status](https://travis-ci.com/semainda/store-manager-api.svg?branch=store-manager-challenge2)](https://travis-ci.com/semainda/store-manager-api)
[![codecov](https://codecov.io/gh/semainda/store-manager-api/branch/master/graph/badge.svg)](https://codecov.io/gh/semainda/store-manager-api)

## Features Included

1. Users Login
2. Register Roles
3. Register Store Attendants
4. Assign Role to Attendants
5. Register Products Categories
6. Register Products Sub-Categories
7. Register a Sale
8. Generate Products Sales Status
9. Generate Sales Summary

## Prerequisite

### Installation

#### Step 1: Create a project directory

```$ mkdir store-manager-api```

```$ cd store-manager-api```

#### Step 2: Created virtual enviroment

```$ apt get install pipenv```

```$ pipenv --python 3.6```

#### Step 3: Activate the virtual envinment

```$ pipenv shell```

#### Step 4: Clone the fast-food-api repository

[```here```](https://github.com/semainda/store-manager-api) or ```git clone https://github.com/semainda/store-manager-api.git```


#### Step 5: Install project dependances

```$ pipenv install```

### Exporting environment variable

#### For development purposes

```$ export ENV_CONFIG="development"```

#### For testing purposes

```$ export ENV_CONFIG="testing"```

### Running the application

```$ python run.py```

### Running the Tests

```$ pytest app/tests"```

## Login API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST  | /auth/login | Login a user

## Roles API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /roles | Register a new role
GET  | /roles | Get all roles
GET  | /roles/role_id | Get a specific role
PUT  | /roles/role_id | Update a specific role
DEL  | /roles/role_id | Delete a specific role

## Users API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /users | Register a new store user
GET  | /users | Get all store users
GET  | /users/user_id | Get a specific user
GET  | /users/profile | Get a specific user profile

## Users Roles API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST |  /users/roles | Assign a role to an attendant
GET  | /users/roles  | Get users with assigned roles
GET  | /users/roles/user_role_id | Get a specific user role
PUT  | /users/roles/user_role_id | Update a specific user role
PUT  | /users/roles/role_id | Update users roles with a specific role_id

## Product Categories API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /categories | Register a new product category
GET  | /categories | Get all products categories
GET  | /categories/cat_id | Get a specific products category
PUT  | /categories/cat_id | Update a specific product category

## Product Sub-Categories API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /subcategories | Register a new product subcategory
GET  | /subcategories | Get all products subcategories
GET  | /subcategories/sub_id | Get a specific products subcategory
PUT  | /subcategories/sub_id | Update a specific product subcategory

## Products API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /products | Register a new product
GET  | /products | Get all products
GET  | /products/prod_id | Get a specific products

## Sales API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
POST | /sales | Register a new sale order
GET  | /sales | Get all sales orders
GET  | /sales/sale_id | Get a specific sale order

## Sales Summary API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
GET  | /sales/summary | Get all sales detail summary group by attendants
GET  | /sales/summary/user_id | Get sales summary for a particular user
GET  | /sales/sale_id | Get a specific sale summary
GET  | /sales/mysales | Get attendant all sales orders summary

## Store Sales Summary API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
GET  | /sales/store/summary | Get a general summary of all sales

## Product Sales Status API - Endpoints: /api/v2/

Method | Endpoint | Functionality
----| ---- | ---
GET  | /products/status | Get all products sales status
GET  | /products/status/prod_id | Get a particular product sales status
