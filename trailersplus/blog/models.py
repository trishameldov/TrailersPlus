from urllib.parse import urlparse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import models
from django.conf import settings
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.admin.edit_handlers import (
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    ObjectList,
    TabbedInterface,
)
from wagtail_meta_preview.panels import FacebookFieldPreviewPanel

from home.models import Partners, Footer, Header
from menus.models import MainMenu
from streams import blocks

from trailersplus.utils.decorators import define_user_location, additional_context


def get_next_post_sibling(post):
    sibling = BlogDetailPage.objects.filter(
        post_date__gt=post.post_date, live=True
    ).exclude(pk=post.pk).order_by('post_date').first()
    if not sibling:
        sibling = BlogDetailPage.objects.filter(
            live=True).order_by('post_date').first()
    return sibling


def get_previous_post_sibling(post):
    sibling = BlogDetailPage.objects.filter(
        post_date__lt=post.post_date, live=True
    ).exclude(pk=post.pk).order_by('-post_date').first()
    if not sibling:
        sibling = BlogDetailPage.objects.filter(live=True).order_by('-post_date').first()
    return sibling


class RightSideBlogBanner(Orderable, models.Model):
    page = ParentalKey("blog.BlogListingPage", related_name="rightside_banner")
    title = models.CharField(max_length=99, blank=True)
    sub_title = models.CharField(max_length=99, blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )
    image_alt = models.CharField(max_length=99, blank=True)
    button_text = models.CharField(max_length=99, blank=True)
    button_link = models.CharField(max_length=99, blank=True, null=True)
    button_page_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("sub_title"),
        ImageChooserPanel("image"),
        FieldPanel("image_alt"),
        FieldPanel("button_text"),
        FieldPanel("button_link"),
        PageChooserPanel("button_page_link"),
    ]

    class Meta:
        verbose_name = "RightSide Blog Banner"
        verbose_name_plural = "RightSide Blog Banner"


class BlogListingPage(Page):
    template = "blog/blog_listing_page.html"
    ajax_template = "blog/blog_listing_page_ajax.html"

    custom_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )

    load_more_button = models.CharField(max_length=255, blank=True, null=True)
    read_more_button = models.CharField(max_length=255, blank=True, null=True)

    cache_prefixes = [
        'cache_slider',
        'category_carousel',
        'cache_social_icons',
        'cache_partners_block',
        'big_banner_block',
        'recent_works',
        'carousel_popup',
        'richtext',
        'single_image',
        'call_us',
    ]

    content = StreamField(
        [
            ("slider_block", blocks.SliderBlock()),
            ("big_text_section_block", blocks.BigTextSection()),
            ("category_carousel", blocks.CategoryCarousel()),
            ("call_to_action", blocks.CallToActionBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
            ("big_banner", blocks.BigBanner()),
            ("banners_block", blocks.BannersLink()),
            ("recent_works", blocks.RecentWorksBlock()),
            ("carousel_popup", blocks.CarouselPopup()),
            ("richtext_block", blocks.RichtextBlock()),
            ("single_image_block", blocks.SingleImage()),
            ("share_btn", blocks.ShareBtn()),
            ("call_us_block", blocks.CallUsBlock()),
            ("youtube_block", blocks.YoutubeEmbedBlock()),
            ("divider_line", blocks.DividerLine()),
        ],
        null=True,
        blank=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        FieldPanel("load_more_button"),
        FieldPanel("read_more_button"),
        MultiFieldPanel(
            [InlinePanel("rightside_banner", max_num=5, min_num=1, label="Banner")],
            heading="RightSide Banner",
        ),
        StreamFieldPanel("content"),
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()

        all_posts = BlogDetailPage.objects.live().order_by("-post_date")
        paginator = Paginator(all_posts, 5)
        page = request.GET.get("page")
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        context["posts"] = posts
        context["max_pages"] = paginator.num_pages
        context["main_menus"] = MainMenu.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        return context

    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    def get_sitemap_urls(self, request=None):
        results = super(BlogListingPage, self).get_sitemap_urls(request)
        if hasattr(self, 'slug_es') and self.slug_es:
            base_url = urlparse(self.get_full_url())
            url = f'{base_url.scheme}://{base_url.netloc}/es{base_url.path}'
            lastmod = self.last_published_at or self.latest_revision_created_at
            results.append({
                'location': url,
                'lastmod': lastmod,
            })
        return results

    class Meta:
        verbose_name = "Blog Listing"
        verbose_name_plural = "Blog Listing"


class BlogDetailPage(Page):
    post_title = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Overwrites the default title",
    )
    post_short_description = models.TextField(blank=True, null=True)
    post_preview_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    post_main_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
    )
    post_main_image_mobile = models.ForeignKey(
        "wagtailimages.Image",
        blank=True,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL,
        help_text="Optional",
    )
    post_main_image_overlay = models.CharField(
        max_length=55, blank=True, null=True, default=3, help_text="Min: 1. Max: 5."
    )
    post_image_alt = models.CharField(max_length=255, blank=True, null=True)
    post_date = models.DateField("Post date")

    cache_prefixes = [
        'category_carousel',
        'cache_social_icons',
        'cache_partners_block',
        'big_banner_block',
        'recent_works',
        'richtext',
        'single_image',
        'call_us',
    ]

    content = StreamField(
        [
            ("big_text_section_block", blocks.BigTextSection()),
            ("category_carousel", blocks.CategoryCarousel()),
            ("call_to_action", blocks.CallToActionBlock()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
            ("big_banner", blocks.BigBanner()),
            ("banners_block", blocks.BannersLink()),
            ("recent_works", blocks.RecentWorksBlock()),
            ("richtext_block", blocks.RichtextBlock()),
            ("single_image_block", blocks.SingleImage()),
            ("share_btn", blocks.ShareBtn()),
            ("call_us_block", blocks.CallUsBlock()),
            ("youtube_block", blocks.YoutubeEmbedBlock()),
            ("next_previous_posts_block", blocks.NextPreviousPostsS()),
            ("next_previous_posts_block1", blocks.NextPreviousPostsSt()),
            ("divider_line", blocks.DividerLine()),
        ],
        null=True,
        blank=True,
    )

    og_title = models.CharField(max_length=500, blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.ForeignKey(
        get_image_model_string(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Og image",
    )

    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        MultiFieldPanel(
            [
                FieldPanel("post_short_description"),
                ImageChooserPanel("post_preview_image"),
                FieldPanel("post_main_image_overlay"),
                ImageChooserPanel("post_main_image"),
                ImageChooserPanel("post_main_image_mobile"),
                FieldPanel("post_image_alt"),
            ],
            heading="Preview & Main Images",
        ),
        FieldPanel("post_date"),
        StreamFieldPanel("content"),
        FacebookFieldPreviewPanel([
            FieldPanel("og_title"),
            FieldPanel("og_description"),
            ImageChooserPanel("og_image"),
        ], heading="Facebook")
    ]

    def prev_sibling(self):
        return get_previous_post_sibling(self)

    def next_sibling(self):
        return get_next_post_sibling(self)

    def prev_sibling_image(self):
        sibling = get_previous_post_sibling(self)
        if sibling:
            return sibling.post_preview_image

    def next_sibling_image(self):
        sibling = get_next_post_sibling(self)
        if sibling:
            return sibling.post_preview_image

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["footers"] = Footer.objects.all()
        context["previous_sibling"] = self.prev_sibling()
        context["next_sibling"] = self.next_sibling()
        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    def get_sitemap_urls(self, request=None):
        full_url = self.get_full_url()
        base_url = urlparse(full_url)
        lastmod = self.last_published_at or self.latest_revision_created_at
        eng_url = f'{base_url.scheme}://{base_url.netloc}/{self.slug_en}/'
        results = [{
            'location': eng_url,
            'lastmod': lastmod,
        }]
        if hasattr(self, 'slug_es') and self.slug_es:
            url = f'{base_url.scheme}://{base_url.netloc}/es/{self.slug_es}/'
            results.append({
                'location': url,
                'lastmod': lastmod,
            })
        return results

    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    @property
    def absolute_main_image(self):
        return '{0}{1}'.format(settings.MEDIA_ROOT, self.post_main_image.url)

    @property
    def absolute_main_image_mobile(self):
        return '{0}{1}'.format(settings.MEDIA_ROOT, self.post_main_image_mobile.url)

    @property
    def absolute_preview_image(self):
        return '{0}{1}'.format(settings.MEDIA_ROOT, self.post_preview_image.url)
