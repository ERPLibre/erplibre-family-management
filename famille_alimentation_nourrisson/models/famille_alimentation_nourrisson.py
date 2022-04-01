from datetime import timedelta

from odoo import _, api, fields, models


class FamilleAlimentationNourrisson(models.Model):
    _name = "famille.alimentation.nourrisson"
    _inherit = "portal.mixin"
    _description = (
        "Suivi de l'alimentation et de l'élimination chez le bébé nourri au"
        " sein."
    )

    _order = "date_debut desc"

    name = fields.Char(
        compute="_compute_name",
    )

    fin_allaitement_different = fields.Boolean(
        compute="_compute_fin_allaitement_different",
        store=True,
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

    def action_fin_allaitement(self):
        self.write({"date_fin": fields.Datetime.now()})

    def _compute_access_url(self):
        super(FamilleAlimentationNourrisson, self)._compute_access_url()
        for famille_alimentation_nourrisson in self:
            famille_alimentation_nourrisson.access_url = (
                "/my/famille_alimentation_nourrisson/%s"
                % famille_alimentation_nourrisson.id
            )

    @api.depends("date_debut", "date_fin")
    def _compute_fin_allaitement_different(self):
        for record in self:
            date_timedelta = record.date_fin - record.date_debut
            # time is different if it's not 1 hour delta
            record.fin_allaitement_different = (
                date_timedelta.total_seconds() != 3600
            )

    @api.depends("date_debut", "selles", "mictions")
    def _compute_name(self):
        for record in self:
            record.name = str(record.date_debut)
            if record.selles:
                record.name += " SELLE"
            if record.mictions:
                record.name += " MICTION"
