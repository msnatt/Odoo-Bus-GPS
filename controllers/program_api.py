import json
import base64
from odoo import http
from odoo.http import request, Response


class GetProductAPI(http.Controller):
    @http.route('/appapi/getproduct/list', type='json', csrf=True,  website=True, methods=['GET'], auth='public')
    def product_list(self,  **kw):
        name = kw.get('name')
        print("data value name product:",  name)

        if name:
            products = request.env['product.template'].sudo().search([
                '|',
                ('default_code', 'ilike', '%' + name + '%'),
                ('name', 'ilike', '%' + name + '%')
            ])
        else:
            products = request.env['product.template'].sudo().search([])
        print("data value:", name, products)
        rows = []
        for p in products:

            data = {
                'code': p.default_code,
                'name': p.name,
                'barcode': p.barcode,
                'sale_price': p.list_price,
                'cost_price': p.standard_price,

            }
            rows.append(data)
        print("data value:", rows)
        return rows


    @http.route('/appapi/product/add', methods=['POST'], type='json', csrf=True, auth='public')
    def product_add(self, **kwargs):
        product = http.request.params
        print("data value:",  product)
        request.env['product.template'].sudo().create({
            'name': product['name'],
            'list_price': product['sale_price'],
        })
        return json.dumps({'result': 'Success'})