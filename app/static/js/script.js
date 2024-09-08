// Function to fetch the token from the get_token endpoint
const fetchToken = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_token', {
            method: 'GET',
            credentials: 'include',  // Include cookies in the request
        });

        const tokenData = await response.json();

        if (tokenData.token) {
            document.getElementById('token_input').value = tokenData.token;
            document.getElementById('token_display').value = tokenData.token;
        } else {
            document.getElementById('token_display').innerText = 'Failed to fetch token';
        }
    } catch (error) {
        document.getElementById('token_display').innerText = 'Error fetching token';
        console.error('Error fetching token:', error);
    }
};

// Function to verify token
const verifyToken = async () => {
    try {
        const token = document.getElementById('token_input').value;
        const response = await fetch('http://127.0.0.1:5000/verify_token', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        document.getElementById('verify_result').innerHTML = formatVerificationResult(data);
    } catch (error) {
        document.getElementById('verify_result').innerText = 'Error verifying token';
        console.error('Error verifying token:', error);
    }
};

// Function to refresh token
const refreshToken = async () => {
    try {
        const token = document.getElementById('token_input').value;
        const response = await fetch('http://127.0.0.1:5000/refresh_token', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        const data = await response.json();
        document.getElementById('refresh_result').innerHTML = formatRefreshResult(data);
        if (data.token) {
            document.getElementById('token_input').value = data.token;
            document.getElementById('token_display').value = data.token;
        }
    } catch (error) {
        document.getElementById('refresh_result').innerText = 'Error refreshing token';
        console.error('Error refreshing token:', error);
    }
};

// Format the verification result for better readability
const formatVerificationResult = (data) => {
    if (data && data.data) {
        const { exp, user_id } = data.data;
        const expirationDate = new Date(exp * 1000).toLocaleString();
        return `<strong>User ID:</strong> ${user_id}<br>
                <strong>Expiration Date:</strong> ${expirationDate}`;
    }
    return 'Invalid verification result';
};

// Format the refresh result for better readability
const formatRefreshResult = (data) => {
    if (data && data.message) {
        return `<strong>Message:</strong> ${data.message}`;
    }
    return 'Invalid refresh result';
};

// Add event listeners to buttons
document.getElementById('fetch_token_button').addEventListener('click', fetchToken);
document.getElementById('verify_token_button').addEventListener('click', verifyToken);
document.getElementById('refresh_token_button').addEventListener('click', refreshToken);
