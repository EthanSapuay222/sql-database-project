// Admin login page JS
// Currently minimal — can add client-side checks or enhancements here

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form[action="/admin_login"]');
    if (!form) return;

    form.addEventListener('submit', function() {
        // You can add client-side validation or visual feedback here
    });
});
