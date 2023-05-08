import { getCookie } from '../utils/cookies.utils'
import { getCurrentLanguageOnPage } from '../utils/language.utils'

import config from '../config'

/**
 * Delete search filter
 */

const prodFltr = document.querySelector('.js-prod-fltr'); // wrapper for filter checkboxes
const fltrWrapp = document.querySelector('.js-fltr-wrapp'); // wrapper for filter labels
const fltrToggle = document.querySelectorAll('.js-fltr-toggle'); // filter checkboxes
const fltrCatToggle = document.querySelectorAll('.js-all-fltr-toggle'); // filter checkboxes
const searchGrid = document.querySelector('.js-search-grid'); // filter results box
const products = searchGrid && searchGrid.querySelectorAll('.js-product-wrapp');
const productsCounter = document.querySelector('.js-products-conter');
const baseUrl = fltrWrapp && fltrWrapp.dataset.url;

let filterCategories = [];
let filterLength = [];
let messageFlag = false;
let wasPriceChange = false;
let price1 = 0;
let price2 = 0;

/**
 * ----------------------
 */

/**
 * Redirects to the selected filter. 
 * If the main category was selected, prevents a redirection from clicking on
 * the subcategory's checkboxes and allows for the expected behavior of disabling
 * that option.
 */
function labelSelector() {
    var divs = document.getElementsByClassName('js-fltr-click')

	for (let i = 0; i < divs.length; i++) {
		divs[i].addEventListener('click', () => {
			let url = divs[i].getAttribute('data-url');
			if (divs[i].id === 'child' && !categoryChecker(divs[i]) || divs[i].id === 'parent') {
				window.location.href = url;
			}
		})
	}
}

/**
 * Redirects the user to the correct ATV url if they input the ATV pathname in
 * lowercase.
 */
function redirectToATVUrl() {
	let url = window.location.href;

	url = url.split('/');

	if (url.pathname.includes('atv')) {
		url.pathname = url.pathname.replace('atv', 'ATV');
		window.location.href = url.href;
	}
}


/**
 * Checks if the main category of a given subcategory is checked.
 * @param {HTMLElement} subcategory
 */
function categoryChecker(subcategory) {
    let slug = subcategory.getAttribute('data-slug');
    let parentCheckbox = document.getElementById(slug);

    return parentCheckbox.checked
} 

function clearGrid(array = []) {
	return new Promise((resolve, reject) => {
		try {
			const arr = array.length ? array : products;
			arr.forEach(elem => {
				jQuery(elem).fadeOut(0);
			});
			resolve();
		} catch (error) {
			console.log('cleargrid error', error);
			reject(error);
		}
	});
}

function resultMessage(bool = false) {
	const wrap = document.querySelector('.js-product-filter-section');
	let message = '';
	// console.log('bool = ', bool);
	if (bool) {
		if (!messageFlag) {

			if(wrap && wrap.getAttribute('data-error-text')) {
				message = wrap.getAttribute('data-error-text');
			}
			else {
				message = getCurrentLanguageOnPage() === 'en'
					? 'Sorry, no results returned. Please try a new search.'
					: 'Lo sentimos, no hay resultados devueltos. Por favor, intente una nueva búsqueda.';
			}
			const html = `<div class="col-12 js-filter-message"><h4 class="t-center">${message}</h4></div>`;
			searchGrid.insertAdjacentHTML('afterbegin', html);
			messageFlag = true;
		}
	} else {
		const el = searchGrid.querySelector('.js-filter-message');
		if (el) {
			el.remove();
			messageFlag = false;
		}
	}
}

function matchCat(filteringCategories, elem) {
	let matched = false;
	filteringCategories.forEach(filter => {
		if (elem.dataset.category.split(', ').indexOf(filter) !== -1) {
			matched = true;
		}
	});
	return matched;
}

function matchLength(filteringLength, elem) {
	let matched = false;
	filteringLength.forEach(filter => {
		if (elem.dataset.length.split(', ').indexOf(filter) !== -1) {
			matched = true;
		}
	});
	return matched;
}

function matchPrice(elem) {
	let matched = false;
	const { price } = elem.dataset;
	if (+price <= price2 && +price >= price1) {
		matched = true;
	}
	return matched;
}

function matchSpecial(elem) {
	let matched = false;
	if (elem.dataset.special === 'true') {
		matched = true;
	}
	return matched;
}

function resMessage(result) {
	if (!result.length) {
		resultMessage(true);
	} else {
		resultMessage(false);
	}
}

function getFilteredElements(filteringCategories = [], filteringLength = [], filteringPrice = false, isSpecial = false) {
	// console.log('filteringCategories', filteringCategories);
	// console.log('filteringLength', filteringLength);
	// console.log('filteringPrice', filteringPrice);
	if (filteringCategories.length && !filteringLength.length && !filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && filteringLength.length && !filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchLength(filteringLength, elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && filteringLength.length && filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchLength(filteringLength, elem) && matchPrice(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && !filteringLength.length && filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchPrice(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && filteringLength.length && filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchLength(filteringLength, elem) && matchPrice(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && filteringLength.length && !filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchLength(filteringLength, elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && !filteringLength.length && filteringPrice && !isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchPrice(elem);
			return res;
		});

		resMessage(result);
		return result;
	}

	if (filteringCategories.length && filteringLength.length && filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchLength(filteringLength, elem) && matchPrice(elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && filteringLength.length && !filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchLength(filteringLength, elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && !filteringLength.length && !filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && !filteringLength.length && !filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && !filteringLength.length && filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchPrice(elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (!filteringCategories.length && filteringLength.length && filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchLength(filteringLength, elem) && matchPrice(elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}
	if (filteringCategories.length && !filteringLength.length && filteringPrice && isSpecial) {
		const result = [...products].filter(elem => {
			const res = matchCat(filteringCategories, elem) && matchPrice(elem) && matchSpecial(elem);
			return res;
		});

		resMessage(result);
		return result;
	}

	return products;
}

function setCount(count) {

}

function createGrid(array = []) {
	return new Promise((resolve, reject) => {
		try {
			setCount(array.length);
			array.forEach(elem => {
				jQuery(elem).fadeIn(0);
			});
			resolve();
			// console.log('cleargrid created');
		} catch (error) {
			console.log('creating grid error', error);
			reject(error);
		}
	});
}

function clearFiltering(array = []) {
	// eslint-disable-next-line consistent-return
	return new Promise((resolve, reject) => {
		try {
			const targetElememts = array.length ? array : products;
			setCount(targetElememts.length);
			targetElememts.forEach(elem => {
				const $elem = jQuery(elem);
				if (!$elem.is(':visible')) {
					$elem.fadeIn(0);
				}
			});
			// eslint-disable-next-line no-unused-expressions
			targetElememts && resultMessage();
			resolve();
			console.log('filtering cleared');
		} catch (error) {
			console.log('creating grid error', error);
			reject(error);
		}
	});
}

function makeFiltering(catFltr, lengthFltr, isPrice = wasPriceChange, isSpecial = false) {
	if (catFltr.length || lengthFltr.length || isPrice || isSpecial) {
		const elems = getFilteredElements(catFltr, lengthFltr, isPrice, isSpecial);
		clearGrid()
			.then(() => {
				createGrid(elems);
			});
	} else {
		clearFiltering();
	}
}

function removeFilterItem(type = 'category', elem) {
	if (type === 'category') {
		filterCategories = filterCategories.filter(item => item !== elem);
		makeFiltering(filterCategories, filterLength);
		return false;
	}
	if (type === 'length') {
		filterLength = filterLength.filter(item => item !== elem);
		makeFiltering(filterCategories, filterLength);
		return false;
	}

	return false;
}

/**
 * Create filter label
 * @param {*} label filter text
 * @param {id} label ID required for syncronization left filter with filter labels
 */
const createFilter = (label, id, num) => `
	<div class="tp-search-res__fltr-item js-search-fltr" data-id="${id}" data-num="${num}">${label}
		<span class="js-fltr-del">
			<i class="ion-md-close"></i>
		<span>
	</div>
`;

/**
 * Clear filter value
 * @param {id} label ID of filter
 */
const clearFilter = id => {
	const currentFltr = prodFltr.querySelector(`#${id}`);
	// delete category label
	fltrWrapp.querySelector(`[data-id="${id}"]`).remove();

	if (currentFltr.checked) {
		currentFltr.checked = false;
		removeFilterItem(id);
	}
};

function toggleOneHandler(toggle) {
	const {
		checked,
		id,
		value,
		className,
		dataset
	} = toggle;
	const isLength = className.split(' ').indexOf('js-fltr-length') !== -1;
	const wrapp = toggle.closest('.js-drop-wrapp');
	const toglessInclosest = wrapp
		? wrapp.querySelectorAll('.js-fltr-toggle')
		: null;
	const toglessChecked = wrapp
		? wrapp.querySelectorAll('.js-fltr-toggle:checked')
		: null;
	const allToggle = wrapp
		? wrapp.querySelector('.js-all-fltr-toggle')
		: null;
	const isOpen = wrapp.classList.contains('open');

	if (checked) {
		const filterItem = createFilter(value, id, dataset.num);
		const filterItems = fltrWrapp.querySelectorAll('.js-search-fltr')
		const filterArray = []

		if(filterItems.length) {
			Array.prototype.map.call(filterItems, el => {
				filterArray.push({
					html: el,
					num: parseInt(el.dataset.num, 10)
				})
			})
		}

		filterArray.push({
			html: $(filterItem)[0],
			num: parseInt($(filterItem)[0].dataset.num, 10)
		})

		filterArray.sort((a,b) => a.num - b.num)


		fltrWrapp.innerHTML = ''
		filterArray.map(el => fltrWrapp.append(el.html))
		


		// .insertAdjacentHTML('beforeend', filterItem);

		if (!isOpen) {
			wrapp.querySelector('.js-drop-toggle').click();
		}

		if (!isLength) {
			filterCategories.push(id);
			makeFiltering(filterCategories, filterLength);
		} else {
			filterLength.push(id);
			makeFiltering(filterCategories, filterLength);
		}
	} else {
		if (!isLength) {
			removeFilterItem('category', id);
			makeFiltering(filterCategories, filterLength);
		} else {
			removeFilterItem('length', id);
			makeFiltering(filterCategories, filterLength);
		}
		clearFilter(id);
	}

	// if in area there aren't checked items => uncheck general checkbox
	if (toglessChecked && !toglessChecked.length && allToggle) {
		// allToggle.checked = false;
		// if in area all items checked => check generall checkbox
	} else if (
		toglessInclosest
		&& toglessChecked
		&& toglessInclosest.length === toglessChecked.length
		&& allToggle
	) {
		allToggle.checked = true;
	}
}

/**
 * toggle filter on checkbox change
 */
 function toggleFilter() {
	if (fltrToggle) {
		fltrToggle.forEach(toggle => {
			toggle.addEventListener('click', () => {
				toggleOneHandler(toggle);
			});
		});
	}
}

function toggleAllHandler(item) {
	const wrapp = item.closest('.js-drop-wrapp');
	const innerToggles = wrapp.querySelectorAll('.js-fltr-toggle');
	const dropToggle = wrapp.querySelector('.js-drop-toggle');
	// Check if current area is open
	const isOpen = dropToggle.classList.contains('is-active');

	// if it's check event and area not open => open area
	// eslint-disable-next-line no-unused-expressions

    if (!isOpen && item.checked) {
        dropToggle.click();
    };

	// activate all inner categories(checkboxes)
	innerToggles.forEach(toggle => {
		if (item.checked) {
			if (!toggle.checked) {
				toggle.click();
			}
		} else {
			if (toggle.checked) {
				toggle.click();
			}
		}
	});
}

/**
 * Toggle all category filter on checkbox change
 */
 function toggleAllFilter() {
	if (fltrCatToggle) {
		fltrCatToggle.forEach(item => {
			// click on general checkbox
			item.addEventListener('click', () => {
				toggleAllHandler(item);
			});
		});
	}
}

function checkIfCategoryActive() {
	let active = false;
	fltrCatToggle.forEach(item => {
		// click on general checkbox
		if (item.checked) {
			active = true;
		}
	});

	return active;
}

/**
 * remove filter on label close click
 */

function labelClick() {
	$(document).on('click', '.js-fltr-del', function click() {
		const ID = $(this)
			.parent()
			.data('id');
		if (ID) {
			// clearFilter(ID);
			document.getElementById(ID).click();
		}

		if (!fltrWrapp.querySelector('.js-search-fltr') && !checkIfCategoryActive()) {
			window.location = baseUrl;
		}
	});
}

/**
 * Close filter on mobile
 */

function closeFilterMobile() {
	if (prodFltr) {
		const btn = prodFltr.querySelector('.js-close-prod-fltr');

		btn.addEventListener('click', function click() {
			this.closest('.js-drop-wrapp')
				.querySelector('.js-drop-toggle')
				.click();
		});
	}
}


function filterApply(array) {
	if (array && array.length) {
		array.forEach(filter => {
			if (filter.classList.contains('js-fltr-toggle') || filter.classList.contains('js-all-fltr-toggle')) {
				filter.click();
			}
		});
	}
}

function checkActive() {
	const checked = prodFltr && prodFltr.querySelectorAll('[data-checked]');

	if (checked && checked.length) {
		filterApply(checked);

		if (checked.length === 1 && checked[0].classList.contains('js-all-fltr-toggle')) {
			checked[0].closest('.js-drop-wrapp').classList.add('full');
		}
	}
}

/**
 * Filter special elements
 */

function filterSpecial() {
	const toggle = document.querySelector('.js-filter-special');

	if (toggle) {
		toggle.addEventListener('click', () => {
			const isSpecial = !!toggle.checked;
			makeFiltering(filterCategories, filterLength, wasPriceChange, isSpecial);
		});
	}
}

if ($('#slider-range').length) {
	$('#slider-range').on('slidechange', (_event, ui) => {
		price1 = ui.values[0];
		price2 = ui.values[1];
		wasPriceChange = true;

		// console.log(`price1111: ${ui.values[0]}, price2: ${ui.values[1]}`);
		makeFiltering(filterCategories, filterLength);
	});
}

/**
 * Location change
 */

function changeProductLocation() {
	jQuery('#product-list-location').on('change.select2', async e => {
		const valueArray = e.target.value.split('|')
		const link = valueArray[0]
		const location = valueArray[1]
		const baseUrl = window.location.href
		const type = baseUrl.split('inventory')[1] ? baseUrl.split('inventory')[1].split('/')[1] : ''
		if(location) {
			const rawResponse = await fetch(`${config.env.apiURL}/user_location/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					sessionid: getCookie('sessionid'),
					csrftoken: getCookie('csrftoken'),
					location_id: location
				})
			})
		
			const response = await rawResponse.json()
			window.location = `${link}${type}`
		}
	});
}

export {
	checkActive,
	closeFilterMobile,
	labelClick,
	toggleAllFilter,
	toggleFilter,
	filterSpecial,
	changeProductLocation,
    labelSelector,
	redirectToATVUrl,
};
