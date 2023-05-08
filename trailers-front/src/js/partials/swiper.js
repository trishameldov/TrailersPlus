import { BREAKPOINTS } from '../setup/variables';

export function swiperInit() {
	const swipers = [];
	const swipersDOM = document.getElementsByClassName('swiper-container');

	// eslint-disable-next-line func-names
	const findClosestDescendant = ($item, el, closest) => $item.find(el).filter(function () {
		return $(this)
			.closest(closest)
			.is($item);
	});

	/**
	 * SET SLIDES TOTAL
	 *
	 * @param slider
	 */
	function setSlidesTotal(slider, zero) {
		const $parent = $(slider).parent();
		let total = $parent.find('.swiper-slide:not(.swiper-slide-duplicate)').length;

		if (zero) {
			total = total < 10 ? `0${total}` : total;
		}

		$parent.find('.swiper-slides-total').html(total);
	}

	/**
	 * Get slides
	 *
	 * @param swiper
	 * @param slider
	 */
	function setSlidesSiblings(swiper, slider, zero) {
		const $parent = $(slider).parent();

		const realIndex = swiper.realIndex + 1;
		const total = $parent.find('.swiper-slide:not(.swiper-slide-duplicate)')
			.length;

		let nextIndex = realIndex + 1;
		nextIndex = nextIndex > total ? nextIndex - total : nextIndex;

		let prevIndex = realIndex - 1;
		prevIndex = prevIndex <= 0 ? total - prevIndex : prevIndex;

		if (zero) {
			nextIndex = nextIndex < 10 ? `0${nextIndex}` : nextIndex;
			prevIndex = prevIndex < 10 ? `0${prevIndex}` : prevIndex;
		}

		$parent.find('.swiper-slides-prev').html(prevIndex);
		$parent.find('.swiper-slides-next').html(nextIndex);
	}

	const initSwiperElement = (_this, key) => {
		const index = `swiper-unique-${key}`;

		_this.classList.add(index);
		_this.setAttribute('id', index);

		/* ----- ARROWS ------ */
		const $parent = $(_this).parent();
		const arrowPrev = findClosestDescendant(
			$parent,
			'.swiper-button-prev',
			'.js-swiper',
		);

		const arrowNext = findClosestDescendant(
			$parent,
			'.swiper-button-next',
			'.js-swiper',
		);

		/* ----- PAGINATION ------ */
		const paginationEl = _this.parentNode.querySelector(
			':not(.swiper-slide) .swiper-pagination',
		);

		if (paginationEl) {
			paginationEl.classList.add(`swiper-pagination-${index}`);
		}

		/* ----- GET PARAMS ----- */
		const touchRatio = _this.getAttribute('data-touch-ratio') !== null ? +_this.getAttribute('data-touch-ratio') : 1;
		const observeParents = !!_this.getAttribute('data-observe-parents');
		const speed = +_this.getAttribute('data-speed') || 500;
		const initialSlide = +_this.getAttribute('data-initial_slide') || 0;
		const autoplayDelay = +_this.getAttribute('data-autoplay') || 0;
		const spaceBetween = +_this.getAttribute('data-spaces') || 0;
		const simulateTouch = !!_this.getAttribute('data-simulate_touch');
		const direction = _this.getAttribute('data-direction') || 'horizontal';
		const effect = _this.getAttribute('data-effect') || 'slide';
		const loop = !!_this.getAttribute('data-loop');
		const progressMove = !!_this.getAttribute('data-progress-move');
		const centeredSlides = !!_this.getAttribute('data-centeredSlides');
		const paginationType = _this.getAttribute('data-pagination-type') || 'bullets';
		const autoHeight = !!_this.getAttribute('data-autoHeight') || false;
		let lazy = +_this.getAttribute('data-lazy') || 0;
		let thumbs = +_this.getAttribute('data-thumbs') || 0;
		let mousewheel = +_this.getAttribute('data-mousewheel') || 0;

		if (mousewheel) {
			mousewheel = {
				invert: false,
			};
		}

		if (lazy) {
			lazy = {
				loadPrevNext: true,
				loadPrevNextAmount: lazy,
				loadOnTransitionStart: true,
			};
		}

		if (thumbs) {
			thumbs = {
				swiper: swipers[`swiper-unique-${key - 1}`],
			};
		}

		let autoplay = false;
		let progressFunc = false;
		let progressFuncSlideChange = false;
		const autoplayTime = autoplayDelay / 100;
		let countF = 1;

		if (autoplayDelay) {
			autoplay = {
				delay: autoplayDelay,
				disableOnInteraction: false,
			};
		}

		if (progressMove) {
			if (!$parent.find(`#aheto-progress-${index}`).length) {
				$parent.prepend(
					`<div id="aheto-progress-${
						index
					}" class="swiper__progress-line"></div>`,
				);
			}
		}

		const slidesPerView = _this.getAttribute('data-slides') || 'auto';

		// responsive sliders count
		const slidesPerView_lg = +_this.getAttribute('data-slides_lg') || slidesPerView;
		const slidesPerView_md = +_this.getAttribute('data-slides_md') || slidesPerView_lg;
		const slidesPerView_sm = +_this.getAttribute('data-slides_sm') || slidesPerView_md;
		const slidesPerView_xs = +_this.getAttribute('data-slides_xs') || slidesPerView_sm;

		// responsive spaces
		const spaces_lg = _this.getAttribute('data-spaces_lg') !== null ? +_this.getAttribute('data-spaces_lg') : spaceBetween;
		const spaces_md = _this.getAttribute('data-spaces_md') !== null ? +_this.getAttribute('data-spaces_md') : spaces_lg;
		const spaces_sm = _this.getAttribute('data-spaces_sm') !== null ? +_this.getAttribute('data-spaces_sm') : spaces_md;
		const spaces_xs = _this.getAttribute('data-spaces_xs') !== null ? +_this.getAttribute('data-spaces_xs') : spaces_sm;

		const breakpoints = {
			[BREAKPOINTS.zero]: {
				slidesPerView: slidesPerView_xs,
				spaceBetween: spaces_xs,
			},
			[BREAKPOINTS.xs]: {
				slidesPerView: slidesPerView_sm,
				spaceBetween: spaces_sm,
			},
			[BREAKPOINTS.sm]: {
				slidesPerView: slidesPerView_md,
				spaceBetween: spaces_md,
			},
			[BREAKPOINTS.md]: {
				slidesPerView: slidesPerView_lg,
				spaceBetween: spaces_lg,
			},
			[BREAKPOINTS.lg]: {
				slidesPerView,
				spaceBetween,
			},
		};

		/* ----- INIT PARAMS ----- */
		// eslint-disable-next-line no-undef
		swipers[index] = new Swiper(`.${index}`, {
			simulateTouch,
			direction,
			initialSlide,
			speed,
			autoplay,
			spaceBetween,
			loop,
			autoHeight,
			lazy,
			thumbs,
			effect,
			slidesPerView,
			centeredSlides,
			breakpoints,
			mousewheel,
			observeParents,
			touchRatio,
			loopAdditionalSlides: 4,
			paginationClickable: false,
			keyboardControl: true,
			calculateHeight: true,
			roundLengths: true,
			cssWidthAndHeight: true,
			noSwiping: true,
			noSwipingClass: 'swiper-no-swiping',
			watchSlidesVisibility: true,
			slideVisibleClass: 'swiper-slide-visible',
			slideToClickedSlide: true,
			observer: true,	// update slider on style changes
			watchOverflow: true, // hide navigation if no slides for slide
			observeParents: true,
			coverflowEffect: {
				rotate: 30,
				slideShadows: false,
			},
			navigation: {
				nextEl: arrowNext,
				prevEl: arrowPrev,
			},
			pagination: {
				el: `.swiper-pagination-${index}`,
				type: paginationType,
				clickable: true,
				// eslint-disable-next-line no-shadow
				renderBullet(index, className) {
					if (_this.querySelector('.swiper-pagination--numeric')) {
						return `<span class="${className}">${
							index < 9 ? '0' : ''
						}${index + 1}</span>`;
					}

					return `<span class="${className}"></span>`;
				},
			},

			on: {
				init() {
					if (
						arrowNext.length
						&& arrowNext.hasClass('swiper-button-next--number')
					) {
						setSlidesTotal(_this, false);
						setSlidesSiblings(this, _this, false);
					}
					if (
						arrowNext.length
						&& arrowNext.hasClass('swiper-button-next--number-zero')
					) {
						setSlidesTotal(_this, true);
						setSlidesSiblings(this, _this, true);
					}

					if (progressMove) {
						let width = 0;

						progressFunc = setInterval(() => {
							if (width > 100) {
								$(`#aheto-progress-${index}`).width('0%');

								clearInterval(progressFunc);
							} else {
								$(`#aheto-progress-${index}`).width(
									`${width}%`,
								);
								width++;
							}
						}, autoplayTime);
					}
				},
				slideChangeTransitionStart() {
					if (progressMove && countF > 1) {
						clearInterval(progressFuncSlideChange);
						clearInterval(progressFunc);

						$(`#aheto-progress-${index}`).width('0%');

						setTimeout(() => {
							let width = 0;

							progressFuncSlideChange = setInterval(() => {
								if (width > 100) {
									$(`#aheto-progress-${index}`).width('0%');
									clearInterval(progressFuncSlideChange);
								} else {
									$(`#aheto-progress-${index}`).width(
										`${width}%`,
									);
									width++;
								}
							}, autoplayTime);
						}, speed);
					}

					countF++;
				},
				slideChange() {
					if (
						arrowNext.length
						&& arrowNext.hasClass('swiper-button-next--number')
					) {
						setSlidesSiblings(this, _this, false);
					}
					if (
						arrowNext.length
						&& arrowNext.hasClass('swiper-button-next--number-zero')
					) {
						setSlidesSiblings(this, _this, true);
					}
				},
			},
		});
	};

	window.initSwiper = target => {
		if (target) {
			Array.prototype.forEach.call(target, initSwiperElement);
		}
	};

	window.initSwiper(swipersDOM);
}