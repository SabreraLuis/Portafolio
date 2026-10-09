/* INK / IMPACT — enhancement only; all content works without JavaScript. */
(() => {
  "use strict";
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  const navToggle = document.getElementById("nav-toggle");
  const nav = document.getElementById("site-nav");
  const progress = document.getElementById("reading-progress");
  const closeMenu = () => {
    nav.classList.remove("is-open");
    navToggle.setAttribute("aria-expanded", "false");
  };
  navToggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
  nav.querySelectorAll("a").forEach(link => link.addEventListener("click", closeMenu));
  document.addEventListener("keydown", event => {
    if (event.key === "Escape") {
      const wasOpen = nav.classList.contains("is-open");
      closeMenu();
      if (wasOpen) navToggle.focus();
    }
  });
  document.addEventListener("click", event => {
    if (!nav.contains(event.target) && !navToggle.contains(event.target)) closeMenu();
  });
  const updateProgress = () => {
    const total = document.documentElement.scrollHeight - window.innerHeight;
    const percent = total > 0 ? Math.min(100, Math.max(0, window.scrollY / total * 100)) : 0;
    progress.style.width = percent + "%";
  };
  window.addEventListener("scroll", updateProgress, { passive:true });
  window.addEventListener("resize", updateProgress, { passive:true });
  updateProgress();

  const blocks = Array.from(document.querySelectorAll("[data-reveal]"));
  if ("IntersectionObserver" in window && !reduced.matches) {
    // Only hide blocks after observers are prepared to preserve no-JS accessibility.
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold:0.09, rootMargin:"0px 0px -32px 0px" });
    blocks.forEach(el => observer.observe(el));
    document.documentElement.classList.add("js-motion");
    // Fail-open: late content must never remain hidden.
    window.setTimeout(() => {
      blocks.forEach(el => el.classList.add("is-visible"));
      observer.disconnect();
    }, 9000);
  }
  reduced.addEventListener?.("change", event => {
    if (event.matches) blocks.forEach(el => el.classList.add("is-visible"));
  });
  document.getElementById("print-cv").addEventListener("click", () => window.print());
})();
