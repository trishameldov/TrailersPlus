/**
 * Make content for hidden Iframe(Print content)
 */

export function printContent() {
	const $printBtn = document.querySelector('.js-product-print');
	const $printElements = document.querySelectorAll('.js-print');
	const $printImage = document.querySelector('.js-print-img');

	const printArr = [];

	if ($printImage) {
		const url = $printImage.classList.contains('lazyload') ? $printImage.dataset.src : $printImage.getAttribute('src');
		printArr.push(`<div class="t-center margin-20t"><img src="${url}"></div>`);
		printArr.push('<div class="margin-30b"></div>');
	}

	if ($printElements) {
		[...$printElements].forEach(elem => {
			printArr.push(elem.innerHTML);
		});
	}

	if ($printBtn) {
		$printBtn.addEventListener('click', () => {
			window.frames.print_frame.window.focus();
			window.frames.print_frame.window.print();
		});
	}
}
