document.addEventListener('DOMContentLoaded', () => {
    const toggleButtons = document.querySelectorAll('[data-toggle-password]');
    toggleButtons.forEach((button) => {
        const targetId = button.getAttribute('data-target');
        const target = document.getElementById(targetId);
        if (!target) {
            return;
        }
        button.addEventListener('click', () => {
            const isHidden = target.type === 'password';
            target.type = isHidden ? 'text' : 'password';
            button.textContent = isHidden ? 'Hide' : 'Show';
            button.setAttribute('aria-pressed', isHidden ? 'true' : 'false');
        });
    });
});
