from datetime import timedelta

from odoo import _, api, fields, models


class FamilleAlimentationNourrisson(models.Model):
    _name = "famille.alimentation.nourrisson"
    _inherit = "portal.mixin"
    _description = (
        "Suivi de l'alimentation et de l'élimination chez le bébé nourri au"
        " sein."
    )

    name = fields.Char(
        compute="_compute_name",
    )

    commentaire = fields.Text(
        string="Allaitement",
        help=(
            "Commentaire au besoin. (ex : bébé dort, tête bien, tête par"
            " intervalles)"
        ),
    )

    date_debut = fields.Datetime(
        string="Date début",
        required=True,
        default=lambda self: fields.Datetime.now(),
    )

    date_fin = fields.Datetime(
        string="Date fin",
        default=lambda self: fields.Datetime.now() + timedelta(hours=1),
    )

    selles = fields.Boolean(
        help="Le bébé a fait des selles avant/durant l'allaitement."
    )

    mictions = fields.Boolean(
        help="Le bébé a fait des mictions avant/durant l'allaitement."
    )

    def _compute_access_url(self):
        super(FamilleAlimentationNourrisson, self)._compute_access_url()
        for famille_alimentation_nourrisson in self:
            famille_alimentation_nourrisson.access_url = (
                "/my/famille_alimentation_nourrisson/%s"
                % famille_alimentation_nourrisson.id
            )

    @api.depends("date_debut", "selles", "mictions")
    def _compute_name(self):
        for record in self:
            record.name = (
                f"{record.date_debut} S {record.selles} M {record.mictions}"
            )
