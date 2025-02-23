function validateForm() {
    let email = document.getElementById("email").value.trim();
    let password = document.getElementById("password").value.trim();

    if (email === "" || password === "") {
        alert("Please fill in both email and password.");
        return false;
    }

    return true;
}

function showGlobalAlert(message, type) {
    $('#globalAlert')
        .stop(true, true)
        .removeClass('alert-success alert-warning alert-danger text-success text-danger text-warning')
        .addClass(`alert alert-${type} text-${type}`)
        .text(message)
        .fadeIn()
        .delay(5000)
        .fadeOut(function () {
            $(this).removeClass('alert-success alert-warning alert-danger text-success text-danger text-warning'); // Remove all alert classes
        });
}