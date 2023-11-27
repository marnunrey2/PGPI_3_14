// static/main.js

console.log("Sanity check!");

// Get Stripe publishable key
fetch("utils/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);

  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("utils/create-checkout-session/") //This is an example. Change this to utils/create-custom-checkout-session/"id" for production
  .then((result) => {
    if (!result.ok) {
      throw new Error('Network response was not ok');
    }
    return result.json();
  })
  .then((data) => {
    console.log(data);
    // Redirect to Stripe Checkout
    return stripe.redirectToCheckout({ sessionId: data.sessionId });
  })
  .catch((error) => {
    console.error('Fetch error:', error);
  });
  });
});