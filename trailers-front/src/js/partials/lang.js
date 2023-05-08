import { setCookie, getCookie } from '../utils/cookies.utils'

/**
 * Set coockie with choosen language by click to "language switcher"
 */
export function initLangListener() {
    const linksNode = document.getElementsByClassName('js-lang-link')

    if(linksNode) {
        // Set "click" listeners for all "language link"
        Array.prototype.map.call(linksNode, el => {
            el.addEventListener('click', event => {
                event.preventDefault()

                const link = event.target
                const href = link.getAttribute('href')
                const lang = link.getAttribute('data-lang')

                if(lang) {
                    setCookie('django_language', lang)
                    window.location.href = href
                }
                else if(href) {
                    window.location.href = href
                }
            })
        }) 
    }
}
