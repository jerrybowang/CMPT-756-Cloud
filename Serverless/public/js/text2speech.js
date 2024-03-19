document.getElementById("text2speech").addEventListener("submit", function (e) {
  e.preventDefault(); // Prevent the default form submission

  // Construct the JSON object from the form data
  const data = {
    input: document.getElementById("input-text2speech").value,
  };
  const audioPlayer = document.getElementById("text2speech-result");

  console.log(data);
  console.log(JSON.stringify(data));
  // Send the JSON object to the Google Cloud Function using fetch
  fetch(
    "https://us-central1-nice-beanbag-416418.cloudfunctions.net/function-2",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    }
  )
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
      if (data.audio_content) {
        // Convert base64 audio content to a playable URL
        // const audioSrc = `data:${data.content_type};base64,${data.audio_content}`;
        // console.log("29");
        // audioPlayer.src = audioSrc;
        // console.log("30");
        // audioPlayer.play();
        document.getElementById("text2speech-result").innerText = "Audio content received.";
      } else {
        console.error("No audio content received.");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
