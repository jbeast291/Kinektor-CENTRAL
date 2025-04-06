var isCreated = false;

function createAccount() {
    if(isCreated){
        window.location.href = "/";
    }
    var username = document.getElementById("Username");
    var password = document.getElementById("Password");
    var minecratUUID = document.getElementById("MCUUUID");
    var discordID = document.getElementById("DiscordID");
    
    var title = document.getElementById("Title");

    if (username.value === "" || password.value === "" || minecratUUID.value === "" || discordID.value === "") {
        title.innerText = "Fill In All Boxes";
        title.style.color = "red";
        return;
    }


    fetch('/auth/createAccout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
            minecratUUID: minecratUUID.value,
            discordID: discordID.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);
            if(data["success"] != null){
                console.log("Account Created!");
                
                title.innerText = "Account Created!";
                title.style.color = "green";
                var button = document.getElementById("createAccountButton");
                button.style.backgroundColor = "rgb(32, 171, 41)";
                button.innerText = "Return Home"
                isCreated = true;
            } else {
                title.innerText = data["error"]
                title.style.color = "red";
            }
        })
        .catch(error => {
            console.error('Request failed:', error);
        });

}