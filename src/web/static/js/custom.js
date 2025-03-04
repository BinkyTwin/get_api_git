// Gestion du formulaire d'analyse
document.addEventListener('DOMContentLoaded', function() {
    const analyzeForm = document.getElementById('analyze-form');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            // Désactiver le bouton et afficher le spinner
            submitBtn.disabled = true;
            submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyse en cours...`;
            
            // Réactiver le bouton après 30 secondes (timeout de sécurité)
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 30000);
        });
    }
    
    // Animation des cartes de statistiques
    const statsCards = document.querySelectorAll('.stats-card');
    statsCards.forEach(card => {
        const value = card.querySelector('.display-4');
        if (value) {
            const finalValue = parseInt(value.textContent);
            let currentValue = 0;
            const duration = 1000; // 1 seconde
            const steps = 50;
            const increment = finalValue / steps;
            const stepDuration = duration / steps;
            
            const counter = setInterval(() => {
                currentValue += increment;
                if (currentValue >= finalValue) {
                    value.textContent = finalValue;
                    clearInterval(counter);
                } else {
                    value.textContent = Math.floor(currentValue);
                }
            }, stepDuration);
        }
    });
    
    // Gestion des boutons d'export
    const exportButtons = document.querySelectorAll('[data-export]');
    exportButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const format = this.dataset.export;
            const originalText = this.innerHTML;
            
            // Afficher le spinner pendant l'export
            this.disabled = true;
            this.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Export en cours...`;
            
            // Réactiver le bouton après l'export
            setTimeout(() => {
                this.disabled = false;
                this.innerHTML = originalText;
            }, 3000);
        });
    });
});

// Gestion des messages flash
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
    alertContainer.role = 'alert';
    
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.querySelector('.container').insertBefore(
        alertContainer,
        document.querySelector('.container').firstChild
    );
    
    // Auto-fermeture après 5 secondes
    setTimeout(() => {
        alertContainer.remove();
    }, 5000);
}

// Gestion des erreurs AJAX
function handleAjaxError(error) {
    console.error('Erreur:', error);
    showAlert('Une erreur est survenue. Veuillez réessayer.', 'danger');
} 