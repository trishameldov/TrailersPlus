/* eslint-disable no-restricted-globals */
import {
	$scrollNav, $innerNav, $innerNavScroll, mobileMenuBreakpoint,
} from '../setup/variables';

const supportPageOffset = window.pageXOffset !== undefined;
const isCSS1Compat = (document.compatMode || '') === 'CSS1Compat';

/**
 * return offset values of DOM element
 * @param {*} elem DOM element
 */

function getCoords(elem) {
	const box = elem.getBoundingClientRect();

	return {
		top: box.top + pageYOffset,
		left: box.left + pageXOffset,
	};
}

/**
 * make inner naviagation fixed on scroll
 */

export function innerNavScroll() {
	if ($innerNav && window.innerWidth > mobileMenuBreakpoint) {
		const scrollNavH = +window.getComputedStyle($scrollNav).height.split('px')[0];
		const { innerNavH } = window.calcSizes;
		const navOffsetTop = $innerNav ? getCoords($innerNav).top : 0;
		// eslint-disable-next-line no-nested-ternary
		const pageScrollY = supportPageOffset
			? window.pageYOffset
			: isCSS1Compat
				? document.documentElement.scrollTop
				: document.body.scrollTop;

		if (pageScrollY + scrollNavH > navOffsetTop + innerNavH) {
			$innerNavScroll.style.top = `${scrollNavH}px`;
			$innerNavScroll.classList.remove('hide');
		} else {
			$innerNavScroll.style.top = '-200px';
			$innerNavScroll.classList.add('hide');
		}
	}
}
