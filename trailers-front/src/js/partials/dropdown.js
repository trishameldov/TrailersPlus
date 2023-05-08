/**
 * Tp Dropdown
 */

export const saaDropdown = () => {
	const dropdowns = document.querySelectorAll('.js-dropdown');

	[...dropdowns].forEach(item => {
		const head = item.querySelector('.tp-dropdown__head');
		head.addEventListener('click', () => {
			if (item.classList.contains('open')) {
				item.classList.remove('open');
			} else {
				[...dropdowns].forEach(drop => {
					drop.classList.remove('open');
				});
				item.classList.add('open');
			}
		});
	});
};

/**
 * Close dropdown on document click
 */
export function closeDropdown() {
	document.addEventListener('click', e => {
		if (e.target && !e.target.closest('.js-dropdown')) {
			const dropdowns = document.querySelectorAll('.js-dropdown');
			[...dropdowns].forEach(item => {
				if (item.classList.contains('open')) {
					item.classList.remove('open');
				}
			});
		}
	});
}

/**
 * Open active dropdown on load
 */

export function openActiveDrop() {
	const $dropdown = document.querySelectorAll('.js-drop-wrapp');

	[...$dropdown].forEach(item => {
		const $active = item.querySelector('.active');

		if ($active) {
			const $toggle = item.querySelector('.js-drop-toggle');
			const $content = item.querySelector('.js-drop-content');

			if (!item.classList.contains('open')) {
				item.classList.add('open');
			}
			if (!$toggle.classList.contains('is-active')) {
				$toggle.classList.add('is-active');
			}
			$content.style.display = 'block';
		}
	});
}
