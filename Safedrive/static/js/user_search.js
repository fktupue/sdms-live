const searchField = document.getElementById('userSearch')
const itemInit = document.getElementById("item-container")
const itemOutput = document.getElementById("item-container-output")
const itemBody = document.getElementById("item-body")
itemOutput.style.display = 'none'

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;
    
    if(searchValue.trim().length>0){
        itemBody.innerHTML = "";
        fetch("/user-search", {
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
                        <div class="col-6 justify-content-center">
                            <div class="user">
                                <div class="row">
                                    <div class="col-4 justify-content-center">
                                        <div class="prof-pic-wrapper">
                                            <img src="https://res.cloudinary.com/project-99-sdms/image/upload/v1/${item.profile_pic}">
                                        </div>
                                    </div>
                                    <div class="col-8 justify-content-center">
                                        <div class="row">
                                            <div class="col-8 justify-content-center">
                                                <h1>${item.first_name} ${item.last_name}</h1>
                                            </div>
                                            <div class="col-4 justify-content-center">
                                                <div class="user-action-cont" id="user-action-cont">
                                                    <div class="viewusercnt" href="#">
                                                        <button type='button' class= 'view-user' onclick="location.href='superuser-users/user${item.id}'"><i class="fa-solid fa-pen-to-square"></i></i></button>
                                                    </div>
                                                    <div class="viewusercnt" href="#">
                                                        <button type='button' class= 'view-user' onclick="location.href='superuser-users/delete/user${item.id}'"><i class="fa-solid fa-trash-can"></i></button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <h2>Account Role: ${item.user__groups__name}</h2>
                                        <h2>Contact Number: ${item.contact_number}</h2>
                                        <h2>Email Address: ${item.email_address}</h2>
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