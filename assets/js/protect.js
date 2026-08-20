/*
 * Lightweight deterrents against casual image saving + drag-copy.
 * Honest limitation, documented in README: none of this stops a determined
 * person (devtools, screenshots, and screen recording all still work — no
 * client-side JS can prevent that). What this DOES do:
 *   1. Removes the trivial "right click > Save Image As" path site-wide.
 *   2. Renders the enlarged lightbox image onto a <canvas> with your logo
 *      drawn into the bottom-right corner at render time, so any screenshot
 *      or screen-recording of the enlarged view carries the mark too.
 *   3. Serves web-sized images only (see README) rather than your originals,
 *      so even a successful "save" only nets a small, watermarked file.
 *   4. Reveals large galleries in batches ("Load more") so page weight
 *      scales with what's actually been viewed, not the whole set at once.
 *   5. Detects each thumbnail's real orientation so portrait photos get a
 *      2:3 box instead of being cropped into a landscape 3:2 frame.
 */

(function () {
  // 1. Site-wide: no context menu, no native drag-out, on any image.
  document.addEventListener('contextmenu', function (e) {
    if (e.target.tagName === 'IMG' || e.target.tagName === 'CANVAS') e.preventDefault();
  });
  document.addEventListener('dragstart', function (e) {
    if (e.target.tagName === 'IMG' || e.target.tagName === 'CANVAS') e.preventDefault();
  });
})();

// Orientation-aware thumbnails: landscape photos sit in a 3:2 box (the
// contact-sheet default), portrait photos get a 2:3 box instead — detected
// from each image's real dimensions once it loads, so no manual tagging is
// needed per photo. object-fit: cover still applies within whichever box,
// so a photo is very rarely cropped at all, just contained properly.
(function () {
  document.querySelectorAll('.frame img').forEach(function (img) {
    function setOrientation() {
      if (img.naturalWidth && img.naturalHeight && img.naturalHeight > img.naturalWidth) {
        img.closest('.frame').classList.add('is-portrait');
      }
    }
    if (img.complete && img.naturalWidth) setOrientation();
    else img.addEventListener('load', setOrientation);
  });
})();

// Load more: reveal thumbnails in batches instead of rendering a huge
// contact sheet in one go. Hidden frames use display:none, so their
// loading="lazy" <img> doesn't fetch until they're revealed — keeps a
// 100+ photo gallery light on first load.
(function () {
  var sheet = document.getElementById('contactSheet');
  var btn = document.getElementById('loadMoreBtn');
  if (!sheet || !btn) return;

  var batchSize = parseInt(sheet.dataset.batchSize, 10) || 24;
  var frames = Array.prototype.slice.call(sheet.querySelectorAll('.frame'));
  var shown = batchSize;

  function apply() {
    frames.forEach(function (frame, i) {
      frame.classList.toggle('is-more-hidden', i >= shown);
    });
    var remaining = frames.length - shown;
    if (remaining > 0) {
      btn.hidden = false;
      document.getElementById('loadMoreCount').textContent =
        '(' + remaining + ' more)';
    } else {
      btn.hidden = true;
    }
  }

  btn.addEventListener('click', function () {
    shown += batchSize;
    apply();
  });

  if (frames.length > batchSize) apply();
})();

// Lightbox with canvas watermarking (only runs on gallery pages).
(function () {
  var images = window.GALLERY_IMAGES;
  if (!images || !images.length) return;

  var lightbox = document.getElementById('lightbox');
  var canvas = document.getElementById('lightboxCanvas');
  var caption = document.getElementById('lightboxCaption');
  var closeBtn = document.getElementById('lightboxClose');
  var prevBtn = document.getElementById('lightboxPrev');
  var nextBtn = document.getElementById('lightboxNext');
  var ctx = canvas.getContext('2d');
  var current = 0;

  // Preload the logo once. It's tiny (a PNG), so this is normally ready
  // well before anyone opens the lightbox — the "logoReady" guard below
  // just covers the rare case someone opens it before the logo finishes.
  var logo = new Image();
  var logoReady = false;
  logo.crossOrigin = 'anonymous';
  logo.onload = function () {
    logoReady = true;
    render(current); // redraw current frame in case it rendered before the logo was ready
  };
  if (window.WATERMARK_LOGO) logo.src = window.WATERMARK_LOGO;

  function drawLogo(w, h) {
    if (!logoReady) return;
    var targetWidth = w * 0.14; // logo scales to ~14% of the image's width
    var scale = targetWidth / logo.naturalWidth;
    var lw = logo.naturalWidth * scale;
    var lh = logo.naturalHeight * scale;
    var margin = w * 0.03;
    ctx.save();
    ctx.globalAlpha = 0.85;
    ctx.drawImage(logo, w - lw - margin, h - lh - margin, lw, lh);
    ctx.restore();
  }

  function render(index) {
    current = (index + images.length) % images.length;
    var entry = images[current];
    var img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = function () {
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      ctx.drawImage(img, 0, 0);
      drawLogo(canvas.width, canvas.height);
    };
    img.src = entry.src;
    caption.textContent = entry.caption + '  ·  ' + (current + 1) + ' / ' + images.length;
  }

  function open(index) {
    render(index);
    lightbox.hidden = false;
    document.body.style.overflow = 'hidden';
  }

  function close() {
    lightbox.hidden = true;
    document.body.style.overflow = '';
  }

  document.querySelectorAll('.frame').forEach(function (btn) {
    btn.addEventListener('click', function () {
      open(parseInt(btn.dataset.index, 10));
    });
  });

  closeBtn.addEventListener('click', close);
  prevBtn.addEventListener('click', function () { render(current - 1); });
  nextBtn.addEventListener('click', function () { render(current + 1); });
  lightbox.addEventListener('click', function (e) { if (e.target === lightbox) close(); });
  document.addEventListener('keydown', function (e) {
    if (lightbox.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') render(current - 1);
    if (e.key === 'ArrowRight') render(current + 1);
  });
})();
