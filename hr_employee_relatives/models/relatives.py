from datetime import date

from odoo import models, fields, api


class Relatives(models.Model):
    _name = "relatives.relatives"

    employee_rel_id = fields.Many2one('employee.relatives',
                                      ondelete='cascade', string="Employee")

    name = fields.Char(string="Name", required=False, )
    degree_of_relation = fields.Selection([('father', 'Father'),
                                           ('mother', ' Mother'),
                                           ('husband', 'Husband'),
                                           ('wife', 'Wife'),
                                           ('son', 'Son'),
                                           ('daughter', 'Daughter')
                                           ], string='Degree of relation', required=True, defualt='Father')
    birth_date = fields.Date()
    age = fields.Integer(string="Age", compute='_compute_age')

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year
            else:
                rec.age = 0
