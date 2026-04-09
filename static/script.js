let interval = null;

function startAutoCheck() {
    const url = document.getElementById("url").value.trim();

    if (!url) {
        showToast("Please enter a valid URL first.", "warning");
        return;
    }

    const startBtn = document.getElementById("startBtn");
    const btnText = startBtn.querySelector(".btn-text");

    if (interval) {
        // Stop Polling
        clearInterval(interval);
        interval = null;
        startBtn.classList.remove("polling");
        btnText.innerText = "Start Polling";
        showToast("Monitoring stopped.", "success");
        return;
    }

    // Start Polling
    startBtn.classList.add("polling");
    btnText.innerText = "Stop Polling";
    showToast(`Started monitoring: ${url}`, "success");
    
    checkWebsite(url);
    interval = setInterval(() => {
        checkWebsite(url);
    }, 10000);
}

function checkWebsiteNow() {
    const url = document.getElementById("url").value.trim();
    if (!url) {
        showToast("Please enter a valid URL first.", "warning");
        return;
    }
    checkWebsite(url);
    showToast("Manual check initiated...", "success");
}

function checkWebsite(url) {
    const statusTxt = document.getElementById("status-txt");
    const alertBox = document.getElementById("alertBox");

    statusTxt.innerText = "Fetching...";
    
    fetch("/check", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            showAlert(data.error, "error");
            statusTxt.innerText = "Error";
            return;
        }

        // Update Dashboard Cards
        statusTxt.innerText = data.status;
        document.getElementById("change-txt").innerText = data.change_type;
        document.getElementById("time-txt").innerText = data.time.split(" ")[1] || data.time;

        // Update Code Areas
        document.getElementById("old").textContent = data.old || "No previous record.";
        document.getElementById("new").textContent = data.new || "No content found.";
        
        let diffContent = data.diff || "No differences detected.";
        if (data.status === "First Time Stored" || data.status === "No Change") {
             diffContent = `<span style="color: #94a3b8;">${data.status}. No highlighting required.</span>`;
        }
        document.getElementById("diff").innerHTML = diffContent;

        // Alerts and Toasts
        if (data.status === "Changed") {
            showAlert(`Change Detected: ${data.change_type}`, "warning");
            showToast(`${data.change_type} Change Detected!`, data.change_type === "Major" ? "major" : "minor");
        } else if (data.status === "First Time Stored") {
            showAlert("First snapshot stored successfully.", "success");
        } else {
            showAlert("No changes detected.", "success");
        }
    })
    .catch(err => {
        showAlert("Failed to connect to the server.", "error");
        statusTxt.innerText = "Offline";
    });
}

function showAlert(message, type) {
    const alertBox = document.getElementById("alertBox");
    alertBox.className = `alert-box ${type}`;
    alertBox.innerText = message;
    alertBox.classList.remove("hidden");
}

let toastCount = 0;
function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    
    const toast = document.createElement("div");
    toast.className = `toast toast-${type.toLowerCase()}`;
    toast.innerText = message;
    
    container.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => {
        toast.classList.add("show");
    }, 10);
    
    // Remove after 4 seconds
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 4000);
}