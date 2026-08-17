document.addEventListener("DOMContentLoaded", function () {
  // Select all necessary DOM elements
  const cartItems = document.querySelectorAll(".card-body");
  const totalPriceElement = document.querySelector(".total");

  // Function to calculate and update total price
  function updateTotal() {
    let total = 0;
    const currentItems = document.querySelectorAll(".card-body");

    currentItems.forEach((item) => {
      // Get price text, remove '$' sign, and convert to float
      const priceText = item.querySelector(".unit-price").textContent;
      const unitPrice = parseFloat(priceText.replace("$", "").trim());

      // Get quantity
      const quantity = parseInt(item.querySelector(".quantity").textContent);

      // Add to total
      total += unitPrice * quantity;
    });

    // Update total price on screen formatted to 2 decimal places
    totalPriceElement.textContent = `${total.toFixed(2)} $`;
  }

  // Attach event listeners to each cart item
  cartItems.forEach((item) => {
    const btnPlus = item.querySelector(".fa-plus-circle");
    const btnMinus = item.querySelector(".fa-minus-circle");
    const btnDelete = item.querySelector(".fa-trash-alt");
    const btnHeart = item.querySelector(".fa-heart");
    const quantitySpan = item.querySelector(".quantity");

    // 1. Plus Button: Increase quantity
    btnPlus.addEventListener("click", function () {
      let quantity = parseInt(quantitySpan.textContent);
      quantitySpan.textContent = quantity + 1;
      updateTotal();
    });

    // 2. Minus Button: Decrease quantity (minimum 0)
    btnMinus.addEventListener("click", function () {
      let quantity = parseInt(quantitySpan.textContent);
      if (quantity > 0) {
        quantitySpan.textContent = quantity - 1;
        updateTotal();
      }
    });

    // 3. Delete Button: Remove item from DOM and update total
    btnDelete.addEventListener("click", function () {
      // Remove the item container card
      const card = item.closest(".card");
      if (card) {
        card.remove();
      } else {
        item.remove();
      }
      updateTotal();
    });

    // 4. Heart Button: Toggle like (change color)
    btnHeart.addEventListener("click", function () {
      btnHeart.classList.toggle("liked");
    });
  });

  // Initial total calculation on page load
  updateTotal();
});