// like.js
document.addEventListener('DOMContentLoaded', () => {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const postId = button.getAttribute('data-post-id');
            const likeCountElement = button.nextElementSibling;

            // Simulate an API call to the backend to toggle the like status
            const response = await toggleLike(postId);

            if (response.success) {
                button.classList.toggle('liked');
                likeCountElement.textContent = response.likeCount;
            }
        });
    });
});

// Simulate an API call to the backend (replace with your actual backend logic)
async function toggleLike(postId) {
    try {
        // Your backend API endpoint to handle likes (e.g., /like)
        const response = await fetch(`/like/${postId}`, {
            method: 'POST',
            // Add any necessary headers or authentication tokens
        });

        if (response.ok) {
            const data = await response.json();
            return { success: true, likeCount: data.likeCount };
        } else {
            return { success: false };
        }
    } catch (error) {
        console.error('Error toggling like:', error);
        return { success: false };
    }
}
