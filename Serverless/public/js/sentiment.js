document.getElementById("sentiment").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent the default form submission

  // Construct the JSON object from the form data
  const data = {
    string: document.getElementById("input-sentiment").value,
  };
  // Send the JSON object to the Google Cloud Function using fetch
  fetch("https://us-east1-nice-beanbag-416418.cloudfunctions.net/sentiment", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.text())
    .then((data) => {
      console.log("Success:", data);
      document.getElementById("sentiment-result").innerText = data;
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
