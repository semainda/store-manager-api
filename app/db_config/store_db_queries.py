"""This module contains SQL Queries for both CREATE and DROP database tables for API_V2"""
# Create database queries
roles = """CREATE TABLE IF NOT EXISTS roles(
                    role_id serial PRIMARY KEY,
                    role_name  varchar(50) NOT NULL);"""

users = """CREATE TABLE IF NOT EXISTS users(
                    user_id serial PRIMARY KEY,
                    first_name varchar(30) NOT NULL,
                    last_name varchar(30) NOT NULL,
                    email varchar(30) UNIQUE NOT NULL,
                    user_name  varchar(30) UNIQUE NOT NULL,
                    password text NOT NULL,
                    created_at date NOT NULL);"""

user_roles = """CREATE TABLE IF NOT EXISTS user_roles(
                    role_id int REFERENCES roles(role_id) ON DELETE CASCADE,
                    user_id int REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE(role_id, user_id));"""

categories = """CREATE TABLE IF NOT EXISTS categories(
                    cat_id serial PRIMARY KEY,
                    cat_name varchar(50) UNIQUE NOT NULL);"""

subcategories = """CREATE TABLE IF NOT EXISTS sub_categories(
                    sub_id serial PRIMARY KEY,
                    sub_name varchar(50) UNIQUE NOT NULL,
                    cat_id int REFERENCES categories(cat_id) ON DELETE CASCADE);"""


products = """CREATE TABLE IF NOT EXISTS products(
                    p_id serial PRIMARY KEY,
                    prod_name varchar(50) NOT NULL,
                    qty int NOT NULL,
                    size varchar(20) NOT NULL,
                    price  int  NOT NULL,
                    cat_id int REFERENCES categories(cat_id) ON DELETE CASCADE,
                    sub_id int REFERENCES sub_categories(sub_id) ON DELETE CASCADE
                    );"""

sales = """CREATE TABLE IF NOT EXISTS sales(
                    sale_id serial PRIMARY KEY,
                    user_id int REFERENCES users(user_id) ON DELETE CASCADE,
                    created_date date NOT NULL,
                    UNIQUE(user_id, created_date));"""

sales_transactions = """CREATE TABLE IF NOT EXISTS sales_transactions(
                    trans_id serial PRIMARY KEY,
                    sale_id int REFERENCES sales(sale_id) ON DELETE RESTRICT,
                    p_id int  REFERENCES products(p_id) ON DELETE RESTRICT,
                    sold_qty int NOT NULL);"""

product_status = """CREATE TABLE IF NOT EXISTS product_status(
                p_id int  REFERENCES products(p_id) ON DELETE RESTRICT,
                stock_qty int  DEFAULT 0 NOT NULL,
                sold_qty  int DEFAULT 0 NOT NULL,
                remain_qty int DEFAULT -1 NOT NULL,
                PRIMARY KEY(p_id));"""

import os, json
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as hash256

admin = json.loads(os.getenv("ADMIN_CONFIG"))
created_date = datetime.now().strftime("%Y-%m-%d")

sql ="""WITH role AS(
                    INSERT INTO roles(role_name) VALUES(%s) RETURNING role_id
                ), new_user AS(
                    INSERT INTO users(first_name, last_name, email, user_name,
                    password, created_at)
                SELECT %s, %s, %s, %s, %s, %s RETURNING user_id
                )
                INSERT INTO user_roles(role_id, user_id)
                SELECT role.role_id, new_user.user_id FROM role, new_user;"""
sql_val = (
    admin["role_name"], admin["first_name"],
    admin["last_name"], admin["email"], admin["user_name"],
    hash256.hash(admin["password"]), created_date)

admin = [sql, sql_val]


create_table_queries = [
    roles, users, user_roles, categories, subcategories,
    products, sales, sales_transactions, product_status, admin
]

# Drop database queries
roles ="DROP TABLE IF EXISTS roles CASCADE;"
users ="DROP TABLE IF EXISTS users CASCADE;"
user_roles ="DROP TABLE IF EXISTS user_roles CASCADE;"
categories ="DROP TABLE IF EXISTS categories CASCADE;"
subcategories ="DROP TABLE IF EXISTS sub_categories CASCADE;"
products ="DROP TABLE IF EXISTS products CASCADE;"
sales ="DROP TABLE IF EXISTS sales CASCADE;"
sales_transactions ="DROP TABLE IF EXISTS sales_transactions CASCADE;"
product_status ="DROP TABLE IF EXISTS product_status CASCADE;"

drop_table_queries = [
    roles, users, user_roles, categories, subcategories,
    products, sales, sales_transactions, product_status
]