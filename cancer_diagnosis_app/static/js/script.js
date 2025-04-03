// File: static/js/script.js

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("upload-form");
  const fileInput = document.getElementById("image-input");
  const uploadedImage = document.getElementById("uploaded-image");
  const resultContainer = document.getElementById("result-container");
  const predictedClass = document.getElementById("predicted-class");
  const confidenceScore = document.getElementById("confidence-score");
  const progressBar = document.getElementById("progress-bar");

  fileInput.addEventListener("change", function () {
    const file = fileInput.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        uploadedImage.src = e.target.result;
        uploadedImage.style.display = "block";
      };
      reader.readAsDataURL(file);
    }
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    // Reset result display
    resultContainer.style.display = "none";
    predictedClass.innerText = "Predicting...";
    confidenceScore.innerText = "";
    progressBar.style.width = "0%";

    fetch("/predict", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text()) // Expecting an HTML response
      .then((html) => {
        document.open();
        document.write(html);
        document.close();
      })
      .catch((error) => {
        console.error("Error:", error);
        predictedClass.innerText = "Error processing the image!";
        confidenceScore.innerText = "";
      });
  });
});
