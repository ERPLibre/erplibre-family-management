from odoo import _, api, fields, models


class FamilleMedicamentNourisson(models.Model):
    _name = "famille.medicament.nourisson"
    _inherit = "portal.mixin"
    _description = "famille_medicament_nourisson"

    name = fields.Char()

    def _compute_access_url(self):
        super(FamilleMedicamentNourisson, self)._compute_access_url()
        for famille_medicament_nourisson in self:
            famille_medicament_nourisson.access_url = (
                "/my/famille_medicament_nourisson/%s"
                % famille_medicament_nourisson.id
            )
