# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date


class EmployeeRelatives(models.Model):
    _name = "employee.relatives"
    _description = "employee.relatives"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee = fields.Many2one('hr.employee',
                               ondelete='cascade', string="Employee ", required=True,
                               )

    phone = fields.Char(string="Employee phone", related='employee.work_phone')

    num_of_relatives = fields.Integer(string="Number of relatives", compute="compute_no_of_relatives")
    relatives = fields.One2many(comodel_name="relatives.relatives", inverse_name="employee_rel_id", string="Relatives")

    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('done', 'Ended'),
                              ('cancel', 'Canceled')],
                             string='Status', tracking=True, readonly=True, default='draft')

    last_user_id = fields.Many2one(comodel_name="res.users", string="Last changes by")
    color = fields.Integer()

    @api.model
    def check_end_date(self):
        for rec in self.search([]):
            if rec.employee.contract_id.date_end and rec.employee.contract_id.date_end <= date.today():
                rec.state = 'done'

    @api.depends('relatives')
    def compute_no_of_relatives(self):
        self.num_of_relatives = len(self.relatives)

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'
            rec.last_user_id = self.env.user.id

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            rec.last_user_id = self.env.user.id

    def action_done(self):
        for rec in self:
            rec.state = 'done'
            rec.last_user_id = self.env.user.id

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
            rec.last_user_id = self.env.user.id
