import config from './config'

const button = document.querySelector('.js-load-more-review')
let id = document.querySelector('.tp-product-head .tp-pagination li:last-child')
id = id ? id.innerText : null
const container = document.querySelector('.js-reviews-wrapper')

if(button && id && container) {
    button.addEventListener('click', async event => {
        event.preventDefault()

        const link = button.getAttribute('data-next-link') || `${config.env.apiURL}/product_reviews/?format=json&vin=${id}`

        let response = await fetch(link)
        response = await response.json()

        if(!response.links.next) {
            button.style.display = 'none'
        }

        if(response.results) {
            button.setAttribute('data-next-link', response.links.next)

            const scrollPosition = document.documentElement.scrollTop

            response.results.map((el, index) => {
                const text = el.content.length > 100 ? el.content.slice(0, 97) + ' ...' : el.content
                const title = el.title.length > 35 ? el.title.slice(0, 32) + ' ...' : el.title


                const reviewNode = document.querySelector('.tp-review').cloneNode(true)
                reviewNode.querySelector('.tp-review__title').innerText = title
                reviewNode.querySelector('.tp-review__text').innerHTML = text + '<br><a href="https://www.trustpilot.com/review/www.trailersplus.com">Read More</a>'
                reviewNode.querySelector('.tp-review__author').innerText = el.author
                reviewNode.querySelector('.tp-review__time').innerText = el.created_ago
                
                const raitingNodes = reviewNode.querySelectorAll('.tp-rating__star')

                Array.prototype.map.call(raitingNodes, (item, index) => {
                    if(el.stars >= index + 1) {
                        item.classList = `tp-rating__star bg-${el.stars} checked`
                    }
                    else {
                        item.classList = `tp-rating__star`
                    }
                })

                const wrapper = document.createElement('div')
                wrapper.className += ' col-md-6 col-lg-4 margin-25b margin-md-45b'
                wrapper.append(reviewNode)
                container.append(wrapper)

                if(index === response.results.length - 1) {
                    document.documentElement.scrollTop = scrollPosition
                }
            })
        }
    })
}
