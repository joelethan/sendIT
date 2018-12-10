window.addEventListener('load', checkUser);

function checkUser(e) {
    e.preventDefault();
    if (localStorage.getItem("access_token") === '') {
        window.location.href = 'index.html';
    }
    document.querySelector('#user').innerHTML = localStorage.getItem("user");
        }