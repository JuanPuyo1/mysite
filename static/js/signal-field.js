(function () {
  let timeline = null;

  function prepareWave(path) {
    const length = path.getTotalLength();
    path.style.strokeDasharray = String(length);
    path.style.strokeDashoffset = String(length);
    return length;
  }

  function animateSignalField() {
    const svg = document.getElementById("signal-field");
    if (!svg || typeof gsap === "undefined") {
      return;
    }

    if (timeline) {
      timeline.kill();
    }

    const waves = svg.querySelectorAll(".signal-wave");
    const node = svg.querySelector(".signal-node");
    const rings = svg.querySelectorAll(".signal-ring");

    waves.forEach(prepareWave);

    gsap.set([node, ...rings], { transformOrigin: "50% 50%", opacity: 0, scale: 0.6 });

    timeline = gsap.timeline({ defaults: { ease: "power2.out" } });

    timeline.to(waves, {
      strokeDashoffset: 0,
      duration: 1.8,
      stagger: 0.2,
    });

    timeline.to(
      node,
      {
        opacity: 1,
        scale: 1,
        duration: 0.45,
      },
      "-=0.9"
    );

    timeline.to(
      rings,
      {
        opacity: (index, target) =>
          target.classList.contains("signal-ring--inner") ? 0.35 : 0.18,
        scale: 1,
        duration: 0.6,
        stagger: 0.12,
      },
      "-=0.25"
    );

    waves.forEach((wave, index) => {
      gsap.to(wave, {
        y: index % 2 === 0 ? -4 : 4,
        duration: 2.8 + index * 0.4,
        repeat: -1,
        yoyo: true,
        ease: "sine.inOut",
        delay: 1.2 + index * 0.15,
      });
    });

    gsap.to(rings, {
      scale: 1.12,
      opacity: (index, target) =>
        target.classList.contains("signal-ring--inner") ? 0.55 : 0.28,
      duration: 2.2,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      stagger: 0.2,
      delay: 1.4,
    });

    gsap.to(node, {
      scale: 1.15,
      duration: 1.6,
      repeat: -1,
      yoyo: true,
      ease: "sine.inOut",
      delay: 1.6,
    });
  }

  window.initSignalField = animateSignalField;

  document.addEventListener("DOMContentLoaded", animateSignalField);
})();
