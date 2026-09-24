/* ==========================================================================
   DIS · Gallery — behaviour
   1. Scroll reveals (IntersectionObserver, reduced-motion aware)
   2. Photo lightbox (keyboard, focus handling, preloading)
   ========================================================================== */
(function () {
  "use strict";

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------------------------------------------------------------
     1. Reveal on scroll
     --------------------------------------------------------------------- */
  function initReveals() {
    var items = document.querySelectorAll(".reveal, .rule-draw");

    if (!("IntersectionObserver" in window) || reduceMotion) {
      items.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------------------------------------------------------------------
     2. Mobile navigation
     --------------------------------------------------------------------- */
  function initNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var menu = document.querySelector("[data-mobile-nav]");
    if (!toggle || !menu) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      if (open) {
        menu.removeAttribute("hidden");
      } else {
        menu.setAttribute("hidden", "");
      }
      document.body.classList.toggle("is-locked", open);
    }

    function isOpen() {
      return toggle.getAttribute("aria-expanded") === "true";
    }

    toggle.addEventListener("click", function () {
      setOpen(!isOpen());
    });

    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) setOpen(false);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });

    window.addEventListener("resize", function () {
      if (window.matchMedia("(min-width: 64rem)").matches && isOpen()) {
        setOpen(false);
      }
    });
  }

  /* ---------------------------------------------------------------------
     3. Contact form — static site, so hand the message to the mail client
     --------------------------------------------------------------------- */
  function initContactForm() {
    var form = document.querySelector("[data-contact-form]");
    if (!form) return;

    var status = form.querySelector("[data-form-status]");
    var office = "info@dis.ac.tz";

    form.addEventListener("submit", function (event) {
      event.preventDefault();

      /* Honeypot: bots fill the hidden field, humans never see it. */
      var trap = form.querySelector('input[name="website"]');
      if (trap && trap.value) {
        if (status) status.textContent = "Thank you — your message has been sent.";
        form.reset();
        return;
      }

      var data = new FormData(form);
      var name = (data.get("name") || "").toString().trim();
      var email = (data.get("email") || "").toString().trim();
      var phone = (data.get("phone") || "").toString().trim();
      var subject = (data.get("subject") || "").toString().trim() || "Website enquiry";
      var message = (data.get("message") || "").toString().trim();

      var body =
        "Name: " + name + "\n" +
        "Email: " + email + "\n" +
        (phone ? "Phone: " + phone + "\n" : "") +
        "\n" + message;

      window.location.href =
        "mailto:" + office +
        "?subject=" + encodeURIComponent("[DIS website] " + subject) +
        "&body=" + encodeURIComponent(body);

      if (status) {
        status.textContent =
          "Your mail app is opening with the message ready to send to " + office + ".";
      }
    });
  }

  /* ---------------------------------------------------------------------
     4. Lightbox
     --------------------------------------------------------------------- */
  function initLightbox() {
    var root = document.querySelector("[data-lightbox-root]");
    if (!root) return;

    var triggers = Array.prototype.slice.call(
      document.querySelectorAll("[data-lightbox]")
    );
    if (!triggers.length) return;

    var image = root.querySelector("[data-lightbox-image]");
    var caption = root.querySelector("[data-lightbox-caption]");
    var counter = root.querySelector("[data-lightbox-counter]");
    var closeButton = root.querySelector("[data-lightbox-close]");
    var prevButton = root.querySelector("[data-lightbox-prev]");
    var nextButton = root.querySelector("[data-lightbox-next]");
    var index = 0;
    var lastFocused = null;

    function pad(value) {
      return String(value).padStart(2, "0");
    }

    function current() {
      return triggers[index];
    }

    function preload(offset) {
      var target = triggers[(index + offset + triggers.length) % triggers.length];
      if (target) {
        var img = new Image();
        img.src = target.getAttribute("data-src");
      }
    }

    function render() {
      var trigger = current();
      image.src = trigger.getAttribute("data-src");
      image.alt = trigger.getAttribute("data-caption") || "";
      caption.textContent = trigger.getAttribute("data-caption") || "";
      counter.textContent =
        pad(index + 1) + " / " + pad(triggers.length);
      preload(1);
      preload(-1);
    }

    function open(target) {
      index = triggers.indexOf(target);
      if (index < 0) index = 0;
      lastFocused = document.activeElement;
      render();
      root.classList.add("is-open");
      root.removeAttribute("aria-hidden");
      document.body.classList.add("is-locked");
      closeButton.focus();
    }

    function close() {
      root.classList.remove("is-open");
      root.setAttribute("aria-hidden", "true");
      document.body.classList.remove("is-locked");
      if (lastFocused && typeof lastFocused.focus === "function") {
        lastFocused.focus();
      }
    }

    function step(offset) {
      index = (index + offset + triggers.length) % triggers.length;
      render();
    }

    triggers.forEach(function (trigger) {
      trigger.addEventListener("click", function (event) {
        event.preventDefault();
        open(trigger);
      });
    });

    closeButton.addEventListener("click", close);
    prevButton.addEventListener("click", function () {
      step(-1);
    });
    nextButton.addEventListener("click", function () {
      step(1);
    });

    /* Click the backdrop (but never the image or the controls) to dismiss. */
    root.addEventListener("click", function (event) {
      if (event.target === root || event.target.hasAttribute("data-lightbox-stage")) {
        close();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (!root.classList.contains("is-open")) return;

      if (event.key === "Escape") {
        event.preventDefault();
        close();
      } else if (event.key === "ArrowRight") {
        event.preventDefault();
        step(1);
      } else if (event.key === "ArrowLeft") {
        event.preventDefault();
        step(-1);
      } else if (event.key === "Tab") {
        /* Keep focus inside the dialog while it is open. */
        var focusable = [
          closeButton,
          prevButton,
          nextButton
        ].filter(function (el) {
          return el.offsetParent !== null;
        });
        if (!focusable.length) return;
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });
  }

  function init() {
    initReveals();
    initNav();
    initContactForm();
    initLightbox();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
