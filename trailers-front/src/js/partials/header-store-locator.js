import { getCookie } from '../utils/cookies.utils'
import config from '../config'


export function initHeaderStoreLocator() {
    const cityItems = document.querySelectorAll('.js-locations-city')

    if(cityItems) {
        Array.prototype.map.call(cityItems, el => {
            el.addEventListener('click', async event => {
                event.preventDefault()
                const cityEl = event.target.classList.contains('js-locations-city') ? event.target : event.target.parentElement
                const location = cityEl.getAttribute('data-locations-city')
                const locationCity = cityEl.getAttribute('data-store-slug') ? cityEl.getAttribute('data-store-slug').split('/') : false
                const baseUrl = window.location.href.split('/')
       

                if(location) {
                    const rawResponse = await fetch(`${config.env.apiURL}/user_location/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            sessionid: getCookie('sessionid'),
                            csrftoken: getCookie('csrftoken'),
                            location_id: location
                        })
                    })
                
                    const response = await rawResponse.json()
                    if (locationCity) {
                        if (baseUrl.indexOf('en') !== -1 || baseUrl.indexOf('es') !== -1) {
                            baseUrl[4]= locationCity[0]
                            baseUrl[5]= locationCity[1]
                        } else {
                            baseUrl[3]= locationCity[0]
                            baseUrl[4]= locationCity[1]
                        }
                        window.location = `${baseUrl.join('/')}`
                    } else {
                        window.location.reload()
                    }
                    
                }
            })
        })
    }
}
