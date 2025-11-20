/* JavaScript to trigger the notification when the alarm time is reached */
document.addEventListener("DOMContentLoaded", function () {
    function checkAlarm() {
        fetch("/check-alarm/")
            .then(response => response.json())
            .then(data => {
                if (data.trigger) {
                    showNotification(data.message);
                }
            });
    }

    function showNotification(message) {
        let notification = document.createElement("div");
        notification.className = "popup-notification";
        notification.innerHTML = `
            <div class="popup-header">
                <span class="popup-title">Night Pillow</span>
                <span class="popup-icon">&#128276;</span>
            </div>
            <div class="popup-body">${message}</div>
            <div class="popup-footer">
                <button onclick="dismissNotification(this)">Resolve</button>
            </div>
        `;
        document.body.appendChild(notification);
    }

    function dismissNotification(button) {
        button.parentElement.parentElement.remove();
    }

    setInterval(checkAlarm, 5000); // Check alarm every 5 seconds
});
