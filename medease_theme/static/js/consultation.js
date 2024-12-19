function checkConsultationStatus(consultationId) {
    fetch(`/consultation/check-status/${consultationId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const statusElement = document.querySelector(`#consultation-${consultationId} .status-text`);
                const chatButton = document.querySelector(`#consultation-${consultationId} .chat-button`);
                
                // Update text status
                if (data.consultation_status === 'not_started') {
                    statusElement.textContent = 'Belum Mulai';
                    statusElement.className = 'status-text text-orange-600';
                    chatButton.disabled = true;
                    chatButton.className = 'chat-button block mt-2 px-4 py-2 bg-gray-300 text-gray-500 cursor-not-allowed';
                } else if (data.consultation_status === 'in_progress') {
                    statusElement.textContent = 'Sedang Berlangsung';
                    statusElement.className = 'status-text text-green-600';
                    chatButton.disabled = false;
                    chatButton.className = 'chat-button block mt-2 px-4 py-2 bg-[#2196f3] text-white hover:bg-blue-600';
                } else {
                    statusElement.textContent = 'Telah Berakhir';
                    statusElement.className = 'status-text text-gray-600';
                    chatButton.disabled = false;
                    chatButton.className = 'chat-button block mt-2 px-4 py-2 bg-[#2196f3] text-white hover:bg-blue-600';
                }
            }
        });
}

// Fungsi untuk mengecek status konsultasi
async function checkConsultationStatus() {
    try {
        const response = await fetch(`/consultation/check-status/${consultationId}/`);
        const data = await response.json();
        
        if (data.status === 'success') {
            // Update status text dan styling
            const statusElement = document.querySelector('.status-text');
            const remainingTimeElement = document.getElementById('remainingTime');
            
            if (statusElement) {
                if (data.consultation_status === 'not_started') {
                    statusElement.textContent = 'Belum Mulai';
                    statusElement.className = 'status-text text-orange-600';
                    if (messageInput) messageInput.disabled = true;
                    if (sendButton) sendButton.disabled = true;
                    if (chatForm) chatForm.classList.add('opacity-50');
                    if (endSessionBtn) endSessionBtn.style.display = 'none';
                } else if (data.consultation_status === 'in_progress') {
                    statusElement.textContent = 'Sedang Berlangsung';
                    statusElement.className = 'status-text text-green-600';
                    if (messageInput) messageInput.disabled = false;
                    if (sendButton) {
                        sendButton.disabled = !messageInput.value.trim();
                        sendButton.classList.toggle('opacity-50', !messageInput.value.trim());
                    }
                    if (chatForm) chatForm.classList.remove('opacity-50');
                    if (endSessionBtn) endSessionBtn.style.display = 'block';
                    
                    // Jika baru saja berubah ke in_progress, reload halaman
                    if (window.lastStatus && window.lastStatus === 'not_started') {
                        location.reload();
                    }
                } else if (data.consultation_status === 'completed') {
                    statusElement.textContent = 'Telah Berakhir';
                    statusElement.className = 'status-text text-gray-600';
                    if (messageInput) messageInput.disabled = true;
                    if (sendButton) sendButton.disabled = true;
                    if (endSessionBtn) endSessionBtn.style.display = 'none';
                    
                    // Hapus tampilan remaining time
                    if (remainingTimeElement) {
                        remainingTimeElement.textContent = '';
                    }
                    
                    // Ganti form chat dengan pesan berakhir
                    if (chatForm) {
                        const container = chatForm.parentElement;
                        chatForm.remove();
                        container.innerHTML = `
                            <div class="text-center text-gray-600 py-2">
                                Sesi konsultasi telah berakhir.
                            </div>
                        `;
                    }
                }
            }

            // Update remaining time jika konsultasi belum berakhir
            if (remainingTimeElement) {
                if (data.consultation_status !== 'completed' && data.remaining_time) {
                    remainingTimeElement.textContent = `Sisa waktu: ${data.remaining_time}`;
                } else {
                    remainingTimeElement.textContent = '';
                }
            }

            // Simpan status terakhir
            window.lastStatus = data.consultation_status;
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Jalankan pengecekan pertama kali saat halaman dimuat
document.addEventListener('DOMContentLoaded', () => {
    checkConsultationStatus();
});

// Update setiap 5 detik
const statusInterval = setInterval(checkConsultationStatus, 5000);

// Bersihkan interval saat halaman ditutup
window.addEventListener('beforeunload', () => {
    clearInterval(statusInterval);
});

// Dapatkan elemen yang diperlukan
const chatMessages = document.getElementById('chatMessages');
const chatForm = document.getElementById('chatForm');
const messageInput = document.getElementById('messageInput');
const endSessionBtn = document.getElementById('endSessionBtn');
const sendButton = document.querySelector('button[type="submit"]');

// Fungsi untuk scroll window ke pesan terbaru
function scrollToBottom(smooth = true) {
    if (chatMessages) {
        // Tambahkan timeout kecil untuk memastikan DOM sudah diupdate
        setTimeout(() => {
            const lastMessage = chatMessages.lastElementChild;
            if (lastMessage) {
                lastMessage.scrollIntoView({
                    behavior: smooth ? 'smooth' : 'auto',
                    block: 'end'
                });
            }
        }, 100);
    }
}

// Scroll saat halaman pertama kali dimuat
document.addEventListener('DOMContentLoaded', () => {
    scrollToBottom(false);
});

// Scroll setelah gambar dan konten lain dimuat
window.addEventListener('load', () => {
    scrollToBottom(false);
});

// Tambahkan observer untuk memantau perubahan di chat messages
if (chatMessages) {
    const observer = new MutationObserver(() => {
        scrollToBottom();
    });

    observer.observe(chatMessages, {
        childList: true,
        subtree: true,
        characterData: true
    });
}

// Hanya jalankan logika input dan form jika konsultasi masih aktif (form masih ada)
if (chatForm) {
    if (messageInput && sendButton) {
        // Disable/enable send button berdasarkan input
        messageInput.addEventListener('input', () => {
            const isEmpty = !messageInput.value.trim();
            sendButton.disabled = isEmpty;
            
            if (isEmpty) {
                sendButton.classList.add('opacity-50', 'cursor-not-allowed');
                sendButton.classList.remove('hover:bg-blue-600');
            } else {
                sendButton.classList.remove('opacity-50', 'cursor-not-allowed');
                sendButton.classList.add('hover:bg-blue-600');
            }
        });

        // Set initial state
        sendButton.disabled = true;
        sendButton.classList.add('opacity-50', 'cursor-not-allowed');
        sendButton.classList.remove('hover:bg-blue-600');
    }

    // Form submission handler
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = messageInput.value.trim();
        if (!message) return;

        try {
            const response = await fetch(`/consultation/send-message/${consultationId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ content: message })
            });

            const data = await response.json();
            if (data.status === 'success') {
                // Clear input
                messageInput.value = '';
                sendButton.disabled = true;
                sendButton.classList.add('opacity-50', 'cursor-not-allowed');
                sendButton.classList.remove('hover:bg-blue-600');

                // Add user message to chat
                const userMessageHtml = `
                    <div class="flex items-end justify-end">
                        <div class="bg-white rounded-lg p-3 max-w-md shadow">
                            <p class="text-gray-800">${data.user_message.content}</p>
                            <p class="text-xs text-gray-500 mt-1">${data.user_message.created_at}</p>
                        </div>
                    </div>
                `;
                chatMessages.insertAdjacentHTML('beforeend', userMessageHtml);
                scrollToBottom(); // scroll setelah pesan user

                // Add doctor's response after a delay
                setTimeout(() => {
                    const doctorMessageHtml = `
                        <div class="flex items-start">
                            <div class="flex-shrink-0 mr-3">
                                <img src="${doctorProfilePicture}" 
                                     alt="Doctor Profile"
                                     class="w-8 h-8 rounded-full"
                                     onload="scrollToBottom()"> 
                            </div>
                            <div class="bg-blue-50 rounded-lg p-3 max-w-md shadow">
                                <p class="text-gray-800">${data.doctor_message.content}</p>
                                <p class="text-xs text-gray-500 mt-1">${data.doctor_message.created_at}</p>
                            </div>
                        </div>
                    `;
                    chatMessages.insertAdjacentHTML('beforeend', doctorMessageHtml);
                    scrollToBottom(); // scroll setelah respon dokter
                }, 1000);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
}

// End session button handler
if (endSessionBtn) {
    endSessionBtn.addEventListener('click', async () => {
        if (confirm('Apakah Anda yakin ingin mengakhiri sesi konsultasi ini?')) {
            try {
                const response = await fetch(`/consultation/end-session/${consultationId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                });

                const data = await response.json();
                if (data.status === 'success') {
                    // Hapus form chat dan tampilkan pesan ended
                    if (chatForm) {
                        const container = chatForm.parentElement;
                        chatForm.remove();
                        container.innerHTML = `
                            <div class="text-center text-gray-600 py-2">
                                Sesi konsultasi telah berakhir.
                            </div>
                        `;
                    }
                    
                    // Sembunyikan tombol end session dan hapus remaining time
                    endSessionBtn.style.display = 'none';
                    const remainingTimeElement = document.getElementById('remainingTime');
                    if (remainingTimeElement) {
                        remainingTimeElement.textContent = '';
                    }
                }
            } catch (error) {
                console.error('Error ending session:', error);
            }
        }
    });
}

// Validasi variabel yang diperlukan
if (typeof consultationId === 'undefined') {
    console.error('consultationId is not defined');
}

if (typeof doctorProfilePicture === 'undefined') {
    console.error('doctorProfilePicture is not defined');
}

// Tambahkan event listener untuk keyboard
if (messageInput) {
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!messageInput.value.trim()) return;
            chatForm.dispatchEvent(new Event('submit'));
        }
    });
}