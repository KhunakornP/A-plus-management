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
function setStudentUser() {
    document.getElementById('type').value = 'student';
    document.getElementById('c2').style.border='5px solid blue'
    document.getElementById('c1').style.border='1px solid rgba(0, 0, 0, 0.175)'
}
function setParentUser() {
    document.getElementById('type').value = 'parent';
    document.getElementById('c1').style.border='5px solid blue'
    document.getElementById('c2').style.border='1px solid rgba(0, 0, 0, 0.175)'
}
function setExamineeStatus() {
    document.getElementById('exam').value = true;
    document.getElementById('c3').style.border='5px solid blue'
    document.getElementById('c4').style.border='1px solid rgba(0, 0, 0, 0.175)'
}
function setNotExamineeStatus() {
    document.getElementById('exam').value = false;
    document.getElementById('c4').style.border='5px solid blue'
    document.getElementById('c3').style.border='1px solid rgba(0, 0, 0, 0.175)'
}

// disabling next line since the function is used in html but not in js
// eslint-disable-next-line
function validateForm(event) {
    if (document.getElementById('type').value === '') {
    event.preventDefault()} if (document.getElementById('type').value === 'student' &&
    document.getElementById('exam').value === '') {
    event.preventDefault()}
}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('student').addEventListener("click", setStudentUser)
    document.getElementById('parent').addEventListener("click", setParentUser);
    document.getElementById('a_level').addEventListener("click", setExamineeStatus);
    document.getElementById('not_a_level').addEventListener("click", setNotExamineeStatus);
});