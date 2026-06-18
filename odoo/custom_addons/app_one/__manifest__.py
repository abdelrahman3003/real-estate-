{
    "name": "App One",
    "author": "abdo",
    "version": "17.0.1.0.0",
    "depends":
        [
        "base",
        "sale_management"
        ],
    'category': '',
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/properties_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/sale_order_view.xml',
        'views/property_history_view.xml',
        'reports/property_report.xml',
        'wizard/property_change_state_wizard_view.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "app_one/static/src/css/property.css",
        ],
    },
    "application": True,
}