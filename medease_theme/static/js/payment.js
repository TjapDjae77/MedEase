document.addEventListener('DOMContentLoaded', function() {
    const paymentButton = document.querySelector('.payment-button');
    
    if (paymentButton) {
        paymentButton.addEventListener('click', async function(e) {
            e.preventDefault();
            
            // Ambil data yang diperlukan dengan pengecekan null
            const doctorId = document.querySelector('[name="doctor_id"]')?.value;
            const packageType = document.querySelector('[name="package_type"]')?.value;
            const consultationDate = document.querySelector('[name="consultation_date"]')?.value;
            const consultationTime = document.querySelector('[name="consultation_time"]')?.value;
            const paymentMethod = document.querySelector('input[name="payment_method"]:checked')?.value;

            // Validasi data yang diperlukan
            if (!doctorId || !packageType || !consultationDate) {
                alert('Data konsultasi tidak lengkap');
                return;
            }

            if (!paymentMethod) {
                alert('Silakan pilih metode pembayaran');
                return;
            }

            try {
                const response = await fetch('/payment/process/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value
                    },
                    body: JSON.stringify({
                        doctor_id: doctorId,
                        package_type: packageType,
                        consultation_date: consultationDate,
                        consultation_time: consultationTime || null,
                        payment_method: paymentMethod
                    })
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    window.location.href = data.redirect_url;
                } else {
                    alert('Terjadi kesalahan: ' + data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Terjadi kesalahan saat memproses pembayaran');
            }
        });
    } else {
        console.error('Payment button not found');
    }
});
