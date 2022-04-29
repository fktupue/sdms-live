const date = new Date();
const renderFinancialReport = () => {
    date.setDate(1);
    const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    const totalsFinancialData = document.getElementById("col1-wrapper")
    const clientFinancialData = document.getElementById("col2-wrapper");
    const driverFinancialData = document.getElementById("col3-wrapper");

    document.querySelector("#financial-report-header h1").innerHTML = "Financial Report - " + months[date.getMonth()] + " " + date.getFullYear();
    fetch("/totals-financial-data", {
        body: JSON.stringify({yearValue: date.getFullYear(), monthValue: (date.getMonth() + 1)}),
        method: "POST",
    })
        .then((res) => res.json())
        .then((data) => {
            if(data.length === 0) {
                totalsFinancialData.innerHTML=``
                totalsFinancialData.innerHTML= `
                <div class="trips">
                    <h3>Total Trips: 0</h3>
                    <h4>In Progress: 0</h4>
                    <h4>Completed: 0</h4>
                </div>
                <div class="bags">
                    <h3>Total Bags: 0</h3>
                    <h4>In Progress: 0</h4>
                    <h4>Completed: 0</h4>
                </div>
                <div class="receivables">
                    <h3>Total Receivables </h3>
                    <h4>Php 0.00 </h4>
                </div>
                `
            }
            else {
                totalsFinancialData.innerHTML=``
                totalsFinancialData.innerHTML += `
                <div class="trips">
                    <h3>Total Trips: ${data.total_trips}</h3>
                    <h4>In Progress: ${data.active_trips}</h4>
                    <h4>Completed: ${data.completed_trips}</h4>
                </div>
                <div class="bags">
                    <h3>Total Bags: ${data.total_bags}</h3>
                    <h4>In Progress: ${data.active_bags}</h4>
                    <h4>Completed: ${data.completed_bags}</h4>
                </div>
                <div class="receivables">
                    <h3>Total Receivables </h3>
                    <h4>Php ${data.total_receivables} </h4>
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
                <h6> No data found </h6>
                `
            }
            else {
                let nf = new Intl.NumberFormat('en-US');
                clientFinancialData.innerHTML=``
                cdata.forEach(item => {
                    clientFinancialData.innerHTML += `
                    <div class="company-financial" id="comp-fin">
                        <div class="row">
                            <div class="col-8 justify-content-center">
                                <h3>${item.client__company_name}</h3>
                            </div>
                            <div class="col-4 justify-content-center">
                                <a href="../financialreport-download/cl${item.client__id}-${item.trip_month}-${item.trip_year}" id="button-link"><button type='button' class= 'indiv-report-btn' id="rep-btn"> Download Report </button></a>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-6 justify-content-center" id="comp-fin-col">
                                <h4>Total Trips: ${item.trip_inprogress + item.trip_completed}</h4>
                                <h5>In Progress: ${item.trip_inprogress}</h5>
                                <h5>Completed: ${item.trip_completed}</h5>
                            </div>
                            <div class="col-6 justify-content-center" id="comp-fin-col2">
                                <h4>Total Bags: ${item.bag_count}</h4>
                                <h4>Total Receivables: </h4>
                                <h5>Php ${((parseFloat(item.base_rate) + parseFloat(item.rate_adjust)).toFixed(2)).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}</h5>
                            </div>
                        </div>
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
                <h6> No data found </h6>
                `
            }
            else {
                driverFinancialData.innerHTML=``
                ddata.forEach(item => {
                    driverFinancialData.innerHTML += `
                    <div class="company-financial" id="driver-fin">
                        <div class="row">
                            <div class="col-4 justify-content-center">
                                <div class="prof-pic-wrapper">
                                    <img src="https://res.cloudinary.com/project-99-sdms/image/upload/v1/${item.driver__profile_pic}">
                                </div>
                            </div>
                            <div class="col-8 justify-content-center">
                                <h3>${item.driver__first_name} ${item.driver__last_name}</h3>
                                <h4>Total Trips: ${item.trip_count}</h4>
                                <h4>Total Bags: ${item.bag_count}</h4>
                                <span><h5>Driver Basic: Php ${item.driver_basic}.00</h5></span>
                                <h4>Driver Additional: Php ${item.driver_additional}</h4>
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