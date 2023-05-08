import datetime
import uuid

from django.contrib.postgres.fields import ArrayField, JSONField
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.db import models
from django.shortcuts import get_object_or_404

ENGLISH = "EN"
SPANISH = "ES"
LANGUAGE_CHOICES = [
    (ENGLISH, "English"),
    (SPANISH, "Spanish"),
]


def DEFAULT_WORK_HOURS():
    return {
        "sunday_hours": None,
        "monday_hours": None,
        "tuesday_hours": None,
        "wednesday_hours": None,
        "thursday_hours": None,
        "friday_hours": None,
        "saturday_hours": None,
    }


class CustomQuerySet(models.QuerySet):

    def get_trailers_per_subcategory(self, sub_category):
        return self.extra(
                select={"sub": "product_category.web_category", "cat": "product_categorymap.slug"},
                tables=["product_category", "product_categorymap"],
                where=[
                    "product_trailer.model=product_category.base_type",
                    "product_categorymap.id=product_category.category_map_id",
                    "UPPER(product_category.web_category) = UPPER(%s)"
                ],
                params=[sub_category]
        )

    def get_trailers_per_category(self, category):
        return self.extra(
                select={"cat": "product_categorymap.slug", "sub": "product_category.web_category"},
                tables=["product_category", "product_categorymap"],
                where=[
                    "product_trailer.model=product_category.base_type",
                    "product_categorymap.id=product_category.category_map_id",
                    "UPPER(product_categorymap.slug) = UPPER(%s)",
                    "product_category.web_category <> 'EcoCC'"
                ],
                params=[category]
        )

    def category_map_filter(self, slug):
        from trailersplus.utils.objects import multiple_q
        include = {
            "Dump": [
                {"category__web_category__startswith": "Dump"},
            ],
            "Cargo": [
                {"category__web_category__startswith": "Enc"},
            ],
            "Equipment": [
                {"category__web_category__startswith": "Eqp"},
                {"model__startswith": "CO7X18"},
                {"model__startswith": "CO7X20"},
                # {"category__web_category__exact": "Flt7TA"},
            ],
            "Utility": [
                {"category__web_category__startswith": "Flt"},
            ],
            "Hauler": [
                {"category__web_category__endswith": "CC"},
                {"category__web_category__exact": "Flt7TA"},
            ],
            "Gooseneck": [
                {"coupler__exact": "GN"},
            ],
            "ATV": [
                {"category__web_category__endswith": "ATV"},
            ],
        }
        exclude = {
            "Dump": [
                {"category__web_category__endswith": "CC"},
                {"category__web_category__endswith": "ATV"}
            ],
            "Cargo": [
                # {"category__web_category__endswith": "CC"},
                {"category__web_category__endswith": "ATV"}
            ],
            "Equipment": [
                {"category__web_category__endswith": "CC"},
                {"category__web_category__endswith": "ATV"},
            ],
            "Utility": [
                {"category__web_category__endswith": "CC"},
                {"category__web_category__endswith": "ATV"},
                {"category__web_category__exact": "Flt7TA"},
            ],
            "Hauler": [],
            "Gooseneck": [],
            "ATV": [],
        }
        return self.filter(models.Q(multiple_q(include[slug]) & ~ multiple_q(exclude[slug])))

    def filter_state_choices(self, lookup, state):
        short_states = dict((v, k) for k, v in Location.STATE_CHOICES)
        state = state.replace('_', ' ')
        kwargs = {lookup: short_states[state]}
        return self.filter(**kwargs)

class SecondDbManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()

        # if `use_db` is set on model use that for choosing the DB
        if hasattr(self.model, "use_db"):
            qs = qs.using(self.model.use_db)

        return qs


class SecondDbBase(models.Model):
    use_db = "default"
    objects = SecondDbManager.from_queryset(CustomQuerySet)()

    class Meta:
        abstract = True


class Trailer(SecondDbBase):
    vin = models.CharField("VIN number", max_length=21, primary_key=True)
    store = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Trailer's location",
    )
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Trailer's type", null=True
    )
    # primary_web_category = models.CharField('Web Category', max_length=255)
    # ToDo Signal to set up
    order_number = models.IntegerField(null=True, blank=True)
    status = models.IntegerField(null=True, blank=True, db_index=True)
    sale_price = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    cash_price = models.CharField(max_length=45, null=True, blank=True)
    calculated_cash_price = models.CharField(max_length=45, null=True, blank=True)
    msrp = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    width = models.CharField(max_length=5, null=True, blank=True)
    length = models.CharField(max_length=5, null=True, blank=True)
    gvwr = models.IntegerField(null=True, blank=True)
    gawr = models.IntegerField(null=True, blank=True)
    empty_weight = models.IntegerField(null=True, blank=True)
    overall_height = models.IntegerField(null=True, blank=True)
    overall_length = models.IntegerField(null=True, blank=True)
    overall_width = models.IntegerField(null=True, blank=True)
    interior_height = models.IntegerField(null=True, blank=True)
    interior_length = models.IntegerField(null=True, blank=True)
    interior_width = models.IntegerField(null=True, blank=True)
    rear_door_height = models.IntegerField(null=True, blank=True)
    rear_door_width = models.IntegerField(null=True, blank=True)
    platform_height = models.IntegerField(null=True, blank=True)
    hitch_height = models.IntegerField(null=True, blank=True)
    frame_centers = models.IntegerField(null=True, blank=True)
    roof_centers = models.IntegerField(null=True, blank=True)
    wall_centers = models.IntegerField(null=True, blank=True)
    axles = models.IntegerField(null=True, blank=True)
    stone_guard = models.IntegerField(null=True, blank=True)
    door_type = models.CharField(max_length=50, null=True, blank=True)
    coupler = models.CharField(max_length=25, null=True, blank=True)
    coupler_size = models.CharField(max_length=255, null=True, blank=True)

    sale_date = models.DateField(null=True, blank=True, db_index=True)
    delivery_date = models.DateField(null=True, blank=True)
    year = models.CharField(max_length=45, null=True, blank=True)
    model = models.CharField(max_length=45, null=True, blank=True)

    pictures = ArrayField(JSONField(), verbose_name="Pictures list", null=True)

    def web_category(self):
        map_obj = {
            "EncCC": "Enc102, EncCC",
            "Flt7TA": "EncCC, FltCC, Eqp7",
        }
        new_web_category = map_obj.get(self.category.web_category, None)
        if new_web_category:
            return new_web_category
        return self.category.web_category

    def get_inventory_url(self):
        return f'{self.store.get_slug()}/{self.category.slug}'
    
    def get_relative_inventory_url(self):
        return f'{self.category.slug}/trailer/{self.vin}/'

    def sold_in_seven_days(self):
        now = datetime.date.today()
        return self.sale_date <= now and self.sale_date > (now - datetime.timedelta(days=7))

    def my_store_url(self):
        from my_store.models import MyStore
        ms = get_object_or_404(MyStore, related_store=self.store)
        return f'{ms.url}{self.category.slug}/trailer/{self.vin}/'

    def sold_over_seven_days(self):
        return self.sale_date < (datetime.date.today() - datetime.timedelta(days=7))

    def __str__(self):
        return self.vin

    class Meta:
        ordering = ['sale_price']
        indexes = [
            models.Index(
                fields=["model"]
            )
        ]


class TrailerTranslation(SecondDbBase):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    trailer = models.ForeignKey(
        Trailer, on_delete=models.CASCADE, verbose_name="Related trailer"
    )
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=ENGLISH, db_index=True)

    actual_color = models.CharField(max_length=50, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    axle_warranty = models.CharField(max_length=255, null=True, blank=True)
    roof_warranty = models.CharField(max_length=255, null=True, blank=True)
    warranty = models.CharField(max_length=255, null=True, blank=True)
    tires = models.CharField(max_length=255, null=True, blank=True)
    wheels = models.CharField(max_length=255, null=True, blank=True)
    doors = models.CharField(max_length=75, null=True, blank=True)
    stabilizer_jacks = models.CharField(max_length=255, null=True, blank=True)
    side_door = models.CharField(max_length=255, null=True, blank=True)
    rear_door = models.CharField(max_length=255, null=True, blank=True)
    side_walls = models.CharField(max_length=255, null=True, blank=True)
    suspension = models.CharField(max_length=255, null=True, blank=True)
    frame = models.CharField(max_length=255, null=True, blank=True)
    brakes = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)
    clearance_lights = models.CharField(max_length=255, null=True, blank=True)
    tail_lights = models.CharField(max_length=255, null=True, blank=True)
    protected_undercarriage = models.CharField(max_length=255, null=True, blank=True)

    long_description = models.TextField(blank=True, null=True)
    short_description = models.CharField(max_length=50, blank=True, null=True)
    package = models.CharField(max_length=255, null=True, blank=True)
    tag = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.language} {self.trailer.vin}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["language", "trailer_id"], name="unique_translation"
            )
        ]
        verbose_name = "Trailer's translation"
        verbose_name_plural = "Trailers' translations"


class Location(SecondDbBase):
    STATE_CHOICES = [
        ("AL", "Alabama"),
        ("AK", "Alaska"),
        ("AZ", "Arizona"),
        ("AR", "Arkansas"),
        ("CA", "California"),
        ("CO", "Colorado"),
        ("CT", "Connecticut"),
        ("DE", "Delaware"),
        ("FL", "Florida"),
        ("GA", "Georgia"),
        ("HI", "Hawaii"),
        ("ID", "Idaho"),
        ("IL", "Illinois"),
        ("IN", "Indiana"),
        ("IA", "Iowa"),
        ("KS", "Kansas"),
        ("KY", "Kentucky"),
        ("LA", "Louisiana"),
        ("ME", "Maine"),
        ("MD", "Maryland"),
        ("MA", "Massachusetts"),
        ("MI", "Michigan"),
        ("MN", "Minnesota"),
        ("MS", "Mississippi"),
        ("MO", "Missouri"),
        ("MT", "Montana"),
        ("NE", "Nebraska"),
        ("NV", "Nevada"),
        ("NH", "New Hampshire"),
        ("NJ", "New Jersey"),
        ("NM", "New Mexico"),
        ("NY", "New York"),
        ("NC", "North Carolina"),
        ("ND", "North Dakota"),
        ("OH", "Ohio"),
        ("OK", "Oklahoma"),
        ("OR", "Oregon"),
        ("PA", "Pennsylvania"),
        ("RI", "Rhode Island"),
        ("SC", "South Carolina"),
        ("SD", "South Dakota"),
        ("TN", "Tennessee"),
        ("TX", "Texas"),
        ("UT", "Utah"),
        ("VT", "Vermont"),
        ("VA", "Virginia"),
        ("WA", "Washington"),
        ("WV", "West Virginia"),
        ("WI", "Wisconsin"),
        ("WY", "Wyoming"),
        ("DC", "District of Columbia"),
        ("MH", "Marshall Islands"),
    ]
    store_id = models.CharField(max_length=100, primary_key=True)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    active = models.BooleanField(default=True)
    store_name = models.CharField(max_length=100, null=True, blank=True)
    store_city = models.CharField(max_length=100, null=True, blank=True)
    store_address = models.CharField(max_length=500, null=True, blank=True)
    store_zip = models.IntegerField(null=True, blank=True)
    store_directions = models.TextField(null=True, blank=True)
    store_spanish_directions = models.TextField(null=True, blank=True)
    store_email = models.EmailField(max_length=255, null=True, blank=True)
    store_map_url = models.URLField(max_length=500, null=True, blank=True)
    store_phone = models.CharField(max_length=45, null=True, blank=True)
    store_keywords = ArrayField(models.CharField(max_length=45))
    store_lat = models.CharField(max_length=45, null=True, blank=True)
    store_long = models.CharField(max_length=45, null=True, blank=True)
    point = models.PointField(srid=4326)
    store_description = models.CharField(max_length=255, null=True, blank=True)
    store_title = models.CharField(max_length=255, null=True, blank=True)
    work_hours = JSONField(default=DEFAULT_WORK_HOURS)
    uta_merchant = models.CharField(max_length=100, default='0306933001')
    podium_id = models.CharField(max_length=25, null=True, blank=True)
    podium_text_number = models.CharField(max_length=25, default="(208) 647-4117")

    def get_city_name(self):
        try:
            return self.store_name.replace('TrailersPlus ', '')
        except AttributeError:
            return ''

    def get_slug(self):
        try:
            return self.pages.first().get_slug()
        except (ObjectDoesNotExist, AttributeError):
            return ''

    def __str__(self):
        return f'{self.get_city_name()}({self.store_city}), {self.state}'


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, null=True)
    name_es = models.CharField(max_length=100, default='')
    description_es = models.CharField(max_length=255, null=True, default='')
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(
                fields=["name"]
            )
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location"],
                name="unique_service_name_location"
            )
        ]


class CategoryFilter(models.Model):
    FILTER_CHOICES = [
        ("exact", "Exact"),
        ("contains", "Contains"),
        ("startswith", "Starts With"),
        ("endswith", "Ends With"),
        ("regex", "Regex"),
    ]
    FIELDS_CHOICES = [
        ("category__web_category", "Web Category"),
        ("coupler", "Coupler"),
    ]
    case_sensitive = models.BooleanField('Case Sensitive?')
    type = models.CharField(max_length=15, choices=FILTER_CHOICES, help_text="SQL Regex https://dataschool.com/how-to-teach-people-sql/how-regex-works-in-sql/")
    field_name = models.CharField(max_length=25, choices=FIELDS_CHOICES, null=False, blank=False, default='category__web_category__')
    filter = models.CharField(max_length=25)

    def __str__(self):
        name = f"{self.get_type_display()} {self.filter}"
        if self.case_sensitive:
            name += " | CS"
        return name

    class Meta:
        verbose_name = "Category Filter"
        verbose_name_plural = "Category Filters"


class CategoryMap(models.Model):
    name_en = models.CharField(max_length=25)
    name_es = models.CharField(max_length=30)
    slug = models.SlugField(max_length=25, unique=True)
    include = models.ManyToManyField(CategoryFilter, related_name='include', blank=True)
    exclude = models.ManyToManyField(CategoryFilter, related_name='exclude', blank=True)
    order = models.IntegerField('Position in product list filter')
    translations = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.order} {self.name_en}"

    class Meta:
        verbose_name = "Category Map"
        verbose_name_plural = "Category Maps"
        ordering = ['order', 'slug']


class Category(SecondDbBase):
    web_category = models.CharField(max_length=25)
    base_type = models.CharField(max_length=255)
    primary = models.BooleanField("Is primary?", default=False)
    slug = models.CharField(max_length=255, null=True, blank=True)
    category_map = models.ForeignKey(CategoryMap, null=True, blank=True, on_delete=models.SET_NULL, verbose_name="Global Category")
    description = models.TextField(null=True, blank=True)
    keywords = ArrayField(models.CharField(max_length=25), null=True, blank=True)
    pictures = ArrayField(JSONField(), verbose_name="Pictures list", null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["web_category", "base_type"], name="unique_category"
            )
        ]
        indexes = [
            models.Index(
                fields=["base_type"]
            )
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Image360(models.Model):
    class ImageTypes(models.TextChoices):
        EXT360 = "EXT360", "ext360"
        INT360 = "INT360", "int360"

    uuid = models.UUIDField(default=uuid.uuid4)
    vin = models.ForeignKey(Trailer,on_delete=models.CASCADE)
    image_type = models.CharField(max_length=10, choices=ImageTypes.choices, default=ImageTypes.EXT360)
    url = models.CharField(max_length=255)
    class Meta:
        indexes = [
            models.Index(
                fields=["vin"]
            ),
            models.Index(
                fields=["uuid"]
            ),
        ]
        verbose_name = "Image360"
        verbose_name_plural = "Images360"
