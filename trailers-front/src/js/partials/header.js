import {
	$header, headerHNumb, $scrollNav, $mainNav, mobileMenuBreakpoint,
} from '../setup/variables';

/**
 * Toggle navbar
 */

export function toggleNavbar() {
	const ANIMATION_TIME = 250;
	const navbarToggle = document.querySelector('.js-nav-toggle');
	const navbarClose = document.querySelector('.js-nav-close');
	let closing = false;

	navbarToggle.addEventListener('click', function navbartoggle() {
		if (this.classList.contains('open')) {
			closing = true;
			$mainNav.classList.add('closing');
			this.classList.remove('open');
			$mainNav.classList.remove('open');
			window.scrollControl.disable();

			setTimeout(() => {
				$mainNav.classList.remove('closing');
				closing = false;
			}, ANIMATION_TIME);
		} else {
			if (!closing) {
				this.classList.add('open');
				$mainNav.classList.add('open');
				window.scrollControl.enable();
			}
		}
	});

	navbarClose.addEventListener('click', () => {
		navbarToggle.click();
	});
}

/**
 * Navbar on Scroll
 */

export function headerScroll() {
	const scrollPos = window.scrollY
		|| window.scrollTop
		|| document.getElementsByTagName('html')[0].scrollTop;

	if (scrollPos > headerHNumb + 100) {
		$scrollNav.classList.add('open');
	} else {
		$scrollNav.classList.remove('open');
	}
}

/**
 * Get children elements
 * @param {*} node node element on which u need to get a child elements
 * @param {*} itemClass class of element what u want to get
 * @param {*} notClass not selector(exclude elemenents by className / default = null)
 */

function getChildNodes(node, itemClass, notClass = null) {
	const children = [];

	[...node.childNodes].forEach((child) => {
		if (child.nodeType === 1 && child.classList.contains(itemClass) && !child.classList.contains(notClass)) {
			children.push(child);
		}
	});

	return children;
}

/**
 * Paddings for mega menu
 */

export function menuPaddings() {
	const menuItems = document.querySelectorAll('.tp-nav__list > li');
	const menuPadding = () => (window.innerWidth > 1210 ? ((window.innerWidth - 1190) / 2) : null);

	if (menuPadding) {
		[...menuItems].forEach((item) => {
			const subMenuWrapp = getChildNodes(item, 'js-submenu');
			const padd = menuPadding();
			if (subMenuWrapp[0]) {
				subMenuWrapp[0].style.paddingLeft = `${padd}px`;
				subMenuWrapp[0].style.paddingRight = `${padd}px`;
			}
		});
	}
}


/**
 * Check mega menu child items count
 */

export function menuChildCount() {
	const subMenus = document.querySelectorAll('.js-submenu');

	if (subMenus.length) {
		[...subMenus].forEach((menu) => {
			const ul = menu.querySelector('ul');
			const count = menu.querySelectorAll('li');

			if (count && count.length > 7 && ul) {
				ul.classList.add('small');
			}
		});
	}
}

/**
 * Open inner menu on mobile
 * @param {*} $target dropdown toggle element
 * @param {*} $content content slide wrapp
 * @param {*} $closest dropdown wrapper
 * @param {*} $closestClass class which will be added to dropdown wrap on open
 */

export function mobileNavEvents($target, $content, $closest, $closestClass = null) {
	const submenuToggle = document.querySelectorAll($target);

	[...submenuToggle].forEach((item) => {
		item.addEventListener('click', function click(e) {
			e.stopPropagation();

			const $subMenu = this.closest($closest).querySelector($content);

			if (this.classList.contains('is-active')) {
				$subMenu.classList.remove('open');
				$($subMenu).slideUp(350);
				this.classList.remove('is-active');
				// eslint-disable-next-line no-unused-expressions
				$closestClass && this.closest($closest).classList.remove($closestClass);
			} else {
				$($subMenu).slideDown(350, () => {
					$subMenu.classList.add('open');
				});
				this.classList.add('is-active');
				// eslint-disable-next-line no-unused-expressions
				$closestClass && this.closest($closest).classList.add($closestClass);
			}
		});
	});
}

/**
 * Open active mobile menu on load
 */

export function openActive() {
	if (window.innerWidth <= mobileMenuBreakpoint) {
		const $mainNavToggleBtn = document.querySelectorAll('.js-submenu-toggle');

		[...$mainNavToggleBtn].forEach((elem) => {
			const $li = elem.closest('li');
			const $subMenu = $(elem).parent().find('> .js-submenu');

			if ((($li.classList.contains('active')
				|| $li.classList.contains('parent-active'))
				&& !elem.classList.contains('is-active'))) {
				$subMenu.css('display', 'block');
				elem.classList.add('is-active');
				$subMenu.addClass('open');
			}
		});
	}
}

/**
 * Window height + Header height for mobile
 */
export function calcMobileWinSize() {
	const vh = window.innerHeight * 0.01;
	const headerH = $header ? +window.getComputedStyle($header, null).height.split('px')[0] : 0;
	document.documentElement.style.setProperty('--windowHeight', `${vh}px`);	// fixing mobile additional header heaight in vieport
	document.documentElement.style.setProperty('--headerHeight', `${headerH}px`);
}