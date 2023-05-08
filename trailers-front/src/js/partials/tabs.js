/**
 * Tabs
 *
 * @param $target $('.class') - tab link item
 * @param $selector1 '.class' - tabs main wrapper
 * @param $selector2 '.class' - tabs content item
 */

export function tabChange($target, $selector1, $selector2) {
	$target.on('click', function tabClick(e) {
		e.preventDefault();

		const indexEl = $(this)
			.parent()
			.index();

		$(this)
			.parent()
			.addClass('active')
			.siblings()
			.removeClass('active')
			.closest($selector1)
			.find($selector2)
			.removeClass('active')
			.eq(indexEl)
			.addClass('active');
	});
}
