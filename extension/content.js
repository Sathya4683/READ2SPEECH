document.addEventListener("DOMContentLoaded", () => {
  const sendBtn = document.getElementById("send");

  sendBtn.addEventListener("click", async () => {
    // Get current tab URL
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    const url = tab.url;

    console.log("Sending URL:", url);

    // Send to FastAPI backend
    fetch("http://127.0.0.1:8000/convert", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    })
    .then(res => res.json())
    .then(data => console.log("Response:", data))
    .catch(err => console.error("Error:", err));
  });
});
