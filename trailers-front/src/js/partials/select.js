/**
 * Select2 init
 */
export function select2() {
	$('select').select2({
		minimumResultsForSearch: -1,
        templateResult: function (data) {
            if (!data.element) {
                return data.text;
            }
            if(data.element.classList.contains('storeState')){
                var $wrapper = $('<span></span>');
                $wrapper.addClass(data.element.classList[0]);
                $wrapper.text(data.text);
                return $wrapper;
            }
        return data.text;
        }
	});
}