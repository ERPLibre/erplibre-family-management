import base64
import logging

import werkzeug

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class FamilleAlimentationNourrissonController(http.Controller):
    @http.route(
        "/new/famille_alimentation_nourrisson",
        type="http",
        auth="user",
        website=True,
    )
    def create_new_famille_alimentation_nourrisson(self, **kw):
        name = http.request.env.user.name
        default_commentaire = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["commentaire"])
            .get("commentaire")
        )
        default_date_debut = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["date_debut"])
            .get("date_debut")
        )
        default_date_fin = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["date_fin"])
            .get("date_fin")
        )
        default_mictions = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["mictions"])
            .get("mictions")
        )
        default_selles = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["selles"])
            .get("selles")
        )
        return http.request.render(
            "famille_alimentation_nourrisson.portal_create_famille_alimentation_nourrisson",
            {
                "name": name,
                "page_name": "create_famille_alimentation_nourrisson",
                "default_commentaire": default_commentaire,
                "default_date_debut": default_date_debut,
                "default_date_fin": default_date_fin,
                "default_mictions": default_mictions,
                "default_selles": default_selles,
            },
        )

    @http.route(
        "/submitted/famille_alimentation_nourrisson",
        type="http",
        auth="user",
        website=True,
        csrf=True,
    )
    def submit_famille_alimentation_nourrisson(self, **kw):
        vals = {}

        if kw.get("name"):
            vals["name"] = kw.get("name")

        if kw.get("commentaire"):
            vals["commentaire"] = kw.get("commentaire")

        if kw.get("date_debut"):
            vals["date_debut"] = kw.get("date_debut")

        if kw.get("date_fin"):
            vals["date_fin"] = kw.get("date_fin")

        default_mictions = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["mictions"])
            .get("mictions")
        )
        if kw.get("mictions"):
            vals["mictions"] = kw.get("mictions") == "True"
        elif default_mictions:
            vals["mictions"] = False

        default_selles = (
            http.request.env["famille.alimentation.nourrisson"]
            .default_get(["selles"])
            .get("selles")
        )
        if kw.get("selles"):
            vals["selles"] = kw.get("selles") == "True"
        elif default_selles:
            vals["selles"] = False

        new_famille_alimentation_nourrisson = (
            request.env["famille.alimentation.nourrisson"].sudo().create(vals)
        )
        return werkzeug.utils.redirect(
            f"/my/famille_alimentation_nourrisson/{new_famille_alimentation_nourrisson.id}"
        )
