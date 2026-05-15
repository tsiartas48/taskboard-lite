const API_URL = 'http://127.0.0.1:8000';

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

async function apiCall(endpoint, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    const response = await fetch(`${API_URL}${endpoint}`, options);

    if (response.status === 401) {
        removeToken();
        window.location.href = 'index.html';
        return;
    }

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Something went wrong');
    return data;
}

function checkAuth() {
    if (!getToken()) {
        window.location.href = 'index.html';
    }
}

function logout() {
    removeToken();
    window.location.href = 'index.html';
}