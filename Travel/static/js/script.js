
fetch('http://127.0.0.1:5000/register', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ 
        username: "JohnDoe", 
        email: "john@example.com", 
        password: "securepassword", 
        confirm: "securepassword" 
    })
})
.then(response => {
    if (response.ok) {
        return response.json(); // Parse JSON response if successful
    } else {
        throw new Error('Registration failed'); // Handle errors
    }
})
.then(data => {
    console.log(data);
    // Redirect to sign-in page after successful registration
    window.location.href = 'http://127.0.0.1:5000/signin'; // Adjust the URL as necessary
})
.catch(error => console.error('Error:', error));

