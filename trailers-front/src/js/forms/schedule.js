import config from '../config'


export function initScheduleCF() {
    const form = document.getElementById('schedule-cf')

    if(form) {
        const submitBtn = form.querySelector('[type=submit]')
        const successBlock = form.querySelector('.tp-form-msg__text--success')
        const errorBlock = form.querySelector('.tp-form-msg__text--error')
        form.addEventListener('submit', submitForm)


        async function submitForm(event) {
            event.preventDefault()

            submitBtn.disabled = true
            submitBtn.classList.add('tp-btn--loading')
        
            const response = await fetch(`${config.env.apiURL}/forms/appointment`, {
                method: 'POST',
                body: $(form).serialize(),
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }) 

            if(response.status === 201) {
                const location = submitBtn.getAttribute('data-redirect');
                window.location.replace(`${config.env.siteURL}${location}`); 
                form.reset()
                const tel = form.querySelector('[type=tel]')
                if(tel) {
                    tel.classList.remove('valid')
                }
            }
            else {
                errorBlock.style.display = 'block'
                let html = ''

                const responseData = await response.json()

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
}
