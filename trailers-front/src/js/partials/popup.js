/**
 * Magnific Popup
 */

export function initPopup() {
	$('.js-popup').each(function popup() {
		const $this = $(this);
		const type = $(this).data('type') ? $(this).data('type') : 'inline';

		$this.magnificPopup({
			type,
			midClick: true,
			mainClass: 'mfp-fade',
			closeOnBgClick: false,
			iframe: {
				markup:
					`<div class="mfp-iframe-scaler">
					<div class="mfp-close"></div>
					<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>
					</div>`,
			},
			callbacks: {
				open: () => {
					// eslint-disable-next-line no-unused-expressions
					window.scrollControl.enable();
				},
				close: () => {
					// eslint-disable-next-line no-unused-expressions
					window.scrollControl.disable();
				},
			},
		});
	});
}

export function initSchedulePopup() {
    $('.js-popup-schedule').each(function popup() {
        const $this = $(this);
        const type = $(this).data('type') ? $(this).data('type') : 'inline';

        $this.magnificPopup({
            type,
            midClick: true,
            mainClass: 'mfp-fade',
            closeOnBgClick: false,
            iframe: {
                markup:
                    `<div class="mfp-iframe-scaler">
                    <div class="mfp-close"></div>
                    <iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>
                    </div>`,
            },
            callbacks: {
                open: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.enable();
                    window.history.pushState("", "", '#schedule');
                },
                close: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.disable();
                },
            },
        });
    });
}

export function closePopup() {
	$('.js-close-popup').on('click', () => {
		$.magnificPopup.close();
	});

	document.addEventListener('mousedown', e => {
		if (e.target && (e.target.classList.contains('mfp-content') || e.target.classList.contains('mfp-container'))) {
			$.magnificPopup.close();
		}
	});
}


export function schedulePopup(){
    // Load schedule pop up on url with #schedule 
    var urlTemp = window.location.href;
    var indexUrl = urlTemp.indexOf("#");
    if (indexUrl !== -1)
    {
        var hash = urlTemp.substring(indexUrl + 1);
        console.log(hash);
        
        if (hash == 'schedule' || hash == 'schedule/') {
            $('.js-popup-schedule, .js-popup-service').magnificPopup({
                type: 'inline',
                midClick: true,
                mainClass: 'mfp-fade',
                closeOnBgClick: false,
                iframe: {
                    markup:
                        `<div class="mfp-iframe-scaler">
                        <div class="mfp-close"></div>
                        <iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>
                        </div>`,
                },
                callbacks: {
                    open: () => {
                        // eslint-disable-next-line no-unused-expressions
                        window.scrollControl.enable();
                    },
                    close: () => {
                        // eslint-disable-next-line no-unused-expressions
                        window.scrollControl.disable();
                    },
                },
            }, 0).magnificPopup('open');
        }
    }   
}

export function initReviewsPopup() {
    $('.js-popup-reviews').each(function popup() {
        const $this = $(this);
        const type = $(this).data('type') ? $(this).data('type') : 'inline';
        console.log('reviews popup');
        $this.magnificPopup({
            type,
            midClick: true,
            mainClass: 'mfp-fade',
            closeOnBgClick: false,
            iframe: {
                markup:
                    `<div class="mfp-iframe-scaler">
                    <div class="mfp-close"></div>
                    <iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>
                    </div>`,
            },
            callbacks: {
                open: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.enable();
                },
                close: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.disable();
                },
            },
        });
    });
}

export function initServicePopup() {
    $('.js-popup-service').each(function popup() {
        const $this = $(this);
        const type = $(this).data('type') ? $(this).data('type') : 'inline';

        $this.magnificPopup({
            type,
            midClick: true,
            mainClass: 'mfp-fade',
            closeOnBgClick: false,
            iframe: {
                markup:
                    `<div class="mfp-iframe-scaler">
                    <div class="mfp-close"></div>
                    <iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>
                    </div>`,
            },
            callbacks: {
                open: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.enable();
                    window.history.pushState("", "", '#schedule');
                },
                close: () => {
                    // eslint-disable-next-line no-unused-expressions
                    window.scrollControl.disable();
                },
            },
        });
    });
}
