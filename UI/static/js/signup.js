document.getElementById('yipy').addEventListener('submit', addUser);
const url = 'https://joelweek2.herokuapp.com/auth/signup';

function addUser(e) {
    e.preventDefault();

    let first_name = document.getElementById('fname').value;
    let last_name = document.getElementById('lname').value;
    let username = document.getElementById('username').value;
    let email = document.getElementById('email').value;
    let password1 = document.getElementById('password1').value;
    let password2 = document.getElementById('password2').value;

    if (password1 === password2) {
        password = password1
    } else {
        alert('Passwords do not match')
    }

    let data = {
        first_name: first_name,
        last_name: last_name,
        username: username,
        email: email,
        password : password 
    }
    // console.log(data)
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            console.log((response.message))
            if ((response.message).includes('registered.')) {
                window.location.href = 'index.html';
                console.log((response.message))
            } else {
                alert(response.message);
            }
        })
};