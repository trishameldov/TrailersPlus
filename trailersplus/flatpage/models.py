from urllib.parse import urlparse
from django.db import models
from django_extensions.db.fields import AutoSlugField
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    PageChooserPanel,
    StreamFieldPanel,
    ObjectList,
    TabbedInterface,
    FieldRowPanel,
)
from wagtail.images import get_image_model_string
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail_meta_preview.panels import FacebookFieldPreviewPanel

from home.models import Partners, Footer, Header
from menus.models import MainMenu
from streams import blocks
from api.models import ServiceReviews
from product.models import CategoryMap, Location

from trailersplus.utils.decorators import define_user_location, additional_context


class FlatPage(Page):
    template = "flatpage/flat_page.html"

    cache_prefixes = [
        'custom_trailers_form',
        'fleet_sales_form',
        'cache_slider',
        'category_carousel',
        'cache_social_icons',
        'cache_partners_block',
        'big_banner_block',
        'call_us_banner_v2',
        'trailers_for_sale_search',
        'banner_and_breadcrumbs',
        'recent_works',
        'carousel_popup',
        'popular_parts_tabs',
        'text_block',
        'text_background_image',
        'richtext',
        'richtext_plus',
        'policy_block',
        'single_image',
        'image_gallery_2',
        'our_team_carousel',
        'our_team_images',
        'trustpilot',
        'call_us',
        'call_us_today_v2',
        'call_now',
        'service_and_repair',
        'before_after_slider',
        'store_finder',
        'fleet_sales_banner',
        'why_choose_us',
        'case_studies',
        'learn_more',
        'why_wait_block',
        'why_wait_v2',
        'article_sidebar',
        'service_icons',
        'checkpoint_list',
        'about_us_images_text',
        'contact_us',
        'financing_cards',
        'options_section',
        'option_section2',
        'carrers_section',
        'trailers_offer_image',
        'trailers_offer_options',
        'why_service_text',
        'richtext',
        'reviews_gallery',
        'store_dropdown',
    ]

    content = StreamField(
        [
            ("custom_trailer_form", blocks.CustomTrailerForms()),
            ("fleet_sales_forms", blocks.FleetSalesForms()),
            ("warranty_form", blocks.WarrantyForm()),
            ("slider_block", blocks.SliderBlock()),
            ("big_text_section_block", blocks.BigTextSection()),
            ("category_carousel", blocks.CategoryCarousel()),
            ("call_to_action", blocks.CallToActionBlock()),
            ("call_to_action_v2", blocks.CallToActionV2()),
            ("social_icons_banner", blocks.SocialIconBanner()),
            ("partners", blocks.PartnersBlock()),
            ("big_banner", blocks.BigBanner()),
            ("big_banner_v2", blocks.BigBannerV2()),
            ("banner_search", blocks.BannerSearch()),
            ("banner_breadcrumbs", blocks.BannerBreadCrumbs()),
            ("banners_block", blocks.BannersLink()),
            ("youtube_banner", blocks.YoutubeBanner()),
            ("recent_works", blocks.RecentWorksBlock()),
            ("carousel_popup", blocks.CarouselPopup()),
            ("popular_parts_tabs", blocks.PartsAndAccessoriesBlock()),
            ("h2_title", blocks.H2Title()),
            ("h3_title", blocks.H3Title()),
            ("text_block", blocks.TextBlock()),
            ("text_background_image", blocks.TextAreaBackgroundImage()),
            ("richtext_block", blocks.RichtextBlock()),
            ("richtext_block_plus", blocks.RichtextBlockPlus()),
            ("return_policy_block", blocks.ReturnPolicy()),
            ("single_image_block", blocks.SingleImage()),
            ("image_and_text", blocks.ImageAndText()),
            ("image_gallery", blocks.ImageGallery()),
            ("image_gallery_v2", blocks.ImageGalleryV2()),
            ("image_carousel", blocks.ImagesCarousel()),
            ("buttons_block", blocks.ButtonsBlock()),
            ("image_icon_navigation_block", blocks.ImageIconNavigationBlock()),
            ("image_text_block", blocks.ImagesTextBlocks()),
            ("share_btn", blocks.ShareBtn()),
            ("trustpilot_widget", blocks.TrustPilotWidget()),
            ("trustpilot_widget_horizontal", blocks.TrustPilotWidgetHorizontal()),
            ("call_us_block", blocks.CallUsBlock()),
            ("call_us_today", blocks.CallUsToday()),
            ("call_us_today_v2", blocks.CallUsTodayV2()),
            ("call_now_block", blocks.CallNowBlock()),
            ("youtube_block", blocks.YoutubeEmbedBlock()),
            ("why_buy_youtube", blocks.WhyBuyYoutube()),
            ("divider_line", blocks.DividerLine()),
            ("search_and_repair_banner", blocks.ServiceAndRepairBanner()),
            ("specializations", blocks.Specializations()),
            ("before_after_slider", blocks.BeforeAfterSlider()),
            ("table_row", blocks.TableRow()),
            ("store_finder_map", blocks.StoreFinderMap()),
            ("fleet_sales_banner", blocks.FleetSalesBanner()),
            ("why_choose_us", blocks.WhyChooseUs()),
            ("case_studies_carousel", blocks.CaseStudiesCarousel()),
            ("learn_more_block", blocks.LearnMoreBlock()),
            ("why_wait_block", blocks.WhyWaitBlock()),
            ("why_wait_block_v2", blocks.WhyWaitBlockV2()),
            ("models_offer_block", blocks.ModelsWeOfferBlock()),
            ("trailer_size_block", blocks.TrailersSizeBlock()),
            ("blockquotes_block", blocks.BlockquotesReview()),
            ("article_sidebar_block", blocks.ArticleSidebar()),
            ("service_icons_block", blocks.ServiceIconsBlock()),
            ("checkpoint_list_block", blocks.CheckpointList()),
            ("about_us_image_text_block", blocks.AboutUsImagesTextButton()),
            ("contact_us_block", blocks.ContactUsBlock()),
            ("styled_h2_and_text_block", blocks.StyledH2TextBlock()),
            ("financing_cards", blocks.FinancingCards()),
            ("options_block", blocks.OptionsBlock()),
            ("options_block_v2", blocks.OptionsBlockV2()),
            ("careers_block", blocks.VacanciesSection()),
            ("resources_block", blocks.ResourcesBlock()),
            ("trailer_we_offer_block", blocks.TrailersOfferImagesBlocks()),
            ("trailer_we_options_block", blocks.TrailersOfferOptionsLinks()),
            ("why_service_text_button", blocks.WhyServiceTextButton()),
            ("why_service_list_buttons", blocks.WhyServiceListButtons()),
            ("reviews_gallery", blocks.ReviewsGallery()),
            ("warranty_title", blocks.WarrantyTitle()),
            ("check_list", blocks.CheckList()),
            ("paragraph_image", blocks.ParagraphImage()),
            ("banner_title", blocks.BannerTitle()),
            ("why_banner_title", blocks.WhyChooseBannerTitle()),
            ("banner_title_buttons", blocks.BannerTitleButtons()),
            ("banner_title_financing", blocks.BannerTitleFinancing()),
            ("schedule_service", blocks.ScheduleService()),
        ],
        null=True,
        blank=True,
    )

    field_for_schema = models.TextField(blank=True, null=True)
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
        StreamFieldPanel("content"),
        FieldPanel("field_for_schema"),
        FacebookFieldPreviewPanel([
            FieldPanel("og_title"),
            FieldPanel("og_description"),
            ImageChooserPanel("og_image"),
        ], heading="Facebook")
    ]

    @additional_context
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["headers"] = Header.objects.all()
        context["partners"] = Partners.objects.all()
        context["footers"] = Footer.objects.all()
        context["main_menus"] = MainMenu.objects.all()
        context["reviews"] = ServiceReviews.objects.all().order_by("-created_at")[:10]
        context["categories"] = CategoryMap.objects.all()

        en_url_path = ['en'] + self.url_path_en.split('/')[2:]
        es_url_path = ['es'] + self.url_path_es.split('/')[2:]
        context["translation_path"] = {
            "en": '/'.join(en_url_path),
            "es": '/'.join(es_url_path),
        }

        return context

    # @define_user_location
    def serve(self, request, *args, **kwargs):
        return super().serve(request, *args, **kwargs)

    def get_sitemap_urls(self, request=None):
        result = []
        url_parsed = urlparse(self.get_full_url())
        lastmod = self.last_published_at or self.latest_revision_created_at
        locs = None
        if hasattr(self, 'slug_es') and self.slug_es:
            es_url = url_parsed.scheme + '://' + url_parsed.netloc + '/es/' + self.slug_es + '/'
            result.append({
                'location': es_url,
                'lastmod': lastmod
            })
            # delete these lines once we confirm with Blake this chance is okay
            # considering that now we have Statepages.
            # if self.slug_es == 'locaciones' or self.slug_en == 'trailer-dealerships':
            #     locs = set('_'.join(x.get_state_display().split(' ')) for x in Location.objects.all().order_by('state'))
            #     for loc in locs:
            #         result.append({
            #             'location': es_url + '?state=' + loc,
            #             'lastmod': lastmod
            #         })
        en_url = url_parsed.scheme + '://' + url_parsed.netloc + '/' + self.slug_en + '/'
        result.append({
            'location': en_url,
            'lastmod': lastmod
        })
        if locs:
            for loc in locs:
                result.append({
                    'location': en_url + '?state=' + loc,
                    'lastmod': lastmod
                })
        return result

    class Meta:
        verbose_name = "Flat Page"
        verbose_name_plural = "Flat Pages"
