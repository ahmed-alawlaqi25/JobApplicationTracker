const hash = window.location.hash.substring(1);
const params = new URLSearchParams(hash);
const accessToken = params.get("access_token");
const refreshToken = params.get("refresh_token");
const error = params.get("error");
const errorDescription = params.get("error_description");

if (error) {
    document.body.innerHTML = `
        <div class="error-container">
            <h2>فشل تسجيل الدخول</h2>
            <p>انتهت صلاحية رابط تسجيل الدخول أو أنه غير صالح. يرجى طلب رابط جديد والمحاولة مرة أخرى</p>
        </div>
        <a class="sign-in-button" href="/register">تسجيل الدخول</a>
    `;
    throw new Error(error);
}
if (accessToken) {
    fetch("/session", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            access_token: accessToken,
            refresh_token: refreshToken
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                window.location.href = "/tracker";
            } else {
                window.location.href = "/register";
            }
        })
        .catch(error => {
            console.error(error);
            window.location.href = "/register";
        });
}