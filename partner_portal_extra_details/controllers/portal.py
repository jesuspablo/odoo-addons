# -*- coding: utf-8 -*-

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.http import request, route


class RayitoCustomerPortal(CustomerPortal):

    MANDATORY_BILLING_FIELDS = [
        "birthdate_date",
        "city",
        "country_id",
        "email",
        "gender",
        "name",
        "phone",
        "street",
        "tutor_phone",
        "tutor_name",
        "vat",
    ]
    OPTIONAL_BILLING_FIELDS = [
        "company_name",
        "state_id",
        "zipcode",
    ]

    def _get_mandatory_billing_fields(self):
        MANDATORY_BILLING_FIELDS = [
            "birthdate_date",
            "city",
            "country_id",
            "email",
            "gender",
            "name",
            "phone",
            "street",
            "tutor_phone",
            "tutor_name",
            "vat",
        ]
        return MANDATORY_BILLING_FIELDS

    def _get_optional_billing_fields(self):
        OPTIONAL_BILLING_FIELDS = [
            "company_name",
            "state_id",
            "zipcode",
        ]
        return OPTIONAL_BILLING_FIELDS

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post:
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {
                    key: post[key]
                    for key in self._get_mandatory_billing_fields()}
                values.update(
                    {
                        key: post[key]
                        for key in self._get_optional_billing_fields()
                        if key in post
                    }
                )
                values.update({'zip': values.pop('zipcode', '')})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response
