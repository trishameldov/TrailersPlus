import { $cartToggle } from '../setup/variables';

/**
 * Open / close cart on mobile
 */
export function cartOpen() {
	if ($cartToggle) {
		[...$cartToggle].forEach(cart => {
			cart.addEventListener('touchstart', function cartClick(e) {
				e.preventDefault();
				if (this.parentNode.classList.contains('open')) {
					this.parentNode.classList.remove('open');
				} else {
					this.parentNode.classList.add('open');
				}
			});
		});
	}
}

/**
 * Close cart on document click
 */
export function closeCart() {
	document.addEventListener('click', e => {
		if (e.target && !e.target.closest('.js-cart') && !e.target.classList.contains('js-to-cart-btn') && !e.target.classList.contains('js-reserv-btn')) {
			$('.js-cart').removeClass('open', 'added');
		}
	});
}
