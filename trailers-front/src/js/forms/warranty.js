import config from '../config'


export function initWarrantyCF() {
    const form = document.getElementById('warranty-cf');
    const form_vin = document.getElementById('vin-cf');
    const form_photos = document.getElementById('photos-cf');
    const csrftoken_input = document.querySelector('[name=csrfmiddlewaretoken]');

    if(csrftoken_input) {
        const csrftoken = csrftoken_input.value;
    }

    if (form_vin) {
        const vinContainer = document.getElementById('vin-wrapper');
        const submitVin = document.getElementById('vin-submit');
        const successVinBlock = document.getElementById('warranty-wrapper');
        successVinBlock.style.display = 'none';
        const errorVinBlock = form_vin.querySelector('.vin-form-msg__text--error');
        form_vin.addEventListener('submit', submitVinForm);
        async function submitVinForm(event) {
            var formVinData = new FormData(form_vin);
            event.preventDefault()

            submitVin.disabled = true
            submitVin.classList.add('tp-btn--loading')
        
            const response = await fetch(`${config.env.apiURL}/warranty-vin-validation/${formVinData.get("vin")}`, {
                method: 'GET'
            })

            if(response.status === 200) {
                successVinBlock.style.display = 'block'
                vinContainer.style.display = 'none';
            }
            else {
                errorVinBlock.style.display = 'block'
                let html = ''

                const responseData = await response.json()

                Object.keys(responseData).forEach(key => {
                    const fieldName = form.querySelector(`[name=${key}]`).getAttribute('placeholder')

                    if(fieldName) {
                        html += `${fieldName.replace('*', '')}: ${responseData[key]}<br />`
                    }
                })

                errorVinBlock.innerHTML = html
            }
            submitVin.disabled = false
            submitVin.classList.remove('tp-btn--loading')
        }
    }

    if(form) {
        const warrantyInput = document.getElementById('warranty-id');
        const warrantyContainer = document.getElementById('warranty-wrapper');
        const submitBtn = form.querySelector('[type=submit]')
        const successBlock = document.getElementById('photos-wrapper')
        successBlock.style.display = 'none';
        const errorBlock = form.querySelector('.tp-form-msg__text--error')
        form.addEventListener('submit', submitForm)

        async function submitForm(event) {
            var formData = new FormData(form);
            formData.append("trailer", document.getElementById("vin").value);
            event.preventDefault()

            submitBtn.disabled = true
            submitBtn.classList.add('tp-btn--loading')
        
            const response = await fetch(`${config.env.apiURL}/forms/warranty/`, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body: JSON.stringify({
                    name: formData.get('name'),
                    email: formData.get('email'),
                    trailer: formData.get('trailer'),
                    phone: formData.get('phone'),
                    description: formData.get('description')
                }),
            })

            const responseData = await response.json()

            if(response.status === 201) {
                warrantyInput.value = responseData['pk'];
                document.querySelector('[name=csrfmiddlewaretoken]').value = responseData['csrfmiddlewaretoken'];
                successBlock.style.display = 'block'
                warrantyContainer.style.display = 'none';
                form.reset()

                const tel = form.querySelector('[type=tel]')

                if(tel) {
                    tel.classList.remove('valid')
                }
            }
            else {
                errorBlock.style.display = 'block'
                let html = ''

                Object.keys(responseData).forEach(key => {
                    const fieldName = form.querySelector(`[name=${key}]`).getAttribute('placeholder')

                    if(fieldName) {
                        html += `${fieldName.replace('*', '')}: ${responseData[key]}<br />`
                    }
                })

                errorBlock.innerHTML = html
            }
        
            submitBtn.disabled = false
            submitBtn.classList.remove('tp-btn--loading')
        }
    }

    if(form_photos) {
        const photosInputContainer = document.getElementById('photo-wrapper');
        const submitPhotosBtn = form_photos.querySelector('[type=submit]')
        const successPhotoBlock = form_photos.querySelector('.tp-form-msg__text--success')
        const errorPhotoBlock = form_photos.querySelector('.tp-form-msg__text--error')
        form_photos.addEventListener('submit', submitPhotoForm)

        async function submitPhotoForm (event) {
            var formData = new FormData(form_photos);
            event.preventDefault()

            submitPhotosBtn.disabled = true
            submitPhotosBtn.classList.add('tp-btn--loading')

            function getBase64(file) {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(file);
                    reader.onload = function () {
                        resolve(reader.result);
                    };
                    reader.onerror = function (error) {
                        reject(reader.result);
                    };
                });
            }
            
            formData.getAll("images").forEach(
                (image) => {
                    getBase64(image).then((data) => {
                        var photoData = new FormData();
                        const response = fetch(`${config.env.apiURL}/warranty-images/`, {
                            method: 'POST',
                            body: JSON.stringify({
                                image: data,
                                warranty: document.getElementById('warranty-id').value,
                            }),
                            headers: {
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                                'Accept': 'application/json',
                                'Content-Type': 'application/json',
                            },
                        }).then(response => response.json())
                        .then(data => {
                            console.log('Success:', data);
                            document.querySelector('[name=csrfmiddlewaretoken]').value = data['csrfmiddlewaretoken'];
                            photosInputContainer.style.display = 'none';
                            submitPhotosBtn.style.display = 'none';
                            successPhotoBlock.style.display = 'block';
                        })
                        .catch((error) => {
                            console.error('Error:', error);
                            photosInputContainer.style.display = 'block';
                            submitPhotosBtn.style.display = 'block';
                            successPhotoBlock.style.display = 'none';
                        });
                    });
                }
            );
            submitPhotosBtn.classList.remove('tp-btn--loading')
        }
    }
}
