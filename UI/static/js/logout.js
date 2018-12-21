function logOut() {
    localStorage.setItem("access_token", 'loggedout');
    window.history.forward();
}
