console.log('Sanity check');

// add materialize nav transition
 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);
  })

const spinnerBox = document.getElementById('spinner-box')
const dataBox = document.getElementById('data-box')

$.ajax({
  type: "GET",
  url: '/jobs/',
  success: function(response){
    spinnerBox.classList.add('not-visible')
    console.log("something here", response)
  },
  error: function(error){
    console.log(error)
  }
})