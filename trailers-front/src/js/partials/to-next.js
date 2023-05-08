export function toNextSection() {
	$('.js-to-next').on('click', e => {
		e.preventDefault();

		const el = $(e.target).closest('section').next('section');

		if (el.length) {
			$([document.documentElement, document.body]).animate({
				scrollTop: $(el).offset().top - 50,
			}, 300);
		}
	});
}