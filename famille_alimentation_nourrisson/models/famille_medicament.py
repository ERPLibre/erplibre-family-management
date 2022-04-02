from odoo import _, api, fields, models


class FamilleMedicament(models.Model):
    _name = "famille.medicament"
    _inherit = "portal.mixin"
    _description = "famille_medicament"

    name = fields.Char()

    def _compute_access_url(self):
        super(FamilleMedicament, self)._compute_access_url()
        for famille_medicament in self:
            famille_medicament.access_url = (
                "/my/famille_medicament/%s" % famille_medicament.id
            )
