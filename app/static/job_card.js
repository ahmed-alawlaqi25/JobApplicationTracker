const switch_status = document.getElementById("job_status");
const path = window.location.pathname;
const jobId = path.split('/').pop();

document.querySelectorAll(".job-card").forEach((card) => {
    card.addEventListener("click", () => {
        window.location.href = `/application/${card.dataset.jobId}`;
    });
});


function copyLink(event, element) {
    event.preventDefault();

    const url = element.href;

    navigator.clipboard.writeText(url)
        .then(() => {
            alert("Link copied to clipboard!");
        })
        .catch(err => {
            console.error("Failed to copy link:", err);
        });
}

document.querySelectorAll(".copy-link").forEach(link => {
    link.textContent = new URL(link.href).hostname;
});


switch_status.addEventListener("change", () => {
    fetch("/switch_status", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            job_id: jobId,
            status: switch_status.value
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                console.log(data);
            }
        })
        .catch(error => {
            console.error(error);
        });
})