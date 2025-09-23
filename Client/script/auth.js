const validateEmail = (email) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
};

const registerForm = document.getElementById("registerForm");
if (registerForm) {
    registerForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const fullName = document.getElementById("full_name").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        if (!validateEmail(email)) {
            alert("Invalid email format!");
            return;
        }

        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            return;
        }

        if (password.length < 8 || !/\d/.test(password) || !/[a-zA-Z]/.test(password)) {
            alert("Password must be at least 8 characters long and include both letters and numbers.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({
                    email: email,
                    full_name: fullName,
                    password: password
                })
            });

            const data = await response.json();
            if (response.ok) {
                alert(data.message || "Sign up successful!");
                window.location.href = "./login.html";
            } else {
                alert(data.error || "Registration failed!");
            }
        } catch (err) {
            console.error("Error:", err);
            alert("Cannot connect to server!");
        }
    });
}
const loginForm = document.getElementById("loginForm");
if (loginForm) {
    loginForm.addEventListener("submit", async function (e) {
        e.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (!validateEmail(email)) {
            alert("Invalid email format!");
            return;
        }

        try {
            const [loginResponse, userResponse] = await Promise.all([
                fetch("http://localhost:8000/auth/token", {
                    method: "POST",
                    headers: { "Content-Type": "application/x-www-form-urlencoded" },
                    body: new URLSearchParams({
                        username: email, 
                        password: password
                    })
                }),
                fetch(`http://localhost:8000/users/e/${email}`)
            ]);

            const loginData = await loginResponse.json();
            const userData = await userResponse.json();

            if (loginResponse.ok && userResponse.ok) {

                localStorage.setItem("user", JSON.stringify(userData));

                window.location.href = "./chatroom.html";
            } else {
                alert(loginData.error || userData.error || "Login failed!");
            }
        } catch (err) {
            console.error("Error:", err);
            alert("Cannot connect to server!");
        }
    });
}

