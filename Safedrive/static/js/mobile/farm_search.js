const searchField = document.getElementById('farmSearch')
const itemInit = document.getElementById("trip-init")
const itemOutput = document.getElementById("trip-container-output")
const itemBody = document.getElementById("trip-output")
itemOutput.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/farm-search", {
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
                                        <h3>${item.farm_name}</h3>
                                        <p>Account: ${item.company__company_name}</p>
                                        <p>Address: ${item.address_line_1} ${item.address_line_2} ${item.city} ${item.province} ${item.zip_code}</p>
                                        <p>Distance: ${item.distance}</p>
                                    </div>
                                    <div class="col-3 justify-content-center" id="action-cont">
                                        <div class="view-item" id="superuser-view-item">
                                            <div class="row">
                                                <div class="col-6 justify-content-center" id="view">
                                                    <a class="btn" href="../superuser-farms/frm${item.id}"><i class="fa-solid fa-pen-to-square"></i></a>
                                                </div>
                                                <div class="col-6 justify-content-center" id="delete">
                                                    <a class="btn" href="../superuser-farms/delete/frm${item.id}"><i class="fa-solid fa-trash-can"></i></a>
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