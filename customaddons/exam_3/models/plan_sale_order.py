from odoo import models, fields, api
from odoo.exceptions import UserError


class PlanSaleOrder(models.Model):
    _name = 'plan.sale.order'
    _description = 'Plan Sale Order'
    _inherit = ['mail.thread']

    name = fields.Text(required=True, tracking=True)
    quotation = fields.Many2one('sale.order', store=True, required=True)
    content = fields.Text(string='Content of the quotations', required=True, tracking=True)

    state = fields.Selection([
        ('unknown', 'Unknown'),
        ('new', 'New'),
        ('send', 'Send'),
        ('approve', 'Approve'),
        ('refuse', 'Refuse'),
    ], string='State of quotation', readonly=True, tracking=True, default='unknown')

    order_line = fields.One2many('plan.sale.order.list', 'order_id', string='Order Lines', tracking=True)
    can_confirm = fields.Selection([('yes', 'Yes'), ('no', 'No'), ('new', 'New')], tracking=True)

    # Button set up new plan
    def btn_new(self):
        self.state = 'new'
        self.order_line.approval_status = 'unavailable'
        self.can_confirm = 'new'

    # Button send plan for supreme approver
    def btn_send(self):

        mess_send = 'The new plan has been sent to the person in charge by email on %s . Created by %s.' \
                    % (fields.Datetime.now(), self.create_uid.name)

        if self.state == 'new':
            if self.order_line.approver:
                self.state = 'send'
                self.message_post(subject='Send to Approver', body=mess_send, message_type='notification',
                                  partner_ids=self.order_line.approver.ids)
            else:
                raise UserError('This plan does not have any approvers.')
        else:
            raise UserError('Cannot send this approver.'
                            ' Maybe you sent gmail before. Please press New button to create a new plan and try again.')

    # Button confirm approve (for supreme approver)
    def btn_confirm_approve(self):

        mess_approve = "The new plan of %s has been approved on %s" % (self.create_uid.name, fields.Datetime.now())

        if self.can_confirm == 'yes':
            if self.order_line.approver:
                self.state = 'approve'
                self.message_post(subject='Approve New Plan', body=mess_approve)
            else:
                raise UserError('Please write your approvers.')
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')

    # Button confirm refuse (for supreme approver)
    def btn_confirm_refuse(self):

        mess_refuse = "The new plan of %s has been refused on %s" % (self.create_uid.name, fields.Datetime.now())

        if self.can_confirm == 'no':
            self.state = 'refuse'
            self.message_post(subject='Refuse New Plan', body=mess_refuse)
        else:
            raise UserError('Cannot confirm this approve. Please check your data.')

    def unlink(self):
        for r in self:
            valid_list = ['approve', 'send']
            # if r.state == 'approve' or r.state == 'send':
            #     raise UserError("You cannot delete this plan sale order in Approve state or Send state.")
            if r.state in valid_list:
                raise UserError("You cannot delete this plan sale order in Approve state or Send state.")
        return super(PlanSaleOrder, self).unlink()

    @api.model
    def create(self, vals):
        if vals.get('name'):
            vals['name'] = vals['name'].title()
        return super(PlanSaleOrder, self).create(vals)

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(PlanSaleOrder, self).write(vals)

    def copy(self, default={}):
        default['name'] = 'Clone of' + ' ' + self.name
        default['content'] = 'Clone of' + ' ' + self.content
        return super(PlanSaleOrder, self).copy(default=default)

    # @api.model
    # def default_get(self, fields_list=[]):
    #     print('call out default_get function')
    #     res = super(PlanSaleOrder, self).default_get(fields_list)
    #     res['name'] = "Name of quotation - Name of creator"
    #     res['content'] = 'Plan sale order of + name of quotation + details of content'
    #     return res
