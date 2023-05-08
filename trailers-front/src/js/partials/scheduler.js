import { getCurrentLanguageOnPage } from '../utils/language.utils'

export default class Scheduler {
    constructor() {
        this.appContainer = document.querySelector('.js-tp-scheduler')
        this.timeSlotsContainer = this.appContainer?.querySelector('.js-time-slots')
        this.datesContainer = this.appContainer?.querySelector('.js-dates-container')
        this.slotInput = this.appContainer?.querySelector('#js-sheduler-time-slot')
        this.locationInput = this.appContainer?.querySelector('#js-sheduler-time-slot')
        this.calendar = null

        this.ITEMS_SCROLLED_BY_ARROWS = 3 
        this.DAY_NAMES_ENGLISH = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        this.DAY_NAMES_SPANISH = ['Lu', 'Ma', 'Mi', 'Ju', 'Vi', 'Sa', 'Do']
        this.MONTH_NAMES_ENGLISH = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        this.MONTH_NAMES_SPANISH = ['Enero', 'Feb', 'Marzo', 'Abr', 'Mayo', 'Jun', 'Jul', 'Agosto', 'Set', 'Oct', 'Nov', 'Dic']
        this.ERROR_TEXT_ENGLISH = 'No available slots for this date'
        this.ERROR_TEXT_SPANISH = 'No hay espacios disponibles para esta fecha'
        this.CURRENT_LANGUAGE = getCurrentLanguageOnPage()
        
        this.dayNames = this.DAY_NAMES_ENGLISH
        this.monthNames = this.MONTH_NAMES_ENGLISH

        this.activeDate = new Date()
        this.errorMessage = null

        // Index (by order in HTML) of date for which will be shown time slots
        this.activeDateOrderIndex = 1

        if(this.appContainer && this.timeSlotsContainer && this.slotInput && this.datesContainer && window.jsCalendar) {
            if(this.CURRENT_LANGUAGE === 'es') {
                this.dayNames = this.DAY_NAMES_SPANISH
                this.monthNames = this.MONTH_NAMES_SPANISH
            }

            this.initScheduler()
        }
    }

    /**
     * First time initialization of Scheduler
     */
    initScheduler() {
        this.appContainer.querySelector('.js-backward-date')?.addEventListener('click', () => {
            this.activeDate = ( d => new Date(d.setDate(d.getDate() - this.ITEMS_SCROLLED_BY_ARROWS)) )(new Date(this.activeDate))
            this.renderApp()
        })

        this.appContainer.querySelector('.js-forward-date')?.addEventListener('click', () => {
            this.activeDate = ( d => new Date(d.setDate(d.getDate() + this.ITEMS_SCROLLED_BY_ARROWS)) )(new Date(this.activeDate))
            this.renderApp()
        })

        this.appContainer.querySelector('.js-back-to-slots')?.addEventListener('click', event => {
            event.preventDefault()
            this.appContainer.classList.remove('tp-scheduler--chosen-slot')
        })

        this.appContainer.querySelector('.js-open-calendar')?.addEventListener('click', this.onOpenCalendar.bind(this))

        const locationItems = this.appContainer.querySelectorAll('.js-sheduler-location-item')

        if(locationItems) {
            Array.prototype.forEach.call(locationItems, el => {
                el.addEventListener('click', event => {
                    event.preventDefault()
                    
                    this.locationInput.value = el.getAttribute('data-locations-city')
                    this.appContainer.querySelector('.js-sheduler-location-link').innerText = el.querySelector('span').innerText
                })
            })
        }

        this.renderApp()
    }

    /**
     * Render app
     */
    async renderApp() {
        this.setLoadingStatus(true)

        this.errorMessage = null
        this.timeSlotsContainer.innerHTML = ''
        this.datesContainer.innerHTML = ''

        const dates = this.getVisibleDates()
        this.buildVisibleDatesHTML(dates)

        const slots = await this.getAvailableSlots()

        // console.log(this.errorMessage)
        if(this.errorMessage) {
            this.showErrorMessage()
        }
        else {
            this.buildSlotsHTML(slots)
        }
        
        this.setLoadingStatus(false)
    }

    /**
     * Just renders block with error message
     */
    showErrorMessage() {
        const block = document.createElement('div')
        block.classList.add('tp-scheduler__error-block')
        block.innerText = this.errorMessage

        this.timeSlotsContainer.append(block)
    }

    /**
     * Gets available time slots from server
     */
    async getAvailableSlots() {
        const d = this.activeDate
        const dateString = `${d.getDate()}-${d.getMonth() + 1}-${d.getFullYear()}`
        
        try {
            const response = await fetch(`http://localhost:8080/available_slots/${dateString}`)

            if(response.status !== 200) {
                this.errorMessage = this.CURRENT_LANGUAGE === 'en' ? this.ERROR_TEXT_ENGLISH : this.ERROR_TEXT_SPANISH
                return false
            }

            return await response.json()
        }
        catch(err) {
            this.errorMessage = this.CURRENT_LANGUAGE === 'en' ? 'Something went wrong, try to reload page' : 'Algo salió mal, intenta volver a cargar la página'
        }
    }

    /**
     * Builds HTML with got time slots and sets event listeners
     * @param {Array} slots
     * @param {string} slots.title
     */
    buildSlotsHTML(slots = []) {
        if(Array.isArray(slots)) {
            slots.forEach((slot) => {
                const div = document.createElement('div')
                div.classList.add('time-slots__slot')
                div.innerText = slot.title
                div.setAttribute('data-slot', slot.title)

                div.addEventListener('click', event => {
                    const slots = this.appContainer.querySelectorAll('.time-slots__slot--active')
                    Array.prototype.forEach.call(slots, el => {
                        el.classList.remove('time-slots__slot--active')
                    })

                    this.slotInput.value = event.target.getAttribute('data-slot')
                    event.target.classList?.add('time-slots__slot--active')
                    this.appContainer.classList.add('tp-scheduler--chosen-slot')
                })
                this.timeSlotsContainer.append(div)
            })
        }
    }

    /**
     * Sets class for show the loading animation
     * @param {Boolean} status 
     */
    setLoadingStatus(status = false) {
        if(status) {
            this.appContainer.classList.add('tp-scheduler--loading')
        }
        else {
            setTimeout(() => {
                this.appContainer.classList.remove('tp-scheduler--loading')
            }, 500)
        }
    }

    /**
     * Gets date objects for yesterday, today and tomorrow
     * @return {Date[]}
     */
    getVisibleDates() {
        const yesterdayDate = ( d => new Date(d.setDate(d.getDate() - 1)) )(new Date(this.activeDate))
        const tomorrowDate = ( d => new Date(d.setDate(d.getDate() + 1)) )(new Date(this.activeDate))

        return [yesterdayDate, this.activeDate, tomorrowDate]
    }

    /**
     * Builds and sets HTML, sets event handlers for visible dates
     * @param {Date} dates 
     */
    buildVisibleDatesHTML(dates) {
        // Prepare date string
        const dateStrings = dates.map(date => {
            const day = this.dayNames[date.getDay()]
            const month = this.monthNames[date.getMonth()]
            const dateNum = date.getDate() < 10 ? `0${date.getDate()}` : date.getDate()

            return `${day}, ${month} ${dateNum}`
        })

        // Insert date string into HTML and set event handlers
        dateStrings.forEach((el, index) => {
            const dateNode = document.createElement('div')
            dateNode.classList.add('date-slider__date')
            dateNode.innerText = el

            if(index === this.activeDateOrderIndex) {
                dateNode.classList.add('date-slider__date--active')
            }

            if(index === 0) {
                dateNode?.addEventListener('click', this.decreaseActiveDateHandler.bind(this))
            }
            else if(index === dateStrings.length - 1) {
                dateNode?.addEventListener('click', this.increaseActiveDateHandler.bind(this))
            }

            this.datesContainer.append(dateNode)
        })
    }

    /**
     * Handle a click to next day after active date
     */
    increaseActiveDateHandler() {
        this.activeDate = ( d => new Date(d.setDate(d.getDate() + 1)) )(new Date(this.activeDate))
        this.renderApp()
    }

    /**
     * Handle a click to previous day after active date
     */
    decreaseActiveDateHandler() {
        this.activeDate = ( d => new Date(d.setDate(d.getDate() - 1)) )(new Date(this.activeDate))
        this.renderApp()
    }

    /**
     * Fired by click to link for open calendar
     * @param {*} event 
     */
    onOpenCalendar(event) {
        event.preventDefault()

        if(!this.calendar) {
            this.calendar = window.jsCalendar.new("#js-scheduler-calendar", this.activeDate, {
                "monthFormat": "month YYYY",
                "dayFormat": "DD",
                "firstDayOfTheWeek": "2"
            })

            this.calendar.onDateClick((event, date) => {
                const activeDateString = `${this.activeDate.getDate()}-${this.activeDate.getMonth()}-${this.activeDate.getFullYear()}`
                const chosenDateString = `${date.getDate()}-${date.getMonth()}-${date.getFullYear()}`

                if(activeDateString === chosenDateString) {
                    this.appContainer.classList.remove('tp-scheduler--open-calendar')
                }
                else {
                    this.activeDate = date
                    this.appContainer.classList.remove('tp-scheduler--open-calendar')
                    this.renderApp()
                }
            })

            this.appContainer.querySelector('#js-scheduler-calendar > span')?.addEventListener('click', event => {
                event.preventDefault()
                this.appContainer.classList.remove('tp-scheduler--open-calendar')
            })
        }
        else {
            this.calendar.set(this.activeDate)
        }

        this.appContainer.classList.add('tp-scheduler--open-calendar')
    }
}