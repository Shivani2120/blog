$(document).ready(function () {
	$('.like-button').click(function () {
			var postId = $(this).data('post-id');
			$.ajax({
					type: 'POST',
					url: '/like/' + postId + '/',
					headers: { 'X-CSRFToken': csrf_token },
					success: function (data) {
							// Update the like count in the UI
							$('.like-count').text(data.like_count);
					}
			});
	});

	$('.dislike-button').click(function () {
			var postId = $(this).data('post-id');
			$.ajax({
					type: 'POST',
					url: '/dislike/' + postId + '/',
					headers: { 'X-CSRFToken': csrf_token },
					success: function (data) {
							// Update the dislike count in the UI
							$('.dislike-count').text(data.dislike_count);
					}
			});
	});
});