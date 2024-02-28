//profile.js

document.addEventListener('DOMContentLoaded', function () {
    const otherUserProfiles = document.querySelectorAll('.other-user-profile-image');
    otherUserProfiles.forEach(profile => {
        const userId = profile.dataset.userId;
        fetch(`/get_profile_image/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.profile_image) {
                    const img = document.createElement('img');
                    img.src = data.profile_image;
                    img.alt = 'Profile Image';
                    img.classList.add('h-10', 'w-10', 'rounded-full', 'mb-2');
                    profile.appendChild(img);
                }
            });
    });
});
