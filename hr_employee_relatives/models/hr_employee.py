from odoo import api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    contract_state = fields.Selection(string="contract state", related="contract_id.state")

    number_of_relatives = fields.Integer(string="Relatives #", compute="compute_number_of_relatives")

    def compute_number_of_relatives(self):
        for rec in self:
            count = 0
            relative_list = self.env['employee.relatives'].search(
                [('employee', '=', rec.id), ('state', '=', 'confirm')]
            )
            if relative_list:
                for relative in relative_list:
                    count += len(relative.relatives)
            rec.number_of_relatives = count
