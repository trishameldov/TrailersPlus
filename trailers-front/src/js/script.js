import {
	$body, $header, $scrollNav, $innerNav, mobileMenuBreakpoint, $innerNavScroll,
} from './setup/variables';
import { saaDropdown, openActiveDrop, closeDropdown } from './partials/dropdown';
import {
	toggleNavbar,
  headerScroll,
  menuPaddings,
  mobileNavEvents,
  calcMobileWinSize,
	menuChildCount,
} from './partials/header';
import { cartOpen, closeCart } from './partials/cart';
import { priceSlider } from './partials/price-slider';
import { swiperInit } from './partials/swiper';
import { select2 } from './partials/select';
import {
	labelClick,
  toggleFilter,
  toggleAllFilter,
  closeFilterMobile,
  checkActive,
  filterSpecial,
  changeProductLocation,
  labelSelector,
} from './partials/search-filter';
import { tabChange } from './partials/tabs';
import { printContent } from './partials/print';
import { initPopup, initSchedulePopup, closePopup, schedulePopup, initReviewsPopup, initServicePopup } from './partials/popup';
import { initMap, initMainMap } from './partials/map';
import { phoneMask, checkValid, inputCheckForValue } from './partials/form';
import { setScrollToID } from './partials/scroll-links';
import { innerNavScroll } from './partials/inner-nav';
import { shareLink } from './partials/social-sharing';
import { replaceSVG } from './partials/svg-icons';
import { initBeforeAfterSlider } from './partials/ba-slider';
import { chatOpen } from './partials/livechat';
import { toNextSection } from './partials/to-next';
// import { Checkout } from './partials/checkout';
import { initShowMore } from './partials/show-more';
import { initLoadMorePosts } from './partials/load-more-posts';
import { initLangListener } from './partials/lang';
import { initForms } from './forms';
import { initCookiePolicy } from './partials/policy';
import { initHeaderStoreLocator } from './partials/header-store-locator'
import Scheduler from './partials/scheduler'
import { getCookie } from './utils/cookies.utils'

/**
 * GLOBAL SCRIPTS
 */

window.$ = jQuery;

/**
 * Calculate required sizes
 */

function calculateSize() {
	// Scroll header height
	const scrollNavH = ((window.innerWidth > mobileMenuBreakpoint) && $scrollNav)
		? +window.getComputedStyle($scrollNav).height.split('px')[0]
		: 0;
	// Header height
	const headerH = $header
		? +window.getComputedStyle($header, null).height.split('px')[0]
		: 0;
	// inner navigation height
	const innerNavH = ((window.innerWidth > mobileMenuBreakpoint) && $innerNav)
		? +window.getComputedStyle($innerNav, null).height.split('px')[0]
		: 0;
	// inner scroll navigation height
	const innerNavScrollH = ((window.innerWidth > mobileMenuBreakpoint) && $innerNavScroll)
		? +window.getComputedStyle($innerNavScroll, null).height.split('px')[0]
		: 0;

	window.calcSizes = {
		scrollNavH,
		headerH,
		innerNavH,
		innerNavScrollH,
	};
}

/**
 * Scroll Control
 */

let scrollPosition = 0;

window.scrollControl = {
	enable() {
		scrollPosition = window.pageYOffset;
		$body.style.overflow = 'hidden';
		$body.style.position = 'fixed';
		$body.style.top = `-${scrollPosition}px`;
		$body.style.width = '100%';
	},
	disable() {
		$body.style.removeProperty('overflow');
		$body.style.removeProperty('position');
		$body.style.removeProperty('top');
		$body.style.removeProperty('width');
		window.scrollTo(0, scrollPosition);
	},
};

/**
 * Document padding if Header fixed
 */

function docPadding() {
	const headerH = $header ? window.getComputedStyle($header, null).height : 0;
	if (window.innerWidth < 1025) {
		$body.style.paddingTop = headerH;
	} else {
		$body.style.paddingTop = 0;
	}
}

/**
 * Formats phone numbers
 * From: ###-###-####
 * To:   (###) ###-####
 */
function formatPhones() {
    // let phone_banner = document.getElementById("phone_banner").textContent;
    let phone_location = document.getElementById("phone_location");
    let phone_footer = document.getElementById("phone_footer").innerText;
    let phone_block = document.getElementById("phone_block");
    let formatted_phone = '';

    // if (phone_banner) {
    //     let array = phone_banner.split("-");
    //     formatted_phone = `(${array[0]}) ${array[1]}-${array[2]}`;
    //     document.getElementById("phone_banner").textContent = formatted_phone;
    // }

    if (phone_location) {
        let array_location = phone_location.innerText.split("-");
        let formatted_location = `(${array_location[0]}) ${array_location[1]}-${array_location[2]}`;
        document.getElementById("phone_location").innerText = formatted_location;
    }

    if (phone_footer) {
        let array_footer = phone_footer.split("-");
        let formatted_footer = `(${array_footer[0]}) ${array_footer[1]}-${array_footer[2]}`;
        document.getElementById("phone_footer").innerText = formatted_footer;
    }

    if (phone_block) {
        let array_block = phone_block.innerText.split("-");
        let formatted_block = `(${array_block[0]}) ${array_block[1]}-${array_block[2]}`;
        document.getElementById("phone_block").innerText = formatted_block;
    }

    let phones = document.getElementsByClassName("phone-nos");
    let array_phones;
    for (let i = 0; i < phones.length; i++) {
        array_phones = phones[i].innerText.split("-");
        phones[i].innerText = `(${array_phones[0]}) ${array_phones[1]}-${array_phones[2]}`;
    }
}

/**
 * Adds spacing to blog blocks.
 * Only executes if 'blog' appears on URL.
 */
function blogSpacing() {

    let containers = document.getElementsByClassName('blog-container');
    if (containers.length > 0) {
        for (let i = 0; i< containers.length; i++) {
            let paragraphs = containers[i].childNodes;
            for (let i = 0; i < paragraphs.length; i++) {
                if (paragraphs[i].tagName) {
                    paragraphs[i].style.cssText += 'padding-top:1rem';
                }
            }
        }
    }
}

function tireWarrantyRemoval() {
	// Removes the tire and wheel warranty link for CarryOn trailers.
	window.addEventListener('DOMContentLoaded', (event) => {
		if (document.getElementById('tires-url')) {
			let tires_url = document.getElementById('tires-url');
			let detail_vin = document.getElementById('vin').textContent.trim();

			if (detail_vin.startsWith('4YMB')) tires_url.style.display = "none";
		}
	});
}

/**
 * Disables the Store selector dropdown on certain pages.
 * Currently, these pages have the dropdown disabled:
 * -    Trailer detail
 * -    Checkout
 */
function disableStoreDropdown() {
	// Pages where we want to disable the dropdown.
	// These strings were selected because they're unique for these pages once
	// we split the URL.
	const pages = ['checkout', 'trailer', 'thankyou', 'success-checkout'];
	const currentUrl = window.location.href;
	const urlParts = currentUrl.split('/');

	let inPage = false;
	// Checks if each element of the pages array is in the split URL.
	for (let i = 0; i < pages.length; i++) {
		console.log(pages[i]);
		console.log(urlParts.includes(pages[i]));
		if (urlParts.includes(pages[i])) {
			inPage = true;
			break;
		}
	}
	if (inPage) {
		let dropdown = document.getElementById('location-dropdown-list');
		dropdown.remove();

		let dropdown_block = document.getElementById('dropdown');
		dropdown_block.classList.remove('tp-dropdown__head');

		let three_classes = document.getElementById('three-classes')
		three_classes.classList.remove('tp-dropdown');
		three_classes.classList.remove('js-dropdown');

		const element = document.querySelector('#link-store');

		element.style.color = 'white';
	}
}


/**
 * Check language
 */
const lang = getCookie("django_language")
window.language = (window.location.href.indexOf('/es/') > 0 || lang) ? 'es' : 'en';

/**
 * LOAD EVENTS
 */
document.addEventListener('DOMContentLoaded', () => {
	calculateSize();
	swiperInit();
	saaDropdown();
	closeDropdown();
	toggleNavbar();
	cartOpen();
	closeCart();
	menuPaddings();
	mobileNavEvents('.js-submenu-toggle', '.js-submenu', 'li');
	mobileNavEvents('.js-drop-toggle', '.js-drop-content', '.js-drop-wrapp', 'open');
	// openActive();
	select2();
	openActiveDrop();
	priceSlider();
	menuChildCount();
	tabChange($('.js-tab-link'), '.js-tabs', '.js-tab-box');
	checkValid();
	setScrollToID();
	shareLink();
	initBeforeAfterSlider();
	toNextSection();
	initShowMore();
	inputCheckForValue();
	initLoadMorePosts();
	labelClick();
	toggleFilter();
	toggleAllFilter();
	closeFilterMobile();
	checkActive();
	filterSpecial();
	initLangListener();
	initForms();
	initCookiePolicy();
	changeProductLocation();
	initHeaderStoreLocator();
    labelSelector();
    formatPhones();
    blogSpacing();
	tireWarrantyRemoval();
	disableStoreDropdown();
	new Scheduler()
});

window.addEventListener('load', () => {
	calculateSize();
	headerScroll();
	printContent();
	initPopup();
    initSchedulePopup();
	closePopup();
	initMap();
	initMainMap();
	innerNavScroll();
	replaceSVG();
	chatOpen();
    initReviewsPopup();
    initServicePopup();
});

document.addEventListener('scroll', () => {
	calculateSize();
	headerScroll();
	innerNavScroll();
});

window.addEventListener('resize', () => {
	calculateSize();
	// docPadding();
	menuPaddings();
	calcMobileWinSize();
});

$(document).ready(() => {
	phoneMask();
    schedulePopup();
})
