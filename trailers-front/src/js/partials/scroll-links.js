import { mobileMenuBreakpoint } from '../setup/variables';

/**
 * Scroll To ID
 * @param {*} id BlockID
 */

function scrollTo(id) {
	if (id.indexOf('#') >= 0) {
		const headerH = (window.innerWidth > mobileMenuBreakpoint)
			? window.calcSizes.scrollNavH
			: window.calcSizes.headerH;
		const { innerNavScrollH } = window.calcSizes;

		const offsetValue = headerH ? +headerH + +innerNavScrollH : 0;
		const diff = $(id).length && $(id).hasClass('tp-size-block') ? 100 : 0;
		const offsetTop = $(id).length
			? $(id).offset().top - offsetValue - 30 - diff
			: 0;

		if (offsetTop) {
			$('html, body')
				.stop()
				.animate(
					{
						scrollTop: offsetTop,
					},
					350,
				);
		}
	}
}

/**
 * Set scroll to ID on link click
 */

export function setScrollToID() {
	const links = document.querySelectorAll('a[href*="#"]');

	if (links) {
		[...links].forEach(link => {
			$(link).on('click', function click(e) {
				const href = $(this)
					.get(0)
					.getAttribute('href');

				if (href.indexOf('#') === 0 && href.length > 1) {
					e.preventDefault();
					scrollTo(href);
				}
			});
		});
	}
}
