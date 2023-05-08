

const productsWrapper = document.querySelector('.js-category-items-wrapper > div')
const productColumns = document.querySelectorAll('.js-category-items-wrapper .tp-product')

if(productsWrapper && productColumns) {
    const items = []
    
    Array.prototype.map.call(productColumns, el => {
        items.push({
            html: el.parentNode,
            price: parseInt(el.getAttribute('data-price'), 10),
            length: parseInt(el.getAttribute('data-length'), 10)
        })
    })
    
    $(document).on('change', '#js-sorting', function() {
        switch(this.value) {
            case 'price-to-high':
                items.sort((a, b) => {
                    return a.price - b.price
                })
            break;
    
            case 'price-to-low':
                items.sort((a, b) => {
                    return b.price - a.price
                })
            break;
    
            case 'size-to-large':
                items.sort((a, b) => {
                    return a.length - b.length
                })
            break;
    
            case 'size-to-small':
                items.sort((a, b) => {
                    return b.length - a.length
                })
            break;
        }
    
        productsWrapper.innerHTML = ''
        items.map(el => productsWrapper.append(el.html))
    })
}



$(document).on('change', '#js-trailers-type-category', function() {
    window.location.href = this.value
})