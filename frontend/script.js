document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("recommendation-form");
  const resultContainer = document.getElementById("results");
  const loader = document.getElementById("loader");
  const darkModeToggle = document.getElementById("dark-mode-toggle");

  // Dark Mode Toggle
  darkModeToggle.addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");
  });

  // Form Submission
  form.addEventListener("submit", async function (event) {
      event.preventDefault(); // Prevent page refresh

      const submitButton = form.querySelector("button[type='submit']");
      submitButton.disabled = true;
      submitButton.textContent = "Fetching...";

      // Get skin type
      const skinType = document.querySelector('input[name="skin-type"]:checked');
      if (!skinType) {
          showError("Please select a skin type.");
          resetButton(submitButton);
          return;
      }

      // Get skin concerns
      const selectedConditions = Array.from(
          document.querySelectorAll('input[name="skin-condition"]:checked')
      ).map(checkbox => checkbox.value);

      if (selectedConditions.length === 0) {
          showError("Please select at least one skin concern.");
          resetButton(submitButton);
          return;
      }

      // Prepare request data
      const requestData = {
          skin_type: skinType.value,
          conditions: selectedConditions
      };

      // Show loader & clear previous results
      loader.style.display = "block";
      resultContainer.innerHTML = "";

      try {
          const response = await fetch("http://127.0.0.1:8000/recommend", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(requestData)
          });

          if (!response.ok) throw new Error("Failed to fetch recommendations. Please try again later.");

          const data = await response.json();
          displayRecommendations(data.recommended_products);
      } catch (error) {
          showError(error.message);
      } finally {
          loader.style.display = "none"; // Hide loader
          resetButton(submitButton);
      }
  });

  function displayRecommendations(products) {
      if (!products || products.length === 0) {
          showError("No suitable products found. Try adjusting your selection.");
          return;
      }

      resultContainer.innerHTML = products
          .map(product => `
              <div class="product">
                  <h3>${product.product_name}</h3>
                  <p><strong>Price:</strong> ${product.price_kes} KES</p>
                  <p>🛠 Benefits: ${product.benefits.join(", ")}</p>
              </div>
          `)
          .join("");

      resultContainer.style.display = "block";
  }

  function showError(message) {
      resultContainer.innerHTML = `<p class="error">${message}</p>`;
      resultContainer.style.display = "block";
  }

  function resetButton(button) {
      button.disabled = false;
      button.textContent = "Get Recommendations";
  }
});
