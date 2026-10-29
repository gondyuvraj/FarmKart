document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(a => {
                a.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                a.style.opacity = '0';
                a.style.transform = 'translateY(-10px)';
                setTimeout(() => a.remove(), 500);
            });
        }, 5000);
    }

    // 2. Pincode delivery check simulator
    const pincodeBtn = document.getElementById('checkPincodeBtn');
    const pincodeInput = document.getElementById('pincodeInput');
    const pincodeResult = document.getElementById('pincodeResult');

    if (pincodeBtn && pincodeInput && pincodeResult) {
        pincodeBtn.addEventListener('click', () => {
            const pin = pincodeInput.value.trim();
            if (pin.length === 6 && /^\d+$/.test(pin)) {
                pincodeResult.innerHTML = `
                    <div style="color: #16a34a; font-weight: 600; font-size: 13px; margin-top: 8px;">
                        ✓ Delivery available to <strong>${pin}</strong> within 2-3 Business Days.
                        <br><span style="color: #64748b; font-size: 12px;">Cash on Delivery (COD) & Kisan Doorstep Delivery available.</span>
                    </div>
                `;
            } else {
                pincodeResult.innerHTML = `
                    <div style="color: #dc2626; font-size: 13px; margin-top: 8px;">
                        Please enter a valid 6-digit Indian postal code.
                    </div>
                `;
            }
        });
    }

    // 3. Detail page tabs (Specifications, Farmer Dosage, Reviews)
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const targetId = btn.getAttribute('data-tab');

                tabBtns.forEach(b => b.classList.remove('active'));
                tabContents.forEach(c => c.style.display = 'none');

                btn.classList.add('active');
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.style.display = 'block';
                }
            });
        });
    }

    // 4. Cart quantity stepper quick submit
    const stepperBtns = document.querySelectorAll('.stepper-action-btn');
    stepperBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const form = btn.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    console.log('🌾 FarmKart Kisan E-Commerce portal initialized.');
});