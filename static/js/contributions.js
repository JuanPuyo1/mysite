(function () {
  if (typeof gsap !== "undefined" && typeof ScrollTrigger !== "undefined") {
    gsap.registerPlugin(ScrollTrigger);
  }
  let activeTimeline = null;

  function visibleCells(root) {
    const grid = root.querySelector("#contributions-grid");
    if (!grid) {
      return [];
    }

    return Array.from(grid.querySelectorAll(".contribution-cell")).filter((cell) => {
      const column = cell.closest("[data-week]");
      return column && column.offsetParent !== null;
    });
  }

  function animateContributions(root = document, options = {}) {
    if (typeof gsap === "undefined") {
      return;
    }

    const cells = visibleCells(root);
    if (!cells.length) {
      return;
    }

    if (activeTimeline) {
      activeTimeline.kill();
    }

    gsap.set(cells, {
      opacity: 0,
      scale: 0.35,
      transformOrigin: "50% 50%",
    });

    const config = {
      opacity: 1,
      scale: 1,
      duration: 0.35,
      ease: "back.out(1.4)",
      stagger: {
        amount: options.immediate ? 0.9 : 1.4,
        grid: "auto",
        from: "start",
      },
    };

    if (options.immediate) {
      activeTimeline = gsap.timeline();
      activeTimeline.to(cells, config);
      return;
    }

    if (typeof ScrollTrigger !== "undefined") {
      activeTimeline = gsap.timeline({
        scrollTrigger: {
          trigger: root.querySelector("#contributions-panel") || root,
          start: "top 80%",
          once: true,
        },
      });
      activeTimeline.to(cells, config);
      return;
    }

    activeTimeline = gsap.timeline();
    activeTimeline.to(cells, config);
  }

  window.initContributions = animateContributions;

  document.addEventListener("DOMContentLoaded", () => {
    animateContributions(document);
  });

  document.body.addEventListener("htmx:afterSwap", (event) => {
    if (event.target.id !== "contributions-panel") {
      return;
    }
    animateContributions(event.target, { immediate: true });
  });
})();
