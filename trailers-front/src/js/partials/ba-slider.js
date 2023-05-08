export function initBeforeAfterSlider() {
	let active = false;
	let activeContainer = null;

	// First we'll have to set up our event listeners
	// We want to watch for clicks on our scroller
	$('.js-scroller').on('mousedown', event => {
		active = true;
		activeContainer = $(event.target).closest('.js-ba-slider');
		// Add our scrolling class so the scroller has full opacity while active
		$('.js-scroller', activeContainer)[0].classList.add('scrolling');
	});

	// We also want to watch the body for changes to the state,
	// like moving around and releasing the click
	// so let's set up our event listeners
	document.body.addEventListener('mouseup', () => {
		active = false;
		if (activeContainer) {
			$('.js-scroller', activeContainer)[0].classList.remove('scrolling');
		}
	});

	document.body.addEventListener('mouseleave', () => {
		active = false;

		if (activeContainer) {
			$('.js-scroller', activeContainer)[0].classList.remove('scrolling');
		}
	});

	// Let's use this function
	function scrollIt(x, el) {
		const transform = Math.max(0, (Math.min(x, $('.js-wrapper', el)[0].offsetWidth)));
		$('.js-after', el)[0].style.width = `${transform}px`;
		$('.js-scroller', el)[0].style.left = `${transform - 12}px`;
	}

	// Let's set our opening state based off the width,
	// we want to show a bit of both images so the user can see what's going on
	$('.js-ba-slider').each((i, el) => {
		const blockWidth = $(el).width();
		scrollIt(blockWidth / 2, el);
	});

	window.addEventListener('resize', () => {
		$('.js-ba-slider').each((i, el) => {
			const blockWidth = $(el).width();
			scrollIt(blockWidth / 2, el);
		});
	});

	// Let's figure out where their mouse is at
	document.body.addEventListener('mousemove', (e) => {
		if (!active) return;
		// Their mouse is here...
		let x = e.pageX;
		// but we want it relative to our wrapper
		x -= $('.js-wrapper', activeContainer)[0].getBoundingClientRect().left;
		// Okay let's change our state
		scrollIt(x, activeContainer);
	});

	document.body.addEventListener('touchmove', e => {
		if (!active) return;

		let touch;

		if (e.touches) {
			// eslint-disable-next-line prefer-destructuring
			touch = e.touches[0];
		}

		let x = e.pageX || touch.pageX;
		x -= $('.js-wrapper', activeContainer)[0].getBoundingClientRect().left;

		scrollIt(x, activeContainer);
	});

	// And finally let's repeat the process for touch events
	// first our middle scroller...
	$('.js-scroller').on('touchstart', event => {
		active = true;
		activeContainer = $(event.target).closest('.js-ba-slider');
		$('.js-scroller', activeContainer)[0].classList.add('scrolling');
	});

	document.body.addEventListener('touchend', () => {
		active = false;

		if (activeContainer) {
			$('.js-scroller', activeContainer)[0].classList.remove('scrolling');
		}
	});

	document.body.addEventListener('touchcancel', () => {
		active = false;

		if (activeContainer) {
			$('.js-scroller', activeContainer)[0].classList.remove('scrolling');
		}
	});
}