self.addEventListener("message", (event) => {
    console.log("Service Worker received message:", event.data);
    if (event.data.type === "alarm") {
        self.registration.showNotification("Test Notification", {
            body: event.data.message,
            icon: "/static/bell_icon.png", // Replace with your icon
        });
    }
});