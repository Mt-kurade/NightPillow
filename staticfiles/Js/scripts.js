function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.style.display = 'none');
    document.getElementById(pageId).style.display = 'block';
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
