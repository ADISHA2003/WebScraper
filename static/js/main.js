function startScraping() {
    const url = document.getElementById('urlInput').value;
    const notifications = document.getElementById('notifications');
    notifications.innerText = 'Scraping in progress...';

    fetch('/scrape', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            notifications.innerText = 'Error: ' + data.error;
        } else {
            notifications.innerText = data.message;
            document.getElementById('output').innerText = JSON.stringify(data.data, null, 2);
        }
    })
    .catch(error => {
        notifications.innerText = 'Error occurred during scraping!';
        console.error(error);
    });
}

function downloadFile(fileType) {
    window.location.href = `/download/${fileType}`;
}
