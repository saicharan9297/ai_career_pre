document.addEventListener('DOMContentLoaded', () => {
    // Basic micro-animations for cards
    const cards = document.querySelectorAll('.card-glass');
    cards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
            card.style.transition = 'transform 0.3s ease';
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });

    // Handle session results logging (Simulated)
    const interviewForm = document.getElementById('interview-form');
    if (interviewForm) {
        interviewForm.addEventListener('submit', () => {
            const btn = interviewForm.querySelector('button[type="submit"]');
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Evaluating...';
            btn.disabled = true;
        });
    }
});
