/* eslint-disable no-restricted-globals */
/* eslint-disable no-nested-ternary */
/* eslint-disable max-len */

function shareLinkToFacebook(event) {
	event.preventDefault();

	const w = 550;
	const h = 750;
	const url = `https://www.facebook.com/sharer/sharer.php?u=${location.href.split('#')[0]}`;

	const dualScreenLeft = window.screenLeft !== undefined ? window.screenLeft : window.screenX;
	const dualScreenTop = window.screenTop !== undefined ? window.screenTop : window.screenY;

	const width = window.innerWidth ? window.innerWidth : document.documentElement.clientWidth ? document.documentElement.clientWidth : screen.width;
	const height = window.innerHeight ? window.innerHeight : document.documentElement.clientHeight ? document.documentElement.clientHeight : screen.height;

	const systemZoom = width / window.screen.availWidth;
	const left = (width - w) / 2 / systemZoom + dualScreenLeft;
	const top = (height - h) / 2 / systemZoom + dualScreenTop;
	const newWindow = window.open(url, 'Share to Facebook',
		`
			scrollbars=yes,
			width=${w / systemZoom}, 
			height=${h / systemZoom}, 
			top=${top}, 
			left=${left}
		`);

	if (window.focus) newWindow.focus();
}

export function shareLink() {
	const fbLinks = document.querySelectorAll('.js-saring-fb');

	[...fbLinks].forEach(el => {
		el.addEventListener('click', shareLinkToFacebook);
	});
}