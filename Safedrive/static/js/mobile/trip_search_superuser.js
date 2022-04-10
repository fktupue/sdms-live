const searchField = document.getElementById('tripSearch')
const itemInit = document.getElementById("trip-init")
const itemOutput = document.getElementById("trip-container-output")
const itemBody = document.getElementById("trip-output")
itemOutput.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/trip-search", {
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
                                        <h3>${item.ref_num}</h3>
                                        <p>Farm: ${item.farm__farm_name}</p>
                                        <p>Trip Date: ${item.trip_date}</p>
                                        <p>Bag Count: ${item.bag_count}</p>
                                    </div>
                                    <div class="col-3 justify-content-center" id="superuser-action-cont">
                                        <div class="view-item" id="superuser-view-item">
                                            <div class="row">
                                                <div class="col-6 justify-content-center" id="view">
                                                    <a class="btn" href="../superuser-home/edit${item.id}"><i class="fa-solid fa-pen-to-square"></i></a>
                                                </div>
                                                <div class="col-6 justify-content-center" id="view">
                                                    <a class="btn" href="../superuser-home/delete${item.id}"><i class="fa-solid fa-trash-can"></i></a>
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