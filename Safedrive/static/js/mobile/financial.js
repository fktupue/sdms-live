const date = new Date();
const renderFinancialReport = () => {
    date.setDate(1);
    const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const totalsFinancialData = document.getElementById("financial-overview")
    const clientFinancialData = document.getElementById("client-breakdown-wrapper");
    const driverFinancialData = document.getElementById("driver-breakdown-wrapper");

    document.querySelector("#header h2").innerHTML = "Financial Report - " + months[date.getMonth()] + " " + date.getFullYear();
    fetch("/totals-financial-data", {
        body: JSON.stringify({yearValue: date.getFullYear(), monthValue: (date.getMonth() + 1)}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((data) => {
            if(data.length === 0) {
                totalsFinancialData.innerHTML=``
                totalsFinancialData.innerHTML= `
                <div class="financial-trips" id="financial-trips">
                    <h4>Total Trips: 0</h4>
                    <p>In Progress: 0</p>
                    <p>Completed: 0</p>
                </div>
                <div class="financial-bags" id="financial-bags">
                    <h4>Total Bags: 0</h4>
                    <p>In Progress: 0</p>
                    <p>Completed: 0</p>
                </div>
                <div class="bag-count" id="bag-count-home">
                    <h3>Php 0.00</h3>
                    <h4>total receivables</h4>
                </div>
                `
            }
            else {
                totalsFinancialData.innerHTML=``
                totalsFinancialData.innerHTML += `
                <div class="financial-trips" id="financial-trips">
                    <h4>Total Trips: ${data.total_trips}</h4>
                    <p>In Progress: ${data.active_trips}</p>
                    <p>Completed: ${data.completed_trips}</p>
                </div>
                <div class="financial-bags" id="financial-bags">
                    <h4>Total Bags: ${data.total_bags}</h4>
                    <p>In Progress: ${data.active_bags}</p>
                    <p>Completed: ${data.completed_bags}</p>
                </div>
                <div class="bag-count" id="bag-count-home">
                    <h3>Php ${data.total_receivables}</h3>
                    <h4>total receivables</h4>
                </div>
                `
            }

        });

    fetch("/client-financial-data", {
        body: JSON.stringify({yearValue: date.getFullYear(), monthValue: (date.getMonth() + 1)}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((cdata) => {
            if(cdata.length === 0) {
                clientFinancialData.innerHTML=``
                clientFinancialData.innerHTML= `
                <div class="error-container" id="error-container">
                    <h6> No data found </h6>
                </div>
                `
            }
            else {
                clientFinancialData.innerHTML=``
                cdata.forEach(item => {
                    clientFinancialData.innerHTML += `
                    <div class="client-breakdown" id="client-breakdown">
                        <div class="row">
                            <div class="col-7 justify-content-center">
                                <h4>${item.client__company_name}</h4>
                            </div>
                            <div class="col-5 justify-content-center" id="add-item-cont">
                                <a href="../financialreport-download/cl${item.client__id}-${item.trip_month}-${item.trip_year}" id="button-link"><button type='btn' class= 'new-item' id="new-item">Download</button></a>
                            </div>
                        </div>
                        <p>Total Trips: ${item.trip_inprogress + item.trip_completed}</p>
                        <p>Total Bags: ${item.bag_count}</p>
                        <p>Receivables: Php ${((parseFloat(item.base_rate) + parseFloat(item.rate_adjust)).toFixed(2)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</p>
                    </div>
                    `
                });
            }

        });

    fetch("/driver-financial-data", {
        body: JSON.stringify({yearValue: date.getFullYear(), monthValue: (date.getMonth() + 1)}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((ddata) => {
            if(ddata.length === 0) {
                driverFinancialData.innerHTML=``
                driverFinancialData.innerHTML= `
                <div class="error-container" id="error-container">
                    <h6> No data found </h6>
                </div>
                `
            }
            else {
                driverFinancialData.innerHTML=``
                ddata.forEach(item => {
                    driverFinancialData.innerHTML += `
                    <div class="driver-breakdown" id="driver-breakdown">
                        <div class="row">
                            <div class="col-5 justify-content-center" id="pfp-col">
                                <div class="pfp-wrapper" id="pfp-wrapper">
                                    <img src="https://res.cloudinary.com/project-99-sdms/image/upload/v1/${item.driver__profile_pic}">
                                </div>
                            </div>
                            <div class="col-7 justify-content-center" id="det-col">
                                <div class="details-wrapper">
                                    <h4>${item.driver__first_name} ${item.driver__last_name}</h4>
                                    <p>Total Trips: ${item.trip_count}</p>
                                    <p>Total Bags: ${item.bag_count}</p>
                                    <p>Driver Basic: Php ${item.driver_basic}.00</p>
                                    <p>Driver Additional: Php ${item.driver_additional}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    `
                });
            }

        });
}

document.querySelector(".prev").addEventListener('click', () => {
    date.setMonth(date.getMonth() - 1);
    renderFinancialReport();
})

document.querySelector(".next").addEventListener('click', () => {
    date.setMonth(date.getMonth() + 1);
    renderFinancialReport();
})

renderFinancialReport();