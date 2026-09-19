document.addEventListener("alpine:init", () => {
  Alpine.data("mobileNav", () => ({
    open: false,
    toggle() {
      this.open = !this.open;
    },
    close() {
      this.open = false;
    },
  }));
});

function setContactPlaceholders() {
  const message = document.querySelector('textarea[name="message"]');
  if (!message) {
    return;
  }
  message.placeholder =
    window.matchMedia("(max-width: 1023px)").matches
      ? "Message"
      : "What are you working on?";
}

document.addEventListener("DOMContentLoaded", setContactPlaceholders);
document.body.addEventListener("htmx:afterSwap", (event) => {
  setContactPlaceholders();
  if (event.target.id === "contact-form-wrapper" && window.grecaptcha) {
    window.grecaptcha.reset();
  }
});
