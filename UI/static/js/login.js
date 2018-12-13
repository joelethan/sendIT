document.getElementById('yipy').addEventListener('submit', addUser);
const url = 'https://joelweek2.herokuapp.com/auth/login';

function addUser(e) {
    e.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password1').value;


    let data = {
        username: username,
        password: password
    }
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            if ((response.message).includes('successful')) {
                window.location.href = 'order.html';
                localStorage.setItem("access_token", response.token);
                localStorage.setItem("user", response.user);
                // alert(response.user)
            } else {
                alert(response.message);             
            }
        })
};