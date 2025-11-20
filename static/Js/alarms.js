function checkAlarms() {
    fetch("/check-alarms/")
        .then(response => response.json())
        .then(data => {
            data.alarms.forEach(alarm => {
                notifyUser(alarm.title, alarm.message);
            });
        })
        .catch(error => console.error("Error fetching alarms:", error));
}

function notifyUser(title, message) {
    if (Notification.permission === "granted") {
        navigator.serviceWorker.ready.then(function (registration) {
            registration.showNotification(title, {
                body: message,
                icon: "/static/images/alarm-icon.png",
            });
        });
    }
}

// Check alarms every 60 seconds
setInterval(checkAlarms, 60000);
