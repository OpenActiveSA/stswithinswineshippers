(function () {
  function bindFilterSelects(root) {
    if (!root) return;
    root.querySelectorAll('[data-sts-filter-select]').forEach(function (select) {
      if (select.dataset.stsBound === 'true') return;
      select.dataset.stsBound = 'true';
      select.addEventListener('change', function () {
        var url = select.value;
        if (url) window.location.assign(url);
      });
    });
  }

  function init() {
    document.querySelectorAll('[data-sts-shop-intro]').forEach(bindFilterSelects);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', function (event) {
    bindFilterSelects(event.target.querySelector('[data-sts-shop-intro]'));
  });
})();
