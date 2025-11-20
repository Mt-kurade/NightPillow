function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.style.display = 'none');
    document.getElementById(pageId).style.display = 'block';
}

function saveSleepData() {
    let sleepTime = document.getElementById("sleep_time").value;
    let wakeUpTime = document.getElementById("wakeUpTime").value;
    let rating = document.querySelector('input[name="rating"]:checked') ? document.querySelector('input[name="rating"]:checked').value : 0;

    fetch("/save-sleep-data/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: `sleep_time=${sleepTime}&wake_up_time=${wakeUpTime}&rating=${rating}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("Error: " + data.error);
        } else {
            alert("Sleep data saved! Duration: " + data.duration + " hours.");
        }
    })
    .catch(error => console.error("Error:", error));
}

function calculateSleepTimes() {
    const wakeUpTime = document.getElementById('wakeUpTime').value;
    if (!wakeUpTime) return;
   
    const wakeUpDate = new Date(`2023-01-01T${wakeUpTime}`);
    const sleepCycles = [9, 7.5, 6, 4.5];
    let recommendations = "<h3>Recommended Sleep Times:</h3><ul>";
   
    sleepCycles.forEach(cycle => {
        let sleepTime = new Date(wakeUpDate.getTime() - cycle * 90 * 60000);
        recommendations += `<li>${sleepTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</li>`;
    });
    recommendations += "</ul>";
   
    document.getElementById('recommendations').innerHTML = recommendations;
}
