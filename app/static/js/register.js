function getDate(event) {
    event.preventDefault(); // Prevent form submission

    var error_msg = document.getElementById('error_msg');
    var success_msg = document.getElementById('success_msg');

    // Capture form inputs
    var name = document.getElementById('name').value.trim();
    var name2 = document.getElementById('name2').value.trim();
    var name3 = document.getElementById('name3').value.trim();
    var email = document.getElementById('email').value.trim();
    var pass1 = document.getElementById('password').value.trim(); // Fixed ID
    var confirmPassword = document.getElementById('confirmPassword').value.trim();
    var gender = document.querySelector('input[name="gender"]:checked');
    var educationSelect = document.querySelector('select[name="education"]');

    // Validation
    if (name === "" || name2 === "" || name3 === "") {
        displayError("Fadlan buuxi dhammaan magacyada.");
        return;
    }

    if (name.length < 3 || name2.length < 3 || name3.length < 3) {
        displayError("Magacyadu waa inay ugu yaraan ahaadaan 3 xaraf.");
        return;
    }

    if (email === "") {
        displayError("Fadlan geli email-kaaga.");
        return;
    }

    if (pass1 === "" || confirmPassword === "") {
        displayError("Fadlan geli sirta iyo xaqiijinta sirta.");
        return;
    }

    if (pass1 !== confirmPassword) {
        displayError("Fadlan xaqiiji in labada sir ah is waafaqayaan.");
        return;
    }

    if (!gender) {
        displayError("Fadlan dooro jinsigaaga.");
        return;
    }

    if (educationSelect.value === "") {
        displayError("Fadlan dooro heerka waxbarasho.");
        return;
    }

    // Hide error messages
    error_msg.style.display = 'none';

    // Convert data into an object
    var data = {
        name: name,
        name2: name2,
        name3: name3,
        email: email,
        pass1: pass1,
        confirmPassword: confirmPassword,
        gender: gender.value,
        educationSelect: educationSelect.value
    };

    console.log('Here is the sign-up data: ', data);

    // Sending the data using fetch (API)
    fetch('/design', {
        method: 'POST',
        credentials: 'include',
        body: JSON.stringify(data),
        cache: 'no-cache',
        headers: new Headers({
            'Content-Type': 'application/json'
        })
    })
    .then(response => {
        if (response.status !== 200) {
            console.log(`Response status not 200: ${response.status}`);
            alert("Khalad dhacay, laxiriir maamulka.");
            return;
        }
        return response.json();
    })
    .then(info => {
        if (info.status === 'success') {
            success_msg.style.display = 'block';
            success_msg.innerHTML = info.message;
            setTimeout(() => {
                window.location.href = "/log_in";
            }, 4000);
        } else {
            displayError(info.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        displayError("Khalad ayaa dhacay, fadlan isku day mar kale.");
    });

    // Helper function to display error messages
    function displayError(message) {
        success_msg.style.display = 'none';
        error_msg.style.display = 'block';
        error_msg.innerHTML = message;
    }
}
