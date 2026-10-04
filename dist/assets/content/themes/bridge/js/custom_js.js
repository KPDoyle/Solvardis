
var $j = jQuery.noConflict();

$j(document).ready(function() {
	"use strict";

	var $footerLogoTarget = $j("footer .footer_col1 .column_inner").first();
	if ($footerLogoTarget.length && !$footerLogoTarget.find(".solvardis-footer-logo").length) {
		$footerLogoTarget.append('<a class="solvardis-footer-logo" href="/" aria-label="Solvardis home"><img src="/assets/content/uploads/2017/02/Solvardis-Footer.png" alt="Solvardis"></a>');
	}

	});
