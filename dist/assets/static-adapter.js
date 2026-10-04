/* Local-only adapters for the original theme's server-backed embellishments. */
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.qode-like').forEach(function (link) {
    var key = 'solvardis-like-' + link.id;
    try { if (localStorage.getItem(key)) link.classList.add('liked'); } catch (_) {}
    link.addEventListener('click', function (event) {
      event.preventDefault();
      var liked = link.classList.toggle('liked');
      var count = link.querySelector('span');
      if (count) count.textContent = Math.max(0, (parseInt(count.textContent, 10) || 0) + (liked ? 1 : -1));
      try { if (liked) localStorage.setItem(key, '1'); else localStorage.removeItem(key); } catch (_) {}
    });
  });
});
