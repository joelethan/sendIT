window.addEventListener('load', getParcel);
// const url = ;

function getParcel(e) {
    e.preventDefault();



    fetch('https://joelweek2.herokuapp.com/api/v1/parcels', {

        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        }
    })
        .then(res => res.json())
        .then(data => {
            let output = ''
            if (data.msg) {
                window.location.href = 'index.html';
            }
            data.Orders.forEach(function (parcel) {
                let tah = `<input type="text" onblur="updatePresentLocal(event,${parcel.parcel_id});" value="${parcel.present_location}">`
                output += `
                <tr>
                    <td>${parcel.parcel_id}</td>
                    <td>${parcel.username}</td>
                    <td>
                        ${tah}
                    </td>

                    
                    
                    <td><button onclick="viewbtn(${parcel.parcel_id});">View</button></td>
                </tr>`;
            });

            document.querySelector('#all_orders').innerHTML = output;
        })
    };
function updateDestination(e, id) {
    new_dest = e.target.value;
    // id = id;
    // console.log(new_dest);


    let data = {
        destination: new_dest
    }
    let order_id = id

    // let url = ;
    fetch(`https://joelweek2.herokuapp.com/api/v1/parcels/${order_id}/destination`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            if (response.msg) {
                // aelert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Parcel destination Updated to')) {
            } else {
                // aelert(response.message);
                window.location.reload()
            }
        })
    };
function updatePresentLocal(e, id) {
    new_location = e.target.value;
    id = id;
    console.log(new_location);


    let data = {
        present_location: new_location
    }
    let order_id = id

    // let url = ;
    fetch(`https://joelweek2.herokuapp.com/api/v1/parcels/${order_id}/presentLocation`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(data)
    })
        .then(res => res.json())
        .then(response => {
            if (response.msg) {
                // aelert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Parcel present location Updated to')) {
            } else {
                // aelert(response.message);
                window.location.reload()
            }
        })
    };

function updateStatus(e, id) {
    new_status = e.target.value;
    id = id;
    console.log(id);
    console.log(new_status);
    window.location.reload()

    let data = {
        status: new_status
    }
    let order_id = id

    // let url = ;
    fetch(`https://joelweek2.herokuapp.com/api/v1/parcels/${order_id}/status`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(data => {
        // aelert(data.message);
        // if (response.msg) {
            // aelert('You have been logged out. Please login again');
            // window.location.href = 'index.html';
        // }
        // if ((response.message).includes('Parcel status Updated to')) {
        // } else {
            // aelert(response.message);
            // window.location.reload()
        // }
    })
};

function viewbtn(id) {
    console.log(id);
    order.style.display = "block";
    // new_status = e.target.value;
    // id = id;
    // console.log(id);
    // console.log(new_status);
    // window.location.reload()

    // let data = {
    //     status: new_status
    // }
    // let order_id = id

    // let url = ;
    fetch(`https://joelweek2.herokuapp.com/api/v1/parcels/${id}`, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        }
    })
        .then(res => res.json())
        .then(data => {
            if (data.msg) {
                window.location.href = 'index.html';
            } output = `
                    <tr>
                        <p><td>Order ID: </td>
                        <td>${data.Order.parcel_id}</td></p>
                    </tr>
                    <tr>
                        <p><td>Username: </td>
                        <td>${data.Order.username}</td></p>
                    </tr>
                    <tr>
                        <td>Pick-up Location: </td><br>
                        <td>${data.Order.pickup_location}</td><br>
                    </tr>
                    <tr>
                        <td>Present Location: </td><br>
                        <td>${data.Order.present_location}</td><br>
                    </tr>
                    <tr>
                        <td>Delivery Location: </td><br>
                        <td><input type="text" onblur="updatePresentLocal(event,${parcel.parcel_id});" value="${data.Order.destination}"></td><br>
                    </tr>
                    <tr>
                        <td>Order Status: </td><br>
                        <td>${data.Order.status}</td><br>
                    </tr>
                    <tr>
                        <td>Created On: </td><br>
                        <td>${data.Order.date}</td><br>
                    </tr>`

            document.querySelector('#one_order').innerHTML = output;
        })
};

var order = document.getElementById('myOrder');

var span = document.getElementById("close");

span.onclick = function () {
    window.location.reload();
    order.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == order) {
        window.location.reload();
        order.style.display = "none";
    }
}

document.getElementById('yipy').addEventListener('submit', placeOrder);
// const url = ;

function placeOrder(e) {
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
    fetch('https://joelweek2.herokuapp.com/api/v1/parcels', {
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
                // aelert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Order placed')) {
                // aelert(response.message)
                // aelert(response.Order.parcel_id)
                viewbtn(response.Order.parcel_id)
            } else {
                // aelert(response.message);
            }
        })
};