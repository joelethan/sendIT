// window.addEventListener('load', checkUser);
// function checkUser() {
//     alert(localStorage.getItem("access_token"))
// }
document.getElementById('yipy').addEventListener('submit', addUser);
const url = 'https://joelweek2.herokuapp.com/api/v1/parcels';

function addUser(e) {
    e.preventDefault();

    let pickup_location = document.getElementById('pickup').value;
    let destination = document.getElementById('destination').value;
    let weight = document.getElementById('weight').value;


    let data = {
        pickup_location: pickup_location,
        present_location: pickup_location,
        destination: destination,
        weight: parseFloat(weight)
    }
    console.log(data)
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            if (response.msg) {
                alert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Order placed')) {
                alert(response.message)
                window.location.reload();
            } else {
                alert(response.message);
            }
        })
};