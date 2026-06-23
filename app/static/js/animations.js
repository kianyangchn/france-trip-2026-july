// Intersection Observer for scroll-in animations with stagger
document.addEventListener('DOMContentLoaded', () => {
    let staggerIndex = 0;
    let staggerTimer = null;

    const observer = new IntersectionObserver(
        (entries) => {
            const visible = entries.filter((e) => e.isIntersecting);
            visible.forEach((entry, i) => {
                const delay = i * 50;
                setTimeout(() => {
                    entry.target.classList.add('visible');
                }, delay);
                observer.unobserve(entry.target);
            });
        },
        { threshold: 0.05, rootMargin: '50px 0px 0px 0px' }
    );

    document.querySelectorAll('.animate-in').forEach((el) => observer.observe(el));

    // Snap active nav item into view
    const activeNav = document.querySelector('.day-nav-item--active');
    if (activeNav) {
        activeNav.scrollIntoView({ inline: 'center', block: 'nearest', behavior: 'instant' });
    }
});
