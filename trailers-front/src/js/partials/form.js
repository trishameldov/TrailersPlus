/**
 * Phone mask
 */

export function phoneMask() {
	const inputs = document.querySelectorAll('input[type="tel"]');
	const errorBlock = document.querySelector('.tp-form-msg__text--error');
	const button = document.querySelector('button[type="submit"]');
	const next_button = document.querySelector('.js-checkout-next');
	const lang = document.querySelector(".tp-lang__head").querySelector("span").innerText;
	const event_button = next_button || button;
	var message = "";

	if(lang === 'ES') {
		message = 'Teléfono: Ingrese un número de teléfono válido de 10 dígitos para continuar. El número no puede comenzar con 0 o 1.';
	}else{
		message = 'Phone: Please enter a valid 10-digit phone number to continue. The number cannot start with a 0 or 1.';
	}
	if(event_button) {
		event_button.addEventListener("click", e => {
			var value = $(e.target).closest("form").find("input[type='tel']").val();
			var input = $(e.target).closest("form").find("input[type='tel']")[0];
			if (!(value.trim().length >= 14 && value.match(/^[(][2-9]+/))) {
				errorBlock.style.display = 'block';
				errorBlock.innerHTML = message;
				input.classList.remove('valid');
				input.classList.add('not-valid');
				e.stopPropagation();
				e.preventDefault();
			}
		});
	}

	if (inputs) {
		[...inputs].forEach(input => {
			const x = input.value
				.replace(/\D/g, '')
				.match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
			input.value = !x[2]
				? x[1]
				: `(${x[1]}) ${x[2]}${x[3] ? `-${x[3]}` : ''}`;
			if (input.value.trim().length >= 14 && input.value.match(/^[(][2-9]+/)) {
				input.classList.add('valid');
				input.classList.remove('not-valid');
			} else {
				if (input.value.trim().length >= 1){
					input.classList.remove('valid');
					input.classList.add('not-valid');
				}
			}


			input.addEventListener('input', e => {
				const x = e.target.value
					.replace(/\D/g, '')
					.match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
				e.target.value = !x[2]
					? x[1]
					: `(${x[1]}) ${x[2]}${x[3] ? `-${x[3]}` : ''}`;

				if (e.target.value.trim().length >= 14 && input.value.match(/^[(][2-9]+/)) {
					input.classList.add('valid');
					input.classList.remove('not-valid');
					errorBlock.classList.add('d-none');
				}else if(e.target.value.trim().length >= 14 && !input.value.match(/^[(][2-9]+/)){
					// complete but incorrect input.
					input.classList.add('not-valid');
					errorBlock.classList.remove('d-none');
					input.classList.remove('valid');
				}else {
					input.classList.remove('valid');
					input.classList.add('not-valid');
					errorBlock.classList.add('d-none');
				}
			});

			input.addEventListener('change', e => {
				if (e.target.value.trim().length >= 14 && input.value.match(/^[(][2-9]+/)) {
					input.classList.add('valid');
					input.classList.remove('not-valid');
					errorBlock.classList.add('d-none');
				}else if(e.target.value.trim().length >= 14 && !input.value.match(/^[(][2-9]+/)){
					// complete but incorrect input.
					input.classList.add('not-valid');
					errorBlock.classList.remove('d-none');
					input.classList.remove('valid');
				}else {
					input.classList.remove('valid');
					errorBlock.classList.add('d-none');
				}
			});
		});
	}
}

/**
 * Check if checkox on form is checked
 */

export function checkValid() {
	const checkboxes = document.querySelectorAll('.js-accept');

	if (checkboxes) {
		[...checkboxes].forEach(item => {
			if (!item.checked) {
				const $btn = item
					.closest('form')
					.querySelector('button[type="submit"]');

				if ($btn) {
					$btn.disabled = true;

					item.addEventListener('change', () => {
						$btn.disabled = !item.checked;
					});
				}
			}
		});
	}
}

export function inputCheckForValue() {
	const inputs = document.querySelectorAll('.js-space-check');

	if (inputs && inputs.length) {
		[...inputs].forEach(input => {
			input.addEventListener('input', e => {
				const { value } = e.target;

				if (value.length < 1){
					input.classList.add('not-valid');
				} else {
					if (value.length >= 1 && value.length < 3){
						input.classList.add('not-valid');
					}else{
						input.classList.remove('not-valid');
						input.classList.add('valid');
					}
				}
			});
		});
	}

	const input_email = document.querySelectorAll('.js-space-email');
	if (input_email && input_email.length) {
		[...input_email].forEach(input => {
			input.addEventListener('input', e => {
				const { value } = e.target;

				if (value.match(/^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/)){
					input.classList.add('valid');
					input.classList.remove('not-valid');
				}
				else{
					input.classList.add('not-valid');
					input.classList.remove('valid');
				}
			});
		});
	}

	const input_address = document.querySelectorAll('.js-space-address');

	if (input_address && input_address.length) {
		[...input_address].forEach(input => {
			input.addEventListener('input', e => {
				const { value } = e.target;

				if (value.length < 1){
					input.classList.add('not-valid');
				} else {
					if (value.length >= 1 && value.length < 5){
						input.classList.add('not-valid');
					}else{
						input.classList.remove('not-valid');
						input.classList.add('valid');
					}
				}
			});
		});
	}

	$('#trailer_type').on('select2:select', function (e) {
		$('#trailer_type').siblings('.select2').children(":first").children(":first").addClass('valid')
	});
	$('#trailer_length').on('select2:select', function (e) {
		$('#trailer_length').siblings('.select2').children(":first").children(":first").addClass('valid')
	});
	$('#store_id').on('select2:select', function (e) {
		$('#store_id').siblings('.select2').children(":first").children(":first").addClass('valid')
	});
	$('#quantity').on('select2:select', function (e) {
		$('#quantity').siblings('.select2').children(":first").children(":first").addClass('valid')
	});

}
