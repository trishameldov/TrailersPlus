/**
 * Pricde slider
 */
export function priceSlider() {
	if ($('#slider-range').length) {
		$('#slider-range').slider({
			range: true,
			step: +$('#slider-range').data('step'),
			min: +$('#slider-range').data('min'),
			max: +$('#slider-range').data('max'),
			values: [
				+$('#slider-range').attr('data-price-first'),
				+$('#slider-range').attr('data-price-second'),
			],
			create() {
				const slides = $('#slider-range').find('.ui-slider-handle');
				$(slides[0]).attr(
					'data-value',
					$('#slider-range').slider('values', 0),
				);
				$(slides[1]).attr(
					'data-value',
					$('#slider-range').slider('values', 1),
				);
			},
			slide(_event, ui) {
				const slides = $('#slider-range').find('.ui-slider-handle');
				$(slides[0]).attr('data-value', ui.values[0]);
				$(slides[1]).attr('data-value', ui.values[1]);
			},
		});
	}
}
