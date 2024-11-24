// Функція, яка обробляє подію завантаження сторінки
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm'); // Форма реєстрації з ID "registerForm"
    const leaderboardBody = document.getElementById('leaderboard-body'); // Таблиця рейтингу

    // Обробник для форми входу
    if (loginForm) {
        loginForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value;

            fetch('/api/users/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Помилка при вході: ' + response.statusText);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Токен:", data);
                    localStorage.setItem('access_token', data.access);
                    localStorage.setItem('refresh_token', data.refresh);
                    window.location.href = "/";
                })
                .catch(error => {
                    console.error("Помилка при вході:", error);
                    alert('Невірні облікові дані. Спробуйте ще раз.');
                });
        });
    }

    // Обробник для форми реєстрації
    if (registerForm) {
        registerForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const username = document.getElementById("register-username").value.trim();
            const email = document.getElementById("register-email").value.trim();
            const password = document.getElementById("register-password").value.trim();

            if (!username || !email || !password) {
                alert("Усі поля обов'язкові для заповнення.");
                return;
            }

            console.log("Дані для реєстрації:", { username, email, password });

            fetch('/api/users/register/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password })
            })
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(err => {
                            console.error("Відповідь сервера:", err);
                            throw new Error('Помилка при реєстрації: ' + err);
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    console.log("Користувач зареєстрований:", data);
                    alert("Реєстрація пройшла успішно! Тепер ви можете увійти.");
                    window.location.href = "/api/users/login/";
                })
                .catch(error => {
                    console.error("Помилка:", error);
                    alert(error.message);
                });
        });
    }

    // Функція для завантаження рейтингу
    if (leaderboardBody) {
        fetch('/api/quizzes/leaderboard/')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Не вдалося завантажити рейтинг.');
                }
                return response.json();
            })
            .then(data => {
                leaderboardBody.innerHTML = ""; // Очистити таблицю перед додаванням
                if (data.length === 0) {
                    leaderboardBody.innerHTML = `<tr><td colspan="4">Рейтинг поки що порожній.</td></tr>`;
                    return;
                }

                data.forEach((user, index) => {
                    const row = `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${user.username}</td>
                            <td>${user.email}</td>
                            <td>${user.score}</td>
                        </tr>
                    `;
                    leaderboardBody.innerHTML += row;
                });
            })
            .catch(error => {
                console.error("Помилка завантаження рейтингу:", error);
                leaderboardBody.innerHTML = `<tr><td colspan="4">Не вдалося завантажити рейтинг.</td></tr>`;
            });
    }
});
