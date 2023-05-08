/* eslint-disable no-unused-expressions */
/* eslint-disable no-undef */
import { getCookie } from '../utils/cookies.utils'

/**
 * Make LiveChat button HTML
 * @param {Boolean} status Is chat online?
 * @param {String} lang site language
 */
function btnHtml(status, lang) {
	const btnText = status
		? lang === 'es'
			? 'Chat en vivo'
			: 'Live Chat'
		: lang === 'es'
			? 'Correo Electrónico'
			: 'Email';

	return `
        <a href="#" class="tp-btn tp-btn--red tp-chat-btn js-chat-btn">
            <i class="fa fa-commenting" aria-hidden="true"></i>
            ${btnText}
        </a>
    `;
}

/**
 * Live chat API
 */
export function chatOpen(lang = 'en') {
	// eslint-disable-next-line no-restricted-globals

	lang = getCookie("django_language") || lang
	document.addEventListener('click', e => {
		if (e.target && e.target.closest('.js-chat-btn')) {
			e.preventDefault();
			window.SnapEngage && window.SnapEngage.openProactiveChat(true, true);
		}
	});

	window.SnapEngage && window.SnapEngage.getAgentStatusAsync(online => {
		const btn = btnHtml(online, lang);
		document.body.insertAdjacentHTML('beforeend', btn);
	});
}
