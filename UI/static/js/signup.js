document.getElementById('yipy').addEventListener('submit', addUser);
const url = 'http://127.0.0.1:5003/auth/signup';

function addUser(e) {
    e.preventDefault();

    let first_name = document.getElementById('fname').value;
    let last_name = document.getElementById('lname').value;
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password = document.getElementById('password1').value;
    let password2 = document.getElementById('password2').value;


    let data = {
        first_name: first_name,
        last_name: last_name,
        username: username,
        email: email,
        password: password,
        password2: password2
    }
    console.log(data)
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            console.log(response);
        })
};