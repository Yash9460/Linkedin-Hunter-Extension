document.addEventListener('DOMContentLoaded', function () {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = 'Loading...';

    // Get active tab
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        // Check if tab exists and is a LinkedIn profile page
        if (!tabs[0] || !tabs[0].url || !tabs[0].url.startsWith('https://www.linkedin.com/in/')) {
            resultDiv.innerHTML = '<span>Please open this popup on a LinkedIn profile page.</span>';
            return;
        }
        chrome.tabs.sendMessage(tabs[0].id, { action: 'getProfileDetails' }, function (profile) {
            if (!profile || (!profile.fullName && !profile.org && !profile.designation)) {
                resultDiv.innerHTML = '<span>No data found</span>';
                return;
            }

            // Fetch email from backend (send fullName and organisation)
            fetch('http://localhost:5000/fetch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ organisation: profile.org, fullName: profile.fullName })
            })
            .then(res => res.json())
            .then(data => {
                let emailHtml = '';
                if (data.email) {
                    emailHtml = `<strong>Email:</strong> ${data.email}<br>`;
                } else if (data.emails && data.emails.length > 0) {
                    emailHtml = `<strong>Emails:</strong><br>` + data.emails.map(e => `<span>${e}</span>`).join('<br>');
                } else {
                    emailHtml = `<strong>Email:</strong> No data found<br>`;
                }
                let html = `<strong>Full Name:</strong> ${profile.fullName || 'N/A'}<br>
                            ${emailHtml}
                            <strong>Organisation:</strong> ${profile.org || 'N/A'}<br>
                            <strong>Designation:</strong> ${profile.designation || 'N/A'}`;
                resultDiv.innerHTML = html;
            })
            .catch(() => {
                resultDiv.innerHTML = '<span>No data found</span>';
            });
        });
    });
});
