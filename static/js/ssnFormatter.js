document.addEventListener("DOMContentLoaded", function() {
    const ssnInput = document.getElementById("ssn");

    ssnInput.addEventListener("input", function () {
        let value = ssnInput.value.replace(/\D/g, ""); // Remove all non-digit characters
        if (value.length > 3 && value.length <= 5) {
            value = value.replace(/^(\d{3})(\d{0,2})/, "$1-$2");
        } else if (value.length > 5) {
            value = value.replace(/^(\d{3})(\d{2})(\d{0,4})/, "$1-$2-$3");
        }
        ssnInput.value = value;
    });
});
