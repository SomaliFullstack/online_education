async function getDate(event) {
    event.preventDefault(); // Prevent form submission
    const email = document.getElementById('email');
    console.log(email)
    const pass = document.getElementById('password');
    const error_msg = document.getElementById('error_msg');
    const success_msg = document.getElementById('success_msg');

    // Clear messages
    error_msg.style.display = 'none';
    success_msg.style.display = 'none';

    // Input validation
    if (email.value.trim() === '') {
        displayError('Fadlan geli email sax ah.');
        return;
    }

    if (pass.value.trim() === '') {
        displayError('Fadlan geli password sax ah.');
        return;
    }

    // Prepare data to send
    const data = {
        email: email.value,
        password: password.value // Correct key
    };

    try {
        // Fetch data from server
        const response = await fetch('/getinfo', {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json(); // Parse JSON error response
            displayError(errorData.message || 'Waan ka xumahay cilad dhacday.');
            return;
        }

        const responseData = await response.json();

        if (responseData.status === 'success') {
            displaySuccess(responseData.message);
        } else {
            displayError(responseData.message);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        displayError('Waxaa dhacay qalad lama filaan ah.');
    }
}

function displayError(message) {
    const error_msg = document.getElementById('error_msg');
    error_msg.style.display = 'block';
    error_msg.innerHTML = message;
}

function displaySuccess(message) {
    const success_msg = document.getElementById('success_msg');
    success_msg.style.display = 'block';
    success_msg.innerHTML = message;
    setTimeout(() => {
        window.location.href = "/user/user_dashboard"; // Redirect after success
    }, 3000);
}




window.addEventListener("beforeunload", function () {
    const url = "/logout"; // The route for logging out
    navigator.sendBeacon(url); // Send a beacon request to the server to clear the session
    console.log("Logout request sent.");
});
console.log('designer')
