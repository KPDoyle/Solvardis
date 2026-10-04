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

/* Shared footer and legal-page styling. */
(function () {
  var style = document.createElement('style');
  style.textContent = ".solvardis-legal-page .title h1{color:#244f88!important}.solvardis-footer{position:relative!important;background:#244f88;color:#e8edf5;text-align:left;font-size:14px;line-height:1.8}.solvardis-footer *{box-sizing:border-box}.solvardis-footer .sf-wrap{max-width:1100px;margin:0 auto;padding:52px 30px 24px}.solvardis-footer .sf-grid{display:grid;grid-template-columns:1.25fr .85fr 1fr;gap:64px}.solvardis-footer h2{color:#fff;font-size:20px;line-height:1.4;letter-spacing:0;margin:0 0 18px;text-transform:none}.solvardis-footer h3{color:#fff;font-size:14px;letter-spacing:1px;margin:0 0 18px;text-transform:uppercase}.solvardis-footer p{color:#e8edf5;margin:0 0 12px}.solvardis-footer .sf-logo{display:inline-block;width:min(230px,100%);margin:0 0 20px;line-height:0}.solvardis-footer .sf-logo img{display:block;width:100%;height:auto}.solvardis-footer .sf-brand:after{content:'';display:block;width:42px;height:3px;background:#ee8e32;margin-top:16px}.solvardis-footer a{color:#e8edf5;text-decoration:none;transition:color .2s}.solvardis-footer a:hover{color:#fff;text-decoration:underline}.solvardis-footer a:focus-visible{outline:2px solid #fff;outline-offset:4px}.solvardis-footer ul{list-style:none;padding:0;margin:0}.solvardis-footer li{margin:0 0 5px}.solvardis-footer address{font-style:normal;margin-bottom:12px}.solvardis-footer .sf-bottom{border-top:1px solid rgba(255,255,255,.22);margin-top:35px;padding-top:20px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:12px}.solvardis-footer .sf-legal{display:flex;gap:22px;flex-wrap:wrap}.solvardis-legal{max-width:900px;margin:auto;padding:55px 30px 70px;color:#555;line-height:1.85}.solvardis-legal h2{font-size:21px;margin:32px 0 12px;letter-spacing:0;text-transform:none}.solvardis-legal p{margin-bottom:16px}.solvardis-legal a{color:#244f88;text-decoration:underline}@media(max-width:800px){.solvardis-footer .sf-grid{grid-template-columns:1fr 1fr;gap:30px}.solvardis-footer .sf-grid>section:first-child{grid-column:1/-1}}@media(max-width:520px){.solvardis-footer .sf-wrap{padding:36px 24px 24px}.solvardis-footer .sf-grid{grid-template-columns:1fr;gap:26px}.solvardis-footer .sf-bottom{margin-top:26px}.solvardis-footer .sf-legal{gap:12px 20px}.solvardis-legal{padding:35px 24px 50px}}";
  document.head.appendChild(style);
  document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.solvardis-legal')) {
      document.body.classList.add('solvardis-legal-page');
      document.querySelectorAll('.solvardis-legal a').forEach(function (link) { link.classList.add('no_ajax'); });
    }
    var footer = document.querySelector('footer');
    if (footer) footer.outerHTML = "<footer class=\"solvardis-footer\" aria-label=\"Site footer\"><div class=\"sf-wrap\"><div class=\"sf-grid\"><section><a class=\"sf-logo no_ajax\" href=\"/\" aria-label=\"Solvardis home\"><img src=\"/assets/content/uploads/2017/02/Solvardis-Footer.png\" alt=\"Solvardis\"></a><p>Delivering quality with excellence.</p><p>Specialty products and solutions for our customers and business partners.</p></section><section><h3>Explore</h3><nav aria-label=\"Footer navigation\"><ul><li><a class=\"no_ajax\" href=\"/about/\">About Solvardis</a></li><li><a class=\"no_ajax\" href=\"/#portfolio\">Products</a></li><li><a class=\"no_ajax\" href=\"/portfolio/with-text/markets/\">Markets</a></li><li><a class=\"no_ajax\" href=\"/techdata/\">Technical data</a></li><li><a class=\"no_ajax\" href=\"/contact/\">Contact us</a></li></ul></nav></section><section><h3>Get in touch</h3><address>Solvardis LLC<br>24044 Cinco Village Drive, Suite 100<br>Katy, TX 77494, USA</address><p><a class=\"no_ajax\" href=\"tel:+12819374428\">+1 (281) 937 4428</a><br><a class=\"no_ajax\" href=\"mailto:info@solvardis.com\">info@solvardis.com</a></p></section></div><div class=\"sf-bottom\"><span>© 2026 Solvardis LLC. All rights reserved.</span><nav class=\"sf-legal\" aria-label=\"Legal information\"><a class=\"no_ajax\" href=\"/terms-and-conditions/\">Terms &amp; Conditions</a><a class=\"no_ajax\" href=\"/privacy-policy/\">Privacy Policy</a><a class=\"no_ajax\" href=\"/cookie-policy/\">Cookie Policy</a></nav></div></div></footer>";
    window.dispatchEvent(new Event('resize'));
  });
})();
