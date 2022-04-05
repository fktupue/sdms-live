const searchField = document.getElementById('tripSearch')
const itemInit = document.getElementById("trip-init")
const itemOutput = document.getElementById("trip-table-output")
const itemBody = document.getElementById("driver-trip-body-output")
const tableError = document.getElementById("table-error")
itemOutput.style.display = 'none'
tableError.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/driver-trip-search", {
            body: JSON.stringify({textSearch: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                itemInit.style.display = 'none';
                itemOutput.style.display = 'block';

                if(data.length === 0) {
                    tableError.style.display = 'block'
                    tableError.innerHTML= `
                    <h6> No results found </h6>
                    `
                }
                else {
                    data.forEach(item => {
                        itemBody.innerHTML += `
                        <tr>
                            <td id="table-body" data-heading="Ref No.">${item.ref_num}</td>
                            <td id="table-body" data-heading="Farm">${item.farm__farm_name}</td>
                            <td id="table-body" data-heading="Bags Delivered">${item.bag_count}</td>
                            <td id="table-body" data-heading="Trip Date">${item.trip_date}</td>
                            <td id="table-body" data-heading="Trip Status">${item.trip_status}</td>
                            <td id="table-body" data-heading="Action">
                                <a href="../driver-trips/${item.id}" class="table-edit-btn" id="driver-view-edit-btn">
                                    <i class="fa-solid fa-eye"></i>
                                </a>
                            </td>
                        </tr>
                        `
                        tableError.innerHTML=""
                    });
                }

            });
    }
    else {
        
        itemInit.style.display = 'block';
        itemOutput.style.display = 'none';
        tableError.style.display = 'none';
    }
});