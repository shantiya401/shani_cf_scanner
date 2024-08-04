function updateLog(message) {
    const logDiv = document.getElementById('log-content');
    logDiv.textContent += message + "\n";
    logDiv.scrollTop = logDiv.scrollHeight; // اسکرول به پایین
}

function startScan() {
    // نمایش پیام شروع اسکن
    document.getElementById('start-message').style.display = 'block';
    document.getElementById('complete-message').style.display = 'none';

    updateLog("Shani Scanner is starting...");
    const formData = new FormData(document.getElementById('scan-form'));
    fetch('/start_scan', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json'
        }
    })
    .then(response => {
        console.log('Response:', response); // لاگ کردن پاسخ برای دیباگ
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Data:', data); // لاگ کردن داده‌ها برای دیباگ
        if (data.error) {
            updateLog(`Error: ${data.error}`);
        } else {
            data.details.forEach(detail => updateLog(detail));
            updateResults(data.results);
        }
        updateLog("Shani Scan is complete...");

        // نمایش پیام پایان اسکن
        document.getElementById('start-message').style.display = 'none';
        document.getElementById('complete-message').style.display = 'block';
    })
    .catch(error => {
        updateLog(`Error: ${error.message}`);

        // نمایش پیام پایان اسکن حتی در صورت بروز خطا
        document.getElementById('start-message').style.display = 'none';
        document.getElementById('complete-message').style.display = 'block';
    });
}

function testPing() {
    updateLog("Starting ping test...");
    const formData = new FormData(document.getElementById('scan-form'));
    fetch('/test_ping', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        data.details.forEach(detail => updateLog(detail));
    })
    .catch(error => updateLog(`Error: ${error}`));
}

function testSpeed() {
    updateLog("Starting speed test...");
    const formData = new FormData(document.getElementById('scan-form'));
    fetch('/test_speed', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        data.details.forEach(detail => updateLog(detail));
    })
    .catch(error => updateLog(`Error: ${error}`));
}

function updateResults(results) {
    console.log('Updating results:', results); // لاگ کردن نتایج برای دیباگ
    const resultTable = document.getElementById('results-table').getElementsByTagName('tbody')[0];
    resultTable.innerHTML = "";
    results.forEach(result => {
        const row = document.createElement('tr');
        row.innerHTML = `<td>${result[0]}</td><td>${result[1]}</td><td>${result[2]}</td>`;
        resultTable.appendChild(row);
    });
}
