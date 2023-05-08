import { getCookie } from '../utils//cookies.utils'

/**
 * Get language on the page
 * @return {string} - es|en
*/
export const getCurrentLanguageOnPage = () => {
    const link = window.location.href
    const URLObject = new URL(link)
    const path = URLObject.pathname

    if(path === '/') {
        return getCookie('django_language') || 'en'
    }
    else {
        const arr = path.split('/')

        if(arr[1] === 'es') {
            return 'es'
        }
        else return 'en'
    }
}