export function initLoadMorePosts() {
	const loadButton = document.getElementById('load-more-posts');
	const postsContainer = document.getElementById('posts-container');
	// const url = postsContainer ? $(postsContainer).data('url') : undefined

	if (loadButton && postsContainer) {
		loadButton.addEventListener('click', e => {
			e.preventDefault();

			$(loadButton).prop('disabled', true);

			$.ajax({
				url: `?page=${parseInt($(postsContainer).data('currentPage'), 10) + 1}`,
				type: 'GET',
				success: data => { 
					const scrollPosition = document.documentElement.scrollTop

					$(postsContainer).append(data);
					$(postsContainer).data('currentPage', parseInt($(postsContainer).data('currentPage'), 10) + 1);

					if ($(postsContainer).data('currentPage') >= $(postsContainer).data('maxPages')) {
						loadButton.style.display = 'none';
					}

					// const posts = postsContainer.querySelectorAll('.tp-post')
					document.documentElement.scrollTop = scrollPosition
					// $([document.documentElement, document.body]).animate({
					// 	scrollTop: $(posts[posts.length - 5]).offset().top - 100
					// }, 2000);
					
				},
				error: err => {
					console.log(err);
				},
				complete: () => {
					$(loadButton).prop('disabled', false);
				},
			});
		});
	}
}
