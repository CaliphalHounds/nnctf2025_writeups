function fetchMessages() {
    // Get URL parameter "id"
    const urlParams = new URLSearchParams(window.location.search);
    const id = urlParams.get("id");

    // Build the endpoint
    const endpoint = id ? `/messages?id=${encodeURIComponent(id)}` : `/messages`;

    fetch(endpoint)
        .then(r => r.json())
        .then(data => {
            const container = document.getElementById("messages-container");
            container.innerHTML = "";

            data.messages.forEach(msg => {
                const div = document.createElement("div");
                div.classList.add("message");
                div.innerHTML = `<strong>#${msg.id} </strong> ${DOMPurify.sanitize(msg.message)}`;
                container.appendChild(div);
            });
        });
}

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("panel-title").textContent = `Panel de soporte`;
    fetchMessages();

    document.getElementById("support-form").addEventListener("submit", (e) => {
        e.preventDefault();
        const message = e.target.message.value.trim();
        if (!message) return;

        fetch(`/create_msg`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        })
        .then(r => r.json())
        .then(() => {
            e.target.reset();
            fetchMessages();
        });
    });
});
