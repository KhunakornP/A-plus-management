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
function setUserRole(role) {
    document.getElementById('type').value = role;
}

function setExamineeStatus(status) {
    document.getElementById('exam').value = status;
}
document.addEventListener('DOMContentLoaded', init, false)

function init(){
document.getElementById('student').addEventListener("click", setUserRole('student'));
document.getElementById('parent').addEventListener("click", setUserRole('parent'));
document.getElementById('a_level').addEventListener("click", setExamineeStatus(true));
document.getElementById('not_a_level').addEventListener("click", setExamineeStatus(false));
}