// Fungsi untuk mengupdate tampilan card konsultasi
function updateConsultationCard(card, status) {
    const statusElement = card.querySelector('.status-text');
    const chatButton = card.querySelector('.chat-button');
    const countdownContainer = card.querySelector('.countdown-container');
    
    if (!statusElement || !chatButton) return;

    switch(status) {
        case 'not_started':
            statusElement.textContent = 'Belum Mulai';
            statusElement.className = 'status-text text-orange-600';
            chatButton.disabled = true;
            chatButton.classList.add('bg-gray-300', 'text-gray-500', 'cursor-not-allowed');
            chatButton.classList.remove('bg-[#2196f3]', 'text-white', 'hover:bg-blue-600');
            break;
            
        case 'in_progress':
            statusElement.textContent = 'Sedang Berlangsung';
            statusElement.className = 'status-text text-green-600';
            chatButton.disabled = false;
            chatButton.classList.remove('bg-gray-300', 'text-gray-500', 'cursor-not-allowed');
            chatButton.classList.add('bg-[#2196f3]', 'text-white', 'hover:bg-blue-600');
            if (countdownContainer) countdownContainer.remove();
            break;
            
        case 'completed':
            statusElement.textContent = 'Telah Berakhir';
            statusElement.className = 'status-text text-gray-600';
            chatButton.disabled = false;
            chatButton.classList.remove('bg-gray-300', 'text-gray-500', 'cursor-not-allowed');
            chatButton.classList.add('bg-[#2196f3]', 'text-white', 'hover:bg-blue-600');
            if (countdownContainer) countdownContainer.remove();
            break;
    }
}

// Fungsi untuk mengupdate countdown
function updateCountdown() {
    document.querySelectorAll('.countdown').forEach(element => {
        const startDate = element.dataset.startDate;
        const startTime = element.dataset.startTime;
        const consultationId = element.dataset.consultationId;
        
        if (!startDate || !startTime || !consultationId) return;
        
        const startDateTime = new Date(`${startDate}T${startTime}`);
        const now = new Date();
        let diff = startDateTime - now;
        
        // Dapatkan card parent
        const card = element.closest('.consultation-card');
        if (!card) {
            console.error('Could not find parent consultation card');
            return;
        }
        
        // Jika waktu sudah habis, update status melalui API
        if (diff <= 0) {
            checkConsultationStatus(consultationId, card);
            return;
        }
        
        // Hitung selisih waktu akhir
        const endedAt = new Date(card.dataset.endedAt); // Pastikan card memiliki data endedAt
        const remainingDiff = endedAt - now;

        // Jika selisih waktu akhir sudah lebih dari nol, update status
        if (remainingDiff <= 0) {
            checkConsultationStatus(consultationId, card);
            return;
        }
        
        // Convert to hours, minutes, seconds
        const hours = Math.floor(diff / (1000 * 60 * 60));
        diff -= hours * (1000 * 60 * 60);
        
        const minutes = Math.floor(diff / (1000 * 60));
        diff -= minutes * (1000 * 60);
        
        const seconds = Math.floor(diff / 1000);
        
        // Format the output
        let timeString = '';
        if (hours > 0) timeString += `${hours} jam `;
        if (minutes > 0 || hours > 0) timeString += `${minutes} menit `;
        timeString += `${seconds} detik`;
        
        element.textContent = timeString;
    });
}

// Fungsi untuk mengecek status konsultasi
async function checkConsultationStatus(consultationId, card) {
    try {
        const response = await fetch(`/consultation/check-status/${consultationId}/`);
        const data = await response.json();
        
        if (data.status === 'success') {
            updateConsultationCard(card, data.consultation_status);
        }
    } catch (error) {
        console.error('Error checking consultation status:', error);
    }
}

// Fungsi untuk mengecek semua status konsultasi
function checkAllConsultationStatuses() {
    document.querySelectorAll('.consultation-card').forEach(card => {
        const consultationId = card.querySelector('.countdown')?.dataset.consultationId;
        if (consultationId) {
            checkConsultationStatus(consultationId, card);
        }
    });
}

// Jalankan update pertama kali
document.addEventListener('DOMContentLoaded', () => {
    updateCountdown();
    checkAllConsultationStatuses();
});

// Update countdown setiap 1 detik
const countdownInterval = setInterval(updateCountdown, 1000);

// Update status setiap 5 detik
const statusInterval = setInterval(checkAllConsultationStatuses, 5000);

// Bersihkan interval saat halaman ditutup
window.addEventListener('beforeunload', () => {
    clearInterval(countdownInterval);
    clearInterval(statusInterval);
});

// Tab switching logic
const tabButtons = document.querySelectorAll('.tab-button');
const tabContents = document.querySelectorAll('.tab-content');

tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Remove active state from all buttons
        tabButtons.forEach(btn => {
            btn.classList.remove('border-[#2196f3]', 'text-[#2196f3]');
            btn.classList.add('text-gray-500');
        });

        // Add active state to clicked button
        button.classList.add('border-[#2196f3]', 'text-[#2196f3]');
        button.classList.remove('text-gray-500');

        // Hide all tab contents
        tabContents.forEach(content => {
            content.classList.add('hidden');
        });

        // Show selected tab content
        const tabId = button.dataset.tab + 'Tab';
        document.getElementById(tabId).classList.remove('hidden');
    });
});