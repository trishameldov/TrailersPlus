import { setCookie } from '../utils/cookies.utils';

export function initCookiePolicy() {
	const policyBlock = document.getElementById('cookie-policy');

	if (policyBlock) {
		const btn = policyBlock.querySelector('.js-accept-btn');

		btn.addEventListener('click', event => {
			event.preventDefault();
			setCookie('policy', 'accept');
			policyBlock.style.display = 'none';
		});
	}
}
