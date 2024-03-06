document.getElementById("dataForm").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent the default form submission

  // Construct the JSON object from the form data
  const data = {
    male: document.getElementById("male").value,
    age: document.getElementById("age").value,
    salary: document.getElementById("salary").value,
    price: document.getElementById("price").value,
  };

  // Send the JSON object to the Google Cloud Function using fetch
  fetch("https://us-central1-cmpt756-container.cloudfunctions.net/function-3", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.text())
    .then((data) => {
      console.log("Success:", data);
      document.getElementById("result").innerText = data; // Display the result
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
