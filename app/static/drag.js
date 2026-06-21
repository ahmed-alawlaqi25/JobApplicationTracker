const draggables = document.querySelectorAll(".job-card");
const droppables = document.querySelectorAll(".tracker-items");

draggables.forEach((task) => {
    task.addEventListener("dragstart", () => {
        task.classList.add("is-dragging");
    });
    task.addEventListener("dragend", () => {
        task.classList.remove("is-dragging");
    });
});

droppables.forEach((zone) => {

    zone.addEventListener("dragover", (e) => {
        e.preventDefault();

        if (deleteZone.classList.contains("drag-over")) return;

        const bottomTask = insertAboveTask(zone, e.clientY);
        const curTask = document.querySelector(".is-dragging");

        if (!curTask) return;


        if (!bottomTask) {
            zone.appendChild(curTask);
        } else {
            zone.insertBefore(curTask, bottomTask);
        }
    });

    zone.addEventListener("drop", (e) => {
        e.preventDefault();

        const curTask = document.querySelector(".is-dragging");

        if (!curTask) return;

        fetch("/switch_status", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                job_id: curTask.dataset.jobId,
                status: zone.id
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
    });
});

const insertAboveTask = (zone, mouseY) => {
    const els = zone.querySelectorAll(".job-card:not(.is-dragging)");

    let closestTask = null;
    let closestOffset = Number.POSITIVE_INFINITY; // changed from NEGATIVE_INFINITY

    els.forEach((task) => {
        const {top} = task.getBoundingClientRect();
        const offset = top - mouseY; // flipped: how far is this element's top BELOW the cursor

        if (offset > 0 && offset < closestOffset) { // changed: smallest positive offset wins
            closestOffset = offset;
            closestTask = task;
        }
    });

    return closestTask;
};

const dropZone = document.querySelector(".drop-zone");

const deleteZone = document.querySelector(".delete-zone");

deleteZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    deleteZone.classList.add("drag-over");
    const curTask = document.querySelector(".is-dragging");
    setTimeout(() => {
        curTask.style.display = "none";
    }, 0);
});

deleteZone.addEventListener("dragleave", () => {
    deleteZone.classList.remove("drag-over");
    const curTask = document.querySelector(".is-dragging");
    if (curTask) curTask.style.display = "";
});

deleteZone.addEventListener("drop", (e) => {
    e.preventDefault();
    deleteZone.classList.remove("drag-over");
    const curTask = document.querySelector(".is-dragging");
    fetch("/delete_job", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            job_id: curTask.dataset.jobId,

        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "success") {
                curTask.remove();
                console.log(data);
            }
        })
        .catch(error => {
            console.error(error);
        });
});