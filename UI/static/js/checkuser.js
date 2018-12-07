window.addEventListener('load', checkUser);

function checkUser(e) {
    e.preventDefault();
    if (localStorage.getItem("access_token") === 'loggedout') {
        window.location.href = 'index.html';
    }

        }