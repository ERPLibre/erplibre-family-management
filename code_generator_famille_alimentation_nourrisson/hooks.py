import logging
import os

from odoo import SUPERUSER_ID, _, api, fields, models

_logger = logging.getLogger(__name__)

MODULE_NAME = "famille_alimentation_nourrisson"


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        # The path of the actual file
        path_module_generate = (
            "./addons/MathBenTech_erplibre-family-management"
        )

        short_name = MODULE_NAME.replace("_", " ").title()

        # Add code generator
        categ_id = env["ir.module.category"].search(
            [("name", "=", "Uncategorized")], limit=1
        )
        value = {
            "shortdesc": short_name,
            "name": MODULE_NAME,
            "license": "AGPL-3",
            "category_id": categ_id.id,
            "summary": "",
            "author": "TechnoLibre",
            "website": "https://technolibre.ca",
            "application": True,
            "enable_sync_code": True,
            "path_sync_code": path_module_generate,
            "icon": os.path.join(
                os.path.dirname(__file__),
                "static",
                "description",
                "code_generator_icon.png",
            ),
        }

        # TODO HUMAN: enable your functionality to generate
        value["enable_sync_template"] = True
        value["ignore_fields"] = ""
        value["post_init_hook_show"] = False
        value["uninstall_hook_show"] = False
        value["post_init_hook_feature_code_generator"] = False
        value["uninstall_hook_feature_code_generator"] = False

        value["hook_constant_code"] = f'MODULE_NAME = "{MODULE_NAME}"'

        code_generator_id = env["code.generator.module"].create(value)

        # Add dependencies
        code_generator_id.add_module_dependency("portal")

        # Add/Update Famille Alimentation Nourrisson
        model_model = "famille.alimentation.nourrisson"
        model_name = "famille_alimentation_nourrisson"
        lst_depend_model = ["portal.mixin"]
        dct_model = {
            "description": (
                "Suivi de l'alimentation et de l'élimination chez le bébé"
                " nourri au sein."
            ),
        }
        dct_field = {
            "commentaire": {
                "code_generator_form_simple_view_sequence": 10,
                "code_generator_sequence": 4,
                "code_generator_tree_view_sequence": 10,
                "field_description": "Allaitement",
                "help": (
                    "Commentaire au besoin. (ex : bébé dort, tête bien, tête"
                    " par intervalles)"
                ),
                "ttype": "text",
            },
            "date_debut": {
                "code_generator_form_simple_view_sequence": 11,
                "code_generator_sequence": 5,
                "code_generator_tree_view_sequence": 11,
                "default_lambda": "lambda self: fields.Datetime.now()",
                "field_description": "Date début",
                "required": True,
                "ttype": "datetime",
            },
            "date_fin": {
                "code_generator_form_simple_view_sequence": 12,
                "code_generator_sequence": 6,
                "code_generator_tree_view_sequence": 12,
                "default_lambda": (
                    "lambda self: fields.Datetime.now() + timedelta(hours=1)"
                ),
                "field_description": "Date fin",
                "ttype": "datetime",
            },
            "mictions": {
                "code_generator_form_simple_view_sequence": 13,
                "code_generator_sequence": 8,
                "code_generator_tree_view_sequence": 13,
                "field_description": "Mictions",
                "help": (
                    "Le bébé a fait des mictions avant/durant l'allaitement."
                ),
                "ttype": "boolean",
            },
            "name": {
                "code_generator_compute": "_compute_name",
                "code_generator_sequence": 3,
                "field_description": "Name",
                "store": True,
                "ttype": "char",
            },
            "selles": {
                "code_generator_form_simple_view_sequence": 14,
                "code_generator_sequence": 7,
                "code_generator_tree_view_sequence": 14,
                "field_description": "Selles",
                "help": (
                    "Le bébé a fait des selles avant/durant l'allaitement."
                ),
                "ttype": "boolean",
            },
        }
        model_famille_alimentation_nourrisson = (
            code_generator_id.add_update_model(
                model_model,
                model_name,
                dct_field=dct_field,
                dct_model=dct_model,
                lst_depend_model=lst_depend_model,
            )
        )

        # Generate code
        if True:
            # Generate code header
            value = {
                "code": """from datetime import timedelta

from odoo import _, api, fields, models""",
                "name": "header",
                "m2o_module": code_generator_id.id,
                "m2o_model": model_famille_alimentation_nourrisson.id,
            }
            env["code.generator.model.code.import"].create(value)

            # Generate code model
            lst_value = [
                {
                    "code": """super(FamilleAlimentationNourrisson, self)._compute_access_url()
for famille_alimentation_nourrisson in self:
    famille_alimentation_nourrisson.access_url = (
        "/my/famille_alimentation_nourrisson/%s"
        % famille_alimentation_nourrisson.id
    )""",
                    "name": "_compute_access_url",
                    "param": "self",
                    "sequence": 0,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                },
                {
                    "code": """for record in self:
    record.code = (
        f"{record.date_debut} S {record.selles} M {record.mictions}"
    )""",
                    "name": "_compute_name",
                    "decorator": (
                        '@api.depends("date_debut", "selles", "mictions")'
                    ),
                    "param": "self",
                    "sequence": 1,
                    "m2o_module": code_generator_id.id,
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                },
            ]
            env["code.generator.model.code"].create(lst_value)

        # Generate view
        lst_view_id = []
        # form view
        if True:
            lst_item_view = []
            # BODY
            view_item_body_group_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_group_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "parent_id": view_item_body_group_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_group_2 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item_body_group_2.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "parent_id": view_item_body_group_2.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_group_3 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item_body_group_3.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "parent_id": view_item_body_group_3.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_group_4 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item_body_group_4.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "mictions",
                    "action_name": "mictions",
                    "parent_id": view_item_body_group_4.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_group_5 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "group",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item_body_group_5.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "selles",
                    "action_name": "selles",
                    "parent_id": view_item_body_group_5.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "form",
                    "view_name": "famille_alimentation_nourrisson_form",
                    "view_attr_string": "Titre",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "has_body_sheet": True,
                    "id_name": "famille_alimentation_nourrisson_view_form",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # graph view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "mictions",
                    "action_name": "mictions",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "selles",
                    "action_name": "selles",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "graph",
                    "view_name": "famille_alimentation_nourrisson_graph",
                    "view_attr_string": "Famille alimentation nourrisson",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "famille_alimentation_nourrisson_view_graph",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # kanban view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "mictions",
                    "action_name": "mictions",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "selles",
                    "action_name": "selles",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_templates_6 = env[
                "code.generator.view.item"
            ].create(
                {
                    "section_type": "body",
                    "item_type": "templates",
                    "sequence": 6,
                }
            )
            lst_item_view.append(view_item_body_templates_6.id)

            view_item_body_t_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "t",
                    "t_name": "kanban-box",
                    "parent_id": view_item_body_templates_6.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_t_1.id)

            view_item_body_div_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "div",
                    "t_attf_class": "oe_kanban_global_click",
                    "parent_id": view_item_body_t_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_div_1.id)

            view_item_body_div_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "div",
                    "class_attr": "oe_kanban_details",
                    "parent_id": view_item_body_div_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_div_1.id)

            view_item_body_ul_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "ul",
                    "parent_id": view_item_body_div_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_ul_1.id)

            view_item_body_li_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "class_attr": "mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_li_1.id)

            view_item_body_strong_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "strong",
                    "parent_id": view_item_body_li_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_strong_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "parent_id": view_item_body_strong_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_2 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "class_attr": "mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item_body_li_2.id)

            view_item_body_strong_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "strong",
                    "parent_id": view_item_body_li_2.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_strong_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "parent_id": view_item_body_strong_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_3 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "class_attr": "mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item_body_li_3.id)

            view_item_body_strong_1 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "strong",
                    "parent_id": view_item_body_li_3.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item_body_strong_1.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "parent_id": view_item_body_strong_1.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_4 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "t_if": "record.mictions.raw_value",
                    "class_attr": "text-success float-right mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item_body_li_4.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "i",
                    "title": "Ok",
                    "aria_label": "Ok",
                    "role": "img",
                    "class_attr": "fa fa-circle",
                    "parent_id": view_item_body_li_4.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_5 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "t_if": "!record.mictions.raw_value",
                    "class_attr": "text-danger float-right mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item_body_li_5.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "i",
                    "title": "Invalid",
                    "aria_label": "Invalid",
                    "role": "img",
                    "class_attr": "fa fa-circle",
                    "parent_id": view_item_body_li_5.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_6 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "t_if": "record.selles.raw_value",
                    "class_attr": "text-success float-right mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 6,
                }
            )
            lst_item_view.append(view_item_body_li_6.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "i",
                    "title": "Ok",
                    "aria_label": "Ok",
                    "role": "img",
                    "class_attr": "fa fa-circle",
                    "parent_id": view_item_body_li_6.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item_body_li_7 = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "li",
                    "t_if": "!record.selles.raw_value",
                    "class_attr": "text-danger float-right mb4",
                    "parent_id": view_item_body_ul_1.id,
                    "sequence": 7,
                }
            )
            lst_item_view.append(view_item_body_li_7.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "i",
                    "title": "Invalid",
                    "aria_label": "Invalid",
                    "role": "img",
                    "class_attr": "fa fa-circle",
                    "parent_id": view_item_body_li_7.id,
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "kanban",
                    "view_name": "famille_alimentation_nourrisson_kanban",
                    "view_attr_class": "o_kanban_mobile",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "famille_alimentation_nourrisson_view_kanban",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # pivot view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "mictions",
                    "action_name": "mictions",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "type": "row",
                    "name": "selles",
                    "action_name": "selles",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "pivot",
                    "view_name": "famille_alimentation_nourrisson_pivot",
                    "view_attr_string": "Famille alimentation nourrisson",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "famille_alimentation_nourrisson_view_pivot",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # search view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "filter",
                    "name": "commentaire",
                    "domain": "[('commentaire','!=',False)]",
                    "label": "Allaitement",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "filter",
                    "name": "date_debut",
                    "domain": "[('date_debut','!=',False)]",
                    "label": "Date début",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "filter",
                    "name": "date_fin",
                    "domain": "[('date_fin','!=',False)]",
                    "label": "Date fin",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "filter",
                    "name": "mictions",
                    "domain": "[('mictions','=',True)]",
                    "label": "Mictions",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "filter",
                    "name": "selles",
                    "domain": "[('selles','=',True)]",
                    "label": "Selles",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "search",
                    "view_name": "famille_alimentation_nourrisson_search",
                    "view_attr_string": "Famille alimentation nourrisson",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "famille_alimentation_nourrisson_view_search",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # tree view
        if True:
            lst_item_view = []
            # BODY
            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "commentaire",
                    "action_name": "commentaire",
                    "sequence": 1,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_debut",
                    "action_name": "date_debut",
                    "sequence": 2,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "date_fin",
                    "action_name": "date_fin",
                    "sequence": 3,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "mictions",
                    "action_name": "mictions",
                    "sequence": 4,
                }
            )
            lst_item_view.append(view_item.id)

            view_item = env["code.generator.view.item"].create(
                {
                    "section_type": "body",
                    "item_type": "field",
                    "name": "selles",
                    "action_name": "selles",
                    "sequence": 5,
                }
            )
            lst_item_view.append(view_item.id)

            view_code_generator = env["code.generator.view"].create(
                {
                    "code_generator_id": code_generator_id.id,
                    "view_type": "tree",
                    "view_name": "famille_alimentation_nourrisson_tree",
                    "m2o_model": model_famille_alimentation_nourrisson.id,
                    "view_item_ids": [(6, 0, lst_item_view)],
                    "id_name": "famille_alimentation_nourrisson_view_tree",
                }
            )
            lst_view_id.append(view_code_generator.id)

        # Action generate view
        wizard_view = env["code.generator.generate.views.wizard"].create(
            {
                "code_generator_id": code_generator_id.id,
                "enable_generate_all": False,
                "disable_generate_menu": False,
                "disable_generate_access": False,
                "code_generator_view_ids": [(6, 0, lst_view_id)],
                "enable_generate_portal": True,
                "portal_enable_create": True,
            }
        )

        wizard_view.button_generate_views()

        # Generate access
        lang = "en_US"
        group_id = env.ref("base.group_portal").with_context(lang=lang)
        access_id = env["ir.model.access"].create(
            {
                "name": (
                    "famille_alimentation_nourrisson Access User types /"
                    " Portal"
                ),
                "model_id": model_famille_alimentation_nourrisson.id,
                "group_id": group_id.id,
                "perm_read": True,
                "perm_create": True,
                "perm_write": True,
                "perm_unlink": True,
            }
        )

        env["ir.model.data"].create(
            {
                "name": "famille_alimentation_nourrisson_access_user_types_/_portal",
                "model": "ir.model.access",
                "module": MODULE_NAME,
                "res_id": access_id.id,
            }
        )

        # Generate module
        value = {"code_generator_ids": code_generator_id.ids}
        env["code.generator.writer"].create(value)


def uninstall_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        code_generator_id = env["code.generator.module"].search(
            [("name", "=", MODULE_NAME)]
        )
        if code_generator_id:
            code_generator_id.unlink()
