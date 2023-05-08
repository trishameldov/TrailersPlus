export function initShowMore() {
	$('.js-desc-wrapper').each((i, el) => {
		$(el).find('p').css('-webkit-line-clamp', '3');
	});

	$(document).on('click', '.js-show-more', e => {
		e.preventDefault();
		$(e.target).closest('div').find('.js-desc-wrapper p').css('-webkit-line-clamp', 'initial');
		$(e.target).remove();
	});
}