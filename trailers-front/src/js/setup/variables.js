// Global
export const $body = document.querySelector('body'); // body
export const mobileMenuBreakpoint = 1024;

const baseUrlMeta = document.querySelector('meta[name="base-url"]');
export const baseUrl = `${new URL(window.location).origin}/`;

// Header
export const $header = document.querySelector('.js-header'); // header
export const headerFixed = $header && !!$header.classList.contains('tp-header--fixed'); // check if header is fixed
export const headerHNumb = $header ? +window.getComputedStyle($header, null).height.split('px')[0] : 0; // Header height
export const $scrollNav = document.querySelector('.js-scroll-nav'); // scroll header
export const $mainNav = document.querySelector('.js-main-nav');

// Navigation
export const $innerNav = document.querySelector('.js-inner-nav');
export const $innerNavScroll = document.querySelector('.js-inner-scroll-nav');

// Cart
export const $cart = document.querySelectorAll('.js-cart'); // cart
export const $cartToggle = document.querySelectorAll('.js-cart-toggle'); // cart toggle

// Swiper
export const BREAKPOINTS = {
	zero: 0,
	xs: 575,
	sm: 768,
	md: 992,
	lg: 1200,
};