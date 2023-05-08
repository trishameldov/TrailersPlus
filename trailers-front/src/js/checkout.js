/* eslint-disable no-unused-expressions */
/* eslint-disable class-methods-use-this */
import { getCookie } from './utils/cookies.utils'
import { baseUrl } from './setup/variables'
class Checkout {
	constructor($root) {
		this.$root = $root && document.getElementById($root);
		this.step = 1;
		this.maxStep = 3;
		this.minStep = 1;
		this.$steps = this.$root && this.$root.querySelectorAll('.js-step');
		this.$contentBox = this.$root && this.$root.querySelector('.js-content-box');
		this.$contents = this.$contentBox && this.$contentBox.querySelectorAll('.js-content');
		this.$backBtn = this.$root && this.$root.querySelector('.js-checkout-back');
		this.$nextBtn = this.$root && this.$root.querySelector('.js-checkout-next');
		this.$payBtn = this.$root && this.$root.querySelector('.js-checkout-pay');
		this.$form = this.$root && this.$root.closest('form');
		this.$confirmbox = this.$contentBox && this.$contentBox.querySelector('.js-confirmation-info');
		this.$errors = this.$root && this.$root.querySelector('.js-checkout-errors');
		this.$cvv = this.$root && this.$root.querySelector('.js-ccv-input');
		this.$expirity = this.$root && this.$root.querySelector('.js-expirity');
		this.$zip = this.$root && this.$root.querySelector('.js-zip-code');
		this.$card = this.$root && this.$root.querySelector('.js-card-input');
		this.$acceptUI = this.$root && this.$root.querySelector('.AcceptUI');
	}

	createData() {
		const data = {};
		if (this.$contents && this.$contents.length) {
			[...this.$contents].forEach(form => {
				const inputs = form.querySelectorAll('input');

				if (inputs && inputs.length) {
					[...inputs].forEach(input => {
						const { value, name } = input;

						if (value.trim()) {
							data[name] = value.trim();
						}
					});
				}
			});
		}

		return data;
	}

	checkStep() {
		var back_button = document.getElementById("back_btn");
		var buttons = document.getElementById("buttons_nxt_back");
		if (this.step === this.minStep) {
			this.$backBtn.disabled = true;
		}
		if (this.step === this.maxStep) {
			this.$nextBtn.classList.add('d-none');
			this.$payBtn.classList.remove('d-none');
			const html = this.makeCustomerHTML(this.createData());
			this.$confirmbox.insertAdjacentHTML('afterbegin', html);
		} else {
			// eslint-disable-next-line no-unused-expressions
			buttons.classList.remove("next_button__right");
			back_button.classList.remove("back_button__disable");
			!this.$payBtn.classList.contains('d-none') && this.$payBtn.classList.add('d-none');
			this.$nextBtn.classList.remove('d-none');
		}
	}

	checkExpitiry() {
		if (this.$expirity) {
			this.$expirity.addEventListener('input', event => {
				const code = event.keyCode;
				const allowedKeys = [8];
				const { value } = event.target;

				if (value.length < 5) {
					event.target.classList.add('not-valid');
				} else {
					event.target.classList.remove('not-valid');
				}

				if (allowedKeys.indexOf(code) !== -1) {
					return;
				}

				// eslint-disable-next-line no-param-reassign
				event.target.value = event.target.value
					.replace(
						/^([1-9]\/|[2-9])$/g,
						'0$1/', // 3 > 03/
					)
					.replace(
						/^(0[1-9]|1[0-2])$/g,
						'$1/', // 11 > 11/
					)
					.replace(
						/^([0-1])([3-9])$/g,
						'0$1/$2', // 13 > 01/3
					)
					.replace(
						/^(0?[1-9]|1[0-2])([0-9]{2})$/g,
						'$1/$2', // 141 > 01/41
					)
					.replace(
						/^([0]+)\/|[0]+$/g,
						'0', // 0/ > 0 and 00 > 0
					)
					.replace(
						// eslint-disable-next-line no-useless-escape
						/[^\d\/]|^[\/]*$/g,
						'', // To allow only digits and `/`
					)
					.replace(
						/\/\//g,
						'/', // Prevent entering more than 1 `/`
					);
			});
		}
	}

	checkCVV() {
		if (this.$cvv) {
			this.$cvv.addEventListener('input', e => {
				const { value } = e.target;

				if (value.length > 2 && value.length < 5) {
					e.target.classList.remove('not-valid');
				} else {
					e.target.classList.add('not-valid');
				}
			});
		}
	}

	checkZip() {
		if (this.$zip) {
			this.$zip.addEventListener('input', e => {
				const { value } = e.target;

				if (value.length !== 5) {
					e.target.classList.add('not-valid');
				} else {
					e.target.classList.remove('not-valid');
					e.target.classList.add('valid');
				}
			});
		}
	}

	checkValid() {
		const currentForm = this.$contentBox ? this.$contentBox.querySelector(`[data-index="${this.step}"]`) : null;

		if (currentForm && (this.step < this.maxStep)) {
			const inputs = currentForm.querySelectorAll('input');

			if (inputs && inputs.length) {
				const errorInputs = [...inputs].filter(input => input.classList.contains('not-valid') || !input.checkValidity());

				if (errorInputs.length) {
					this.$errors.classList.remove('d-none');
					errorInputs[0].focus();

					if (errorInputs[0].type === 'checkbox') {
						!errorInputs[0].classList.contains('not-valid') && errorInputs[0].classList.add('not-valid');

						errorInputs[0].addEventListener('change', function changeCheckbox() {
							if (this.checked) {
								this.classList.remove('not-valid');
							}
						});
					}
					return false;
				}
			}
		}

		!this.$errors.classList.contains('d-none') && this.$errors.classList.add('d-none');
		return true;
	}

	checkCardNumber(target) {
		const cardTypes = {
			visa: /^4[0-9]{12}(?:[0-9]{3})?$/,
			visa2: /^4\d{3}-?\d{4}-?\d{4}-?\d{4}$/,
			visa3: /^4\d{3}\s?\d{4}\s?\d{4}\s?\d{4}$/,
			mastercard: /^5[1-5][0-9]{14}$/,
			mastercard2: /^5[1-5]\d{2}-?\d{4}-?\d{4}-?\d{4}$/,
			mastercard3: /^5[1-5]\d{2}\s?\d{4}\s?\d{4}\s?\d{4}$/,
			amex: /^3[47][0-9]{13}$/,
			amex2: /^3[47][0-9]{2}-[0-9]{6}-[0-9]{5}$/,
			amex3: /^3[47][0-9]{2}\s[0-9]{6}\s[0-9]{5}$/,
			discover: /^6(?:011|5[0-9]{2})[0-9]{12}$/,
			discover2: /^6011-?\d{4}-?\d{4}-?\d{4}$/,
			discover3: /^6011\s?\d{4}\s?\d{4}\s?\d{4}$/,
			express: /^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$/
		};

		// eslint-disable-next-line no-extend-native
		String.prototype.toCardFormat = function toCardFormat() {
			function cardFormat(str, l, i) {
				return str + (!i || i % 4 ? '' : '-') + l;
			}
			return this.replace(/[^0-9]/g, '')
				.substr(0, 16)
				.split('')
				.reduce(cardFormat, '');
		};

		function matchCard(cardVal) {
			const pattern = /^[\d]{4}-[\d]{4}-[\d]{4}-[\d]{3,4}$/
			return pattern.test(cardVal)

			return (
				cardTypes.visa.test(cardVal)
				|| cardTypes.visa2.test(cardVal)
				|| cardTypes.visa3.test(cardVal)
				|| cardTypes.mastercard.test(cardVal)
				|| cardTypes.mastercard2.test(cardVal)
				|| cardTypes.mastercard3.test(cardVal)
				|| cardTypes.amex.test(cardVal)
				|| cardTypes.amex2.test(cardVal)
				|| cardTypes.amex3.test(cardVal)
				|| cardTypes.discover.test(cardVal)
				|| cardTypes.discover2.test(cardVal)
				|| cardTypes.discover3.test(cardVal)
				|| cardTypes.express.test(cardVal)
			);
		}

		if (target) {
			target.addEventListener('input', e => {
				e.target.classList.add('not-valid');
				e.target.value = e.target.value.toCardFormat();

				if (matchCard(e.target.value)) {
					e.target.classList.remove('not-valid');
				}
			});
		}
	}

	stepEvents(stepElement, index) {
		stepElement.classList.remove('active');
		stepElement.classList.remove('done');

		if (this.step === index) {
			stepElement.classList.add('active');
		} else if (index < this.step) {
			stepElement.classList.remove('active');
			stepElement.classList.add('done');
		} else {
			stepElement.classList.remove('active');
			stepElement.classList.remove('done');
		}
	}


	setActiveStep() {
		if (this.$steps) {
			[...this.$steps].forEach(item => {
				const index = +item.dataset.index;
				this.stepEvents(item, index);

				item.addEventListener('click', () => {
					if (index !== this.step) {
						if (index > this.step) {
							if (index - this.step === 2) {
								this.$nextBtn.click();
								this.$nextBtn.click();
							} else {
								this.$nextBtn.click();
							}
						} else {
							if (this.step - index === 2) {
								this.$backBtn.click();
								this.$backBtn.click();
							} else {
								this.$backBtn.click();
							}
						}
					}
				});
			});
		}
	}

	setActiveContent() {
		if (this.$contents && this.$contents.length) {
			[...this.$contents].forEach(item => {
				const index = +item.dataset.index;
				if(index === 2) {
					this.$acceptUI.click();
				}

				if (index !== this.step) {
					item.classList.remove('active');
				} else {
					item.classList.add('active');
				}
			});
		}
	}

	scroltoTop() {
		$('html, body')
			.stop()
			.animate(
				{
					scrollTop: 0,
				},
				350,
			);
	}

	nextClick() {
		if (this.$nextBtn) {
			this.$nextBtn.addEventListener('click', () => {
				if (this.checkValid()) {
					if (this.step < this.maxStep) {
						this.step++;
						this.setActiveStep();
						this.setActiveContent();
					}
					if (this.step > this.minStep) {
						if (this.$backBtn) {
							this.$backBtn.disabled = false;
						}
					}
					this.checkStep();
					this.scroltoTop();
				}
			});
		}
	}

	payClick () {
		this.$root.querySelector('.js-send').addEventListener('click', (e) => {	
			e.preventDefault();
			this.payClickRequest($(this.$form).serialize()).then((res) => {
				this.nextClick();
			});
		});
	}
	toJSONString( form ) {
		var obj = {};
		var elements = form.querySelectorAll( "input, select, textarea" );
		for( var i = 0; i < elements.length; ++i ) {
			var element = elements[i];
			var name = element.name;
			var value = element.value;
			if( name ) {
				obj[ name ] = value;
			}
		}
		return JSON.stringify( obj );
	}
	
	
	prepare_payload(){
        var firstname = document.getElementById("firstname").value;
        var lastname = document.getElementById("lastname").value;
        var trailer_id = document.getElementById("trailer_id").value;
        var email = document.getElementById("email").value;
        var phone = document.getElementById("phone").value;
        var zip = document.getElementById("zip").value;
        var refId = document.getElementById("refId").value
        var bank_auth_code = document.getElementById("authCode").value
        var auth_net_trans = document.getElementById("transId").value
        var card_number = document.getElementById("accountNumber").value
        var card_brand = document.getElementById("accountType").value
        var status = document.getElementById("responseCode").value
        var dataDescriptor = document.getElementById("dataDescriptor").value
        var dataValue = document.getElementById("dataValue").value

        return JSON.stringify({
            firstname: firstname,
            lastname: lastname,
            trailer_id: trailer_id,
            email: email,
            phone: phone,
            zip_code: zip,
            transaction: {
                refId: refId,
                dataDescriptor: dataDescriptor,
                dataValue: dataValue,
                bank_auth_code: bank_auth_code,
                auth_net_trans: auth_net_trans,
                card_number: card_number,
                card_brand: card_brand,
                status: status
            }
        });
	}

	async payClickRequest(data) {
		try {
			this.preloader();
			let url = `${baseUrl}`
			
			if (location.protocol !== 'https:') {
				url = url.replace(/^http:\/\//i, '//');
			}
			console.log(`${url}api/checkout-test/`);
			const rawResponse = await fetch(`${url}api/checkout-test/`, {
				method: 'POST',
                body: this.prepare_payload(),
                headers: {
                    'Content-Type': 'application/json',
                },
			})
			const statusCode = rawResponse.status;
			const response = await rawResponse.json();
			const errorMessage = response.error ? response.error : 'Oooops! Something went wrong.';

			switch(statusCode) {
				case 200:
				case 201:
					location.href = `${url}success-checkout/`;
					break;
				case 400:
				case 502:
					$(this.$root).find('.simple__preloader').remove();
					this.popup(errorMessage);
					break;
				default:
					console.log(`Unexpected status code: ${statusCode}`);
					$(this.$root).find('.simple__preloader').remove();
					this.popup(errorMessage);
					break;
			};
		}
		catch(error) {
			console.log(error);
			debugger;
			$(this.$root).find('.simple__preloader').remove();
			this.popup('Oooops! Something went wrong.');
		}
    }
	popup(mess) {
		let temp = this.htmlToElement(`
		<div class="simple__popup">
			<div class="simple__popup-overlay"></div>
			<div class="simple__popup-inner">
				<span class="close">×</span>
				<p>${mess}</p>
			</div>
		</div>`);
		let close = $(temp).find('.close');
		$(close).on('click', function() {
			$(temp).remove();
	   	});
		this.$root.append(temp);
	}
	preloader() {
		let temp = this.htmlToElement(`<div class="simple__preloader">
		<div class="simple__preloader-overlay"></div>
		<svg version="1.1"
		xmlns="http://www.w3.org/2000/svg"
		xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="25 25 50 50">
		<circle cx="50" cy="50" r="20" fill="none" stroke-width="5" stroke="#f3383f" stroke-linecap="round" stroke-dashoffset="0" stroke-dasharray="100, 200">
		  <animateTransform attributeName="transform" attributeType="XML" type="rotate" from="0 50 50" to="360 50 50" dur="2.5s" repeatCount="indefinite"/>
		  <animate attributeName="stroke-dashoffset" values="0;-30;-124" dur="1.25s" repeatCount="indefinite"/>
		  <animate attributeName="stroke-dasharray" values="0,200;110,200;110,200" dur="1.25s" repeatCount="indefinite"/>
		</circle>
	  </svg></div>`);
	  this.$root.append(temp);
	}
	htmlToElement(html) {
		var template = document.createElement('template');
		html = html.trim(); 
		template.innerHTML = html;
		return template.content.firstChild;
	}
	backClick() {
		if (this.$backBtn) {
			this.$backBtn.addEventListener('click', () => {
				if (this.step > this.minStep) {
					this.step--;
					this.setActiveStep();
					this.setActiveContent();
				}
				this.$confirmbox.innerHTML = '';
				this.checkStep();
				this.scroltoTop();
			});
		}
	}

	makeCustomerHTML(data) {
		const titleCutomer = getCookie('django_language') === 'es' ? 'Información del cliente' : 'Customer Information';
		const titlePay = getCookie('django_language') === 'es' ? 'Información del cliente' : 'Payment Information';
		const cardTitle = getCookie('django_language') === 'es' ? 'Tarjeta' : 'Card';
		const endTitle = getCookie('django_language') === 'es' ? 'Terminando con' : 'Ending with';
		const expireTitle = getCookie('django_language') === 'es' ? 'Caducidad' : 'Expiry';

		// Customer info
		const name = (data.firstname && data.lastname) ? `${data.firstname} ${data.lastname}<br>` : '';
		const company = data.company ? `${data.company}<br>` : '';
		const phone = data.phone ? `${data.phone}<br>` : '';
		const email = data.email ? `${data.email}` : '';

		// Payment info
		const address = data.address ? `${data.address}<br>` : '';
		const city = data.city ? `${data.city},` : '';
		const state = data.state ? `${data.state},` : '';
		const zip = data.zip ? `${data.zip}` : '';
		const cardnumber = data.cardnumber ? `${data.cardnumber}` : '';
		const ccv = data.ccv ? `${data.ccv}` : '';
		const expirity = data.expirity ? `${data.expirity}` : '';

		const cardLast = cardnumber.split('-')[3];

		return `
			<div class="col-sm-6">
				<p><strong>${titleCutomer}</strong></p>
				<div class="p-md">
					<p>
						${name}
						${company}
						${phone}
						${email}
						${zip}
					</p>
				</div>
			</div>
			<div class="col-sm-6 tp-checkout__pay-info">
				<p><strong>${titlePay}</strong></p>
				<table>
					<tbody>
						<tr>
							<td>${cardTitle} #:</td>
							<td>${endTitle} ${cardLast}</td>
						</tr>
						<tr>
							<td>CCV:</td>
							<td>${ccv}</td>
						</tr>
						<tr>
							<td>${expireTitle}:</td>
							<td>${expirity}</td>
						</tr>
					</tbody>
				</table>
			</div>
		`;
	}


	init() {
		if (this.$root) {
			this.$confirmbox.innerHTML = '';
			this.checkCardNumber(this.$card);
			this.checkExpitiry();
			this.checkCVV();
			this.checkZip();
			this.setActiveStep(this.step);
			this.setActiveContent(this.step);
			this.nextClick();
			this.backClick();
			this.payClick();
		}
	}
}
/**
 * Checkout create
 */
const checkout = new Checkout('checkout');

document.addEventListener('DOMContentLoaded', () => {
	checkout.init();

	// Appends 'payment/' to the end of the URL whenever the Credit Card popup
    // appears.

	// Retrieves the body element, since the Popup is generated after loading.
	const bodyElement = document.querySelector('body');

	// Adds an observer to check if a new Node is added.
	const observer = new MutationObserver((mutationsList, observer) => {
		for (const mutation of mutationsList) {
			for (const addedNode of mutation.addedNodes) {
				if (addedNode.id === 'AcceptUIContainer') {
					// Once the Popup node is added (with the ID of 'AcceptUIContainer')
					// add another observer to check if the class of 'show'
					// is added.
					const classObserver = new MutationObserver((classMutationList, classObserver) => {
						for (const classMutation of classMutationList) {
							if (classMutation.attributeName === 'class' && addedNode.classList.contains('show')) {
								console.log('Class "show" was added to AcceptUIContainer');
								// If the class is added, it checks if the
								// current URL doesn't have the payment text
								// If it doesn't, it adds it.
								if (window.location.href.indexOf('payment/') === -1) {
									const currentUrl = window.location.href;
									const newUrl = currentUrl + "payment/";
									window.history.pushState(null, null, newUrl);
								}
							}
						}
					});
					classObserver.observe(addedNode, { attributes: true });
				}
			}
		}
	})
	observer.observe(bodyElement, { childList: true });
});