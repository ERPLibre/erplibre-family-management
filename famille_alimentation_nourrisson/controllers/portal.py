from collections import OrderedDict
from operator import itemgetter

from odoo import _, http
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.portal.controllers.portal import pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.osv.expression import OR
from odoo.tools import groupby as groupbyelem


class FamilleAlimentationNourrissonController(CustomerPortal):
    def _prepare_portal_layout_values(self):
        values = super(
            FamilleAlimentationNourrissonController, self
        )._prepare_portal_layout_values()
        values["famille_alimentation_nourrisson_count"] = request.env[
            "famille.alimentation.nourrisson"
        ].search_count([])
        return values

    # ------------------------------------------------------------
    # My Famille Alimentation Nourrisson
    # ------------------------------------------------------------
    def _famille_alimentation_nourrisson_get_page_view_values(
        self, famille_alimentation_nourrisson, access_token, **kwargs
    ):
        values = {
            "page_name": "famille_alimentation_nourrisson",
            "famille_alimentation_nourrisson": famille_alimentation_nourrisson,
            "user": request.env.user,
        }
        return self._get_page_view_values(
            famille_alimentation_nourrisson,
            access_token,
            values,
            "my_famille_alimentation_nourrissons_history",
            False,
            **kwargs,
        )

    @http.route(
        [
            "/my/famille_alimentation_nourrissons",
            "/my/famille_alimentation_nourrissons/page/<int:page>",
        ],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_famille_alimentation_nourrissons(
        self,
        page=1,
        date_begin=None,
        date_end=None,
        sortby=None,
        filterby=None,
        search=None,
        search_in="content",
        **kw,
    ):
        values = self._prepare_portal_layout_values()
        FamilleAlimentationNourrisson = request.env[
            "famille.alimentation.nourrisson"
        ]
        domain = []

        searchbar_sortings = {
            "date": {"label": _("Newest"), "order": "create_date desc"},
            "name": {"label": _("Name"), "order": "name"},
        }
        searchbar_filters = {
            "all": {"label": _("All"), "domain": []},
        }
        searchbar_inputs = {}
        searchbar_groupby = {}

        # default sort by value
        if not sortby:
            sortby = "date"
        order = searchbar_sortings[sortby]["order"]
        # default filter by value
        if not filterby:
            filterby = "all"
        domain = searchbar_filters[filterby]["domain"]

        # search
        if search and search_in:
            search_domain = []
            domain += search_domain
        # archive groups - Default Group By 'create_date'
        archive_groups = self._get_archive_groups(
            "famille.alimentation.nourrisson", domain
        )
        if date_begin and date_end:
            domain += [
                ("create_date", ">", date_begin),
                ("create_date", "<=", date_end),
            ]
        # famille_alimentation_nourrissons count
        famille_alimentation_nourrisson_count = (
            FamilleAlimentationNourrisson.search_count(domain)
        )
        # pager
        pager = portal_pager(
            url="/my/famille_alimentation_nourrissons",
            url_args={
                "date_begin": date_begin,
                "date_end": date_end,
                "sortby": sortby,
                "filterby": filterby,
                "search_in": search_in,
                "search": search,
            },
            total=famille_alimentation_nourrisson_count,
            page=page,
            step=self._items_per_page,
        )

        # content according to pager and archive selected
        famille_alimentation_nourrissons = (
            FamilleAlimentationNourrisson.search(
                domain,
                order=order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session[
            "my_famille_alimentation_nourrissons_history"
        ] = famille_alimentation_nourrissons.ids[:100]

        values.update(
            {
                "date": date_begin,
                "date_end": date_end,
                "famille_alimentation_nourrissons": famille_alimentation_nourrissons,
                "page_name": "famille_alimentation_nourrisson",
                "archive_groups": archive_groups,
                "default_url": "/my/famille_alimentation_nourrissons",
                "pager": pager,
                "searchbar_sortings": searchbar_sortings,
                "searchbar_groupby": searchbar_groupby,
                "searchbar_inputs": searchbar_inputs,
                "search_in": search_in,
                "searchbar_filters": OrderedDict(
                    sorted(searchbar_filters.items())
                ),
                "sortby": sortby,
                "filterby": filterby,
            }
        )
        return request.render(
            "famille_alimentation_nourrisson.portal_my_famille_alimentation_nourrissons",
            values,
        )

    @http.route(
        [
            "/my/famille_alimentation_nourrisson/<int:famille_alimentation_nourrisson_id>"
        ],
        type="http",
        auth="public",
        website=True,
    )
    def portal_my_famille_alimentation_nourrisson(
        self, famille_alimentation_nourrisson_id=None, access_token=None, **kw
    ):
        try:
            famille_alimentation_nourrisson_sudo = self._document_check_access(
                "famille.alimentation.nourrisson",
                famille_alimentation_nourrisson_id,
                access_token,
            )
        except (AccessError, MissingError):
            return request.redirect("/my")

        values = self._famille_alimentation_nourrisson_get_page_view_values(
            famille_alimentation_nourrisson_sudo, access_token, **kw
        )
        return request.render(
            "famille_alimentation_nourrisson.portal_my_famille_alimentation_nourrisson",
            values,
        )
