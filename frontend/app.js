// ===== API Configuration =====
const API_BASE_URL = 'https://todo-application-y9xb.onrender.com';

// ===== State Management =====
let authToken = localStorage.getItem('token') || null;
let currentUser = JSON.parse(localStorage.getItem('user')) || null;
let allTasks = [];
let filteredTasks = [];
let currentFilter = 'all';

// ===== DOM Elements =====
const authScreen = document.getElementById('authScreen');
const appScreen = document.getElementById('appScreen');
const loginTab = document.getElementById('loginTab');
const signupTab = document.getElementById('signupTab');
const loginForm = document.getElementById('loginForm');
const signupForm = document.getElementById('signupForm');
const loginBtn = document.getElementById('loginBtn');
const signupBtn = document.getElementById('signupBtn');
const logoutBtn = document.getElementById('logout');
const navHome = document.getElementById('navHome');
const navTasks = document.getElementById('navTasks');
const createTaskForm = document.getElementById('createTaskForm');
const tasksList = document.getElementById('tasksList');
const noTasksMessage = document.getElementById('noTasksMessage');
const spinner = document.getElementById('loadingSpinner');
const toast = document.getElementById('toast');
const displayName = document.getElementById('displayName');
const displayEmail = document.getElementById('displayEmail');
const totalTasksEl = document.getElementById('totalTasks');
const completedCountEl = document.getElementById('completedCount');
const pendingCountEl = document.getElementById('pendingCount');

// Filter buttons
const filterAllBtn = document.getElementById('filterAll');
const filterPendingBtn = document.getElementById('filterPending');
const filterCompletedBtn = document.getElementById('filterCompleted');

// ===== Event Listeners =====
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

loginTab.addEventListener('click', () => switchAuthTab('login'));
signupTab.addEventListener('click', () => switchAuthTab('signup'));
loginBtn.addEventListener('click', handleLogin);
signupBtn.addEventListener('click', handleSignup);
logoutBtn.addEventListener('click', handleLogout);
createTaskForm.addEventListener('submit', handleCreateTask);
filterAllBtn.addEventListener('click', () => filterTasks('all'));
filterPendingBtn.addEventListener('click', () => filterTasks('pending'));
filterCompletedBtn.addEventListener('click', () => filterTasks('completed'));
navHome.addEventListener('click', () => {
    navHome.classList.add('active');
    navTasks.classList.remove('active');
});
navTasks.addEventListener('click', () => {
    navTasks.classList.add('active');
    navHome.classList.remove('active');
    loadTasks();
});

// ===== Initialize App =====
function initializeApp() {
    if (authToken && currentUser) {
        showAppScreen();
        loadTasks();
    } else {
        showAuthScreen();
    }
}

// ===== Show/Hide Screens =====
function showAuthScreen() {
    authScreen.style.display = 'block';
    appScreen.style.display = 'none';
    logoutBtn.style.display = 'none';
}

function showAppScreen() {
    authScreen.style.display = 'none';
    appScreen.style.display = 'block';
    logoutBtn.style.display = 'block';
    updateUserProfile();
}

// ===== Auth Tab Switching =====
function switchAuthTab(tab) {
    if (tab === 'login') {
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
        loginForm.style.display = 'flex';
        signupForm.style.display = 'none';
    } else {
        signupTab.classList.add('active');
        loginTab.classList.remove('active');
        signupForm.style.display = 'flex';
        loginForm.style.display = 'none';
    }
}

// ===== Login Handler =====
async function handleLogin() {
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value.trim();
    const message = document.getElementById('loginMessage');

    if (!email || !password) {
        showMessage(message, 'Please fill in all fields', 'error');
        return;
    }

    showSpinner();

    try {
        const response = await fetch(`${API_BASE_URL}/users/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        const data = await response.json();

        if (response.ok) {
            // Assuming response contains user and token
            authToken = data.access_token || data.token;
            currentUser = data.user || { email, first_name: email.split('@')[0] };
            
            localStorage.setItem('token', authToken);
            localStorage.setItem('user', JSON.stringify(currentUser));
            
            clearAuthForms();
            showAppScreen();
            showToast('Welcome! Login successful.', 'success');
        } else {
            showMessage(message, data.detail || 'Invalid email or password', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage(message, 'Connection error. Please try again.', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Signup Handler =====
async function handleSignup() {
    const firstName = document.getElementById('signupFirstName').value.trim();
    const lastName = document.getElementById('signupLastName').value.trim();
    const email = document.getElementById('signupEmail').value.trim();
    const password = document.getElementById('signupPassword').value.trim();
    const message = document.getElementById('signupMessage');

    if (!firstName || !lastName || !email || !password) {
        showMessage(message, 'Please fill in all fields', 'error');
        return;
    }

    showSpinner();

    try {
        const response = await fetch(`${API_BASE_URL}/users/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ first_name: firstName, last_name: lastName, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(message, 'Account created! Please sign in.', 'success');
            setTimeout(() => {
                clearAuthForms();
                switchAuthTab('login');
            }, 2000);
        } else {
            showMessage(message, data.detail || 'Signup failed. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Signup error:', error);
        showMessage(message, 'Connection error. Please try again.', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Logout Handler =====
function handleLogout() {
    authToken = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    allTasks = [];
    clearAuthForms();
    showAuthScreen();
    showToast('Logged out successfully.', 'success');
}

// ===== Create Task Handler =====
async function handleCreateTask(e) {
    e.preventDefault();

    const title = document.getElementById('taskTitle').value.trim();
    const description = document.getElementById('taskDescription').value.trim();
    const date = document.getElementById('taskDate').value;
    const time = document.getElementById('taskTime').value;
    const message = document.getElementById('createTaskMessage');

    if (!title) {
        showMessage(message, 'Please enter a task title', 'error');
        return;
    }

    showSpinner();

    try {
        const taskData = {
            title,
            description: description || null,
            owner_id: currentUser.id || 1, // Use actual user ID if available
            date: date || null,
            time: time || null,
            completed: false
        };

        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(taskData)
        });

        if (response.ok) {
            const newTask = await response.json();
            allTasks.push(newTask);
            filterTasks(currentFilter);
            createTaskForm.reset();
            showMessage(message, 'Task created successfully!', 'success');
            updateStats();
            setTimeout(() => message.style.display = 'none', 3000);
        } else {
            const data = await response.json();
            showMessage(message, data.detail || 'Failed to create task', 'error');
        }
    } catch (error) {
        console.error('Create task error:', error);
        showMessage(message, 'Connection error. Please try again.', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Load Tasks =====
async function loadTasks() {
    showSpinner();

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            allTasks = await response.json();
            filterTasks(currentFilter);
            updateStats();
        } else {
            showToast('Failed to load tasks', 'error');
        }
    } catch (error) {
        console.error('Load tasks error:', error);
        showToast('Connection error. Could not load tasks.', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Filter Tasks =====
function filterTasks(filter) {
    currentFilter = filter;

    // Update active button
    filterAllBtn.classList.remove('active');
    filterPendingBtn.classList.remove('active');
    filterCompletedBtn.classList.remove('active');

    if (filter === 'all') {
        filterAllBtn.classList.add('active');
        filteredTasks = allTasks;
    } else if (filter === 'pending') {
        filterPendingBtn.classList.add('active');
        filteredTasks = allTasks.filter(task => !task.completed);
    } else if (filter === 'completed') {
        filterCompletedBtn.classList.add('active');
        filteredTasks = allTasks.filter(task => task.completed);
    }

    renderTasks();
}

// ===== Render Tasks =====
function renderTasks() {
    tasksList.innerHTML = '';

    if (filteredTasks.length === 0) {
        noTasksMessage.style.display = 'block';
    } else {
        noTasksMessage.style.display = 'none';
        filteredTasks.forEach(task => {
            const taskCard = createTaskCard(task);
            tasksList.appendChild(taskCard);
        });
    }
}

// ===== Create Task Card Element =====
function createTaskCard(task) {
    const card = document.createElement('div');
    card.className = `task-card ${task.completed ? 'completed' : ''}`;

    const dateStr = task.date ? new Date(task.date).toLocaleDateString() : 'No date';
    const timeStr = task.time || 'No time';

    card.innerHTML = `
        <div class="task-header">
            <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''} 
                   onchange="handleToggleTask(${task.id}, this.checked)">
            <div style="flex: 1;">
                <div class="task-title">${escapeHtml(task.title)}</div>
                ${task.description ? `<div class="task-description">${escapeHtml(task.description)}</div>` : ''}
            </div>
        </div>
        ${task.date || task.time ? `
            <div class="task-meta">
                ${task.date ? `<span class="task-date">📅 ${dateStr}</span>` : ''}
                ${task.time ? `<span class="task-time">🕐 ${timeStr}</span>` : ''}
            </div>
        ` : ''}
        <div class="task-actions">
            <button class="btn btn-danger" onclick="handleDeleteTask(${task.id})">Delete</button>
        </div>
    `;

    return card;
}

// ===== Toggle Task Completion =====
async function handleToggleTask(taskId, completed) {
    showSpinner();

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify({ completed })
        });

        if (response.ok) {
            const updatedTask = await response.json();
            const taskIndex = allTasks.findIndex(t => t.id === taskId);
            if (taskIndex !== -1) {
                allTasks[taskIndex] = updatedTask;
                filterTasks(currentFilter);
                updateStats();
                showToast(completed ? 'Task marked as completed!' : 'Task marked as pending.', 'success');
            }
        } else {
            showToast('Failed to update task', 'error');
        }
    } catch (error) {
        console.error('Toggle task error:', error);
        showToast('Connection error', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Delete Task =====
async function handleDeleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }

    showSpinner();

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${authToken}`
            }
        });

        if (response.ok) {
            allTasks = allTasks.filter(t => t.id !== taskId);
            filterTasks(currentFilter);
            updateStats();
            showToast('Task deleted successfully', 'success');
        } else {
            showToast('Failed to delete task', 'error');
        }
    } catch (error) {
        console.error('Delete task error:', error);
        showToast('Connection error', 'error');
    } finally {
        hideSpinner();
    }
}

// ===== Update User Profile =====
function updateUserProfile() {
    if (currentUser) {
        displayName.textContent = `${currentUser.first_name || ''} ${currentUser.last_name || ''}`.trim() || 'User';
        displayEmail.textContent = currentUser.email || '';
    }
}

// ===== Update Stats =====
function updateStats() {
    const total = allTasks.length;
    const completed = allTasks.filter(t => t.completed).length;
    const pending = total - completed;

    totalTasksEl.textContent = total;
    completedCountEl.textContent = completed;
    pendingCountEl.textContent = pending;
}

// ===== Helper Functions =====
function showMessage(element, message, type) {
    element.textContent = message;
    element.className = `form-message ${type}`;
    element.style.display = 'block';
}

function showSpinner() {
    spinner.style.display = 'flex';
}

function hideSpinner() {
    spinner.style.display = 'none';
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function clearAuthForms() {
    document.getElementById('loginEmail').value = '';
    document.getElementById('loginPassword').value = '';
    document.getElementById('signupFirstName').value = '';
    document.getElementById('signupLastName').value = '';
    document.getElementById('signupEmail').value = '';
    document.getElementById('signupPassword').value = '';
    document.getElementById('loginMessage').style.display = 'none';
    document.getElementById('signupMessage').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
