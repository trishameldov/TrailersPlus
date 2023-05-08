/**
 * Get cookie by name
 * @param {string} name 
 * @return {string|undefined} coockie value or undefined if not found cookie
 */
export function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ))
    return matches ? decodeURIComponent(matches[1]) : undefined
}


/**
 * Set cookie
 * @param {string} name 
 * @param {string} value 
 * @param {Object} options params (https://learn.javascript.ru/cookie)
 * @example
 * // setCookie('lang', 'ua', {secure: true, 'max-age': 1314000})
 */
export function setCookie(name, value, options = {}) {
    // Default values
    options = {
        path: '/',
        'max-age': 1314000,
        ...options
    }
    
    // Checking the correctness of the date 
    if(options.expires instanceof Date) {
        options.expires = options.expires.toUTCString()
    }
    
    // Format cookie string
    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value)
  
    // Override default values for cookie params
    for(let optionKey in options) {
        updatedCookie += "; " + optionKey
        let optionValue = options[optionKey]

        if(optionValue !== true) {
            updatedCookie += "=" + optionValue
        }
    }
  
    // Set cookie
    document.cookie = updatedCookie
}


export function deleteCookie(name) {
    setCookie(name, "", {
        'max-age': -1
    })
}