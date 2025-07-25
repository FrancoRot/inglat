// JavaScript para la página de inicio - Home Page
document.addEventListener('DOMContentLoaded', function() {
    // Animación de números en las estadísticas
    const statNumbers = document.querySelectorAll('.stat-item__number');
    
    const animateNumbers = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = target.textContent;
                const numValue = parseInt(finalValue.replace(/[^\d]/g, ''));
                const suffix = finalValue.replace(/[\d]/g, '');
                
                let current = 0;
                const increment = Math.ceil(numValue / 50);
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= numValue) {
                        current = numValue;
                        clearInterval(timer);
                    }
                    target.textContent = current + suffix;
                }, 30);
                
                observer.unobserve(target);
            }
        });
    };
    
    const observer = new IntersectionObserver(animateNumbers, {
        threshold: 0.5
    });
    
    statNumbers.forEach(num => observer.observe(num));
    
    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});