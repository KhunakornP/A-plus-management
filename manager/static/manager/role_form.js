$('.btnNext').click(function() {
  const nextTabLinkEl = $('.nav-tabs .active').next('li');
  const nextTab = new bootstrap.Tab(nextTabLinkEl);
  nextTab.show();
});

$('.btnPrevious').click(function() {
  const prevTabLinkEl = $('.nav-tabs .active').prev('li');
  const prevTab = new bootstrap.Tab(prevTabLinkEl);
  prevTab.show();
});