document.getElementById("translator").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent the default form submission

  // Construct the JSON object from the form data
  const data = {
    input: document.getElementById("input-translator").value,
  };
  // Send the JSON object to the Google Cloud Function using fetch
  fetch(
    "https://us-central1-nice-beanbag-416418.cloudfunctions.net/translator",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  )
    .then((response) => response.text())
    .then((data) => {
      console.log("Success:", data);
      document.getElementById("translator-result").innerText = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
