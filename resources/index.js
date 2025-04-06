function loginButton() {
    var username = document.getElementById("Username");
    var password = document.getElementById("Password");

    fetch('/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Response:', data);
            if(data["token"] != null){
                console.log("Password Correct!");
                window.location.href = "/chat";
                document.cookie = `token=${data["token"]}`;
            } else {
                console.log(data["error"]);
                title = document.getElementById("Title");
                title.innerText = data["error"]
                title.style.color = "red";

            }
        })
        .catch(error => {
            console.error('Request failed:', error);
        });

}

function getCookie(name) {
    const cookies = document.cookie.split(';');

    // Loop through each cookie
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim(); 

        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1); 
        }
    }

    return null;
}

console.log(getCookie("token"));