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

function attachRecaptchaToContactForm(form) {
  if (!form || form.dataset.recaptchaAttached === "true") {
    return;
  }

  const siteKey = form.dataset.recaptchaSiteKey;
  if (!siteKey || !window.grecaptcha) {
    return;
  }

  form.dataset.recaptchaAttached = "true";
  form.addEventListener("submit", (event) => {
    if (form.dataset.recaptchaReady === "true") {
      form.dataset.recaptchaReady = "false";
      return;
    }

    event.preventDefault();
    event.stopImmediatePropagation();

    window.grecaptcha.ready(() => {
      window.grecaptcha
        .execute(siteKey, { action: "contact" })
        .then((token) => {
          const tokenInput = form.querySelector('input[name="g-recaptcha-response"]');
          if (tokenInput) {
            tokenInput.value = token;
          }
          form.dataset.recaptchaReady = "true";
          window.htmx.trigger(form, "submit");
        })
        .catch(() => {
          form.dataset.recaptchaReady = "false";
        });
    });
  }, true);
}

function initContactFormEnhancements(root = document) {
  setContactPlaceholders();
  attachRecaptchaToContactForm(root.querySelector("#contact-form"));
}

document.addEventListener("DOMContentLoaded", () => initContactFormEnhancements());
document.body.addEventListener("htmx:afterSwap", (event) => {
  initContactFormEnhancements(event.target);
});
