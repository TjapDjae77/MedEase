document.addEventListener('DOMContentLoaded', function() {
    const calendarDays = document.getElementById('calendarDays');
    const currentMonthElement = document.getElementById('currentMonth');
    const prevMonthButton = document.getElementById('prevMonth');
    const nextMonthButton = document.getElementById('nextMonth');
    const packageType = document.getElementById('packageType').value;
    
    let currentDate = new Date();
    let selectedDates = [];
    let selectedStartDate = null;
    let selectedTime = null;

    function renderCalendar(date) {
        calendarDays.innerHTML = '';
        
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        const startingDay = firstDay.getDay();
        const totalDays = lastDay.getDate();
        
        currentMonthElement.textContent = new Intl.DateTimeFormat('id-ID', { 
            year: 'numeric', 
            month: 'long' 
        }).format(date);

        // Add empty cells for days before the first day of the month
        for (let i = 0; i < startingDay; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'text-center p-2';
            calendarDays.appendChild(emptyDay);
        }

        // Get today's date for comparison
        const today = new Date();
        today.setHours(0, 0, 0, 0);

        // Add days of the month
        for (let day = 1; day <= totalDays; day++) {
            const dayElement = document.createElement('button');
            const dateToCheck = new Date(date.getFullYear(), date.getMonth(), day);
            
            // Base classes
            let classes = 'text-center p-2 w-full rounded-lg transition-colors';

            if (dateToCheck < today) {
                // Past dates
                classes += ' text-gray-300 cursor-not-allowed';
                dayElement.disabled = true;
            } else {
                // Future and today dates
                classes += ' hover:bg-blue-50';
                
                // Check if it's today
                if (dateToCheck.getTime() === today.getTime()) {
                    classes += ' border-2 border-[#2196f3] today-marker';
                }
            }

            dayElement.className = classes;
            dayElement.textContent = day;

            if (!dayElement.disabled) {
                dayElement.addEventListener('click', () => selectDate(dateToCheck, dayElement));
            }

            calendarDays.appendChild(dayElement);
        }

        // Add empty cells for days after the last day of the month
        const remainingDays = 42 - (startingDay + totalDays);
        for (let i = 0; i < remainingDays; i++) {
            const emptyDay = document.createElement('div');
            emptyDay.className = 'text-center p-2';
            calendarDays.appendChild(emptyDay);
        }

        updateCalendarHighlights();
    }

    function updateCalendarHighlights() {
        // Remove all highlights first
        const allDays = calendarDays.querySelectorAll('button:not([disabled])');
        allDays.forEach(day => {
            day.classList.remove('bg-[#2196f3]', 'text-white');
            
            // Restore today's border if it's not selected
            const dateStr = day.textContent.padStart(2, '0');
            const currentMonth = currentDate.getMonth();
            const currentYear = currentDate.getFullYear();
            const dayDate = new Date(currentYear, currentMonth, parseInt(dateStr));
            
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (dayDate.getTime() === today.getTime() && !selectedDates.some(d => d.getTime() === today.getTime())) {
                day.classList.add('border-2', 'border-[#2196f3]', 'today-marker');
            }
        });

        // Add highlights for selected dates
        selectedDates.forEach(date => {
            const dayElement = findDayElement(date);
            if (dayElement) {
                dayElement.classList.add('bg-[#2196f3]', 'text-white');
                // Remove today's border if it's selected
                dayElement.classList.remove('border-2', 'border-[#2196f3]', 'today-marker');
            }
        });
    }

    function findDayElement(date) {
        const dayButtons = calendarDays.querySelectorAll('button:not([disabled])');
        return Array.from(dayButtons).find(button => {
            const buttonDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), parseInt(button.textContent));
            return buttonDate.getTime() === date.getTime();
        });
    }

    function selectDate(date, element) {
        selectedDates = [];
        
        switch(packageType) {
            case 'regular':
                selectedDates = [date];
                selectedStartDate = date;
                enableTimeSlots();
                break;
                
            case '1day':
                selectedDates = [date];
                selectedStartDate = date;
                break;
                
            case '3day':
                selectedStartDate = date;
                for(let i = 0; i < 3; i++) {
                    const nextDate = new Date(date);
                    nextDate.setDate(date.getDate() + i);
                    selectedDates.push(nextDate);
                }
                break;
                
            case '7day':
                selectedStartDate = date;
                for(let i = 0; i < 7; i++) {
                    const nextDate = new Date(date);
                    nextDate.setDate(date.getDate() + i);
                    selectedDates.push(nextDate);
                }
                break;
        }

        // Perbaikan format tanggal
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const formattedDate = `${year}-${month}-${day}`;
        
        const dateInput = document.getElementById('selectedDateInput');
        dateInput.value = formattedDate;
        dateInput.setAttribute('value', formattedDate);
        console.log('Date input after set:', dateInput.value);
        
        updateCalendarHighlights();
        updateSelectedDatesDisplay();
        updateContinueButton();
    }

    function enableTimeSlots() {
        if (packageType === 'regular') {
            const timeButtons = document.querySelectorAll('#timeSlots button');
            const today = new Date();
            const selectedDate = selectedDates[0]; // Mengambil tanggal yang dipilih
            
            // Set waktu ke 00:00:00 untuk membandingkan tanggal saja
            const todayDate = new Date(today.getFullYear(), today.getMonth(), today.getDate());
            const selectedDateTime = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate());
            
            timeButtons.forEach(button => {
                const hour = parseInt(button.textContent);
                
                if (todayDate.getTime() === selectedDateTime.getTime()) {
                    // Jika tanggal yang dipilih adalah hari ini
                    const currentHour = today.getHours();
                    const currentMinutes = today.getMinutes();
                    
                    // Hitung selisih waktu dalam menit
                    const diffInMinutes = (hour - currentHour) * 60 - currentMinutes;
                    
                    if (hour < currentHour || diffInMinutes < 10) {
                        // Disable jika:
                        // - Jam sudah lewat, ATAU
                        // - Selisih dengan jam berikutnya kurang dari 10 menit
                        button.disabled = true;
                        button.classList.remove('text-[#2196f3]');
                        button.classList.add('text-gray-300', 'cursor-not-allowed');
                    } else {
                        // Enable jam yang masih tersedia dan memiliki selisih >= 10 menit
                        button.disabled = false;
                        button.classList.remove('text-gray-300', 'cursor-not-allowed');
                        button.classList.add('text-[#2196f3]');
                    }
                } else {
                    // Untuk tanggal selain hari ini, enable semua jam
                    button.disabled = false;
                    button.classList.remove('text-gray-300', 'cursor-not-allowed');
                    button.classList.add('text-[#2196f3]');
                }
            });
        }
    }

    function updateSelectedDatesDisplay() {
        const selectedDatesInfo = document.getElementById('selectedDatesInfo');
        const selectedDatesText = document.getElementById('selectedDatesText');
        
        if (selectedDates.length > 0) {
            selectedDatesInfo.classList.remove('hidden');
            
            if (selectedDates.length === 1) {
                // Single date format
                const dateStr = new Intl.DateTimeFormat('id-ID', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                }).format(selectedDates[0]);
                
                // Add time range for regular package
                if (packageType === 'regular' && selectedTime) {
                    // Parse the selected time and add 30 minutes
                    const [hours, minutes] = selectedTime.split(':');
                    const endTime = new Date(2024, 0, 1, parseInt(hours), parseInt(minutes) + 30);
                    const endTimeStr = endTime.toLocaleTimeString('id-ID', {
                        hour: '2-digit',
                        minute: '2-digit',
                        hour12: false
                    });
                    
                    selectedDatesText.textContent = `${dateStr}, ${selectedTime}-${endTimeStr}`;
                } else {
                    selectedDatesText.textContent = dateStr;
                }
            } else {
                // Date range format
                const startDate = new Intl.DateTimeFormat('id-ID', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                }).format(selectedDates[0]);
                
                const endDate = new Intl.DateTimeFormat('id-ID', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric'
                }).format(selectedDates[selectedDates.length - 1]);
                
                selectedDatesText.textContent = `${startDate} - ${endDate}`;
            }

            // Enable continue button only if time is selected for regular package
            const continueButton = document.getElementById('continueButton');
            if (continueButton) {
                if (packageType === 'regular') {
                    continueButton.disabled = !selectedTime;
                } else {
                    continueButton.disabled = false;
                }
            }
        } else {
            selectedDatesInfo.classList.add('hidden');
            if (continueButton) {
                continueButton.disabled = true;
            }
        }
    }

    // Reset selected time when date changes
    const originalSelectDate = selectDate;
    selectDate = function(date, element) {
        selectedTime = null;
        const timeButtons = document.querySelectorAll('#timeSlots button');
        timeButtons.forEach(button => {
            button.classList.remove('bg-[#2196f3]', 'text-white', 'selected');
        });
        originalSelectDate(date, element);
    }

    window.selectTime = function(time, element) {
        // Remove previous selection
        const previousSelection = document.querySelector('#timeSlots .selected');
        if (previousSelection) {
            previousSelection.classList.remove('bg-[#2196f3]', 'text-white', 'selected');
            previousSelection.classList.add('text-[#2196f3]');
        }

        // Add new selection
        element.classList.remove('text-[#2196f3]');
        element.classList.add('bg-[#2196f3]', 'text-white', 'selected');
        selectedTime = time;

        // Format waktu HH:mm
        const timeInput = document.getElementById('selectedTimeInput');
        timeInput.value = time;
        timeInput.setAttribute('value', time);
        console.log('Time input after set:', timeInput.value);
        
        updateSelectedDatesDisplay();
        updateContinueButton();
    }

    function updateContinueButton() {
        const continueButton = document.getElementById('continueButton');
        if (continueButton) {
            if (packageType === 'regular') {
                // Untuk paket regular: butuh tanggal DAN jam
                continueButton.disabled = !(selectedDates.length > 0 && selectedTime);
            } else {
                // Untuk paket lain: hanya butuh tanggal
                continueButton.disabled = !(selectedDates.length > 0);
            }
        }
    }

    prevMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate);
    });

    nextMonthButton.addEventListener('click', () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate);
    });

    // Initial render
    renderCalendar(currentDate);
    
    // Disable continue button initially
    document.getElementById('continueButton').disabled = true;

    // Disable semua time slots di awal
    const timeButtons = document.querySelectorAll('#timeSlots button');
    timeButtons.forEach(button => {
        button.disabled = true;
        button.classList.remove('text-[#2196f3]');
        button.classList.add('text-gray-300', 'cursor-not-allowed');
    });

    // Tambahkan validasi sebelum form submit
    document.querySelector('#scheduleForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const dateInput = document.getElementById('selectedDateInput');
        const timeInput = document.getElementById('selectedTimeInput');
        
        // Buat FormData baru dan tambahkan nilai secara manual
        const formData = new FormData();
        formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);
        formData.append('selectedDate', dateInput.value);
        if (timeInput) {
            formData.append('selectedTime', timeInput.value);
        }
        
        // Debug formData
        console.log('Form data contents:');
        for (let pair of formData.entries()) {
            console.log(pair[0] + ': ' + pair[1]);
        }
        
        try {
            const response = await fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (response.ok) {
                console.log('Data berhasil dikirim!');
                window.location.href = response.url; // Redirect ke URL yang dikembalikan
            } else {
                console.error('Gagal mengirim data:', response.statusText);
                alert('Terjadi kesalahan saat mengirim data');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Terjadi kesalahan');
        }
    });

    // Tambahkan fungsi untuk debug saat halaman dimuat
    console.log('Form elements on load:');
    console.log('Date input:', document.getElementById('selectedDateInput'));
    console.log('Time input:', document.getElementById('selectedTimeInput'));
});

// Tambahkan fungsi untuk mengecek apakah sebuah jam sudah lewat
function isTimeSlotPassed(hour) {
    const now = new Date();
    return hour <= now.getHours();
}