const searchField = document.getElementById('truckSearch')
const itemInit = document.getElementById("item-container")
const itemOutput = document.getElementById("item-container-output")
const itemBody = document.getElementById("item-body")
itemOutput.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/truck-search", {
            body: JSON.stringify({textSearch: searchValue}),
            method: "POST",
        },
        )
            .then((res) => res.json())
            .then((data) => {
                itemInit.style.display = 'none';
                itemOutput.style.display = 'block';

                if(data.length === 0) {
                    itemBody.innerHTML= `
                    <div class="label-cont" id="lbl-cont"><h6> No results found </h6></div>
                    `
                }
                else {
                    data.forEach(item => {
                        itemBody.innerHTML += `
                        <div class="item-v2">
                            <div class="row">
                                <div class="col-4 justify-content-center">
                                    <h1 id="plate-number-label">${item.plate_number}</h1>
                                </div>
                                <div class="col-6 justify-content-center" id="truck-data-cont">
                                    <div class="row">
                                        <div class="col-5 justify-content-center">
                                            <h3>Classification: ${item.truck_classification}</h3>
                                            <h2>Capacity: ${item.capacity}</h2>
                                        </div>
                                        <div class="col-7 justify-content-center">
                                            <h3>Company: ${item.company__company_name}</h3>
                                            <h2>Driver: ${item.driver__first_name} ${item.driver__last_name}</h2>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-2 justify-content-center">
                                    <div class="row" id="truck-action-cont">
                                        <div class="col-6 justify-content-center">
                                            <div class="view-item">
                                                <a class="btn" href="../superuser-trucks/truck${item.id}"><i class="fa-solid fa-pen-to-square"></i></a>
                                            </div>
                                        </div>
                                        <div class="col-6 justify-content-center">
                                            <div class="delete-item">
                                                <a class="btn" href="../superuser-trucks/delete/truck${item.id}/"><i class="fa-solid fa-trash-can"></i></a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>        
                        </div>
                        `
                        //itemOutput.innerHTML=""
                    });
                }

            });
    }
    else {
        
        itemInit.style.display = 'block';
        itemOutput.style.display = 'none';
    }
});