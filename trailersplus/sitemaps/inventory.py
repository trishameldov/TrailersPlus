from urllib.parse import urlparse
from django.db import connection
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap
from wagtail.contrib.sitemaps.views import sitemap


sql = """
    SELECT CONCAT(
                'https://www.trailersplus.com/es/',
                REPLACE(d.state_long, ' ', '_'),
                '/',
                REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_'),
                '/',
                b.slug,
                '/trailer/',
                a.vin,
                '/'
            ) as url,
            REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_') as store,
            c.state as state,
            vin,
            wpg.latest_revision_created_at,
            wpg.last_published_at
        FROM product_trailer a
        INNER JOIN product_category b
            ON a.model=b.base_type AND b.primary=true
        INNER JOIN product_location c
            ON a.store_id=c.store_id
        INNER JOIN state_long d
            ON c.state=d.state_short
        INNER JOIN my_store_mystore ms
            ON ms.related_store_id = c.store_id
        INNER JOIN wagtailcore_page wpg
            ON wpg.id = ms.page_ptr_id
        WHERE a.status < 150
        AND c.active=true
    UNION
        SELECT CONCAT(
                    'https://www.trailersplus.com/',
                    REPLACE(d.state_long, ' ', '_'),
                    '/',
                    REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_'),
                    '/',
                    b.slug,
                    '/trailer/',
                    a.vin,
                    '/'
                ) as url,
                REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_') as store,
                c.state as state,
                vin,
                wpg.latest_revision_created_at,
                wpg.last_published_at
            FROM product_trailer a
            INNER JOIN product_category b
                ON a.model=b.base_type AND b.primary=true
            INNER JOIN product_location c
                ON a.store_id=c.store_id
            INNER JOIN state_long d
                ON c.state=d.state_short
            INNER JOIN my_store_mystore ms
                ON ms.related_store_id = c.store_id
            INNER JOIN wagtailcore_page wpg
                ON wpg.id = ms.page_ptr_id
            WHERE a.status < 150
            AND c.active=true
    ORDER BY state, store, vin, url
"""

catergories_sql = """
        SELECT DISTINCT(b.slug) as slug,
            CONCAT(
                'https://www.trailersplus.com/es/',
                REPLACE(d.state_long, ' ', '_'),
                '/',
                REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_'),
                '/',
                b.slug,
                '/'
            )AS url,
            REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_') as store,
            c.state as state,
            wpg.latest_revision_created_at,
            wpg.last_published_at
            FROM product_trailer a
            INNER JOIN product_category b
                ON a.model=b.base_type AND b.primary=true
            INNER JOIN product_location c
                ON a.store_id=c.store_id
            INNER JOIN state_long d
                ON c.state=d.state_short
            INNER JOIN my_store_mystore ms
                ON ms.related_store_id = c.store_id
            INNER JOIN wagtailcore_page wpg
                ON wpg.id = ms.page_ptr_id
            WHERE a.status < 150
            AND c.active=true
    UNION
        SELECT DISTINCT(b.slug) as slug,
                CONCAT(
                    'https://www.trailersplus.com/',
                    REPLACE(d.state_long, ' ', '_'),
                    '/',
                    REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_'),
                    '/',
                    b.slug,
                    '/'
                )AS url,
                REPLACE(substring(c.store_name from strpos(c.store_name, ' ') + 1), ' ', '_') as store,
                c.state as state,
                wpg.latest_revision_created_at,
                wpg.last_published_at
            FROM product_trailer a
            INNER JOIN product_category b
                ON a.model=b.base_type AND b.primary=true
            INNER JOIN product_location c
                ON a.store_id=c.store_id
            INNER JOIN state_long d
                ON c.state=d.state_short
            INNER JOIN my_store_mystore ms
                ON ms.related_store_id = c.store_id
            INNER JOIN wagtailcore_page wpg
                ON wpg.id = ms.page_ptr_id
            WHERE a.status < 150
            AND c.active=true
    ORDER BY state, store, url
"""

inventario_sql = """
    SELECT DISTINCT(cat.web_category) AS web,
            CONCAT(
                'https://www.trailersplus.com/es/',
                REPLACE(lg.state_long, ' ', '_'),
                '/',
                REPLACE(substring(loc.store_name from strpos(loc.store_name, ' ') + 1), ' ', '_'),
                '/inventario/',
                cm.slug,
                '/',
                cat.web_category,
                '/'
            ) as url, 'spanish' AS lang, lg.state_long as state,
            wpg.latest_revision_created_at,
            wpg.last_published_at
        FROM product_trailer tr
        INNER JOIN product_category cat ON tr.model = cat.base_type AND cat.primary = true
        INNER JOIN product_categorymap cm ON cm.id = cat.category_map_id
        INNER JOIN product_location loc ON tr.store_id = loc.store_id
        INNER JOIN state_long lg ON loc.state = lg.state_short
        INNER JOIN my_store_mystore ms ON ms.related_store_id = loc.store_id
        INNER JOIN wagtailcore_page wpg ON wpg.id = ms.page_ptr_id
    UNION
    SELECT DISTINCT(cat.web_category) AS web,
            CONCAT(
                'https://www.trailersplus.com/',
                REPLACE(lg.state_long, ' ', '_'),
                '/',
                REPLACE(substring(loc.store_name from strpos(loc.store_name, ' ') + 1), ' ', '_'),
                '/inventory/',
                cm.slug,
                '/',
                cat.web_category,
                '/'
            ) as url, 'english' AS lang, lg.state_long as state,
            wpg.latest_revision_created_at,
            wpg.last_published_at
        FROM product_trailer tr
        INNER JOIN product_category cat ON tr.model = cat.base_type AND cat.primary = true
        INNER JOIN product_categorymap cm ON cm.id = cat.category_map_id
        INNER JOIN product_location loc ON tr.store_id = loc.store_id
        INNER JOIN state_long lg ON loc.state = lg.state_short
        INNER JOIN my_store_mystore ms ON ms.related_store_id = loc.store_id
        INNER JOIN wagtailcore_page wpg ON wpg.id = ms.page_ptr_id
    UNION
    SELECT DISTINCT(cm.slug) AS web,
            CONCAT(
                'https://www.trailersplus.com/',
                REPLACE(lg.state_long, ' ', '_'),
                '/',
                REPLACE(substring(loc.store_name from strpos(loc.store_name, ' ') + 1), ' ', '_'),
                '/inventory/',
                cm.slug,
                '/'
            ) as url, 'english' AS lang, lg.state_long as state,
            wpg.latest_revision_created_at,
            wpg.last_published_at
        FROM product_trailer tr
        INNER JOIN product_category cat ON tr.model = cat.base_type AND cat.primary = true
        INNER JOIN product_categorymap cm ON cm.id = cat.category_map_id
        INNER JOIN product_location loc ON tr.store_id = loc.store_id
        INNER JOIN state_long lg ON loc.state = lg.state_short
        INNER JOIN my_store_mystore ms ON ms.related_store_id = loc.store_id
        INNER JOIN wagtailcore_page wpg ON wpg.id = ms.page_ptr_id
UNION
    SELECT DISTINCT(cm.slug) AS web,
            CONCAT(
                'https://www.trailersplus.com/es/',
                REPLACE(lg.state_long, ' ', '_'),
                '/',
                REPLACE(substring(loc.store_name from strpos(loc.store_name, ' ') + 1), ' ', '_'),
                '/inventory/',
                cm.slug,
                '/'
            ) as url, 'spanish' AS lang, lg.state_long as state,
            wpg.latest_revision_created_at,
            wpg.last_published_at
        FROM product_trailer tr
        INNER JOIN product_category cat ON tr.model = cat.base_type AND cat.primary = true
        INNER JOIN product_categorymap cm ON cm.id = cat.category_map_id
        INNER JOIN product_location loc ON tr.store_id = loc.store_id
        INNER JOIN state_long lg ON loc.state = lg.state_short
        INNER JOIN my_store_mystore ms ON ms.related_store_id = loc.store_id
        INNER JOIN wagtailcore_page wpg ON wpg.id = ms.page_ptr_id
ORDER BY state, web, lang
"""


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def sitemap_sql_executor(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = dictfetchall(cursor)
    return row


class InventoryVINSitemap(Sitemap):
    changefreq = "always"
    priority = 0.5

    def items(self):
        return sitemap_sql_executor(sql)

    def lastmod(self, obj):
        return obj['last_published_at']

    def location(self, obj):
        return urlparse(obj['url']).path

    def _urls(self, page, protocol, domain):
        domain = 'www.trailersplus.com'
        return super(Sitemap, self)._urls(page, protocol, domain)


class InventarioCategoriesSitemap(InventoryVINSitemap):
    def items(self):
        return sitemap_sql_executor(inventario_sql)


class CategoriesSitemap(InventoryVINSitemap):
    def items(self):
        return sitemap_sql_executor(catergories_sql)


sitemaps = {
    'trailersplus': Sitemap,
    'inventory': InventoryVINSitemap,
    'inventory_cat': InventarioCategoriesSitemap,
    'categories': CategoriesSitemap,
}
