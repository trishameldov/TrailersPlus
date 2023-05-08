import { deleteCookie, getCookie } from './utils/cookies.utils'
import config from './config'

function addToCartInit() {
    const addToCartButton = document.querySelector('.js-to-cart-btn')
    const productIdNode = document.querySelector('.tp-pagination li:last-child')
    const reservLink = document.querySelectorAll('.js-reserv-link')
    const reservButton = document.querySelector('.js-reserv-btn')
    const reservButton2 = document.querySelector('.js-reserv-btn-2')
    const reservButton3 = document.querySelector('.js-reserv-btn-3')
    const mainCart = document.querySelector('.js-cart')

    let imagePath = document.querySelector('.tp-product-gallery__right .swiper-slide:first-child img')
    imagePath = imagePath ? imagePath.getAttribute('src') : null

    let title = document.querySelector('h1')
    title = title ? title.innerText : null

    let price = document.querySelector('.tp-price span')
    price = price ? price.innerText : null

    let location = document.querySelector('.js-located-at')
    location = location ? location.innerText : null
    
    // Click to button 'add to cart'
    if(addToCartButton && productIdNode) {
        addToCartButton.addEventListener('click', event => {
            event.preventDefault()

            if(!addToCartButton.classList.contains('tp-btn--loading') && !reservButton.classList.contains('tp-btn--loading')) {
                addToCartButton.classList.add('tp-btn--loading')
    
                saveToSessionRequest(productIdNode.innerText).then(() => {
                    addToCartButton.classList.remove('tp-btn--loading')
    
                    addProductToCartDOM()
                    mainCart.classList.add('open')
                })
            }
        })
    }

    // Click to button 'reserve trailer' 
    if(reservButton && productIdNode) {
        reservButton.addEventListener('click', event => {
            event.preventDefault()
            if(!addToCartButton.classList.contains('tp-btn--loading') && !reservButton.classList.contains('tp-btn--loading'))  {
                reservButton.classList.add('tp-btn--loading')

                saveToSessionRequest(productIdNode.innerText).then(() => {
                    reservButton.classList.remove('tp-btn--loading')

                    addProductToCartDOM()
                    $.magnificPopup.close();

                    const href = reservButton.getAttribute('href')
                    if(href) {
                        window.location.href = href
                    }
                })
            }
        })
    }

    // Click to button 'reserve trailer' 
    if(reservLink && productIdNode) {
        
        reservLink.forEach(function(elem) {
            elem.addEventListener("click", function() {
                event.preventDefault()
                saveToSessionRequest(productIdNode.innerText).then(() => {
                    
                    const cartNode = document.querySelector('.js-cart')
                    const imagePath = document.querySelector('.trailer-img').getAttribute('src')
                    const title = document.querySelector('.trailer-title').innerText
                    const price = document.querySelector('.tp-price span').innerText
                    const location = document.querySelector('.located-at').innerText

                    // Main navigation    
                    cartNode.querySelector('.tp-cart__info').innerHTML = 'item successfully added'
                    cartNode.querySelector('.tp-cart__item-title').innerHTML = title
                    cartNode.querySelector('.tp-cart__item-price').innerHTML = price
                    cartNode.querySelector('.tp-cart__item-subtitle').innerHTML = location
                    cartNode.querySelector('.tp-cart__item').setAttribute('href', window.location.href)
                    cartNode.querySelector('.tp-cart__item-img img').setAttribute('src', imagePath)

                    cartNode.classList.add('tp-cart--visible')

                    window.location.href = '/checkout'
                })
            });
        });

    }

    if(reservButton2 && productIdNode) {
        reservButton2.addEventListener('click', event => {
            event.preventDefault()

            if(!addToCartButton.classList.contains('tp-btn--loading') && !reservButton2.classList.contains('tp-btn--loading'))  {
                reservButton2.classList.add('tp-btn--loading')

                saveToSessionRequest(productIdNode.innerText).then(() => {
                    reservButton2.classList.remove('tp-btn--loading')

                    addProductToCartDOM()
                    $.magnificPopup.close();

                    const href = reservButton2.getAttribute('href')
                    if(href) {
                        window.location.href = href
                    }
                })
            }
        })
    }
 
    if(reservButton3 && productIdNode) {
        reservButton3.addEventListener('click', event => {
            event.preventDefault()

            if(!addToCartButton.classList.contains('tp-btn--loading') && !reservButton3.classList.contains('tp-btn--loading'))  {
                reservButton3.classList.add('tp-btn--loading')

                saveToSessionRequest(productIdNode.innerText).then(() => {
                    reservButton3.classList.remove('tp-btn--loading')

                    addProductToCartDOM()
                    $.magnificPopup.close();

                    const href = reservButton3.getAttribute('href')
                    if(href) {
                        window.location.href = href
                    }
                })
            }
        })
    }
}

async function saveToSessionRequest(id) {
    const rawResponse = await fetch(`${config.env.apiURL}/session_cart/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sessionid: getCookie('sessionid'),
            csrftoken: getCookie('csrftoken'),
            cart_item: id
        })
    })

    const response = await rawResponse.json()
    
}

function addProductToCartDOM() {
    const cartNode = document.querySelector('.js-cart')

    let imagePath;
    if (document.querySelector('.tp-product-gallery__right .swiper-slide:first-child img')) {
        imagePath = document.querySelector('.tp-product-gallery__right .swiper-slide:first-child img').getAttribute('src');
    } else {
        imagePath = null;
    }
    const title = document.querySelector('h1').innerText
    const price = document.querySelector('.tp-price span').innerText
    const location = document.querySelector('.js-located-at').innerText

    // Main navigation    
    cartNode.querySelector('.tp-cart__info').innerHTML = 'item successfully added'
    cartNode.querySelector('.tp-cart__item-title').innerHTML = title
    cartNode.querySelector('.tp-cart__item-price').innerHTML = price
    cartNode.querySelector('.tp-cart__item-subtitle').innerHTML = location
    cartNode.querySelector('.tp-cart__item').setAttribute('href', window.location.href)
    if (imagePath) {
        cartNode.querySelector('.tp-cart__item-img img').setAttribute('src', imagePath)
    }

    cartNode.classList.add('tp-cart--visible')
}


function removeFromCartInit() {
    const removeButtons = document.querySelectorAll('.js-remove-from-cart')
    const productIdNode = document.querySelector('.tp-pagination li:last-child')
    const cartNode = document.querySelector('.js-cart')

    if(removeButtons) {
        Array.prototype.map.call(removeButtons, el => {
            el.addEventListener('click', async event => {
                event.preventDefault()

                if(cartNode) {
                    try {
                        cartNode.classList.remove('tp-cart--visible')
                        deleteCookie('cart_product_id')
                        const rawResponse = await fetch(`${config.env.apiURL}/session_cart/`, {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                sessionid: getCookie('sessionid'),
                                csrftoken: getCookie('csrftoken')
                            })
                        })
                    
                        const response = await rawResponse.json()
                    } catch(error) {
                       
                    } 
                }
            })
        })
    }
}



/**
 * Trailers Available counter
 */
$(document).on('change', '#js-for-sale-city', async function() {
    const cityAlias = this.value
    const typeAlias = document.querySelector('#js-for-sale-type').value

    let response = await fetch(`${config.env.apiURL}/count_trailers/?trailer-store=${cityAlias}&trailer-type=${typeAlias}`)
    response = await response.json()

    const span = document.querySelector('.js-s-filter__stat span')
    span.innerHTML = response.count
})


$(document).on('change', '#js-for-sale-type', async function() {
    const cityAlias = document.querySelector('#js-for-sale-city').value
    const typeAlias = this.value

    let response = await fetch(`${config.env.apiURL}/count_trailers/?trailer-store=${cityAlias}&trailer-type=${typeAlias}`)
    response = await response.json()
    
    const span = document.querySelector('.js-s-filter__stat span')
    span.innerHTML = response.count
})



document.addEventListener('DOMContentLoaded', () => {
    addToCartInit()
    removeFromCartInit()
});