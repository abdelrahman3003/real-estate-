{
    "name": "App One",
    "author": "abdo",
    "version": "17.0.1.0.0",
    "depends":
        [
        "base",
        "sale_management",
        "purchase",
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
        'views/purchase_order_view.xml',
        'reports/property_report.xml',
        'wizard/property_change_state_wizard_view.xml',
    ],
    "assets": {
        "web.assets_backend": [
            "app_one/static/src/css/property.css",
            "app_one/static/src/components/list_view/listView.css",
            "app_one/static/src/components/list_view/listView.js",
            "app_one/static/src/components/list_view/listView.xml",

            ],
        "web.report_assets_common": ["/app_one/static/src/css/fonts.css",],
    },
    "application": True,
}