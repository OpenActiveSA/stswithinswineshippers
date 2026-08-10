(function () {
  function closeOthers(filtersRoot, except) {
    if (!filtersRoot) return;
    filtersRoot.querySelectorAll('details.sts-shop-filter[open]').forEach(function (el) {
      if (el !== except) el.removeAttribute('open');
    });
  }

  function bindFilters(root) {
    if (!root) return;
    var filtersRoot = root.querySelector('[data-sts-filters]') || root;
    if (filtersRoot.dataset.stsFiltersBound === 'true') return;
    filtersRoot.dataset.stsFiltersBound = 'true';

    filtersRoot.addEventListener('toggle', function (event) {
      var target = event.target;
      if (!target || target.tagName !== 'DETAILS' || !target.open) return;
      closeOthers(filtersRoot, target);
    });

    document.addEventListener('click', function (event) {
      if (event.target.closest('[data-sts-filters]')) return;
      closeOthers(filtersRoot, null);
    });
  }

  function init() {
    document.querySelectorAll('[data-sts-shop-intro]').forEach(bindFilters);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('shopify:section:load', function (event) {
    bindFilters(event.target.querySelector('[data-sts-shop-intro]'));
  });
})();
