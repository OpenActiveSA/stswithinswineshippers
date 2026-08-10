(function () {
  var SINGLE_PARAMS = {
    'filter.p.product_type': true,
    'filter.p.vendor': true,
    'filter.v.option.vintage': true,
    'filter.p.m.custom.vintage': true,
    'filter.p.tag': true
  };

  function normalizeFilterUrl(href) {
    try {
      var url = new URL(href, window.location.origin);
      if (!url.search) return href;

      var kept = [];
      var seenSingle = {};
      // Walk params in reverse so the newest value for a single-select param wins
      var entries = [];
      url.searchParams.forEach(function (value, key) {
        entries.push([key, value]);
      });

      for (var i = entries.length - 1; i >= 0; i--) {
        var key = entries[i][0];
        var value = entries[i][1];
        if (SINGLE_PARAMS[key]) {
          if (seenSingle[key]) continue;
          seenSingle[key] = true;
        }
        kept.push([key, value]);
      }

      kept.reverse();
      var next = new URLSearchParams();
      kept.forEach(function (pair) {
        next.append(pair[0], pair[1]);
      });
      url.search = next.toString();
      return url.pathname + url.search + url.hash;
    } catch (err) {
      return href;
    }
  }

  function rewriteOptionLinks(root) {
    (root || document).querySelectorAll('a.sts-shop-filter__option[href]').forEach(function (link) {
      var normalized = normalizeFilterUrl(link.getAttribute('href'));
      if (normalized && normalized !== link.getAttribute('href')) {
        link.setAttribute('href', normalized);
      }
    });
  }

  function closeAll(except) {
    document.querySelectorAll('.sts-shop-filter.is-open').forEach(function (el) {
      if (el !== except) el.classList.remove('is-open');
    });
    document.querySelectorAll('details.sts-shop-filter[open]').forEach(function (el) {
      if (el !== except) el.removeAttribute('open');
    });
  }

  function enhanceSelect(select) {
    if (!select || select.dataset.stsEnhanced === 'true') return;
    select.dataset.stsEnhanced = 'true';

    var wrap = select.closest('.sts-shop-filter') || select.parentElement;
    if (!wrap) return;
    wrap.classList.add('sts-shop-filter');

    var menu = document.createElement('ul');
    menu.className = 'sts-shop-filter__menu';
    menu.setAttribute('role', 'list');

    Array.from(select.options).forEach(function (opt) {
      if (!opt.value && opt.index === 0) return;
      var li = document.createElement('li');
      var a = document.createElement('a');
      a.className = 'sts-shop-filter__option' + (opt.selected && opt.value ? ' is-active' : '');
      a.href = opt.value ? normalizeFilterUrl(opt.value) : '#';
      a.textContent = opt.textContent.trim();
      if (!opt.value) {
        a.addEventListener('click', function (e) {
          e.preventDefault();
        });
      }
      li.appendChild(a);
      menu.appendChild(li);
    });

    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'sts-shop-filter__button';
    button.setAttribute('aria-expanded', 'false');
    var labelText = (select.options[0] && select.options[0].textContent.trim()) || 'Filter';
    button.innerHTML =
      '<span class="sts-shop-filter__label">' +
      labelText +
      '</span><span class="sts-shop-filter__caret" aria-hidden="true"></span>';

    button.addEventListener('click', function (event) {
      event.preventDefault();
      event.stopPropagation();
      var willOpen = !wrap.classList.contains('is-open');
      closeAll();
      if (willOpen) {
        wrap.classList.add('is-open');
        button.setAttribute('aria-expanded', 'true');
      } else {
        button.setAttribute('aria-expanded', 'false');
      }
    });

    select.classList.add('sts-shop-filter__select--hidden');
    select.setAttribute('tabindex', '-1');
    select.setAttribute('aria-hidden', 'true');

    wrap.insertBefore(button, select);
    wrap.appendChild(menu);
  }

  function bindNativeFallback() {
    document.querySelectorAll('select.sts-shop-filter__select, [data-sts-filter-select]').forEach(function (select) {
      if (select.dataset.stsBound === 'true') return;
      select.dataset.stsBound = 'true';
      select.addEventListener('change', function () {
        if (select.value) window.location.assign(normalizeFilterUrl(select.value));
      });
    });
  }

  function bindDetails() {
    document.querySelectorAll('[data-sts-filters]').forEach(function (filtersRoot) {
      if (filtersRoot.dataset.stsFiltersBound === 'true') return;
      filtersRoot.dataset.stsFiltersBound = 'true';
      filtersRoot.addEventListener('toggle', function (event) {
        var target = event.target;
        if (!target || target.tagName !== 'DETAILS' || !target.open) return;
        filtersRoot.querySelectorAll('details.sts-shop-filter[open]').forEach(function (el) {
          if (el !== target) el.removeAttribute('open');
        });
      });
    });
  }

  function init() {
    rewriteOptionLinks(document);
    document.querySelectorAll('select.sts-shop-filter__select, [data-sts-filter-select]').forEach(enhanceSelect);
    bindNativeFallback();
    bindDetails();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  document.addEventListener('click', function (event) {
    var option = event.target.closest('a.sts-shop-filter__option');
    if (option && option.getAttribute('href')) {
      var normalized = normalizeFilterUrl(option.getAttribute('href'));
      if (normalized !== option.getAttribute('href')) {
        event.preventDefault();
        window.location.assign(normalized);
        return;
      }
    }
    if (event.target.closest('.sts-shop-filter')) return;
    closeAll();
  });

  document.addEventListener('shopify:section:load', init);
})();
