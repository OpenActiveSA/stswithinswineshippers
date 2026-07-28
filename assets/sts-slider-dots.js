(() => {
  function syncDots(slider) {
    const host = slider.querySelector('[data-sts-slider-dots]');
    if (!host) return;

    const list = host.querySelector('.sts-slider-dots__list');
    if (!list) return;

    const total = Math.max(1, slider.totalPages || 1);
    const current = Math.min(total, Math.max(1, slider.currentPage || 1));

    if (list.children.length !== total) {
      list.replaceChildren();
      for (let i = 1; i <= total; i += 1) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'sts-slider-dots__dot';
        btn.setAttribute('aria-label', 'Go to slide ' + i);
        btn.addEventListener('click', () => {
          if (!slider.sliderItemOffset) return;
          slider.setSlidePosition((i - 1) * slider.sliderItemOffset);
        });
        list.appendChild(btn);
      }
    }

    Array.from(list.children).forEach((dot, index) => {
      dot.classList.toggle('is-active', index + 1 === current);
    });
  }

  function bindSlider(slider) {
    if (slider.dataset.stsDotsBound === 'true') return;
    if (!slider.querySelector('[data-sts-slider-dots]')) return;

    slider.dataset.stsDotsBound = 'true';
    slider.addEventListener('slideChanged', () => syncDots(slider));
    syncDots(slider);

    // Dawn recalculates pages on resize; keep dots in sync.
    const resizeObserver = new ResizeObserver(() => syncDots(slider));
    if (slider.slider) resizeObserver.observe(slider.slider);
  }

  function init() {
    document.querySelectorAll('slider-component').forEach(bindSlider);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', init);
})();
