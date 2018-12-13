function logOut() {
    localStorage.setItem("access_token", '');
    localStorage.setItem("user", '');
    window.history.forward();
}
