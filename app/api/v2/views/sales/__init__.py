from flask import Flask, Blueprint
from flask_restful import Api
from .categories import Categories, CategoriesActivity
from .sub_categories import SubCategories, SubCategoriesActivity
from .products import Products, ProductsActivity
from .sales import Sales, SalesActivity
from .sales_summary import SalesSummary, SalesSummaryActivity,\
UserSalesSummary, StoreSalesSummary
from .sales import UserSales, UserSalesActivity
from .product_status import ProductStatus, ProductStatusActivity

sales_blueprint = Blueprint("sales", __name__, url_prefix="/api/v2")
api = Api(sales_blueprint)
api.add_resource(Categories, "/categories")
api.add_resource(CategoriesActivity, "/categories/<int:cat_id>")
api.add_resource(SubCategories, "/subcategories")
api.add_resource(SubCategoriesActivity, "/subcategories/<int:sub_id>")
api.add_resource(Products, "/products")
api.add_resource(ProductsActivity, "/products/<int:prod_id>")
api.add_resource(Sales, "/sales")
api.add_resource(SalesActivity, "/sales/<int:user_id>")

# returns attendant sales given
api.add_resource(UserSales, "/user/sales")
# returns attendant specific sale given sale_id
api.add_resource(UserSalesActivity, "/user/sales/<int:sale_id>")
api.add_resource(ProductStatus, "/products/status")
api.add_resource(ProductStatusActivity, "/products/status/<int:prod_id>")
# sales summary for all attendants
api.add_resource(SalesSummary, "/sales/summary")
# sales summary for specific attendant
api.add_resource(SalesSummaryActivity, "/sales/summary/<int:user_id>")
# sales summary for own attendant
api.add_resource(UserSalesSummary, "/sales/mysales")
# return a sales summary for the whole store 
api.add_resource(StoreSalesSummary, "/sales/store/summary")
