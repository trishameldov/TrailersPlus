import { baseUrl } from '../setup/variables'
import { setCookie, getCookie } from '../utils/cookies.utils'
import config from '../config'


/**
 * Simple map
 */
export function initMap() {
	try {
		const mapWraps = document.querySelectorAll('.js-simple-map');

		if (mapWraps.length) {
			[...mapWraps].forEach(mapItem => {
				const { lat, lng } = mapItem.dataset;
	
				const marker = mapItem.dataset.marker
					? mapItem.dataset.marker
					: null;
				const zoom = mapItem.dataset.zoom ? +mapItem.dataset.zoom : 17;
	
				const scrollwheel = !!mapItem.dataset.scrollwheel;
				const zoomControl = !!mapItem.dataset.zoom_control;
				const mapTypeControl = !!mapItem.dataset.type_control;
				const scaleControl = !!mapItem.dataset.scale_control;
				const streetViewControl = !!mapItem.dataset.street_view_control;
				const rotateControl = !!mapItem.dataset.rotate_control;
				const fullscreenControl = !!mapItem.dataset.fullscreen_control;
	
				const center = new google.maps.LatLng(lat, lng);
	
				const mapObj = new google.maps.Map(mapItem, {
					zoom,
					center,
					styles: [],
					scrollwheel,
					zoomControl,
					mapTypeControl,
					scaleControl,
					streetViewControl,
					rotateControl,
					fullscreenControl,
				});
	
				const markerObj = new google.maps.Marker({
					position: center,
					icon: marker,
					map: mapObj,
				});
				markerObj.setMap(mapObj);
			});
		}
	} catch (err) {

	}
}

/**
 * Load local JSON file
 */

// async function loadJSON(lang = 'en') {
// 	const url = lang === 'es' ? './js/map-data-es.json' : './js/map-data.json';
// 	const response = await fetch(url);
// 	if (!response.ok) {
// 		throw new Error(`HTTP error, status = ${response.status}`);
// 	}
// 	return response.json();
// }

/**
 * Fetch data by API
 */

async function fetchData(url) {
	const response = await fetch(url);

	if (!response.ok) {
		throw new Error(`HTTP error, status = ${response.status}`);
	}

	const data = await response.json();

	return data;
}

/**
 * Main map init function
 * @param {Node} mapSelector map dom selector
 * @param {Object} mapData info data for map
 */

function initialize(mapSelector, mapData) {
	const data = mapData.locations || null;
	const dataTitles = mapData.titles || {
		get_direction_title: 'Get Directions',
		view_store_invent_title: 'View Store Inventory',
		set_store_title: 'Set as My Store',
		more_information_title: 'More Information',
		store_hours_title: 'Store Hours',
	};
	const markers = [];
	const infoWindows = [];
	const catWrapp = document.querySelector('.js-map-categories');
	const stateToggles = catWrapp ? catWrapp.querySelectorAll('.js-marker-toggle') : null;
	const activeItem = catWrapp ? catWrapp.querySelector('.active') : null;
	// const activeCat = activeItem.dataset.category;
	const markerIcon = mapSelector.dataset.marker
		? mapSelector.dataset.marker
		: null;
	const storeInfos = document.querySelector('.js-locator-stores');

	const map = new google.maps.Map(mapSelector, {
		// gestureHandling: 'greedy',
	});

	window.mainMap = map

	let visibleMarkers = [];

	// eslint-disable-next-line no-use-before-define
	map.addListener('click', closeInfoWindows);

	/**
	 * Return store name
	 * @param {Object} object store data object
	 */
	function getShopName(object) {
		return object.store_name.split('TrailersPlus')[1] || object.store_city;
	}

	/**
	 * Make infowindow HTML structure
	 * @param {Object} data store info object
	 */
	function infowindowHTML(storeData) {
		const storeName = getShopName(storeData);
        let phoneNumber = storeData.store_phone || '';
        let formattedPhone = '';
        if (phoneNumber) {
            let array = phoneNumber.split("-");
            formattedPhone = `(${array[0]}) ${array[1]}-${array[2]}`;
        }
		return `
			<div class="tp-map-window">
				<div class="tp-map-window__box">
					<div class="tp-map-window__left">
						<div class="tp-loc-info-item tp-loc-info-item--map">
							<i class="fa fa-map-marker"></i>
							<a href="${storeData.store_link || '#'}" class="tp-map-window__link tp-map-window__link--direct js-set-and-view-store" data-store="${storeData.store_id}">
								${storeName || ''}<br>
								${storeData.store_address || ''}<br>
								${storeData.store_city || ''}, ${storeData.state || ''} ${storeData.store_zip || ''}
							</a>
						</div>
						<div class="tp-loc-info-item tp-loc-info-item--map">
							<i class="fa fa-phone"></i>
							<div>
								<a href="tel:+1${storeData.store_phone || ''}">${formattedPhone || ''}</a>
							</div>
						</div>
					</div>
					<div class="tp-map-window__right">
						<a href="${storeData.store_map_url || '#'}" 
							class="tp-map-window__link tp-map-window__link--direct" target="_blank" rel="noopener"
						>
							<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
								version="1.1" id="Capa_1" x="0px" y="0px" width="512px" height="512px" viewBox="0 0 510 510" 
								style="enable-background:new 0 0 510 510;" xml:space="preserve">
								<path d="M502.35,237.149l-229.5-229.5l0,0c-10.199-10.2-25.5-10.2-35.7,0l-229.5,229.5c-10.2,10.2-10.2,25.501,
								0,35.7l229.5,229.5 l0,0c10.2,10.2,25.501,10.2,35.7,0l229.5-229.5C512.55,262.65,512.55,247.35,502.35,237.149z 
								M306,318.75V255H204v76.5h-51v-102 c0-15.3,10.2-25.5,25.5-25.5H306v-63.75l89.25,89.25L306,318.75z" 
								data-original="#000000" class="active-path" data-old_color="#000000" fill="#FFFFFF" />
							</svg>
							${dataTitles.get_direction_title}
						</a>
						<a href="${storeData.store_inventory_link || '#'}" class="tp-map-window__link tp-map-window__link--direct js-set-and-view-store" data-store="${storeData.store_id}">
							<i class="fa fa-search"></i> ${dataTitles.view_store_invent_title}
						</a>
						<a href="#" class="tp-map-window__link tp-map-window__link--direct js-set-store" data-store="${storeData.store_id}">
							<i class="fa fa-thumb-tack"></i> ${dataTitles.set_store_title}
						</a>
					</div>
				</div>
			</div>
		`;
	}

	/**
	 * Make first letter uppercase
	 * @param {String} string
	 */
	function capitalizeFirstLetter(string) {
		return string.charAt(0).toUpperCase() + string.slice(1);
	}

	/**
	 * Create working hours block
	 * @param {object} object
	 */
	function makeDays(object) {
		const result = [];
		if (object) {
			// eslint-disable-next-line no-restricted-syntax
			for (const [key, value] of Object.entries(object)) {
				const d = `<tr><td>${capitalizeFirstLetter(key)}</td><td>${value}</td></tr>`;
				result.push(d);
			}
		}
		return result;
	}

	/**
	 * Make store HTML structure
	 * @param {Object} storeData store info object
	 */
	function storeInfoHTML(storeData) {
		const storeName = getShopName(storeData);
		return `
			<div class="tp-locator__store">
				<div class="row">
					<div class="col-md-5 col-lg-3">
						<a href="${storeData.store_link || '#'}" class="h3 h3-h2-mob c-main">${storeName}, ${storeData.state}</a>
						<address class="margin-20t">
							${storeData.store_address}<br>
							${storeData.store_city}, ${storeData.state} ${storeData.store_zip}<br>
							p: <a href="tel:+1${storeData.store_phone || ''}">${storeData.store_phone || ''}</a>
						</address>
						<a href="${storeData.store_map_url || '#'}" class="fz14 margin-20t d-inline-block" target="_blank" rel="noopener">
							${dataTitles.get_direction_title} >
						</a>
					</div>
					<div class="col-md-7 col-lg-5 col-xl-6 margin-20t margin-md-5t margin-lg-10t">
						<div class="tp-locator__schedule">
							<p class="h4">${dataTitles.store_hours_title}</p>
							<table>
								${storeData.work_hours}
							</table>
						</div>
					</div>
					<div class="col-lg-4 col-xl-3 margin-10t">
						<div class="tp-locator__buttons">
							<a href="${storeData.store_link || '#'}" class="tp-btn tp-btn--red tp-btn--md tp-btn--full">
								${dataTitles.more_information_title}
							</a>
							<a href="${storeData.store_inventory_link || '#'}" class="tp-btn tp-btn--grey tp-btn--full tp-btn--md">
								${dataTitles.view_store_invent_title}
							</a>
						</div>
					</div>
				</div>
			</div>
		`;
	}

	/**
	 * filtering markers by category
	 * @param {String} cat category name
	 */
	function filterMarkers(cat) {
		visibleMarkers = [];
		markers.forEach(marker => {
			if (cat === marker.category) {
				// marker.setVisible(true);
				visibleMarkers.push(marker);
			} else {
				// marker.setVisible(false);
			}
		});
	}

	/**
	 * Сlose infowindows
	 */
	function closeInfoWindows() {
		if (infoWindows.length) {
			[...infoWindows].forEach(item => {
				item.close();
			});
		}
	}

	/**
	 * Add store info HTML blocks
	 * @param {string} category category name
	 */
	function showInfo(category) {
		if (category && data) {
			const html = [];
			data.forEach(store => {
				if (category === store.state_long) {
					const storeHtml = storeInfoHTML(store);
					html.push(storeHtml);
				}
			});
			storeInfos.innerHTML = '';
			storeInfos.insertAdjacentHTML('afterbegin', html.join(''));
		}
	}

	// Show info on first page load
	// showInfo(activeCat);

	/**
	 * Center map to show all required markers
	 * @param {Array} markersClosest markers array which need to show
	 */
	function centerMap(markersClosest) {
		const bounds = new google.maps.LatLngBounds();

		if (markersClosest.length) {
			markersClosest.forEach(marker => {
				const LatLng = new google.maps.LatLng(
					marker.position.lat(),
					marker.position.lng(),
				);
				bounds.extend(LatLng);
			});

			if (markersClosest.length > 1) {
				map.fitBounds(bounds);
			} else {
				map.fitBounds(bounds);

				setTimeout(() => {
					map.setZoom(13);
				}, 200)
			}
		}
	}

	/**
	 * Click on "Set Store" link
	 */
	document.addEventListener('click', async e => {
		if (e.target && e.target.classList.contains('js-set-store')) {
			e.preventDefault();
			const storeID = e.target.dataset.store;

			const rawResponse = await fetch(`${config.env.apiURL}/user_location/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					sessionid: getCookie('sessionid'),
					csrftoken: getCookie('csrftoken'),
					location_id: storeID
				})
			})
		
			const response = await rawResponse.json()
			document.location.reload()
		}
		else if(e.target && e.target.classList.contains('js-set-and-view-store')) {
			e.preventDefault()
			const storeID = e.target.dataset.store;
			setCookie('my_location', storeID);
			window.location.href = e.target.getAttribute('href')
		}
	});

	/**
	 * Select change
	 */
	$('.js-locations-select').on('select2:select', e => {
		const toggleBtn = catWrapp.querySelector(`[data-category="${e.target.value}"]`);
		toggleBtn.click();
	});

	/**
	 * Click on category
	 */
	if (stateToggles && stateToggles.length) {
		[...stateToggles].forEach(item => {
			item.addEventListener('click', function stateClick() {
				const { category } = this.dataset;
				const siblings = this.parentNode.children;

				[...siblings].forEach(sibl => {
					sibl.classList.remove('active');
				});

				this.classList.add('active');

				closeInfoWindows();
				filterMarkers(category);
				showInfo(category);
				visibleMarkers.length && centerMap(visibleMarkers);

				$('.js-locations-select').val(category);
				$('.js-locations-select').trigger('change.select2');
			});
		});
	}

	/**
	 * Add marker
	 * @param {Map instance object} map map object
	 * @param {Object} props setting(lat, lng, icon, category)
	 */
	function addMarker(_map, storeObject) {
		const latLng = new google.maps.LatLng(storeObject.store_lat, storeObject.store_long);
		const category = storeObject.state_long;

		const icon = {
			url: markerIcon,
			scaledSize: window.innerWidth < 575 ? new google.maps.Size(40, 40) : new google.maps.Size(50, 50),
		};

		const marker = new google.maps.Marker({
			position: latLng,
			map: _map,
			icon,
			category,
		});

		const infoWindow = new google.maps.InfoWindow({
			content: infowindowHTML(storeObject),
		});

		infoWindows.push(infoWindow);
		markers.push(marker);

		marker.addListener('click', function markerClick() {
			closeInfoWindows();
			infoWindow.open(map, this);
		});
	}

	if (data) {
		data.forEach(store => {
			addMarker(map, store);
		});
	}
	centerMap(markers);
	activeItem.click();
}

/**
 * Init main map
 */
export function initMainMap() {
	const mainMap = document.querySelector('.js-main-map');
	window.language = getCookie('django_language')

	if (mainMap) {
		// loadJSON(window.language)
		// 	.then(mapData => {
		// 		initialize(mainMap, mapData);
		// 	})
		// 	.catch((error) => {
		// 		const p = document.createElement('p');
		// 		p.classList.add('error');
		// 		p.appendChild(document.createTextNode(`Error: ${error.message}`));
		// 		mainMap.parentNode.insertBefore(p, mainMap);
		// 	});

		const apiUrl = window.language === 'es' ? `${baseUrl}es/api/locations/` : `${baseUrl}api/locations/`;
		fetchData(apiUrl)
			.then(mapData => {
				// console.log(mapData);
				initialize(mainMap, mapData);
			})
			.catch((error) => {
				const p = document.createElement('p');
				p.classList.add('error');
				p.appendChild(document.createTextNode(`Error: ${error.message}`));
				mainMap.parentNode.insertBefore(p, mainMap);
			});
	}
}
