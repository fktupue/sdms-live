const searchField = document.getElementById('truckSearch')
const itemInit = document.getElementById("trip-init")
const itemOutput = document.getElementById("trip-container-output")
const itemBody = document.getElementById("trip-output")
itemOutput.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/truck-search", {
            body: JSON.stringify({textSearch: searchValue}),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                itemInit.style.display = 'none';
                itemOutput.style.display = 'block';

                if(data.length === 0) {
                    itemBody.style.display = 'block'
                    itemBody.innerHTML= `
                    <h6> No results found </h6>
                    `
                }
                else {
                    data.forEach(item => {
                        itemBody.innerHTML += `
                        <div class="trip-item" id="trip-item">
                            <div class="item-wrapper" id="item-wrapper">
                                <div class="row">
                                    <div class="col-9 justify-content-center">
                                        <h3>${item.plate_number}</h3>
                                        <p>Company: ${item.company__company_name}</p>
                                        <p>Driver: ${item.driver__first_name} ${item.driver__last_name}</p>
                                        <p>Classification: ${item.truck_classification}</p>
                                        <p>Capacity: ${item.capacity}</p>
                                    </div>
                                    <div class="col-3 justify-content-center" id="action-cont">
                                        <div class="view-item" id="superuser-view-item">
                                            <div class="row">
                                                <div class="col-6 justify-content-center" id="view">
                                                    <a class="btn" href="../superuser-trucks/truck${item.id}"><i class='bx bxs-edit'></i></a>
                                                </div>
                                                <div class="col-6 justify-content-center" id="delete">
                                                    <a class="btn" href="../superuser-trucks/delete/truck${item.id}"><i class='bx bx-trash'></i></a>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        `
                    });
                }

            });
    }
    else {
        
        itemInit.style.display = 'block';
        itemOutput.style.display = 'none';
    }
});