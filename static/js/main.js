document.addEventListener("alpine:init", () => {
  Alpine.data("mobileNav", () => ({
    isOpen: false,
    toggle() {
      this.isOpen = !this.isOpen;
    },
    close() {
      this.isOpen = false;
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
