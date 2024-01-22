function authenticate() {
  $.ajax({
    type: 'GET',
    url: '/authenticate',
    data: {username: $('#login_username').val(), password: $('#login_password').val()},
    success: function(response) {
      var result = response.result;
      alert('Authentication result: ' + result);
    },
    error: function(error) {
      console.error('Error:', error);
    }
  });
}

function authenticateTacacs() {
  $.ajax({
    type: 'GET',
    url: '/authenticateTacacs',
    data: {username: $('#login_username').val(), password: $('#login_password').val(), smth: ""},
    success: function(response) {
      var result = response.result;
      alert('Authentication result: ' + result);
    },
    error: function(error) {
      console.error('Error:', error);
    }
  });
}
