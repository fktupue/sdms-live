const date = new Date();
var currentDay = null;
var currentMonth = date.getMonth() + 1
var currentYear = date.getFullYear()
const renderCalendar = () => {
    date.setDate(1);
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const monthDays = document.querySelector("#days");
    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const firstDayIndex = date.getDay();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    const nextDays = 7 - lastDayIndex - 1;
    const calendarItemContainer = document.getElementById("calendar-event-container")

    document.querySelector("#current-month-year h1").innerHTML = months[date.getMonth()] + " " + date.getFullYear();

    let days = "";
    for(let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`
    }
    for(let i = 1; i <= lastDay; i++) {
        if(i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class="today">${i}</div>`;
            window['currentDay'] = i;
        } else {
            days += `<div>${i}</div>`;
        }
        // days += `<div class="">${i}</div>`;
    }
    for(let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
    }
    monthDays.innerHTML = days;

    fetch("/calendar", {
        body: JSON.stringify({yearValue: currentYear, monthValue: currentMonth, dayValue: currentDay}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((data) => {
            // itemInit.style.display = 'none';
            // itemOutput.style.display = 'block';

            if(data.length === 0) {
                calendarItemContainer.innerHTML=``
                calendarItemContainer.innerHTML= `
                <h6> No trips found </h6>
                `
            }
            else {
                calendarItemContainer.innerHTML=``
                data.forEach(item => {
                    calendarItemContainer.innerHTML += `
                    <div class="calendar-item" id="calendar-item">
                        <h3>Reference No. ${item.ref_num}</h3>
                        <p>Farm: ${item.farm__farm_name}</p>
                        <p>Truck: ${item.truck__plate_number} | Driver: ${item.truck__driver__first_name} ${item.truck__driver__last_name}</p>
                    </div>
                    `
                });
            }

        });
}

document.querySelector(".prev").addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
})

document.querySelector(".next").addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
})

// document.querySelector("#days-day").addEventListener('click', () => {
//     var selectedDay = document.querySelector("#days div");
//     selectedDay.classList.add("today");
//     renderCalendar();
// })

renderCalendar();