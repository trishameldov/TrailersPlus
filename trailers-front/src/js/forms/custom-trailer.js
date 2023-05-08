import config from '../config'


export function initCustomTrailerCF() {
    const form = document.getElementById('custom-trailer-cf')

    if(form) {
        const submitBtn = form.querySelector('[type=submit]')
        const successBlock = form.querySelector('.tp-form-msg__text--success')
        const errorBlock = form.querySelector('.tp-form-msg__text--error')

        const csrftoken_input = document.querySelector('[name=csrfmiddlewaretoken]');

        if(csrftoken_input) {
            var csrftoken = csrftoken_input.value;
        }

        form.addEventListener('submit', submitForm)


        async function submitForm(event) {
            event.preventDefault()

            submitBtn.disabled = true
            submitBtn.classList.add('tp-btn--loading')

            let serializedForm = $(form).serialize();
            let formData = serializedForm.split("&");
            let jsonData = {};
        
            formData.forEach(function(field) {
                let parts = field.split("=");
                jsonData[parts[0]] = decodeURIComponent(parts[1]);
            });

            // Concatenates the first_name and last_name values into the name value
            jsonData["name"] = jsonData["first_name"] + " " + jsonData["last_name"];
            delete jsonData["first_name"];
            delete jsonData["last_name"];

            // Removes the <p>, </p> and </br> tags from the strings.
            jsonData["trailer_type"] = jsonData["trailer_type"].replace(/<[^>]*>/g, "");
            jsonData["trailer_length"] = jsonData["trailer_length"].replace(/<[^>]*>/g, "");
            jsonData["quantity"] = jsonData["quantity"].replace(/<[^>]*>/g, "");

            const response = await fetch(`${config.env.apiURL}/forms/custom`, {
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                },
            })

            if(response.status === 201) {
                successBlock.style.display = 'block'
                form.reset()

                const inputs = document.getElementById('custom-trailer-cf').getElementsByTagName("input");
                for (const key in inputs) {
                    var classList = inputs[key].classList
                    if(classList){
                        inputs[key].classList.remove("valid")
                    }
                }

                $('select').val(null).trigger('change');

                $('#trailer_type').siblings('.select2').children(":first").children(":first").removeClass('valid')
                $('#trailer_length').siblings('.select2').children(":first").children(":first").removeClass('valid')
                $('#store_id').siblings('.select2').children(":first").children(":first").removeClass('valid')
                $('#quantity').siblings('.select2').children(":first").children(":first").removeClass('valid')

            } else if (response.status === 500) {
                submitBtn.disabled = false;
                submitBtn.classList.remove('tp-btn--loading');
                errorBlock.style.display = 'block';
                let html = '';
                Object.keys(responseData).forEach(key => {
                    if(key == 'name'){
                        var fieldName = 'Name'
                    }else if(key=='excepted_fleet'){
                        var fieldName = 'Quantity'
                    }else{
                        const id = form.querySelector(`[name=${key}]`).getAttribute('id')
                        var fieldName = $('label[for="' + id + '"]').html()
                        fieldName.replace('*', '')
                    }

                    if(fieldName) {
                        html += `${fieldName}: ${responseData[key]}<br />`
                    }
                });
                errorBlock.innerHTML = html;
            } else {
                errorBlock.style.display = 'block'
                let html = ''

                const responseData = await response.json()

                Object.keys(responseData).forEach(key => {
                    if(key == 'name'){
                        var fieldName = 'Name'
                    }else if(key=='excepted_fleet'){
                        var fieldName = 'Quantity'
                    }else{
                        const id = form.querySelector(`[name=${key}]`).getAttribute('id')
                        var fieldName = $('label[for="' + id + '"]').html()
                        fieldName.replace('*', '')
                    }

                    if(fieldName) {
                        html += `${fieldName}: ${responseData[key]}<br />`
                    }
                })

                errorBlock.innerHTML = html
            }
        
            submitBtn.disabled = false
            submitBtn.classList.remove('tp-btn--loading')
        }
    }
}
