from odoo import http
from odoo.http import route, request
from werkzeug import utils
import json


class MyController(http.Controller):
    @http.route('/customer', auth='public', website=True)
    def customer(self, **kw):
        custs = request.env['station'].sudo().search([])
        return http.request.render('web_api.index', {'custs': custs})

    @http.route('/customer/add', auth='public', methods=['POST'], csrf=False, website=True)
    def customer_add(self, **kw):
        http.request.env['res.partner'].sudo().create({
            'name': kw['txt_name'],
            'street': kw['txt_address'],
        })
        return utils.redirect('/customer')

    @route('/customer/edit', auth='public', csrf=False, website=True)
    def customer_edit(self):
        id = request.params.get('id')
        print('id=', id)
        allbus = request.env['locate'].sudo().search([])
        # data_id = request.env['res.partner'].sudo().search([('id', '=', id)])
        # print('data=', data_id)
        # customer_name = data_id.name
        # locate_id = request.env['locate'].sudo().search([('name', 'ilike', customer_name)], limit=1)
        # lon = locate_id.longtitude
        # lat = locate_id.latitude
        return http.request.render('web_api.customer_update', {
            'allbus': allbus
            # 'data': data_id,
            # 'lon': lon,
            # 'lat': lat
        })

    @http.route('/customer/update', auth='public', methods=['POST'], csrf=False, website=True)
    def product_update(self, **kw):

        name = kw['txt_name']
        bus = request.env['locate'].sudo().search([('name', '=', name)])
        allbus = request.env['locate'].sudo().search([])
        txt_latitude = bus.latitude
        txt_longtitude = bus.longtitude
        return http.request.render('web_api.customer_update', {'bus': bus, 'allbus': allbus})


        return http.request.render('your_module.customer_update', {
            'bus_data_json': bus_data_json,  # Pass JSON data to template
        })

    #################START API GPS  ###################################
    @http.route('/update_location', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    def update_location(self, **kwargs):
        data = http.request.params
        # search name and update
        rec = request.env['locate'].sudo().search([('name', '=', data['name'])])
        if rec:
            updata = {
                'latitude': data['latitude'],
                'longtitude': data['longtitude'],
            }
            rec.sudo().write(updata)
            rec02 = request.env['station'].sudo().search([('bus_name', '=', data['name'])])

            if rec02:
                updata = {
                    'bus_name': data['name'],
                    'bus_latitude': data['latitude'],
                    'bus_longtitude': data['longtitude'],

                }
                rec02.sudo().write(updata)

        args = {
            'message': 'success',
            'success': 'True',
            'name': data['name'],
            'latitude': data['latitude'],
            'longtitude': data['longtitude']
        }
        print(args)
        return args

    @http.route('/get_location', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    def get_location(self):
        # รับข้อมูลจาก request body ในรูปแบบ JSON
        data = json.loads(http.request.httprequest.get_data())
        name = data.get('name')
        print("Received Bus Name: ", name)  # แสดงค่า name ที่ได้รับจาก client-side

        # ค้นหาข้อมูลจากฐานข้อมูลที่มีชื่อเป็น 'name' ที่รับมาจาก request
        rec = request.env['locate'].sudo().search([('name', '=', name)], limit=1)
        if rec:
            # หากเจอ record ให้ส่งข้อมูล latitude และ longitude กลับไป
            updata = {
                'latitude': rec.latitude,
                'longtitude': rec.longtitude,
            }
            print("Location :", updata)  # แสดงข้อมูล latitude, longitude

            return json.dumps(updata)
        else:
            return json.dumps({'Name': name})

    @http.route('/display/station', auth='public', methods=['GET','POST'], csrf=False, website=True)
    def display_station(self, **kw):

        return http.request.render('web_api.display_station')

    @http.route('/update_passenger', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    def update_passenger(self, **kwargs):
        data = http.request.params
        print("data value:", data)
        # search name and update
        rec = request.env['station'].sudo().search([('name', '=', data['name'])])

        if rec:
            passenger = rec.total_passenger + 1
            updata = {
                'latitude': data['latitude'],
                'longtitude': data['longtitude'],
                'total_passenger': passenger,
            }
            rec.sudo().write(updata)

        args = {
            'meaasge': 'success',
            'success': 'True',
            'data':
                {

                    'name': data['name']
                },
        }
        return args

    # @http.route('/update_bus_location', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    # def update_bus_location(self, **kwargs):
    #     data = http.request.params
    #     print("data value:", data)
    #     # search name and update
    #     rec = request.env['station'].sudo().search()
    #
    #     if rec:
    #
    #         updata = {
    #             'bus_latitude': data['latitude'],
    #             'bus_longtitude': data['longtitude'],
    #
    #         }
    #         rec.sudo().write(updata)
    #
    #     args = {
    #         'meaasge': 'success',
    #         'success': 'True',
    #         'data':
    #             {
    #
    #                 'name': data['name']
    #             },
    #     }
    #     return args
    @http.route('/check_pin', type="json", auth='public', methods=['POST'], csrf=False)
    def check_pin01(self):
        data = http.request.params
        if not data['pin']:
            raise Exception("Parameter pin not found.")

        # get all teachers
        get_rec = request.env['hr.employee'].sudo().search([('pin', '=', data['pin'])], limit=1, order="id desc")
        res_msg = []
        for rec in get_rec:
            res_msg.append({
                'id': rec.id,

                'message': 'found',

            })
        if not res_msg:
            res_msg.append({
                'id': 'NO',
                'code': 'NO',
                'message': 'NO',
            })
        return res_msg

    @http.route('/get_bus', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    def get_bus(self, **kwargs):
        data = http.request.params
        print("data value:", data)
        # search name and update
        rec = request.env['locate'].sudo().search([('name', '=', data['name'])])

        if rec:
            name = rec.name
            latitude = rec.latitude
            longtitude = rec.longtitude

        args = {
            'meaasge': 'success',
            'success': 'True',
            'data':
                {
                    'name': name,
                    'latitude': latitude,
                    'longtitude': longtitude,
                },
        }
        return args

    @http.route('/get_passenger', type="json", auth='public', methods=['POST'], csrf=False, website=True)
    def get_passenger(self, **kwargs):
        data = http.request.params
        print("data value:", data)
        # search name and update
        rec = request.env['station'].sudo().search([('name', '=', data['name'])])

        if rec:
            name = rec.name
            passenger = rec.total_passenger

        args = {
            'meaasge': 'success',
            'success': 'True',
            'data':
                {
                    'name': name,
                    'passenger': passenger,

                },
        }
        return args

    #################END API GPS  ###################################
    @http.route('/customer/delete', auth='public', csrf=False, website=True)
    def customer_delete(self, **kw):
        id = request.params.get('id')
        http.request.env['res.partner'].search([('id', '=', id)]).sudo().unlink()
        # print(kw['txt_name'])
        return utils.redirect('/customer')

    class LongdoMapController(http.Controller):
        @http.route('/longdo_map', type='http', auth='public', website=True)
        def longdo_map(self, **kwargs):
            return http.request.render('web_api.longdo_map_page', {})

    class CustomerController(http.Controller):

        @http.route('/reset_customer_values/<int:customer_id>', type='http', auth='public', methods=['GET'])
        def reset_customer_values(self, customer_id):
            # ค้นหาบันทึกลูกค้าในฐานข้อมูลโดยใช้ customer_id
            customer = request.env['station'].sudo().browse(customer_id)

            if customer:
                # รีเซ็ตค่าของ total_passenger, latitude และ longitude
                customer.update({
                    'total_passenger': 0,
                    'latitude': 0.0,
                    'longtitude': 0.0,
                })
                # ทำการรีเฟรชหน้าจอหลังการรีเซ็ต
                return request.redirect('/customer')  # เปลี่ยน URL ตามที่คุณต้องการแสดง
            return "ไม่พบข้อมูลลูกค้าหรือเกิดข้อผิดพลาด"
