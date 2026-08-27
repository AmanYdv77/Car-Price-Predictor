document.addEventListener('DOMContentLoaded', () => {
    // Initialize Lucide Icons
    lucide.createIcons();

    // Elements
    const form = document.getElementById('prediction-form');
    const tabs = document.querySelectorAll('.step-tab');
    const indicators = document.querySelectorAll('.step-indicator');
    const progressBar = document.getElementById('progress-bar-fill');
    
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');

    let currentStep = 1;
    const totalSteps = tabs.length;

    // 1. Wizard Navigation Logic
    function updateWizard() {
        // Show/hide tabs
        tabs.forEach((tab, index) => {
            if (index + 1 === currentStep) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });

        // Update progress indicators & classes
        indicators.forEach((indicator, index) => {
            const stepNum = index + 1;
            if (stepNum === currentStep) {
                indicator.classList.add('active');
                indicator.classList.remove('completed');
            } else if (stepNum < currentStep) {
                indicator.classList.add('completed');
                indicator.classList.remove('active');
            } else {
                indicator.classList.remove('active', 'completed');
            }
        });

        // Progress bar percentage
        const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
        progressBar.style.width = `${progressPercentage}%`;

        // Button visibility
        if (currentStep === 1) {
            prevBtn.classList.add('hidden');
        } else {
            prevBtn.classList.remove('hidden');
        }

        if (currentStep === totalSteps) {
            nextBtn.classList.add('hidden');
            submitBtn.classList.remove('hidden');
        } else {
            nextBtn.classList.remove('hidden');
            submitBtn.classList.add('hidden');
        }
        
        // Re-trigger icon rendering for dynamically rendered parts (if any)
        lucide.createIcons();
    }

    // Next/Prev click handlers
    nextBtn.addEventListener('click', () => {
        if (currentStep < totalSteps) {
            currentStep++;
            updateWizard();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    prevBtn.addEventListener('click', () => {
        if (currentStep > 1) {
            currentStep--;
            updateWizard();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    });

    // Step indicators clicks (allow clicking completed or active steps to go back)
    indicators.forEach(indicator => {
        indicator.addEventListener('click', () => {
            const clickedStep = parseInt(indicator.getAttribute('data-step'));
            if (clickedStep < currentStep || indicator.classList.contains('completed')) {
                currentStep = clickedStep;
                updateWizard();
            }
        });
    });


    // 2. Custom Range Sliders Live Update
    const sliders = form.querySelectorAll('input[type="range"]');
    sliders.forEach(slider => {
        const valSpan = document.getElementById(`${slider.id}-val`);
        if (valSpan) {
            slider.addEventListener('input', (e) => {
                valSpan.innerText = e.target.value;
            });
        }
    });


    // 3. Dynamic Price Count-Up Animation
    function animatePrice(targetPrice) {
        const priceElement = document.getElementById('predicted-price');
        const priceElementInr = document.getElementById('predicted-price-inr');
        const startPrice = 0;
        const duration = 1200; // milliseconds
        const startTime = performance.now();

        // 1 USD = 83.5 INR (Approx conversion rate)
        const targetPriceInr = targetPrice * 83.5;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Easing: easeOutQuad
            const ease = progress * (2 - progress);
            const currentValUsd = startPrice + (targetPrice - startPrice) * ease;
            const currentValInr = startPrice + (targetPriceInr - startPrice) * ease;

            const formatterUsd = new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });

            const formatterInr = new Intl.NumberFormat('en-IN', {
                style: 'currency',
                currency: 'INR',
                minimumFractionDigits: 0,
                maximumFractionDigits: 0
            });

            priceElement.innerText = formatterUsd.format(Math.round(currentValUsd));
            if (priceElementInr) {
                priceElementInr.innerText = formatterInr.format(Math.round(currentValInr));
            }

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }


    // 4. Form Submission & API Request
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = `Predicting... <i data-lucide="loader" class="animate-spin"></i>`;
        submitBtn.disabled = true;
        lucide.createIcons();

        // Gather form data
        const formData = new FormData(form);
        const payload = {};

        formData.forEach((value, key) => {
            // Convert to numbers if numeric
            if (!isNaN(value) && value.trim() !== '') {
                payload[key] = Number(value);
            } else {
                payload[key] = value;
            }
        });

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            const resultContainer = document.getElementById('result-container');
            const priceElement = document.getElementById('predicted-price');

            if (response.ok) {
                resultContainer.classList.remove('hidden');
                animatePrice(result.predicted_price);
                
                // Scroll to result box smoothly
                setTimeout(() => {
                    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }, 100);
            } else {
                priceElement.innerText = 'Error';
                priceElement.style.color = '#ef4444';
                const priceElementInr = document.getElementById('predicted-price-inr');
                if (priceElementInr) priceElementInr.innerText = '';
                resultContainer.classList.remove('hidden');
                console.error(result);
                alert(`Error: ${result.detail || 'Prediction failed'}`);
            }

        } catch (error) {
            console.error("Network error:", error);
            alert("Unable to reach the prediction server. Please make sure it is running.");
        } finally {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            lucide.createIcons();
        }
    });

    // Run initial wizard setup
    updateWizard();
});
