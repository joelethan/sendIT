window.addEventListener('load', addUser);
const url = 'http://127.0.0.1:5003/api/v1/parcels';

function addUser(e) {
    e.preventDefault();



    fetch(url, {

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
                    <td>${parcel.user_id}</td>
                    <td>${parcel.pickup_location}</td>
                    <td>
                        ${tah}
                    </td>
                    <td>
                        <input type="text" onblur="updateDestination(event,${parcel.parcel_id});" value="${parcel.destination}">
                    </td>
                    <td>${parcel.weight}</td>
                    <td>${parcel.status}</td>
                    <td>
                        <select id="mySelect" onchange="updateStatus(event,${parcel.parcel_id});">
                            <option value="New">status</option>
                            <option value="New">New</option>
	                        <option value="intransit">In-transit</option>
	                        <option value="cancelled">Cancelled</option>
	                        <option value="delivered">Delivered</option>
                        </select>
                    </td>
                    <td><button onclick="viewbtn(${parcel.parcel_id});">View</button></td>
                </tr>`;
            });

            document.querySelector('tbody').innerHTML = output;
        })
    };
function updateDestination(e, id) {
    new_dest = e.target.value;
    id = id;
    console.log(new_dest);


    let data = {
        destination: new_dest
    }
    let order_id = id

    let url = `http://127.0.0.1:5003/api/v1/parcels/${order_id}/destination`;
    fetch(url, {
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
                alert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Parcel destination Updated to')) {
            } else {
                alert(response.message);
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

    let url = `http://127.0.0.1:5003/api/v1/parcels/${order_id}/presentLocation`;
    fetch(url, {
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
                alert('You have been logged out. Please login again');
                window.location.href = 'index.html';
            }
            if ((response.message).includes('Parcel present location Updated to')) {
            } else {
                alert(response.message);
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

    let url = `http://127.0.0.1:5003/api/v1/parcels/${order_id}/status`;
    fetch(url, {
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
            // alert('You have been logged out. Please login again');
            window.location.href = 'index.html';
        }
        if ((response.message).includes('Parcel status Updated to')) {
        } else {
            alert(response.message);
            window.location.reload()
        }
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

    let url = `http://127.0.0.1:5003/api/v1/parcels/${id}`;
    fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`
        }
    })
        .then(res => res.json())
        .then(data => {
            // alert(id)
            alert(data.Order.destination)
            // alert(data.message)
            if (data.msg) {
                window.location.href = 'index.html';
            }
        })
};

var order = document.getElementById('myOrder');

var span = document.getElementById("close");

span.onclick = function () {
    order.style.display = "none";
}

window.onclick = function (event) {
    if (event.target == order) {
        order.style.display = "none";
    }
}